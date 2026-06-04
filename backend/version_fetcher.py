"""Auto-fetch latest version numbers for AI tools from official sources."""

import os
import re
import httpx
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger("version_fetcher")

TIMEOUT = httpx.Timeout(20.0)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

# ---- Proxy support ----
# Priority: VERSION_FETCHER_PROXY > HTTPS_PROXY > HTTP_PROXY
_PROXY_DISABLED = os.environ.get("VERSION_FETCHER_DISABLE", "").lower() in ("1", "true", "yes")


def _get_proxy():
    """Read proxy from env vars at call time so VPN changes take effect without restart."""
    return (
        os.environ.get("VERSION_FETCHER_PROXY")
        or os.environ.get("HTTPS_PROXY")
        or os.environ.get("HTTP_PROXY")
    )


_client = None


def _get_client():
    """Lazy-init HTTP client, re-creating if proxy config changed."""
    global _client
    proxy = _get_proxy()
    if _client is not None:
        if getattr(_client, '_configured_proxy', None) != proxy:
            _client.close()
            _client = None
    if _client is None:
        kwargs = dict(headers=HEADERS, timeout=TIMEOUT, follow_redirects=True,
                      limits=httpx.Limits(max_keepalive_connections=5, max_connections=10))
        if proxy:
            kwargs["proxies"] = proxy
            logger.info(f"version_fetcher using proxy: {proxy}")
        else:
            logger.info("version_fetcher using direct connection (no proxy configured)")
        _client = httpx.Client(**kwargs)
        _client._configured_proxy = proxy
    return _client


def _sane(version):
    """Reject obviously wrong version strings."""
    if not version or len(version) > 40:
        return False
    if re.match(r'^v?0\.\d+', version):
        return False
    return True


# ─── LLM / 对话 ─────────────────────────────────────────────────


def fetch_chatgpt():
    """Scrape OpenAI models doc for latest GPT model name."""
    try:
        resp = _get_client().get("https://platform.openai.com/docs/models")
        resp.raise_for_status()
        # 先找 GPT-5.x 系列
        majors = re.findall(r'gpt-5\.(\d+)', resp.text, re.IGNORECASE)
        if majors:
            latest = max(int(v) for v in majors)
            v = f"GPT-5.{latest}"
            if _sane(v):
                return v
        # fallback: GPT-4o
        if re.search(r'gpt-4o(?!-)', resp.text, re.IGNORECASE):
            return "GPT-4o"
    except Exception:
        logger.warning("fetch_chatgpt failed", exc_info=True)

    # Fallback: try Chinese-accessible mirror / tech blog
    try:
        resp = _get_client().get("https://www.36kr.com/search/articles/GPT")
        resp.raise_for_status()
        for m in re.finditer(r'GPT[-\s]?(\d+(?:\.\d+)?)', resp.text, re.IGNORECASE):
            v = f"GPT-{m.group(1)}"
            if _sane(v) and float(m.group(1)) >= 4:
                return v
    except Exception:
        pass

    return None


def fetch_claude():
    """Scrape Claude release notes."""
    try:
        resp = _get_client().get("https://support.claude.com/en/articles/12138966-release-notes")
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.get_text()
        for m in re.finditer(r'(?:Claude\s+)?(Opus|Sonnet|Haiku)\s+(\d+\.\d+(?:\.\d+)?)', text):
            model = m.group(1)
            ver = m.group(2)
            v = f"{model} {ver}"
            if _sane(v):
                return v
    except Exception:
        logger.warning("fetch_claude failed", exc_info=True)

    # Fallback: Chinese tech media
    try:
        resp = _get_client().get("https://www.jiqizhixin.com/search?q=Claude")
        resp.raise_for_status()
        for m in re.finditer(r'Claude\s+(?:Opus|Sonnet|Haiku)?\s*(\d+\.\d+(?:\.\d+)?)', resp.text, re.IGNORECASE):
            v = f"Sonnet {m.group(1)}"
            if _sane(v):
                return v
    except Exception:
        pass
    return None


