# AI Tool Navigator — 项目对接文档

> 最后更新: 2026-06-05 | 代码仓库: `https://github.com/07wuzheng/Newone` (也可用 `07wuzheng/newone_1`)

---

## 一、项目概览

面试作品集项目「AI 工具导航平台」，帮助用户发现和探索 AI 工具。

| 项目 | 说明 |
|------|------|
| **业务功能** | 首页推荐、分类浏览、实时搜索、工具详情、提交工具、AI 助手对话 |
| **技术栈** | Vue 3 (Composition API) + Vite + Tailwind CSS v4 / Python FastAPI + SQLAlchemy + SQLite |
| **部署** | Vercel 单项目部署（前后端合并） |
| **访问地址** | **https://backend-six-alpha-77.vercel.app** |

---

## 二、项目结构

```
/
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── views/          # 页面：HomePage, SearchPage, CategoryPage, ToolDetailPage, SubmitPage, AboutPage, NotFound
│   │   ├── components/     # 组件：ToolCard, ChatBot（AI 助手右下角浮窗）
│   │   ├── stores/         # Pinia 状态管理：tools.js, categories.js
│   │   └── router/         # Vue Router 路由配置
│   ├── vite.config.js      # Vite 配置（build outDir 指向 ../backend/frontend_dist）
│   └── package.json
│
├── backend/                # Python FastAPI 后端
│   ├── main.py             # 应用入口（含 SPA fallback 路由）
│   ├── database.py         # SQLAlchemy 配置（SQLite: ./data.db）
│   ├── models.py           # ORM 模型
│   ├── agent.py            # 智能体对话（DeepSeek API）
│   ├── seed.py             # 种子数据（69 工具，6 分类）
│   ├── routers/            # API 路由分类
│   │   ├── categories.py   # GET /api/categories, GET /api/categories/{slug}/tools
│   │   ├── tools.py        # GET /api/tools, /featured, /search, /stats, /editor-picks, /{id}
│   │   └── submissions.py  # POST /api/submit
│   ├── version_fetcher.py  # 版本嗅探器（APScheduler定时任务）
│   ├── data.db             # SQLite 数据库
│   ├── static/             # 工具 logo 图片
│   ├── frontend_dist/      # 前端构建产物（Vite 自动输出到这里）
│   ├── .env                # 环境变量（含 DEEPSEEK_API_KEY）
│   └── requirements.txt
│
├── render.yaml             # Render 部署配置（目前未使用）
├── runtime.txt             # Python 版本锁定（Render 遗留）
└── README.md
```

---

## 三、API 接口清单

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/categories` | 分类列表（6 个分类） |
| GET | `/api/categories/{slug}/tools` | 分类下工具 |
| GET | `/api/tools` | 工具列表（分页：?page=1&page_size=10） |
| GET | `/api/tools/featured` | 推荐工具 |
| GET | `/api/tools/editor-picks` | 编辑精选 |
| GET | `/api/tools/stats` | 统计（总数、分类数等） |
| GET | `/api/tools/search?q=` | 搜索工具 |
| GET | `/api/tools/{id}` | 工具详情（含相关工具） |
| POST | `/api/submit` | 提交新工具 |
| POST | `/api/agent/chat` | AI 助手对话（限流：5次/分钟，200次/天） |
| POST | `/api/admin/refresh-versions` | 手动触发版本刷新 |

---

## 四、部署架构

### Vercel 生产环境

- **访问地址**: https://backend-six-alpha-77.vercel.app
- **Vercel 项目**: `07wuzhengs-projects/backend` (FastAPI 框架预设)
- **部署方式**: 从 `backend/` 目录执行 `npx vercel --prod`

### 部署流程

```bash
# 构建前端（生成到 backend/frontend_dist/）
cd frontend && VITE_API_BASE_URL=/api npx vite build

