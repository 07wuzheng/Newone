# API 接口契约

> 用途：定义前后端数据格式，避免开发时各写各的对不上。前端按这个格式请求，后端按这个格式返回。

**基础地址**：`http://localhost:8000/api`

**通用规则**：
- 所有接口返回 JSON
- 成功：HTTP 200，数据在 `data` 字段
- 失败：HTTP 4xx/5xx，错误信息在 `detail` 字段

---

## 1. 获取所有分类

```
GET /categories
```

**响应示例**：
```json
{
  "data": [
    {
      "id": 1,
      "name": "LLM / 对话",
      "slug": "llm",
      "description": "大语言模型和对话式 AI 助手",
      "icon": "chat"
    }
  ]
}
```

---

## 2. 获取单个分类（含工具列表）

```
GET /categories/{slug}
```

**响应示例**：
```json
{
  "data": {
    "id": 1,
    "name": "LLM / 对话",
    "slug": "llm",
    "description": "大语言模型和对话式 AI 助手",
    "icon": "chat",
    "tools": [
      {
        "id": 1,
        "name": "ChatGPT",
        "description": "OpenAI 开发的对话式 AI",
        "url": "https://chatgpt.com",
        "image_url": "https://picsum.photos/seed/chatgpt/400/300",
        "rating": 4.8,
        "is_featured": true,
        "version": "GPT-5.x"
      }
    ]
  }
}
```

---

## 3. 获取首页推荐工具

```
GET /tools/featured
```

**响应示例**：
```json
{
  "data": [
    {
      "id": 1,
      "name": "ChatGPT",
      "description": "OpenAI 开发的对话式 AI",
      "url": "https://chatgpt.com",
      "image_url": "https://picsum.photos/seed/chatgpt/400/300",
      "rating": 4.8,
      "is_featured": true,
      "version": "GPT-5.x",
      "category_name": "LLM / 对话",
      "category_slug": "llm"
    }
  ]
}
```

---

## 4. 获取工具列表（支持分类筛选 + 分页）

```
GET /tools?category=llm&page=1&page_size=10
```

| 参数 | 可选 | 默认 | 说明 |
|------|------|------|------|
| category | 是 | - | 分类 slug，不传返回全部 |
| page | 是 | 1 | 页码，从 1 开始 |
| page_size | 是 | 10 | 每页条数（最大 50） |

**响应示例**：
```json
{
  "data": [
    {
      "id": 1,
      "name": "ChatGPT",
      "description": "OpenAI 开发的对话式 AI",
      "url": "https://chatgpt.com",
      "image_url": "https://picsum.photos/seed/chatgpt/400/300",
      "rating": 4.8,
      "is_featured": true,
      "version": "GPT-5.x",
      "category_name": "LLM / 对话",
      "category_slug": "llm"
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 10
}
```

---

## 5. 获取单个工具详情

```
GET /tools/{id}
```

**响应示例**：
```json
{
  "data": {
    "id": 1,
    "name": "ChatGPT",
    "description": "OpenAI 开发的对话式 AI，支持文本生成、代码编写、分析推理等",
    "url": "https://chatgpt.com",
    "image_url": "https://picsum.photos/seed/chatgpt/400/300",
    "rating": 4.8,
    "is_featured": true,
    "version": "GPT-5.x",
    "version_updated_at": "2026-06-04T12:00:00",
    "created_at": "2026-06-03T00:00:00",
    "category": {
      "id": 1,
      "name": "LLM / 对话",
      "slug": "llm"
    },
    "related_tools": [
      {
        "id": 2,
        "name": "Claude",
        "image_url": "https://picsum.photos/seed/claude/400/300",
        "rating": 4.7
      }
    ]
  }
}
```

**注意**：`version` 可能为 `null`（新提交工具尚未抓取），`version_updated_at` 可能为 `null`（从未更新过版本）。

---

## 6. 搜索工具

```
GET /tools/search?q=关键词
```

| 参数 | 必填 | 说明 |
|------|------|------|
| q | 是 | 搜索关键词，匹配工具名称和描述 |

**响应示例**：
```json
{
  "data": [
    {
      "id": 1,
      "name": "ChatGPT",
      "description": "OpenAI 开发的对话式 AI",
      "url": "https://chatgpt.com",
      "image_url": "https://picsum.photos/seed/chatgpt/400/300",
      "rating": 4.8,
      "version": "GPT-5.x",
      "category_name": "LLM / 对话",
      "category_slug": "llm"
    }
  ],
  "total": 1,
  "query": "chat"
}
```

**搜索无结果**：
```json
{
  "data": [],
  "total": 0,
  "query": "xxxxxxxxx"
}
```

---

## 7. 提交工具

```
POST /tools/submit
Content-Type: application/json

{
  "name": "工具名称",
  "description": "工具描述",
  "url": "https://example.com",
  "category_id": 1
}
```

**字段验证规则**：

| 字段 | 必填 | 规则 |
|------|------|------|
| name | 是 | 2-100 字符 |
| description | 是 | 10-500 字符 |
| url | 是 | 合法 URL 格式 |
| category_id | 是 | 必须是存在的分类 ID |

**提交成功**：
```json
{
  "data": {
    "id": 100,
    "name": "工具名称",
    "status": "pending_review"
  },
  "message": "提交成功，审核后将会展示"
}
```

**校验失败**：
```json
{
  "detail": [
    {
      "field": "name",
      "message": "名称长度应在 2-100 字符之间"
    }
  ]
}
```

---

## 8. 手动触发版本刷新

```
POST /api/admin/refresh-versions
Content-Type: application/json
（无需请求体）
```

**说明**：强制立即执行一次版本抓取（自定义抓取器 + 通用嗅探器），不走调度器等待。适用于开启代理后手动触发更新。

**响应示例**：
```json
{
  "message": "版本刷新任务已提交，将在后台执行"
}
```

---

## 接口一览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/categories` | 所有分类 |
| GET | `/api/categories/{slug}` | 单个分类及工具（含 version） |
| GET | `/api/tools/featured` | 首页推荐（含 version） |
| GET | `/api/tools` | 工具列表（筛选+分页，含 version） |
| GET | `/api/tools/{id}` | 工具详情（含 version + version_updated_at） |
| GET | `/api/tools/search?q=` | 搜索（含 version） |
| POST | `/api/tools/submit` | 提交工具 |
| POST | `/api/admin/refresh-versions` | 手动触发版本抓取 |
| GET | `/api/health` | 健康检查 |
