# 种子数据 — 预置 AI 工具列表

> 用途：开发时直接填充数据库。共 69 个工具，覆盖 6 个分类。

## LLM / 对话（15 个）

| 名称 | 版本 | 官网 |
|------|------|------|
| ChatGPT | GPT-5.x | https://chatgpt.com |
| Claude | Opus 4.8 | https://claude.ai |
| Gemini | Gemini 3.1 Pro | https://gemini.google.com |
| DeepSeek | DeepSeek-V4 | https://chat.deepseek.com |
| Kimi | Kimi K2 | https://kimi.moonshot.cn |
| 豆包 | 豆包 3.0 | https://www.doubao.com |
| 智谱清言 | GLM-5 | https://chatglm.cn |
| Grok | Grok 4 | https://grok.com |
| Mistral AI | Mistral Large 3 | https://chat.mistral.ai |
| 讯飞星火 | 星火 5.0 | https://xinghuo.xfyun.cn |
| 百川智能 | Baichuan 4 | https://www.baichuan-ai.com |
| 腾讯元宝 | 元宝 2.0 | https://yuanbao.tencent.com |
| 零一万物 | Yi-Lightning | https://www.lingyiwanwu.com |
| 文心一言 | 文心 5.1 | https://yiyan.baidu.com |
| 通义千问 | Qwen3.7-Max | https://tongyi.aliyun.com |

## AI 绘画（12 个）

| 名称 | 版本 | 官网 |
|------|------|------|
| Midjourney | V8.1 | https://www.midjourney.com |
| DALL-E 3 | DALL-E 4 | https://openai.com/dall-e-3 |
| Stable Diffusion | SD4 Ultra | https://stability.ai |
| Adobe Firefly | Firefly 4 | https://firefly.adobe.com |
| Flux | Flux.1 Pro | https://blackforestlabs.ai |
| ComfyUI | Latest | https://www.comfy.org |
| Ideogram | Ideogram 4.0 | https://ideogram.ai |
| Recraft | Recraft V3 | https://www.recraft.ai |
| Fooocus | 2.5 | https://fooocus.com |
| Leonardo.ai | Phoenix 1.0 | https://leonardo.ai |
| Clipdrop | Latest | https://clipdrop.co |
| Krea AI | Krea 2.0 | https://www.krea.ai |

## AI 视频（11 个）

| 名称 | 版本 | 官网 |
|------|------|------|
| Runway | Gen-4.5 | https://runwayml.com |
| 可灵 (Kling) | 可灵 2.0 | https://kling.kuaishou.com |
| Vidu | Vidu 2.0 | https://www.vidu.ai |
| Luma Dream Machine | Dream Machine 1.6 | https://lumalabs.ai |
| Pika | 3.0 | https://pika.art |
| Sora | 已关停 | https://openai.com/sora |
| CapCut | Latest | https://www.capcut.com |
| HeyGen | HeyGen 3.0 | https://www.heygen.com |
| Synthesia | Synthesia 3.0 | https://www.synthesia.io |
| Viggle | Viggle 2.0 | https://viggle.ai |
| Haiper | Haiper 2.0 | https://haiper.ai |

## 代码助手（11 个）

| 名称 | 版本 | 官网 |
|------|------|------|
| GitHub Copilot | GPT-5.3-Codex | https://github.com/features/copilot |
| Cursor | 3.3.27 | https://cursor.sh |
| Windsurf | Windsurf 3.0 | https://codeium.com/windsurf |
| Continue | Continue 3.0 | https://continue.dev |
| Amazon Q | Q Developer 3.0 | https://aws.amazon.com/q |
| Replit Agent | Replit Agent 2.0 | https://replit.com |
| Cody | Cody 5.0 | https://sourcegraph.com/cody |
| Cline | 3.2.14 | https://cline.bot |
| Devin AI | Devin 2.0 | https://cognition.ai |
| Tabnine | Latest | https://www.tabnine.com |
| Codeium | Latest | https://codeium.com |

## AI 音频（10 个）

| 名称 | 版本 | 官网 |
|------|------|------|
| Suno | v5.5 | https://suno.com |
| ElevenLabs | Flash v2.5 | https://elevenlabs.io |
| Udio | v1.5 | https://www.udio.com |
| Fish Audio | Fish Speech 2.0 | https://fish.audio |
| 讯飞配音 | Latest | https://peiyun.xfyun.cn |
| Play.ht | Latest | https://play.ht |
| Voicemod | Voicemod 3.0 | https://www.voicemod.net |
| Mubert | Latest | https://mubert.com |
| Adobe Podcast | Latest | https://podcast.adobe.com |
| Resemble AI | Resemble 2.0 | https://www.resemble.ai |

## 其他（10 个）

| 名称 | 版本 | 官网 |
|------|------|------|
| Perplexity | Perplexity 3.0 | https://www.perplexity.ai |
| Grammarly AI | Grammarly 3.0 | https://www.grammarly.com |
| Notion AI | Latest | https://www.notion.so |
| Canva AI | Latest | https://www.canva.com |
| Gamma | Latest | https://gamma.app |
| Otter.ai | Otter 4.0 | https://otter.ai |
| Beautiful.ai | Latest | https://www.beautiful.ai |
| Consensus | Consensus 2.0 | https://consensus.app |
| Krisp AI | Krisp 3.0 | https://krisp.ai |
| Elicit | Elicit 3.0 | https://elicit.com |

## 版本更新机制

详见 `version_fetcher.py`：
- **自定义抓取器**（21 个）：精准抓取官方文档/更新日志中的版本号
- **通用嗅探器**（48 个）：从官网首页可见文本中识别版本号
- **环境变量**：`HTTPS_PROXY` 配置代理、`VERSION_FETCHER_DISABLE=1` 禁用抓取
- **调度**：后台每 12 小时检查一次，失败时每 30 分钟重试
- **手动触发**：`POST /api/admin/refresh-versions`
