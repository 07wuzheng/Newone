# 部署方案

> 用途：确定去哪里部署、怎么部署，避免临到部署才发现踩坑。

## 环境变量说明

| 变量名 | 在哪用 | 说明 |
|--------|--------|------|
| `VITE_API_BASE_URL` | 前端 | 后端 API 地址，默认 `http://localhost:8000/api` |
| `DATABASE_URL` | 后端 | 数据库连接，开发默认为 SQLite |
| `CORS_ORIGINS` | 后端 | 允许的前端域名，默认 `http://localhost:5173` |
| `HTTPS_PROXY` | 后端（版本抓取） | 代理地址，用于访问海外工具官网抓取版本号 |
| `VERSION_FETCHER_DISABLE` | 后端（版本抓取） | 设为 `1` 可禁用版本自动抓取 |

## 方案一：Render + Vercel（推荐）

| 服务 | 部署什么 | 费用 |
|------|---------|------|
| Vercel | 前端（Vue 3 静态站点） | 免费 |
| Render | 后端（FastAPI） | 免费（每月 750 小时，够用） |

### 注意：SQLite 的问题
Render 的免费实例在重启后文件系统会重置，SQLite 数据会丢失。解决方案：

**选 A（简单）**：每次重启后重新跑种子数据，演示够用
**选 B（推荐）**：改用 PostgreSQL，Render 提供免费的 PostgreSQL

### 部署步骤（方案 B）

1. **后端部署到 Render**
   - 在 Render Dashboard 创建 Web Service
   - 连接 GitHub 仓库
   - 启动命令：`uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - 环境变量：`DATABASE_URL=postgresql://...`（Render 自动提供）
   - 如果需要抓取海外 AI 工具版本号，设置 `HTTPS_PROXY` 环境变量
   - 如果需要禁用版本自动抓取，设置 `VERSION_FETCHER_DISABLE=1`
   - 添加 `gunicorn` 和 `psycopg2-binary` 到依赖

2. **前端部署到 Vercel**
   - Vercel 导入项目
   - 框架选择 Vite
   - 环境变量：`VITE_API_BASE_URL=https://your-app.onrender.com/api`

## 方案二：全用 PythonAnywhere（最省事）

- 免费套餐支持一个 web 应用
- SQLite 文件不会被重置
- 缺点：访问速度稍慢，免费套餐有流量限制

## 方案三：本地演示（兜底）

部署失败也没关系，录屏 + 截图一样能面试。
流程：本地启动前后端 → 录屏工具录 3 分钟演示 → 截 4-5 张关键页面截图

---

**建议**：开发阶段用 SQLite，开发完成后决定要不要切 PostgreSQL。部署不是必选项，本地能跑才是底线。
