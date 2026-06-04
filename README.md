# AI 工具导航平台

一个帮助用户发现和探索 AI 工具的导航网站。

## 技术栈

- **前端**: Vue 3 + Vite + Tailwind CSS
- **后端**: Python FastAPI + SQLAlchemy
- **数据库**: SQLite

## 快速开始

### 后端

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API 文档自动生成：http://localhost:8000/docs

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 项目文档

| 文档 | 说明 |
|------|------|
| [产品需求文档 (PRD)](docs/PRD.md) | 产品需求定义 |
| [项目章程](docs/项目章程.md) | 项目范围和成功标准 |
| [API 接口契约](docs/api-contract.md) | 前后端接口定义 |
| [种子数据](docs/seed-data.md) | 预置 27 个 AI 工具列表 |
| [项目架构](docs/architecture.md) | 组件树、数据流、环境变量 |
| [部署方案](docs/deployment.md) | 部署方案和注意事项 |
| [开发任务清单](ai/memory-bank/tasks/ai-tool-navigator-tasklist.md) | 开发任务拆解 |
| [风险登记表](docs/风险登记表.md) | 风险管理计划 |
| [面试材料清单](docs/面试材料清单.md) | 面试准备清单 |