def fetch_wenxin():
    """Static — 文心一言 version floats on homepage occasionally."""
    return None


def fetch_qwen():
    """Static — 通义千问 version not easily fetchable."""
    return None


def fetch_gemini():
    """Scrape Google AI changelog for latest Gemini model."""
    sources = [
        "https://ai.google.dev/gemini-api/docs/changelog",
        "https://developers.googleblog.com/en/search/?q=gemini",
    ]
    for url in sources:
        try:
            resp = _get_client().get(url)
            resp.raise_for_status()
            for m in re.finditer(r'Gemini[\t ]+(\d+\.\d+)[\t ]*(?:Pro|Nano|Flash|Ultra)?', resp.text, re.IGNORECASE):
                v = f"Gemini {m.group(1)}"
                if _sane(v):
                    return v
            for m in re.finditer(r'Gemini\s+(\d+(?:\.\d+)?)', resp.text, re.IGNORECASE):
                v = f"Gemini {m.group(1)}"
                if _sane(v):
                    return v
        except Exception:
            continue
    return None


def fetch_deepseek():
    """Scrape DeepSeek API docs for latest model name."""
    try:
        resp = _get_client().get("https://api-docs.deepseek.com")
        resp.raise_for_status()
        for m in re.finditer(r'deepseek[-\s]*(v\d+(?:\.\d+)?)', resp.text, re.IGNORECASE):
            v = f"DeepSeek-{m.group(1)}"
            if _sane(v):
                return v
        for m in re.finditer(r'(DeepSeek[-\s]*[A-Za-z0-9]+)', resp.text):
            v = m.group(1)
            if _sane(v) and len(v) < 30:
                return v
    except Exception:
        logger.warning("fetch_deepseek failed", exc_info=True)
    return None


def fetch_grok():
    """Scrape xAI site for latest Grok model."""
    try:
        resp = _get_client().get("https://x.ai/blog")
        resp.raise_for_status()
        for m in re.finditer(r'Grok[-\s]*(\d+(?:\.\d+)?)', resp.text, re.IGNORECASE):
            v = f"Grok {m.group(1)}"
            if _sane(v):
                return v
    except Exception:
        logger.warning("fetch_grok failed", exc_info=True)
    return None


# ─── AI 绘画 ───────────────────────────────────────────────────


def fetch_midjourney():
    """Scrape Midjourney main site or docs for latest version."""
    sources = [
        "https://www.midjourney.com",
        "https://docs.midjourney.com",
    ]
    for url in sources:
        try:
            resp = _get_client().get(url)
            resp.raise_for_status()
            for m in re.finditer(r'(?:Midjourney\s+)?V(\d+(?:\.\d+)?)', resp.text, re.IGNORECASE):
                v = f"V{m.group(1)}"
                if _sane(v):
                    return v
        except Exception:
            continue
    return None


def fetch_dalle():
    """DALL-E version from OpenAI docs."""
    sources = [
        "https://platform.openai.com/docs/models",
    ]
    for url in sources:
        try:
            resp = _get_client().get(url)
            resp.raise_for_status()
            matches = re.findall(r'(dall-e-\d+(?:\.\d+)?)', resp.text, re.IGNORECASE)
            if matches:
                latest = sorted(set(matches))[-1]
                parts = latest.replace("dall-e-", "DALL-E ").split("-")
                v = parts[0]
                if _sane(v):
                    return v
        except Exception:
            continue
    return None