# 部署后端（含前端构建产物）
cd ../backend && npx vercel --prod
```

### Vercel 环境变量

| Key | Value | 说明 |
|-----|-------|------|
| `DEEPSEEK_API_KEY` | `sk-b645ca2be7f84f928055c22493b633b9` | DeepSeek API 密钥（加密存储） |
| `CORS_ORIGINS` | （可不设） | 合并部署后前后端同域，无需配置；旧值指向已废弃的独立前端域名，建议从 Vercel 环境变量中删除 |

### 注意事项

- 前端构建时 `VITE_API_BASE_URL=/api` 会编译进 JS 中，生产环境用相对路径
- Vercel FastAPI 预设默认 Python 3.12，自动检测 `main.py` 为入口
- 数据库 `data.db` 是只读的（写入在部署后不会持久化），数据变更需在本地改 → 重新部署

---

## 五、本地开发

### 环境要求

- Python 3.12（安装在 `D:\Python312`）
- Node.js 22+
- Windows 环境

### 启动后端

```bash
cd backend
D:/Python312/python.exe -m uvicorn main:app --reload --port 8899
```

> ⚠️ 不要用 8000 端口！Windows 有 TCP 幽灵条目残留，需重启才能清理
> ⚠️ `--reload` 在 Windows 不可靠，改代码后建议手动重启

### 启动前端

```bash
cd frontend
npm run dev
```

> 前端开发服务器会自动代理 `/api` 和 `/static` 到 `localhost:8899`

### 修改种子数据

```bash
# 修改 seed.py 后重新填充
D:/Python312/python.exe seed.py
```

### 修改前端 API 指向

本地开发在 `frontend/.env` 中设置 `VITE_API_BASE_URL=http://localhost:8899/api`

---

## 六、已知问题和踩坑记录

### 1. Windows 端口幽灵（遗留问题）
- 现象：杀掉 uvicorn 后 `netstat` 仍显示 LISTENING，新进程无法绑定
- 对策：使用 8899 端口（避开 8000 的幽灵条目），如需彻底清理需重启 Windows

### 2. 数据库只读（Vercel 部署）
- Vercel serverless 环境文件系统是只读的，写入 `data.db` 不会持久化
- 数据变更必须在本地修改后重新部署

### 3. AI 助手 token 预算
- 每日 5000 tokens，用完需等次日重置（进程内计数器，重启后也会重置）
- 限流器：5次/分钟，200次/天（基于内存，重启后重置）

### 4. Vercel 冷启动（移动端）
- 首次请求约 2-3 秒（Python 初始化 + 数据库加载）
- 移动端某些网络环境下可能超时，建议添加 keep-warm 机制

### 5. 图标文件
- 工具 logo 图片在 `backend/static/logos/`，Git 已跟踪
- 图片 URL 在生产环境中指向 `https://backend-six-alpha-77.vercel.app/static/logos/...`

---

## 七、后续可做的方向

| 优先级 | 任务 | 说明 |
|--------|------|------|
| 高 | 添加 keep-warm | 用 cron-job.org 或 UptimeRobot 每 5 分钟 ping 一次，解决移动端冷启动问题 |
| 中 | 切换数据库到 PostgreSQL | Vercel + Render 支持 PostgreSQL，解决部署只读问题 |
| 中 | 添加自定义域名 | 绑定自有域名，用 Cloudflare 加速移动端访问 |
| 低 | Docker 化开发环境 | 避免 Windows 各种环境问题 |

---

## 八、关键文件速查

| 文件 | 行数 | 说明 |
|------|------|------|
| `backend/main.py` | ~245 | 应用入口，路由注册，SPA fallback |
| `backend/agent.py` | ~180 | DeepSeek AI 助手逻辑 |
| `backend/routers/tools.py` | ~177 | 工具 CRUD + 搜索 + 统计 |
| `frontend/src/stores/tools.js` | ~120 | 工具状态管理 + API 调用 |
| `frontend/src/components/ChatBot.vue` | ~150 | AI 对话浮窗组件 |
| `frontend/vite.config.js` | ~15 | Vite 构建配置 |

---

*如有疑问，参考 `C:\Users\1\.claude\projects\D--claude-test\memory\` 下的项目记忆文件。*
