"""AI Agent for tool recommendation using DeepSeek API."""
import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from database import SessionLocal
from models import Tool, Category

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(_env_path)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

MAX_TOKENS_PER_DAY = 5000
_daily_tokens = 0

import sys
print(f"[agent] loaded, _daily_tokens={_daily_tokens}", file=sys.stderr)


def _check_daily_budget():
    global _daily_tokens
    return _daily_tokens < MAX_TOKENS_PER_DAY


def _add_tokens(n):
    global _daily_tokens
    _daily_tokens += n


def _get_categories_list():
    db = SessionLocal()
    cats = db.query(Category).all()
    result = [{"slug": c.slug, "name": c.name} for c in cats]
    db.close()
    return result


SYSTEM_PROMPT = """你是一个 AI 工具导航助手，帮助用户发现和推荐 AI 工具。

可用的工具分类（slug → 名称）：
{category_list}

定价类型：free（免费）、freemium（免费增值）、paid（付费）

规则：
- 用户说"画画""绘图""作图""生成图片""AI 绘画"等都算 AI 工具相关
- 用户说"做视频""剪辑""生成视频"等都算 AI 工具相关
- 用户说"写代码""编程""代码助手"等都算 AI 工具相关
- 用户说"做音乐""生成音乐""语音"等都算 AI 工具相关
- 只要模糊涉及上述领域，都算 AI 工具相关，不要拒绝
- 只有当问题完全与 AI 或工具推荐无关时才拒绝

请严格按以下 JSON 格式输出搜索条件（只输出 JSON，不要其他内容）：
{{
  "query": "提取的关键词（用于搜索工具名称/描述，可为空字符串）",
  "category_slug": null 或 "llm"/"ai-image"/"ai-video"/"coding"/"ai-audio"/"others",
  "pricing": null 或 "free"/"freemium"/"paid",
  "max_results": 5
}}

如果问题与 AI 工具完全无关，输出：
{{"error": "抱歉，我只回答 AI 工具相关的问题，比如推荐绘画工具、视频生成工具等等～"}}
"""

# 关键词同义词映射，用于扩展搜索
SYNONYM_MAP = {
    "画画": ["绘画", "图像", "图片", "AI 绘画", "image"],
    "画图": ["绘画", "图像", "图片", "AI 绘画"],
    "绘图": ["绘画", "图像", "图片", "AI 绘画"],
    "图片": ["图像", "绘画", "AI 绘画"],
    "做视频": ["视频", "视频生成", "剪辑", "AI 视频"],
    "生成视频": ["视频", "视频生成", "AI 视频"],
    "剪视频": ["视频", "剪辑", "AI 视频"],
    "剪辑": ["视频", "AI 视频"],
    "写代码": ["代码", "编程", "代码助手"],
    "编程": ["代码", "代码助手"],
    "做音乐": ["音乐", "音频", "AI 音频"],
    "音乐": ["音频", "AI 音频"],
    "语音": ["音频", "AI 音频"],
    "聊天": ["对话", "大语言模型"],
    "对话": ["对话", "大语言模型"],
    "搜索": ["搜索", "研究"],
}

# 意图→分类的映射（关键词匹配不到时兜底）
INTENT_CATEGORY = {
    "画": "ai-image",
    "图": "ai-image",
    "图像": "ai-image",
    "绘画": "ai-image",
    "视频": "ai-video",
    "剪辑": "ai-video",
    "音乐": "ai-audio",
    "音频": "ai-audio",
    "语音": "ai-audio",
    "代码": "coding",
    "编程": "coding",
    "聊天": "llm",
    "对话": "llm",
    "搜索": "others",
}


def parse_search_params(user_message: str) -> dict:
    """Use DeepSeek to extract search params from user message."""
    if not _check_daily_budget():
        return {"error": "DEBUG_TOKEN_BUDGET_EXCEEDED"}

    cats = _get_categories_list()
    cat_desc = "\n".join([f"  - {c['slug']}: {c['name']}" for c in cats])
    system = SYSTEM_PROMPT.format(category_list=cat_desc)

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_message},
            ],
            temperature=0.1,
            max_tokens=300,
        )
        content = resp.choices[0].message.content.strip()
        _add_tokens(resp.usage.total_tokens)

        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            params = json.loads(json_match.group())
            return params
        return {"error": "抱歉，我没有理解你的意思，能换个方式问问吗？"}
    except Exception as e:
        return {"error": f"思考时出了点小问题: {str(e)}"}


if _check_daily_budget():
    pass  # Agent ready


def _expand_keywords(query: str) -> list:
    """Expand keywords using synonym map."""
    keywords = [query]
    for word, syns in SYNONYM_MAP.items():
        if word in query:
            keywords.extend(syns)
    # Deduplicate
    seen = set()
    result = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            result.append(kw)
    return result