def fetch_stable_diffusion():
    """Scrape Stability AI news for latest SD version."""
    try:
        resp = _get_client().get("https://stability.ai/news")
        resp.raise_for_status()
        for m in re.finditer(r'Stable\s+Diffusion[^a-zA-Z]*(\d+\.\d+(?:[a-zA-Z]+)?)', resp.text, re.IGNORECASE):
            v = f"SD {m.group(1)}"
            if _sane(v):
                return v
        for m in re.finditer(r'SD\s+(\d+\.\d+(?:[a-zA-Z]+)?)', resp.text, re.IGNORECASE):
            v = f"SD {m.group(1)}"
            if _sane(v):
                return v
    except Exception:
        logger.warning("fetch_stable_diffusion failed", exc_info=True)
    return None


def fetch_leonardo():
    """Static — Leonardo.ai Phoenix / model versions not publicly scrapeable."""
    return None


# ─── AI 视频 ───────────────────────────────────────────────────


def fetch_runway():
    """Scrape Runway news for latest Gen version."""
    try:
        resp = _get_client().get("https://runwayml.com/news")
        resp.raise_for_status()
        for m in re.finditer(r'Gen[-\s]?(\d+\.\d+(?:\.\d+)?)', resp.text, re.IGNORECASE):
            v = f"Gen-{m.group(1)}"
            if _sane(v):
                return v
    except Exception:
        logger.warning("fetch_runway failed", exc_info=True)
    return None


def fetch_pika():
    """Scrape Pika main site for version."""
    try:
        resp = _get_client().get("https://pika.art")
        resp.raise_for_status()
        for m in re.finditer(r'(?:v|version)?\s*(\d+\.\d+(?:\.\d+)?)', resp.text, re.IGNORECASE):
            ver = m.group(1)
            if re.match(r'^\d+\.\d+$', ver) and float(ver) < 100:
                v = f"v{ver}"
                if _sane(v):
                    return v
    except Exception:
        logger.warning("fetch_pika failed", exc_info=True)
    return None


def fetch_sora():
    """Sora is discontinued."""
    return None


def fetch_capcut():
    """Static — CapCut version not easily fetched."""
    return None


# ─── 代码助手 ─────────────────────────────────────────────────


def fetch_github_copilot():
    """Scrape GitHub blog for latest Copilot model mention."""
    try:
        resp = _get_client().get("https://github.blog/changelog/")
        resp.raise_for_status()
        # Look for GPT-5.x-Codex patterns first (latest)
        for m in re.finditer(r'GPT-(\d+\.\d+(?:-Codex)?)', resp.text):
            v = f"GPT-{m.group(1)}"
            if _sane(v):
                return v
        for m in re.finditer(r'Copilot[^.]*?(GPT-\d+\.\d+(?:-[a-zA-Z0-9]+)?)', resp.text, re.IGNORECASE):
            v = m.group(1)
            if _sane(v):
                return v
    except Exception:
        logger.warning("fetch_github_copilot failed", exc_info=True)
    return None


def fetch_cursor():
    """Scrape Cursor download page for version."""
    try:
        resp = _get_client().get("https://www.cursor.com")
        resp.raise_for_status()
        for m in re.finditer(r'(?:v|version)?\s*(\d+\.\d+\.\d+)', resp.text, re.IGNORECASE):
            ver = m.group(1)
            if re.match(r'^\d+\.\d+\.\d+$', ver):
                parts = [int(x) for x in ver.split('.')]
                if parts[0] < 10:
                    if _sane(ver):
                        return ver
    except Exception:
        logger.warning("fetch_cursor failed", exc_info=True)
    return None


def fetch_tabnine():
    """Static — Tabnine SaaS, version not meaningful."""
    return None


def fetch_codeium():
    """Static — Codeium SaaS."""
    return None


# ─── AI 音频 ───────────────────────────────────────────────────


def fetch_suno():
    """Scrape Suno blog for latest version."""
    try:
        resp = _get_client().get("https://suno.com/blog")
        resp.raise_for_status()
        for m in re.finditer(r'v(\d+\.\d+(?:\.\d+)?)', resp.text, re.IGNORECASE):
            v = f"v{m.group(1)}"
            if _sane(v) and float(m.group(1)) >= 3:
                return v
    except Exception:
        logger.warning("fetch_suno failed", exc_info=True)
    return None


