# HD 高清 Logo 系统

## 背景

项目初期，所有工具的图标使用 DuckDuckGo 图标服务 (`icons.duckduckgo.com/ip3/{domain}.ico`) 获取的网站 favicon。这些 .ico 文件通常只有 16×16 或 32×32 像素，在卡片中以 80×80 显示时严重模糊，影响整体视觉质感。

## 目标

- 为主要 AI 工具替换高清（HD）图标
- 无法获取 HD 图标的工具保留 favicon，不显示空白
- 自动化、可重复的下载流程

---

## 总体策略：多源分级获取 + 自动降级

每个工具按优先级依次尝试三级来源，一级失败自动降级到下一级：

```
LobeHub PNG (最高质量) → SimpleIcons SVG (矢量) → DuckDuckGo/Google Favicon (兜底)
```

---

### 第一级：LobeHub 高清 PNG

[LobeHub/icons](https://github.com/lobehub/lobe-icons) 是一个开源的 AI 工具图标库，收录了 100+ AI 工具的矢量图标，并提供多种风格的 PNG 渲染。

**URL 格式：**
```
https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-png/{variant}/{slug}.png
```

**两种变体：**
- `dark/{slug}.png` — 白色/浅色图标，适配深色背景
- `light/{slug}.png` — 深色/彩色图标，适配浅色背景

**实现方式：** 在 `download_hd_logos.py` 中维护 `LOBE_SLUGS` 映射表，将工具名称翻译为 LobeHub slug。

```python
LOBE_SLUGS = {
    "ChatGPT": "openai",
    "Claude": "claude",
    "Gemini": "gemini",
    "Kimi": "kimi",
    "豆包": "doubao",
    # ... 共 40+ 工具
}
```

**下载核心逻辑：**
```python
def download(url: str, filepath: str, min_size: int = 200) -> bool:
    """通过 curl 下载，检查 HTTP 200 和文件大小阈值"""
    r = subprocess.run(
        ["curl", "-s", "-o", filepath, "-w", "%{http_code} %{size_download}", url],
        capture_output=True, text=True, timeout=30
    )
    # < 200 字节的文件通常是默认占位图，丢弃
    if status == "200" and size >= min_size:
        return True
    # 失败则清理残留文件
    if os.path.exists(filepath):
        os.remove(filepath)
    return False
```

### 第二级：SimpleIcons SVG

[SimpleIcons](https://simpleicons.org/) 收录了大量品牌的 SVG 图标，作为 LobeHub 的降级方案。

**URL 格式：** `https://cdn.simpleicons.org/{slug}`

同样维护 `SI_SLUGS` 映射表。SVG 为矢量格式，缩放不失真，文件通常较小。

### 第三级：DuckDuckGo / Google Favicon

对于两级 HD 源均不存在的工具，降级到网站的 favicon：

- DuckDuckGo: `https://icons.duckduckgo.com/ip3/{domain}.ico`
- Google: `https://www.google.com/s2/favicons?domain={domain}&sz=64`

这些 .ico 图标较小（16-48px），但能保持品牌可识别性，优于显示首字母占位符。

---

## 完整下载流程

```
每个工具循环:
  1. 删除旧的 .ico / .webp 文件
  2. 尝试 LobeHub PNG → 成功则保存 tool_{id}.png，更新 DB
  3. 失败则尝试 SimpleIcons SVG → 成功则保存 tool_{id}.svg
  4. 仍失败则尝试 DuckDuckGo/Google favicon → 保存 tool_{id}.ico
  5. 所有来源都失败 → 报 SKIP
```

更新 DB 时逐个提交，确保部分成功不会丢失进度。

---

## 前端渲染

`ToolCard.vue` 中图片处理逻辑：

```html
<img v-if="tool.image_url && !imgError"
     :src="tool.image_url"
     @error="imgError = true" />
<span v-else>
  {{ tool.name[0] }}  <!-- 首字母占位符 -->
</span>
```

- 有图片 URL 且加载成功 → 显示图片（`object-contain` 保持比例）
- URL 为空或加载失败（`@error`） → 显示首字母
- 首字母搭配分类对应的渐变背景（indigo-100、pink-100 等）
- 悬停时图标有 `scale-110` 放大效果

---

## 文件结构

```
backend/
├── download_hd_logos.py    # 主下载脚本
├── static/logos/            # 下载的图标文件存储目录
│   ├── tool_1.png           # ChatGPT (LobeHub light)
│   ├── tool_2.png           # Claude (LobeHub light)
│   ├── tool_25.ico          # Leonardo.ai (favicon 兜底)
│   └── ...
└── data.db                  # 数据库，image_url 字段记录图片路径
```

---

## 最终数据

| 状态 | 数量 | 来源 |
|------|------|------|
| LobeHub 高清 PNG | 46 | ChatGPT、Claude、Midjourney 等主流工具 |
| SimpleIcons SVG | 1 | Grammarly AI |
| 网站 .ico Favicon | 21 | Fooocus、Canva AI、Gamma 等无 HD 源的工具 |
| .webp（早期遗留） | 1 | Haiper |

总计：69 个工具全部有图标可显示。

---

## 遇到的困难与解决

### 1. DuckDuckGo 图标模糊

**问题：** DuckDuckGo 图标服务返回的 .ico 文件通常只有 16×16 像素，在 80×80 显示区域中严重模糊。

**解决：** 引入 LobeHub（高质量 PNG）和 SimpleIcons（矢量 SVG）作为优先来源，DuckDuckGo 图标仅作为最后降级。

### 2. Python urllib SSL 错误

**问题：** 使用 Python 的 `urllib.request` 下载 Clearbit 图标时持续报 SSL 错误（exit code 35）。

**解决：** 改用 `subprocess.run(["curl", ...])` 调用系统 curl，避免 Python SSL 库的兼容性问题。

### 3. LobeHub 图标变体选错

**问题：** 最初使用了 LobeHub 的 `dark/` 系列图标。这些图标是白色/浅色设计，适配深色背景。而项目的工具卡片背景是浅色渐变（indigo-100、pink-100），导致白色图标完全不可见，用户反馈"统一白色的标"。

**解决：** 切换到 `light/` 系列图标（深色/彩色设计），完美适配浅色背景。删除所有旧 PNG 后重新下载。

### 4. 空 image_url 导致图片加载异常

**问题：** 将无 HD 源工具的 `image_url` 设为空字符串 `""` 后，Vue 的 `<img>` 标签加载 `src=""` 会请求当前页面 URL（返回 HTML），浏览器不会触发 `@error` 事件，导致首字母占位符也未显示。

**解决：** 
- 前端修复：`v-if="tool.image_url && !imgError"` — 增加空字符串判断
- 数据修复：保留 favicon 的 .ico URL，确保始终有图片可加载

### 5. GitHub Raw 下载超时

**问题：** LobeHub 图标从 GitHub Raw 下载，部分请求因网络原因超时（15s 不够），导致下载失败且覆写了已成功的文件（文件变 0 字节）。

**解决：** curl 超时从 15s 提升至 30s；对已损坏的 0 字节文件单独重新下载。

### 6. 部分工具无任何 HD 源

**问题：** Fooocus、Continue、Amazon Q 等 21 个工具在 LobeHub 和 SimpleIcons 中均无对应图标。

**解决：** 降级使用 DuckDuckGo 或 Google Favicons 服务获取网站 favicon。Fooocus 官网 `fooocus.com` 无 favicon，改从 `fooocus.ai` 获取（47KB，实际为 PNG 格式）。

### 7. 图标来源可用性受限

**问题：** Clearbit Logo API（`logo.clearbit.com/{domain}`）在国内网络环境下完全不可用（SSL 连接错误 exit code 35），unavatar.io 返回 403 或被超时阻塞。

**解决：** 移除不可用的来源，集中维护三个可靠的来源链：LobeHub → SimpleIcons → DuckDuckGo/Google。
