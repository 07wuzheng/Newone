from urllib.parse import urlparse
import json
from database import engine, SessionLocal, Base
from models import Category, Tool
from version_fetcher import get_initial_version
from datetime import datetime, timezone
from seed_new_fields import NEW_FIELDS

Base.metadata.create_all(bind=engine)

categories = [
    {"name": "LLM / 对话", "slug": "llm", "description": "大语言模型和对话式 AI 助手", "icon": "chat"},
    {"name": "AI 绘画", "slug": "ai-image", "description": "AI 图像生成和编辑工具", "icon": "image"},
    {"name": "AI 视频", "slug": "ai-video", "description": "AI 视频生成和编辑工具", "icon": "video"},
    {"name": "代码助手", "slug": "coding", "description": "AI 代码补全和编程助手", "icon": "code"},
    {"name": "AI 音频", "slug": "ai-audio", "description": "AI 音乐和语音合成工具", "icon": "music"},
    {"name": "其他", "slug": "others", "description": "其他实用 AI 工具", "icon": "grid"},
]

tools_data = [
    # ─── LLM / 对话（15 个）──────────────────────────────────
    {"name": "ChatGPT", "description": "OpenAI 开发的对话式 AI，擅长文本生成、代码编写、分析推理", "url": "https://chatgpt.com", "category_slug": "llm", "rating": 4.8, "featured": True},
    {"name": "Claude", "description": "Anthropic 开发的 AI 助手，擅长长文本理解和深度分析", "url": "https://claude.ai", "category_slug": "llm", "rating": 4.7, "featured": True},
    {"name": "Gemini", "description": "Google 开发的多模态 AI 助手，支持文本/图片/视频理解", "url": "https://gemini.google.com", "category_slug": "llm", "rating": 4.5, "featured": True},
    {"name": "DeepSeek", "description": "深度求索开发的 AI 对话模型，推理能力强，支持超长上下文", "url": "https://chat.deepseek.com", "category_slug": "llm", "rating": 4.6, "featured": True},
    {"name": "Kimi", "description": "月之暗面开发的 AI 助手，擅长长文本分析和文件处理", "url": "https://kimi.moonshot.cn", "category_slug": "llm", "rating": 4.4, "featured": False},
    {"name": "豆包", "description": "字节跳动开发的 AI 对话助手，支持多模态交互和插件生态", "url": "https://www.doubao.com", "category_slug": "llm", "rating": 4.3, "featured": False},
    {"name": "智谱清言", "description": "智谱 AI 开发的对话模型，基于 GLM 架构，中文能力强", "url": "https://chatglm.cn", "category_slug": "llm", "rating": 4.2, "featured": False},
    {"name": "Grok", "description": "xAI 开发的 AI 助手，实时接入 X 平台数据，风格幽默", "url": "https://grok.com", "category_slug": "llm", "rating": 4.4, "featured": False},
    {"name": "Mistral AI", "description": "法国 AI 公司开发的开放语言模型，性能优异", "url": "https://chat.mistral.ai", "category_slug": "llm", "rating": 4.1, "featured": False},
    {"name": "讯飞星火", "description": "科大讯飞开发的 AI 对话助手，中文语音交互能力强", "url": "https://xinghuo.xfyun.cn", "category_slug": "llm", "rating": 4.1, "featured": False},
    {"name": "百川智能", "description": "百川智能开发的 AI 对话助手，支持多轮对话和知识问答", "url": "https://www.baichuan-ai.com", "category_slug": "llm", "rating": 4.0, "featured": False},
    {"name": "腾讯元宝", "description": "腾讯开发的 AI 对话助手，集成微信生态能力", "url": "https://yuanbao.tencent.com", "category_slug": "llm", "rating": 4.0, "featured": False},
    {"name": "零一万物", "description": "李开复创立的 AI 公司，Yi 系列模型性能强劲", "url": "https://www.lingyiwanwu.com", "category_slug": "llm", "rating": 4.2, "featured": False},
    {"name": "文心一言", "description": "百度开发的 AI 对话助手，中文理解能力强", "url": "https://yiyan.baidu.com", "category_slug": "llm", "rating": 4.2, "featured": False},
    {"name": "通义千问", "description": "阿里巴巴开发的 AI 对话助手，支持多模态", "url": "https://tongyi.aliyun.com", "category_slug": "llm", "rating": 4.1, "featured": False},

    # ─── AI 绘画（12 个）────────────────────────────────────
    {"name": "Midjourney", "description": "以高质量艺术风格著称的 AI 图像生成工具", "url": "https://www.midjourney.com", "category_slug": "ai-image", "rating": 4.7, "featured": True},
    {"name": "DALL-E 3", "description": "OpenAI 开发的文本到图像生成工具，理解自然语言能力强", "url": "https://openai.com/dall-e-3", "category_slug": "ai-image", "rating": 4.5, "featured": True},
    {"name": "Stable Diffusion", "description": "开源 AI 图像生成模型，可本地部署自由定制", "url": "https://stability.ai", "category_slug": "ai-image", "rating": 4.4, "featured": True},
    {"name": "Adobe Firefly", "description": "Adobe 开发的 AI 图像生成工具，与 Creative Cloud 深度集成", "url": "https://firefly.adobe.com", "category_slug": "ai-image", "rating": 4.3, "featured": False},
    {"name": "Flux", "description": "Black Forest Labs 开发的 AI 图像生成模型，画质细腻逼真", "url": "https://blackforestlabs.ai", "category_slug": "ai-image", "rating": 4.5, "featured": False},
    {"name": "ComfyUI", "description": "基于节点的 AI 图像生成工作流工具，高度灵活可定制", "url": "https://www.comfy.org", "category_slug": "ai-image", "rating": 4.3, "featured": False},
    {"name": "Ideogram", "description": "AI 图像生成工具，文字渲染能力行业领先", "url": "https://ideogram.ai", "category_slug": "ai-image", "rating": 4.2, "featured": False},
    {"name": "Recraft", "description": "AI 设计平台，支持生成矢量图和品牌视觉素材", "url": "https://www.recraft.ai", "category_slug": "ai-image", "rating": 4.1, "featured": False},
    {"name": "Fooocus", "description": "开源 AI 图像生成工具，界面简洁，上手即用", "url": "https://fooocus.com", "category_slug": "ai-image", "rating": 4.0, "featured": False},
    {"name": "Leonardo.ai", "description": "AI 图像生成和编辑平台，内置多种风格模型", "url": "https://leonardo.ai", "category_slug": "ai-image", "rating": 4.3, "featured": False},
    {"name": "Clipdrop", "description": "Stability AI 开发的 AI 图像编辑工具，支持一键抠图/替换背景", "url": "https://clipdrop.co", "category_slug": "ai-image", "rating": 4.0, "featured": False},
    {"name": "Krea AI", "description": "AI 图像和视频生成平台，实时生成和编辑能力突出", "url": "https://www.krea.ai", "category_slug": "ai-image", "rating": 4.1, "featured": False},

    # ─── AI 视频（11 个）─────────────────────────────────────
    {"name": "Runway", "description": "AI 视频生成和编辑平台，支持文生视频、图生视频、视频修编", "url": "https://runwayml.com", "category_slug": "ai-video", "rating": 4.4, "featured": True},
    {"name": "可灵 (Kling)", "description": "快手开发的 AI 视频生成工具，支持文生视频和图生视频", "url": "https://kling.kuaishou.com", "category_slug": "ai-video", "rating": 4.5, "featured": False},
    {"name": "Vidu", "description": "生数科技开发的 AI 视频生成工具，支持多风格视频创作", "url": "https://www.vidu.ai", "category_slug": "ai-video", "rating": 4.2, "featured": False},
    {"name": "Luma Dream Machine", "description": "AI 视频生成工具，物理世界模拟和镜头运动表现出色", "url": "https://lumalabs.ai", "category_slug": "ai-video", "rating": 4.3, "featured": False},
    {"name": "Pika", "description": "AI 视频生成工具，操作简单，生成速度快", "url": "https://pika.art", "category_slug": "ai-video", "rating": 4.2, "featured": False},
    {"name": "Sora", "description": "OpenAI 开发的文本到视频生成工具，画质逼真", "url": "https://openai.com/sora", "category_slug": "ai-video", "rating": 4.6, "featured": True},
    {"name": "CapCut", "description": "剪映海外版，集成 AI 功能的视频编辑工具", "url": "https://www.capcut.com", "category_slug": "ai-video", "rating": 4.3, "featured": False},
    {"name": "HeyGen", "description": "AI 数字人视频生成平台，支持多语言口型同步", "url": "https://www.heygen.com", "category_slug": "ai-video", "rating": 4.4, "featured": False},
    {"name": "Synthesia", "description": "AI 虚拟主播视频生成平台，企业级 AI 视频创作", "url": "https://www.synthesia.io", "category_slug": "ai-video", "rating": 4.3, "featured": False},
    {"name": "Viggle", "description": "AI 角色动画生成工具，让静态角色动起来", "url": "https://viggle.ai", "category_slug": "ai-video", "rating": 4.0, "featured": False},
    {"name": "Haiper", "description": "AI 视频生成和编辑工具，免费易用", "url": "https://haiper.ai", "category_slug": "ai-video", "rating": 4.0, "featured": False},

    # ─── 代码助手（11 个）─────────────────────────────────────
    {"name": "GitHub Copilot", "description": "AI 代码补全助手，集成在 VS Code/JetBrains 等编辑器中", "url": "https://github.com/features/copilot", "category_slug": "coding", "rating": 4.6, "featured": True},
    {"name": "Cursor", "description": "AI 优先的代码编辑器，内置对话式编程和智能补全", "url": "https://cursor.sh", "category_slug": "coding", "rating": 4.5, "featured": True},
    {"name": "Windsurf", "description": "Codeium 推出的 AI 原生 IDE，深度集成 AI 编程能力", "url": "https://codeium.com/windsurf", "category_slug": "coding", "rating": 4.4, "featured": False},
    {"name": "Continue", "description": "开源 AI 代码助手，支持接入本地和云端模型", "url": "https://continue.dev", "category_slug": "coding", "rating": 4.2, "featured": False},
    {"name": "Amazon Q", "description": "AWS 开发的 AI 编程助手，深度集成 AWS 生态", "url": "https://aws.amazon.com/q", "category_slug": "coding", "rating": 4.0, "featured": False},
    {"name": "Replit Agent", "description": "Replit 平台内置的 AI 编程代理，从描述直接生成应用", "url": "https://replit.com", "category_slug": "coding", "rating": 4.1, "featured": False},
    {"name": "Cody", "description": "Sourcegraph 开发的 AI 代码助手，理解整个代码仓库上下文", "url": "https://sourcegraph.com/cody", "category_slug": "coding", "rating": 4.1, "featured": False},
    {"name": "Cline", "description": "VS Code AI 编程扩展，支持自主编码和终端操作", "url": "https://cline.bot", "category_slug": "coding", "rating": 4.3, "featured": True},
    {"name": "Devin AI", "description": "Cognition AI 开发的 AI 软件工程师，独立完成编码任务", "url": "https://cognition.ai", "category_slug": "coding", "rating": 4.0, "featured": False},
    {"name": "Tabnine", "description": "AI 代码补全工具，支持本地模型保护代码隐私", "url": "https://www.tabnine.com", "category_slug": "coding", "rating": 4.0, "featured": False},
    {"name": "Codeium", "description": "免费的 AI 代码加速工具，支持 70+ 语言和 IDE", "url": "https://codeium.com", "category_slug": "coding", "rating": 4.1, "featured": False},

    # ─── AI 音频（10 个）─────────────────────────────────────
    {"name": "Suno", "description": "AI 音乐生成平台，输入歌词和风格即可生成完整歌曲", "url": "https://suno.com", "category_slug": "ai-audio", "rating": 4.4, "featured": True},
    {"name": "ElevenLabs", "description": "AI 语音合成工具，支持语音克隆和多种语言、情感表达", "url": "https://elevenlabs.io", "category_slug": "ai-audio", "rating": 4.5, "featured": False},
    {"name": "Udio", "description": "AI 音乐生成平台，生成音质出色，支持多种音乐风格", "url": "https://www.udio.com", "category_slug": "ai-audio", "rating": 4.3, "featured": False},
    {"name": "Fish Audio", "description": "AI 语音合成工具，支持语音克隆、情感控制", "url": "https://fish.audio", "category_slug": "ai-audio", "rating": 4.2, "featured": False},
    {"name": "讯飞配音", "description": "科大讯飞开发的 AI 配音工具，支持多种发音人和方言", "url": "https://peiyun.xfyun.cn", "category_slug": "ai-audio", "rating": 4.1, "featured": False},
    {"name": "Play.ht", "description": "AI 语音生成平台，支持文本转语音和语音克隆", "url": "https://play.ht", "category_slug": "ai-audio", "rating": 4.0, "featured": False},
    {"name": "Voicemod", "description": "AI 实时变声工具，支持游戏和直播场景的语音转换", "url": "https://www.voicemod.net", "category_slug": "ai-audio", "rating": 4.1, "featured": False},
    {"name": "Mubert", "description": "AI 音乐生成平台，可生成背景音乐和电子音乐", "url": "https://mubert.com", "category_slug": "ai-audio", "rating": 3.8, "featured": False},
    {"name": "Adobe Podcast", "description": "AI 音频增强工具，一键降噪和音质提升", "url": "https://podcast.adobe.com", "category_slug": "ai-audio", "rating": 4.2, "featured": False},
    {"name": "Resemble AI", "description": "AI 语音合成工具，支持语音克隆、自定义声音创作", "url": "https://www.resemble.ai", "category_slug": "ai-audio", "rating": 3.9, "featured": False},

    # ─── 其他（10 个）────────────────────────────────────────
    {"name": "Perplexity", "description": "AI 驱动的搜索引擎，直接给出答案并标注信息来源", "url": "https://www.perplexity.ai", "category_slug": "others", "rating": 4.5, "featured": True},
    {"name": "Grammarly AI", "description": "AI 写作助手，支持语法检查、风格优化和 AI 润色", "url": "https://www.grammarly.com", "category_slug": "others", "rating": 4.4, "featured": False},
    {"name": "Notion AI", "description": "笔记和协作平台的内置 AI 助手，支持写作辅助和信息整理", "url": "https://www.notion.so", "category_slug": "others", "rating": 4.3, "featured": False},
    {"name": "Canva AI", "description": "设计平台内置的 AI 功能，支持文生图、AI 编辑和设计生成", "url": "https://www.canva.com", "category_slug": "others", "rating": 4.2, "featured": False},
    {"name": "Gamma", "description": "AI 演示文稿生成工具，输入主题自动生成精美 PPT", "url": "https://gamma.app", "category_slug": "others", "rating": 4.1, "featured": False},
    {"name": "Otter.ai", "description": "AI 会议记录工具，自动转录、总结会议内容", "url": "https://otter.ai", "category_slug": "others", "rating": 4.2, "featured": False},
    {"name": "Beautiful.ai", "description": "AI 演示文稿设计工具，自动排版让 PPT 更专业", "url": "https://www.beautiful.ai", "category_slug": "others", "rating": 4.0, "featured": False},
    {"name": "Consensus", "description": "AI 学术搜索引擎，从海量论文中找到研究答案", "url": "https://consensus.app", "category_slug": "others", "rating": 4.1, "featured": False},
    {"name": "Krisp AI", "description": "AI 降噪工具，实时消除背景噪音和回声", "url": "https://krisp.ai", "category_slug": "others", "rating": 4.0, "featured": False},
    {"name": "Elicit", "description": "AI 学术文献分析工具，帮助研究人员快速筛选和理解论文", "url": "https://elicit.com", "category_slug": "others", "rating": 4.1, "featured": False},
]