def fetch_elevenlabs():
    """Scrape ElevenLabs blog or main site for Flash version."""
    sources = [
        "https://elevenlabs.io",
        "https://elevenlabs.io/docs/changelog",
    ]
    for url in sources:
        try:
            resp = _get_client().get(url)
            resp.raise_for_status()
            for m in re.finditer(r'Flash\s*[Vv]?\s*(\d+\.\d+(?:\.\d+)?)', resp.text):
                v = f"Flash v{m.group(1)}"
                if _sane(v):
                    return v
        except Exception:
            continue
    return None


def fetch_mubert():
    """Static — Mubert SaaS."""
    return None


def fetch_adobe_podcast():
    """Static — Adobe Podcast SaaS."""
    return None


# ─── 其他 ──────────────────────────────────────────────────────


def fetch_notion_ai():
    """Static — Notion AI SaaS, model version not public."""
    return None


def fetch_perplexity():
    """Scrape Perplexity docs for latest model info."""
    try:
        resp = _get_client().get("https://docs.perplexity.ai/docs/overview")
        resp.raise_for_status()
        for m in re.finditer(r'(sonar-[a-z]+(?:-\d+(?:\.\d+)?)?)', resp.text, re.IGNORECASE):
            v = m.group(1)
            if _sane(v):
                return v
    except Exception:
        pass
    return None


def fetch_gamma():
    """Static — Gamma SaaS."""
    return None


def fetch_canva_ai():
    """Static — Canva AI SaaS."""
    return None


# ─── New auto-fetchers ────────────────────────────────────────


def fetch_adobe_firefly():
    """Scrape Adobe Firefly page for latest version."""
    try:
        resp = _get_client().get("https://firefly.adobe.com")
        resp.raise_for_status()
        for m in re.finditer(r'Firefly[^a-z]*(\d+(?:\.\d+)?)', resp.text, re.IGNORECASE):
            v = f"Firefly {m.group(1)}"
            if _sane(v):
                return v
    except Exception:
        pass
    return None


def fetch_windsurf():
    """Scrape Windsurf site for version."""
    try:
        resp = _get_client().get("https://codeium.com/windsurf")
        resp.raise_for_status()
        for m in re.finditer(r'(?:v|version)?\s*(\d+\.\d+\.\d+)', resp.text, re.IGNORECASE):
            if re.match(r'^\d+\.\d+\.\d+$', m.group(1)):
                parts = [int(x) for x in m.group(1).split('.')]
                if parts[0] < 10:
                    return m.group(1)
    except Exception:
        pass
    return None


def fetch_cline():
    """Scrape Cline GitHub releases for latest version."""
    try:
        resp = _get_client().get("https://github.com/cline/cline/releases")
        resp.raise_for_status()
        for m in re.finditer(r'releases/tag/v?(\d+\.\d+\.\d+)', resp.text):
            if _sane(m.group(1)):
                return m.group(1)
    except Exception:
        pass
    return None


def fetch_udio():
    """Scrape Udio blog for latest version mention."""
    try:
        resp = _get_client().get("https://www.udio.com/blog")
        resp.raise_for_status()
        for m in re.finditer(r'v(\d+(?:\.\d+)+)', resp.text, re.IGNORECASE):
            if _sane(m.group(0)):
                return m.group(0)
    except Exception:
        pass
    return None


# ─── Generic fallback fetcher ──────────────────────────────────

_GENERIC_PATTERNS = [
    re.compile(r'(?:v|version)[\s.:-]*(\d+\.\d+(?:\.\d+)?)', re.IGNORECASE),
    re.compile(r'(\d+\.\d+\.\d+)'),
    re.compile(r'(\d+\.\d+)(?:[^.\d]|$)'),
]


