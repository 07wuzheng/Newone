import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from database import engine, Base
from routers import categories, tools, submissions
from routers.submissions import Submission
import models
from agent import chat as agent_chat
from pydantic import BaseModel
from datetime import datetime, timedelta
from collections import defaultdict
import time


# ---- scheduler with dynamic retry ----
from apscheduler.schedulers.background import BackgroundScheduler
from version_fetcher import FETCHERS, fetch_generic
from database import SessionLocal
from concurrent.futures import ThreadPoolExecutor, as_completed

scheduler = BackgroundScheduler()
_RETRY_INTERVAL_MINUTES = 30      # 抓取失败后，每 30 分钟重试
_SUCCESS_INTERVAL_HOURS = 12      # 成功后，每 12 小时检查一次


def run_version_fetch():
    db = SessionLocal()
    from models import Tool
    from datetime import datetime, timezone

    any_success = False
    # 1) 有自定义抓取器的工具
    for fetcher_name, fetcher_fn in FETCHERS.items():
        tool = db.query(Tool).filter(Tool.name == fetcher_name).first()
        if not tool:
            continue
        try:
            version = fetcher_fn()
            if version:
                any_success = True
                tool.version = version
                tool.version_updated_at = datetime.now(timezone.utc)
                db.commit()
        except Exception:
            db.rollback()

    # 2) 其余工具用通用嗅探器（最多 5 个并发）
    generic_tools = [t for t in db.query(Tool).all() if t.name not in FETCHERS]
    if generic_tools:
        def _try_fetch(t):
            return t, fetch_generic(t.url)
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {pool.submit(_try_fetch, t): t for t in generic_tools}
            for future in as_completed(futures):
                tool, version = future.result()
                if version:
                    any_success = True
                    tool.version = version
                    tool.version_updated_at = datetime.now(timezone.utc)
                    try:
                        db.commit()
                    except Exception:
                        db.rollback()

    db.close()

    # 动态调整下次检查间隔
    #   失败 → 30 分钟后快速重试（能及时感知网络恢复）
    #   成功 → 切回 12 小时间隔
    try:
        if any_success:
            scheduler.reschedule_job(
                'version_check',
                trigger='interval',
                hours=_SUCCESS_INTERVAL_HOURS
            )
        else:
            scheduler.reschedule_job(
                'version_check',
                trigger='interval',
                minutes=_RETRY_INTERVAL_MINUTES
            )
    except Exception:
        pass  # 首次调度时 reschedule 可能还没注册，忽略


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: DB migration + scheduler
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        for col in ["version", "version_updated_at"]:
            try:
                conn.execute(text(f"ALTER TABLE tools ADD COLUMN {col}"))
                conn.commit()
            except Exception:
                conn.rollback()
        # add image_url to existing submissions table
        try:
            conn.execute(text("ALTER TABLE submissions ADD COLUMN image_url VARCHAR(500)"))
            conn.commit()
        except Exception:
            conn.rollback()
        # v2 fields
        for col in ["pricing", "tags", "pros", "cons", "screenshots"]:
            try:
                conn.execute(text(f"ALTER TABLE tools ADD COLUMN {col} TEXT"))
                conn.commit()
            except Exception:
                conn.rollback()
        try:
            conn.execute(text("ALTER TABLE tools ADD COLUMN demo_url VARCHAR(500)"))
            conn.commit()
        except Exception:
            conn.rollback()
        try:
            conn.execute(text("ALTER TABLE tools ADD COLUMN editor_pick BOOLEAN DEFAULT 0"))
            conn.commit()
        except Exception:
            conn.rollback()

    scheduler.add_job(run_version_fetch, trigger='date', run_date=None, id='initial_version_check')
    scheduler.add_job(run_version_fetch, trigger='interval', minutes=_RETRY_INTERVAL_MINUTES, id='version_check')
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(title="AI Tool Navigator API", lifespan=lifespan)

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 静态资源 ──
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend_dist")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="frontend_assets")

app.include_router(categories.router)
app.include_router(tools.router)
app.include_router(submissions.router)

# ── SPA fallback ──
from starlette.responses import FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def spa_fallback(request: Request, exc):
    if exc.status_code != 404:
        raise exc
    path = request.url.path
    # API 和静态资源 404 不拦截
    if path.startswith("/api/") or path.startswith("/static/") or path.startswith("/assets/"):
        raise exc
    # 先检查文件是否存在（favicon.svg, icons.svg 等根目录文件）
    file_path = os.path.join(FRONTEND_DIR, path.lstrip("/"))
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    # SPA fallback
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path, media_type="text/html")
    raise exc


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


# ---- 简易内存限流器 ----
class RateLimiter:
    def __init__(self, max_per_minute=5, max_per_day=200):
        self.max_per_minute = max_per_minute
        self.max_per_day = max_per_day
        self.minute_buckets = defaultdict(list)
        self.day_count = defaultdict(int)
        self._day = None

    def check(self, ip: str) -> tuple[bool, str]:
        now = time.time()
        day_key = int(now / 86400)

        # 每日重置
        if day_key != self._day:
            self.day_count.clear()
            self._day = day_key

        # 分钟窗口清理
        self.minute_buckets[ip] = [t for t in self.minute_buckets[ip] if now - t < 60]

        if self.day_count[ip] >= self.max_per_day:
            return False, "今日已用满次数，明天再来吧～"

        if len(self.minute_buckets[ip]) >= self.max_per_minute:
            return False, "发言太频繁了，稍等一分钟再试试～"

        self.minute_buckets[ip].append(now)
        self.day_count[ip] += 1
        return True, ""

rate_limiter = RateLimiter()


# ---- 智能体对话接口 ----
class ChatRequest(BaseModel):
    message: str


@app.post("/api/agent/chat")
def agent_chat_endpoint(req: ChatRequest, request: Request):
    # 限流
    ip = request.client.host if request.client else "unknown"
    ok, msg = rate_limiter.check(ip)
    if not ok:
        return {"response": msg, "tools": []}

    # 输入长度限制
    if len(req.message) > 200:
        return {"response": "消息太长了，请控制在 200 字以内～", "tools": []}

    return agent_chat(req.message)


# ---- 手动触发版本刷新 ----
from fastapi import BackgroundTasks


@app.post("/api/admin/refresh-versions")
def refresh_versions(background_tasks: BackgroundTasks):
    """手动触发一次版本抓取，不走调度器等待。"""
    background_tasks.add_task(run_version_fetch)
    return {"message": "版本刷新任务已提交，将在后台执行"}