# Domain overrides for Clearbit logo URLs
_DOMAIN_OVERRIDES = {
    "Kimi": "moonshot.cn",
    "Grok": "grok.com",
    "Mistral AI": "mistral.ai",
    "DeepSeek": "deepseek.com",
    "豆包": "doubao.com",
    "智谱清言": "chatglm.cn",
    "讯飞星火": "xfyun.cn",
    "百川智能": "baichuan-ai.com",
    "腾讯元宝": "tencent.com",
    "零一万物": "lingyiwanwu.com",
    "文心一言": "baidu.com",
    "通义千问": "aliyun.com",
    "可灵 (Kling)": "kuaishou.com",
    "Vidu": "vidu.ai",
    "Luma Dream Machine": "lumalabs.ai",
    "Pika": "pika.art",
    "HeyGen": "heygen.com",
    "Synthesia": "synthesia.io",
    "Viggle": "viggle.ai",
    "Haiper": "haiper.ai",
    "GitHub Copilot": "github.com",
    "Windsurf": "codeium.com",
    "Continue": "continue.dev",
    "Amazon Q": "amazon.com",
    "Cody": "sourcegraph.com",
    "Devin AI": "cognition.ai",
    "Tabnine": "tabnine.com",
    "Codeium": "codeium.com",
    "ElevenLabs": "elevenlabs.io",
    "Fish Audio": "fish.audio",
    "讯飞配音": "xfyun.cn",
    "Play.ht": "play.ht",
    "Voicemod": "voicemod.net",
    "Mubert": "mubert.com",
    "Adobe Podcast": "adobe.com",
    "Resemble AI": "resemble.ai",
    "Perplexity": "perplexity.ai",
    "Grammarly AI": "grammarly.com",
    "Notion AI": "notion.so",
    "Canva AI": "canva.com",
    "Gamma": "gamma.app",
    "Otter.ai": "otter.ai",
    "Beautiful.ai": "beautiful.ai",
    "Consensus": "consensus.app",
    "Krisp AI": "krisp.ai",
    "Elicit": "elicit.com",
    "Midjourney": "midjourney.com",
    "Stable Diffusion": "stability.ai",
    "Adobe Firefly": "adobe.com",
    "Flux": "blackforestlabs.ai",
    "ComfyUI": "comfy.org",
    "Ideogram": "ideogram.ai",
    "Recraft": "recraft.ai",
    "Fooocus": "fooocus.com",
    "Leonardo.ai": "leonardo.ai",
    "Clipdrop": "clipdrop.co",
    "Krea AI": "krea.ai",
    "Runway": "runwayml.com",
    "Suno": "suno.com",
    "Udio": "udio.com",
    "CapCut": "capcut.com",
    "Replit Agent": "replit.com",
    "Cline": "cline.bot",
    "DALL-E 3": "openai.com",
    "Sora": "openai.com",
    "ChatGPT": "chatgpt.com",
    "Claude": "claude.ai",
    "Gemini": "gemini.google.com",
}