def fetch_generic(url):
    """Fetch a URL and look for common version patterns in visible text."""
    if not url:
        return None
    try:
        resp = _get_client().get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup(['script', 'style', 'svg', 'noscript', 'iframe']):
            tag.decompose()
        text = soup.get_text(separator=' ')

        candidates = []
        for pattern in _GENERIC_PATTERNS:
            for m in pattern.finditer(text):
                ver = m.group(1)
                if _sane(ver) and re.match(r'^\d+\.\d+', ver):
                    parts = ver.split('.')
                    major = int(parts[0])
                    if 1 <= major <= 20:
                        candidates.append(ver)

        if candidates:
            from collections import Counter
            counter = Counter(candidates)
            best = counter.most_common(1)[0][0]
            logger.info(f"Generic fetch from {url}: {best}")
            return best
    except Exception:
        logger.debug(f"Generic fetch failed for {url}", exc_info=True)
    return None


# ─── Registry ──────────────────────────────────────────────────

FETCHERS = {
    # LLM / 对话
    "ChatGPT": fetch_chatgpt,
    "Claude": fetch_claude,
    "DeepSeek": fetch_deepseek,
    "Grok": fetch_grok,
    "Gemini": fetch_gemini,
    "文心一言": fetch_wenxin,
    "通义千问": fetch_qwen,
    # AI 绘画
    "Midjourney": fetch_midjourney,
    "DALL-E 3": fetch_dalle,
    "Stable Diffusion": fetch_stable_diffusion,
    "Adobe Firefly": fetch_adobe_firefly,
    "Leonardo.ai": fetch_leonardo,
    # AI 视频
    "Runway": fetch_runway,
    "Pika": fetch_pika,
    "Sora": fetch_sora,
    "CapCut": fetch_capcut,
    # 代码助手
    "GitHub Copilot": fetch_github_copilot,
    "Cursor": fetch_cursor,
    "Windsurf": fetch_windsurf,
    "Cline": fetch_cline,
    "Tabnine": fetch_tabnine,
    "Codeium": fetch_codeium,
    # AI 音频
    "Suno": fetch_suno,
    "ElevenLabs": fetch_elevenlabs,
    "Udio": fetch_udio,
    "Mubert": fetch_mubert,
    "Adobe Podcast": fetch_adobe_podcast,
    # 其他
    "Notion AI": fetch_notion_ai,
    "Perplexity": fetch_perplexity,
    "Gamma": fetch_gamma,
    "Canva AI": fetch_canva_ai,
}


def fetch_version(tool_name):
    """Try to fetch version for a tool by name."""
    if _PROXY_DISABLED:
        logger.info(f"version_fetcher disabled via VERSION_FETCHER_DISABLE, skipping {tool_name}")
        return None
    fetcher = FETCHERS.get(tool_name)
    if fetcher:
        try:
            result = fetcher()
            if result:
                logger.info(f"Fetched version for {tool_name}: {result}")
            return result
        except Exception as e:
            logger.warning(f"Failed to fetch version for {tool_name}: {e}")
            return None
    return None


