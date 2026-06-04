# 项目架构

> 用途：一张图看清项目长什么样，面试时解释架构用。

```
┌─────────────────────────────────────────────┐
│                  前端 (Vite + Vue 3)          │
│  ┌─────────┐  ┌──────┐  ┌────────────────┐  │
│  │ NavBar  │  │ 路由  │  │    页面组件      │  │
│  │  - 分类  │  │ vue- │  │  HomePage       │  │
│  │  - 搜索  │  │router│  │  CategoryPage   │  │
│  │  - 关于  │  │      │  │  ToolDetailPage  │  │
│  └─────────┘  └──────┘  │  SearchPage      │  │
│                          │  SubmitPage      │  │
│  ┌─────────┐            │  AboutPage       │  │
│  │ Footer  │            │  404Page         │  │
│  └─────────┘            └────────────────┘  │
│                          ┌───────────────┐   │
│                          │  复用组件       │   │
│                          │  ToolCard      │   │
│                          │  SearchBar     │   │
│                          │  LoadingSpinner│   │
│                          │  ErrorMessage  │   │
│                          └───────────────┘   │
│  ┌─────────────────────────────────────────┐  │
│  │  Pinia 状态管理                          │  │
│  │  useToolStore / useCategoryStore         │  │
│  └─────────────────────────────────────────┘  │
└──────────────────────┬────────────────────────┘
                       │ HTTP (axios)
                       ▼
┌─────────────────────────────────────────────┐
│              后端 (FastAPI)                   │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  │
│  │ 路由层   │  │ 业务逻辑  │  │  数据模型   │  │
│  │categories│  │ (主要靠   │  │  Tool      │  │
│  │ tools    │  │  SQLAlchemy)│  │  Category  │  │
│  │ submit   │  │          │  │  Submission │  │
│  └─────────┘  └──────────┘  └───────────┘  │
│                              ┌───────────┐  │
│                              │  数据库     │  │
│                              │  SQLite    │  │
│                              └───────────┘  │
└─────────────────────────────────────────────┘
```

## 前端组件树

```
App.vue
├── NavBar.vue              ← 分类导航、搜索输入框、关于链接
├── RouterView
│   ├── HomePage.vue        ← 首页
│   │   ├── HeroSection.vue ← 标语区域
│   │   ├── ToolCard.vue    ← 工具卡片（复用，6-8 个）
│   │   └── CategorySection.vue ← 分类快速入口
│   ├── CategoryPage.vue    ← 分类浏览
│   │   └── ToolCard.vue    ← 工具卡片（复用）
│   ├── ToolDetailPage.vue  ← 工具详情
│   │   └── 同分类推荐卡片
│   ├── SearchPage.vue      ← 搜索结果
│   │   ├── SearchBar.vue   ← 搜索框
│   │   └── ToolCard.vue    ← 工具卡片（复用）
│   ├── SubmitPage.vue      ← 提交表单
│   └── AboutPage.vue       ← 关于
├── FooterBar.vue
└── NotFound.vue            ← 404 页面
```

## 数据流

```
用户操作 → Vue 组件 → Pinia Store → axios → FastAPI → SQLAlchemy → SQLite
                        ↑                              │
                        └────────── JSON ←──────────────┘
```

## 环境变量约定

| 变量名 | 在哪用 | 开发环境值 | 生产环境值 |
|--------|--------|-----------|-----------|
| `VITE_API_BASE_URL` | 前端 | `http://localhost:8000/api` | Render 域名 |
| `DATABASE_URL` | 后端 | `sqlite:///./data.db` | PostgreSQL URL（部署时） |
| `CORS_ORIGINS` | 后端 | `http://localhost:5173` | Vercel 域名 |