def _infer_category_slug(query: str) -> str | None:
    """Infer category slug from query keywords."""
    for word, slug in INTENT_CATEGORY.items():
        if word in query:
            return slug
    return None


def _search_tools(params: dict) -> list:
    """Search tools in database based on params."""
    db = SessionLocal()
    query = db.query(Tool)

    cat_slug = params.get("category_slug")
    if cat_slug:
        cat = db.query(Category).filter(Category.slug == cat_slug).first()
        if cat:
            query = query.filter(Tool.category_id == cat.id)

    pricing = params.get("pricing")
    if pricing:
        query = query.filter(Tool.pricing == pricing)

    keywords = params.get("query", "")
    if keywords:
        from sqlalchemy import or_
        expanded = _expand_keywords(keywords)
        filters = []
        for kw in expanded:
            kw_filter = f"%{kw}%"
            filters.append(or_(
                Tool.name.like(kw_filter),
                Tool.description.like(kw_filter),
                Tool.tags.contains(kw),
            ))
        query = query.filter(or_(*filters))

    query = query.order_by(Tool.is_featured.desc(), Tool.rating.desc())
    max_results = params.get("max_results", 5)
    tools = query.limit(max_results).all()

    # If no results with keyword, try just category + pricing
    if not tools and cat_slug:
        query2 = db.query(Tool).filter(Tool.category_id == (
            db.query(Category).filter(Category.slug == cat_slug).first().id
        ))
        if pricing:
            query2 = query2.filter(Tool.pricing == pricing)
        tools = query2.order_by(Tool.is_featured.desc(), Tool.rating.desc()).limit(max_results).all()

    results = []
    for t in tools:
        results.append({
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "url": t.url,
            "rating": t.rating,
            "pricing": t.pricing,
            "category_name": t.category.name if t.category else None,
            "tags": json.loads(t.tags) if t.tags else [],
        })

    db.close()
    return results


def format_response(tools: list, params: dict, raw_message: str) -> str:
    """Format tool results into natural language."""
    if not tools:
        # Try to infer category and recommend anyway
        inferred_slug = _infer_category_slug(raw_message)
        if inferred_slug:
            db = SessionLocal()
            cat = db.query(Category).filter(Category.slug == inferred_slug).first()
            if cat:
                fallback = db.query(Tool).filter(
                    Tool.category_id == cat.id
                ).order_by(
                    Tool.is_featured.desc(), Tool.rating.desc()
                ).limit(5).all()
                db.close()
                if fallback:
                    lines = [f"没有找到精确匹配，但为你推荐 {cat.name} 分类下的热门工具：\n"]
                    for t in fallback:
                        pricing_icon = {"free": "🆓", "freemium": "💎", "paid": "💰"}
                        icon = pricing_icon.get(t.pricing, "")
                        lines.append(
                            f"**{t.name}** {icon} ⭐{t.rating}\n"
                            f"  {t.description[:80]}{'…' if len(t.description) > 80 else ''}\n"
                            f"  [去使用]({t.url})\n"
                        )
                    lines.append("\n💡 告诉我想找什么类型、什么价位的，我能更精准推荐～")
                    return "\n".join(lines)

        pricing_map = {"free": "免费", "freemium": "免费增值", "paid": "付费"}
        pricing_str = pricing_map.get(params.get("pricing", ""), "")
        cat_str = params.get("category_slug", "")
        kw = params.get("query", "")

        parts = []
        if kw:
            parts.append(f"「{kw}」")
        if cat_str:
            parts.append("该分类下")
        if pricing_str:
            parts.append(pricing_str)
        return f"抱歉，没有找到{'的'.join(parts)}AI 工具。试试换个说法，比如「推荐AI绘画工具」「免费的视频工具」之类的～"

    lines = [f"为你找到以下 {len(tools)} 个 AI 工具：\n"]
    for t in tools:
        pricing_icon = {"free": "🆓", "freemium": "💎", "paid": "💰"}
        icon = pricing_icon.get(t["pricing"], "")
        lines.append(
            f"**{t['name']}** {icon} ⭐{t['rating']}\n"
            f"  {t['description'][:80]}{'…' if len(t['description']) > 80 else ''}\n"
            f"  [去使用]({t['url']})\n"
        )
    lines.append("\n💡 告诉我想找什么类型、什么价位的，我能更精准推荐～")
    return "\n".join(lines)


def chat(message: str) -> dict:
    """Main chat function."""
    if not _check_daily_budget():
        return {"response": "今日查询额度已用尽，明天再来吧～", "tools": []}

    params = parse_search_params(message)

    if "error" in params:
        return {"response": params["error"], "tools": []}

    tools = _search_tools(params)
    response = format_response(tools, params, message)

    return {
        "response": response,
        "tools": [{"id": t["id"], "name": t["name"]} for t in tools],
    }