def get_initial_version(tool_name):
    """Seed version data — act as fallback if auto-fetch returns None."""
    versions = {
        # LLM / 对话（15）
        "ChatGPT": "GPT-5.x",
        "Claude": "Opus 4.8",
        "Gemini": "Gemini 3.1 Pro",
        "DeepSeek": "DeepSeek-V4",
        "Kimi": "Kimi K2",
        "豆包": "豆包 3.0",
        "智谱清言": "GLM-5",
        "Grok": "Grok 4",
        "Mistral AI": "Mistral Large 3",
        "讯飞星火": "星火 5.0",
        "百川智能": "Baichuan 4",
        "腾讯元宝": "元宝 2.0",
        "零一万物": "Yi-Lightning",
        "文心一言": "文心 5.1",
        "通义千问": "Qwen3.7-Max",
        # AI 绘画（12）
        "Midjourney": "V8.1",
        "DALL-E 3": "DALL-E 4",
        "Stable Diffusion": "SD4 Ultra",
        "Adobe Firefly": "Firefly 4",
        "Flux": "Flux.1 Pro",
        "ComfyUI": "Latest",
        "Ideogram": "Ideogram 4.0",
        "Recraft": "Recraft V3",
        "Fooocus": "2.5",
        "Leonardo.ai": "Phoenix 1.0",
        "Clipdrop": "Latest",
        "Krea AI": "Krea 2.0",
        # AI 视频（11）
        "Runway": "Gen-4.5",
        "可灵 (Kling)": "可灵 2.0",
        "Vidu": "Vidu 2.0",
        "Luma Dream Machine": "Dream Machine 1.6",
        "Pika": "3.0",
        "Sora": "已关停",
        "CapCut": "Latest",
        "HeyGen": "HeyGen 3.0",
        "Synthesia": "Synthesia 3.0",
        "Viggle": "Viggle 2.0",
        "Haiper": "Haiper 2.0",
        # 代码助手（11）
        "GitHub Copilot": "GPT-5.3-Codex",
        "Cursor": "3.3.27",
        "Windsurf": "Windsurf 3.0",
        "Continue": "Continue 3.0",
        "Amazon Q": "Q Developer 3.0",
        "Replit Agent": "Replit Agent 2.0",
        "Cody": "Cody 5.0",
        "Cline": "3.2.14",
        "Devin AI": "Devin 2.0",
        "Tabnine": "Latest",
        "Codeium": "Latest",
        # AI 音频（10）
        "Suno": "v5.5",
        "ElevenLabs": "Flash v2.5",
        "Udio": "v1.5",
        "Fish Audio": "Fish Speech 2.0",
        "讯飞配音": "Latest",
        "Play.ht": "Latest",
        "Voicemod": "Voicemod 3.0",
        "Mubert": "Latest",
        "Adobe Podcast": "Latest",
        "Resemble AI": "Resemble 2.0",
        # 其他（10）
        "Perplexity": "Perplexity 3.0",
        "Grammarly AI": "Grammarly 3.0",
        "Notion AI": "Latest",
        "Canva AI": "Latest",
        "Gamma": "Latest",
        "Otter.ai": "Otter 4.0",
        "Beautiful.ai": "Latest",
        "Consensus": "Consensus 2.0",
        "Krisp AI": "Krisp 3.0",
        "Elicit": "Elicit 3.0",
    }
    return versions.get(tool_name)


def get_version_source(tool_name):
    """Classify each tool's version source type."""
    auto = {
        "ChatGPT", "Claude", "Gemini", "DeepSeek", "Grok",
        "Midjourney", "DALL-E 3", "Stable Diffusion", "Adobe Firefly",
        "Runway", "Pika", "Luma Dream Machine",
        "GitHub Copilot", "Cursor", "Windsurf", "Cline",
        "Suno", "ElevenLabs", "Udio", "Perplexity",
    }
    saas = {
        "CapCut", "Tabnine", "Codeium", "Mubert",
        "Adobe Podcast", "Notion AI", "Gamma", "Canva AI",
        "ComfyUI", "Clipdrop", "Play.ht",
    }
    chinese = {
        "文心一言", "通义千问", "Kimi", "豆包", "智谱清言",
        "讯飞星火", "百川智能", "腾讯元宝", "零一万物",
        "可灵 (Kling)", "Vidu", "Viggle", "Haiper",
        "讯飞配音", "Fish Audio",
    }
    discontinued = {"Sora"}
    if tool_name in auto:
        return "auto"
    if tool_name in saas:
        return "saas"
    if tool_name in chinese:
        return "manual"
    if tool_name in discontinued:
        return "discontinued"
    return "manual"