def _get_logo_url(tool_name: str, tool_url: str) -> str:
    """Build a DuckDuckGo favicon URL for the given tool."""
    domain = _DOMAIN_OVERRIDES.get(tool_name)
    if not domain:
        domain = urlparse(tool_url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
    return f"https://icons.duckduckgo.com/ip3/{domain}.ico"


def seed():
    db = SessionLocal()

    if db.query(Category).count() > 0:
        print("数据库已有数据，跳过填充")
        db.close()
        return

    now = datetime.now(timezone.utc)
    slug_to_id = {}
    for i, cat in enumerate(categories, start=1):
        c = Category(id=i, **cat)
        db.add(c)
        slug_to_id[cat["slug"]] = i

    for i, t in enumerate(tools_data, start=1):
        name = t["name"]
        version = get_initial_version(name)
        extra = NEW_FIELDS.get(name, {})
        tool = Tool(
            id=i,
            name=name,
            description=t["description"],
            url=t["url"],
            category_id=slug_to_id[t["category_slug"]],
            image_url=_get_logo_url(name, t["url"]),
            rating=t["rating"],
            is_featured=t["featured"],
            created_at=now,
            version=version,
            version_updated_at=now,
            pricing=extra.get("pricing"),
            tags=json.dumps(extra.get("tags", []), ensure_ascii=False),
            pros=extra.get("pros"),
            cons=extra.get("cons"),
            editor_pick=extra.get("editor_pick", False),
            screenshots=json.dumps(extra.get("screenshots", []), ensure_ascii=False) if extra.get("screenshots") else None,
        )
        db.add(tool)

    db.commit()
    print(f"填充完成：{len(categories)} 个分类，{len(tools_data)} 个工具")
    db.close()


if __name__ == "__main__":
    seed()
