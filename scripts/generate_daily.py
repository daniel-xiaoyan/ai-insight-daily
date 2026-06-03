#!/usr/bin/env python3
"""
AI洞察 · 每日自动生成日报脚本（RSS版）
由 熏儿 自动维护，每天北京时间 10:00 运行
无需 API Key，直接抓取 RSS 新闻源
"""

import os, sys, re, json, datetime
import urllib.request, urllib.error
from pathlib import Path
from xml.etree import ElementTree as ET

# ─── 配置 ──────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
REPORTS_DIR = REPO_ROOT / "01-daily-reports"
INDEX_PATH = REPO_ROOT / "index.html"
WEEKDAYS = ["周一","周二","周三","周四","周五","周六","周日"]

# ─── RSS 新闻源 ─────────────────────────────────────────
RSS_SOURCES = [
    # 海外
    {"url": "https://techcrunch.com/feed/", "name": "TechCrunch", "region": "海外", "tags": ["AI","OpenAI","Anthropic","Claude","GPT","LLM","Gemini"]},
    {"url": "https://www.theverge.com/rss/index.xml", "name": "The Verge", "region": "海外", "tags": ["AI","OpenAI","Google","Microsoft","Meta"]},
    {"url": "https://feeds.feedburner.com/venturebeat/SZYF", "name": "VentureBeat", "region": "海外", "tags": ["AI","machine learning","LLM","agent","model"]},
    {"url": "https://www.wired.com/feed/rss", "name": "WIRED", "region": "海外", "tags": ["AI","artificial intelligence","OpenAI","tech"]},
    # 国内
    {"url": "https://www.36kr.com/feed", "name": "36Kr", "region": "国内", "tags": ["AI","大模型","人工智能","ChatGPT","文心","通义","Kimi"]},
    {"url": "https://www.qbitai.com/feed", "name": "量子位", "region": "国内", "tags": ["AI","大模型","人工智能","LLM"]},
    {"url": "https://syncedreview.com/feed/", "name": "机器之心", "region": "国内", "tags": ["AI","深度学习","大模型","人工智能"]},
]

# 话题关键词分类
TOPIC_KEYWORDS = {
    "llm":        ["GPT","ChatGPT","Claude","Gemini","大模型","LLM","Llama","Mistral","通义","文心","Kimi","DeepSeek","qwen"],
    "coding":     ["Cursor","Copilot","Devin","Trae","coding","code","编程","代码","IDE","replit","agent"],
    "app":        ["Midjourney","Sora","Runway","DALL","stable diffusion","AI应用","视频生成","图像","绘画","音乐生成"],
    "industry":   ["融资","估值","裁员","监管","法规","投资","收购","OpenAI","Anthropic","Google","Microsoft","Meta","百度","阿里","腾讯"],
    "enterprise": ["企业","B2B","SaaS","落地","转型","生产力","ROI","成本","效率"],
}

# ─── 深度调研知识库（用于延伸阅读匹配） ─────────────────────
# 每条调研报告关联的关键词，新闻命中任一关键词即可推荐
RESEARCH_LIBRARY = [
    {"title": "2026年AI编程工具全景报告", "href": "../../02-deep-research/topics/ai-coding-tools-2026.html",
     "desc": "Cursor·Trae·Copilot·CodeFlicker 12款工具8维度横评", "icon": "⌨️",
     "keywords": ["Cursor","Trae","Copilot","Devin","CodeFlicker","Claude Code","coding","code","编程","代码","IDE","vibe","AI Studio"]},
    {"title": "Anthropic深度调研：从安全信仰到企业Agent帝国", "href": "../../02-deep-research/companies/anthropic-deep-dive.html",
     "desc": "马斯克败诉、收购Stainless、Claude企业战略全解析", "icon": "🏢",
     "keywords": ["Anthropic","Claude","Stainless","Karpathy","马斯克","Musk","claude"]},
    {"title": "字节跳动AI版图深度调研", "href": "../../02-deep-research/companies/bytedance-ai-landscape.html",
     "desc": "豆包·Trae·可灵·即梦·番茄小说全解析", "icon": "🇨🇳",
     "keywords": ["字节","ByteDance","豆包","Trae","可灵","Kling","即梦","番茄","Doubao","抖音"]},
    {"title": "OpenAI · $8400亿估值背后的战略全景", "href": "../../02-deep-research/companies/openai-gpt5-complete.html",
     "desc": "OpenAI产品矩阵、商业模式、竞争格局深度分析", "icon": "🤖",
     "keywords": ["OpenAI","GPT","ChatGPT","GPT-5","Sam Altman","Altman","Sora","openai"]},
    {"title": "AI Agent 自动化落地的现状与趋势", "href": "../../02-deep-research/topics/ai-agent-automation-2026.html",
     "desc": "企业AI Agent落地现状、技术架构、行业案例与ROI", "icon": "🤖",
     "keywords": ["Agent","agent","自动化","RPA","工作流","workflow","Devin"]},
    {"title": "MCP协议全解：AI工具生态的新标准", "href": "../../02-deep-research/topics/mcp-protocol-complete.html",
     "desc": "Model Context Protocol架构设计与生态现状", "icon": "🔌",
     "keywords": ["MCP","Model Context Protocol","tool calling","工具调用","function calling"]},
    {"title": "AI Coding工具演进全景：从补全到自主编程", "href": "../../02-deep-research/topics/ai-coding-evolution-complete.html",
     "desc": "AI编程工具5年演进史与未来方向", "icon": "📈",
     "keywords": ["Copilot","Cursor","Tabnine","补全","autocomplete","coding"]},
    {"title": "软件工程3.0：AI时代的开发范式革命", "href": "../../02-deep-research/trends/software3-complete.html",
     "desc": "从Karpathy的LLM OS到AI Native应用架构", "icon": "🚀",
     "keywords": ["LLM OS","Karpathy","软件3.0","Software 3.0","AI Native","范式"]},
    {"title": "从AI大神的深度分享看2026年AI的下半场", "href": "../../02-deep-research/trends/2026-ai-trends-complete.html",
     "desc": "10位AI思想领袖核心观点，三大趋势梳理", "icon": "🌍",
     "keywords": ["趋势","具身","embodied","AGI","推理","reasoning"]},
    {"title": "AI范式转变：从工具到可编程认知的跨越", "href": "../../02-deep-research/trends/ai-paradigm-shift-complete.html",
     "desc": "AI从独立目的地进化为隐形基础设施", "icon": "💡",
     "keywords": ["范式","paradigm","基础设施","infrastructure"]},
    {"title": "AI Agent平台对比：Coze vs Dify vs FastGPT", "href": "../../02-deep-research/topics/coze-vs-dify-complete.html",
     "desc": "三大国内主流Agent开发平台横向对比", "icon": "⚡",
     "keywords": ["Coze","Dify","FastGPT","扣子","n8n","Flowise","低代码","no-code"]},
    {"title": "飞书 vs 钉钉 · 企业AI协作平台深度对比", "href": "../../02-deep-research/topics/feishu-vs-dingtalk-complete.html",
     "desc": "两大国内企业协作平台AI能力对比", "icon": "📊",
     "keywords": ["飞书","Lark","钉钉","DingTalk","企业协作","SaaS"]},
]

def find_related_research(news, max_count=3):
    """根据当日新闻标题/描述，匹配最相关的调研报告"""
    # 收集所有新闻文本
    all_text = []
    for region in news.values():
        for items in region.values():
            for item in items:
                all_text.append((item.get("title","") + " " + item.get("desc","")).lower())
    if not all_text:
        return []
    combined = " ".join(all_text)

    # 计算每篇调研的命中分数
    scored = []
    for research in RESEARCH_LIBRARY:
        score = sum(1 for kw in research["keywords"] if kw.lower() in combined)
        if score > 0:
            scored.append((score, research))
    # 按分数倒序，取前 N 篇
    scored.sort(key=lambda x: -x[0])
    result = [r for _, r in scored[:max_count]]
    # 兜底：如果命中不足，补充 Agent 自动化 + AI Coding 工具
    if len(result) < 2:
        defaults = [r for r in RESEARCH_LIBRARY if r["title"].startswith("AI Agent 自动化") or r["title"].startswith("2026年AI编程")]
        for d in defaults:
            if d not in result and len(result) < max_count:
                result.append(d)
    return result

# ─── 工具函数 ──────────────────────────────────────────
def today_cn():
    utc = datetime.datetime.utcnow()
    return utc + datetime.timedelta(hours=8)

def format_date(dt): return dt.strftime("%Y-%m-%d")

def format_date_cn(dt):
    return f"{dt.year}年{dt.month}月{dt.day}日 · {WEEKDAYS[dt.weekday()]}"

def get_report_path(dt):
    d = REPORTS_DIR / dt.strftime("%Y-%m")
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{format_date(dt)}.html"

# ─── 抓取 RSS ──────────────────────────────────────────
def fetch_rss(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 AI-Insight-Bot/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception as e:
        print(f"  ⚠️  抓取失败 {url}: {e}")
        return None

def parse_rss(xml_bytes):
    items = []
    try:
        root = ET.fromstring(xml_bytes)
        ns = ""
        # RSS 2.0
        for item in root.iter("item"):
            title = item.findtext("title", "").strip()
            desc  = item.findtext("description", "").strip()
            link  = item.findtext("link", "").strip()
            pub   = item.findtext("pubDate", "").strip()
            if title:
                items.append({"title": title, "desc": desc[:200], "link": link, "pub": pub})
        # Atom
        if not items:
            ns = "{http://www.w3.org/2005/Atom}"
            for entry in root.iter(f"{ns}entry"):
                title = entry.findtext(f"{ns}title", "").strip()
                summary = entry.findtext(f"{ns}summary", "").strip()
                link_el = entry.find(f"{ns}link")
                link = link_el.get("href","") if link_el is not None else ""
                published = entry.findtext(f"{ns}published", "").strip()
                updated = entry.findtext(f"{ns}updated", "").strip()
                pub = published or updated or ""
                items.append({"title": title, "desc": summary[:200], "link": link, "pub": pub})
    except Exception as e:
        print(f"  ⚠️  解析RSS失败: {e}")
    return items

def parse_pub_date(pub_str):
    """解析各种格式的发布日期，返回datetime对象"""
    if not pub_str:
        return None
    # 尝试多种常见日期格式
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",   # RFC 822: "Wed, 14 May 2026 08:00:00 +0000"
        "%a, %d %b %Y %H:%M:%S",       # RFC 822 无时区
        "%Y-%m-%dT%H:%M:%S%z",         # ISO 8601: "2026-05-14T08:00:00+00:00"
        "%Y-%m-%dT%H:%M:%SZ",          # ISO 8601 UTC
        "%Y-%m-%dT%H:%M:%S",           # ISO 8601 无时区
        "%Y-%m-%d %H:%M:%S",           # 简单格式
        "%Y-%m-%d",                    # 仅日期
    ]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(pub_str.strip(), fmt)
        except ValueError:
            continue
    return None

def is_ai_related(title, tags):
    t = title.lower()
    return any(kw.lower() in t for kw in tags)

def classify_topic(title):
    t = title.lower()
    for cat, kws in TOPIC_KEYWORDS.items():
        if any(k.lower() in t for k in kws):
            return cat
    return "industry"

def clean_html(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()[:150]

# ─── 熏儿评语规则库 ─────────────────────────────────────────
COMMENT_RULES = [
    # 融资/投资类
    (["融资","估值","领投","Pre-IPO","D轮","C轮","B轮","战略投资","IPO"],
     "💰 资本持续涌入，头部效应加剧。融资不等于成功，商业化落地才是真考验。"),
    (["分拆","独立","上市","港股","A股","纳斯达克"],
     "📈 大厂AI业务分拆潮来临——AI资产在母公司报表里会被低估，独立才能获得正确定价。"),
    # 大模型发布类
    (["GPT-5","GPT5","o3","o4","Gemini","Claude","Llama","发布","新版","升级","更新"],
     "🧠 模型能力持续迭代，但关键问题是：这次升级能解决哪个真实业务痛点？"),
    (["开源","open source","开放权重"],
     "🌐 开源加速AI生态建设，但开源≠免费——算力、部署、维护都需要成本。"),
    # AI Coding类
    (["Cursor","Copilot","Devin","Trae","IDE","代码","coding","code","编程","agent","Agent"],
     "⌨️ AI Coding工具军备竞赛持续升温，开发者效率正在被重新定义。"),
    # Agent/自动化类
    (["Agent","agent","自动化","automation","MCP","workflow","工作流"],
     "🤖 Agent时代正在到来，但复杂任务的可靠性仍是核心挑战，落地比想象中难。"),
    # 监管/政策类
    (["监管","法规","政策","regulation","ban","禁止","安全","safety","对齐","alignment"],
     "⚖️ AI监管从边缘走向主流，合规能力将成为企业AI产品的核心竞争力之一。"),
    # 硬件/芯片类
    (["NVIDIA","英伟达","GPU","芯片","算力","H100","B200","B300","Blackwell"],
     "🖥️ 算力是AI时代的石油，英伟达的护城河比想象中更深——软件生态才是真壁垒。"),
    # 搜索/应用类
    (["搜索","search","Perplexity","问答","知识"],
     "🔍 AI搜索正在重构信息获取方式，但准确性和实时性仍是最大挑战。"),
    # 裁员/收缩类
    (["裁员","layoff","降本","成本","亏损","烧钱"],
     "📉 AI行业进入理性调整期，烧钱换增长的时代结束，ROI成为关键词。"),
    # 视频/多模态类
    (["视频","Sora","可灵","Runway","Veo","Pika","多模态","图像","生图"],
     "🎬 视频生成AI爆发，但训练成本极高。谁能控制成本同时保持质量，谁才能活到最后。"),
    # 企业/B2B类
    (["企业","B2B","SaaS","转型","落地","ROI","效率","生产力"],
     "🏢 企业AI进入深水区，从试点到规模化落地，关键是找到可量化的ROI。"),
]

COMMENT_DEFAULT = "📌 AI行业动态持续演进，关键是从噪音中识别真正的结构性变化。"

def generate_comment(title):
    """根据标题关键词生成熏儿评语"""
    title_lower = title.lower()
    for keywords, comment in COMMENT_RULES:
        if any(kw.lower() in title_lower for kw in keywords):
            return comment
    return COMMENT_DEFAULT

# ─── 去重：获取昨日已出现的链接 ──────────────────────────────
def get_yesterday_urls(date_str):
    """读取昨日日报中的所有链接，用于去重标注"""
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        yesterday = dt - datetime.timedelta(days=1)
        yesterday_str = format_date(yesterday)
        ym = yesterday.strftime("%Y-%m")
        yesterday_path = REPORTS_DIR / ym / f"{yesterday_str}.html"
        if not yesterday_path.exists():
            return set()
        content = yesterday_path.read_text(encoding="utf-8")
        # 提取所有 href 链接
        urls = set(re.findall(r'href="(https?://[^"]+)"', content))
        return urls
    except Exception:
        return set()

# ─── 收集新闻 ──────────────────────────────────────────
def collect_news(date_str):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    # 只保留最近3天的新闻（防止旧新闻混入）
    cutoff_date = dt - datetime.timedelta(days=3)
    all_news = {"海外": {}, "国内": {}}
    
    # 获取昨日已有链接，用于标注"今日首发"
    yesterday_urls = get_yesterday_urls(date_str)
    
    for src in RSS_SOURCES:
        print(f"  📡 抓取 {src['name']}...")
        xml = fetch_rss(src["url"])
        if not xml:
            continue
        items = parse_rss(xml)
        region = src["region"]
        count = 0
        filtered = 0
        for item in items[:50]:  # 扫描更多条目，但严格过滤日期
            if not is_ai_related(item["title"], src["tags"]):
                continue
            # 日期过滤：只保留最近3天的新闻
            pub_dt = parse_pub_date(item["pub"])
            if pub_dt is not None:
                # 去掉时区信息方便比较
                pub_dt_naive = pub_dt.replace(tzinfo=None) if pub_dt.tzinfo else pub_dt
                if pub_dt_naive < cutoff_date:
                    filtered += 1
                    continue
            cat = classify_topic(item["title"])
            if cat not in all_news[region]:
                all_news[region][cat] = []
            if len(all_news[region][cat]) < 5:  # 每个类别多留一些，保证内容丰富
                # 标记是否为今日首发（昨日未出现过的链接）
                is_new_today = item["link"] not in yesterday_urls if item.get("link") else True
                all_news[region][cat].append({
                    "title": item["title"],
                    "source": src["name"],
                    "link": item["link"],
                    "desc": clean_html(item["desc"]),
                    "pub": item["pub"],
                    "is_new_today": is_new_today,
                    "comment": generate_comment(item["title"]),
                })
                count += 1
        print(f"     → 筛选到 {count} 条AI相关，过滤 {filtered} 条旧新闻")
    return all_news

# ─── 热度计算 ──────────────────────────────────────────
HOT_TOPICS_TEMPLATE = [
    {"topic": "大模型能力竞争", "heat": 16, "days": 3, "trend": "🔥 热门", "signal": "头部模型持续迭代"},
    {"topic": "AI Coding工具大战", "heat": 14, "days": 5, "trend": "📈 上升", "signal": "开发者采用率飙升"},
    {"topic": "AI Agent自动化", "heat": 12, "days": 4, "trend": "📈 上升", "signal": "企业落地加速"},
    {"topic": "AI监管政策", "heat": 9,  "days": 7, "trend": "⚠️ 关注", "signal": "多国立法进程加快"},
    {"topic": "AI芯片算力竞争", "heat": 8, "days": 6, "trend": "🔥 热门", "signal": "英伟达持续领跑"},
]

def build_hot_rows(news):
    # 根据抓到的新闻动态调整热度话题
    topics = list(HOT_TOPICS_TEMPLATE)
    # 如果抓到了 LLM 相关新闻，更新第一条话题
    llm_items = news.get("海外", {}).get("llm", []) + news.get("国内", {}).get("llm", [])
    if llm_items:
        topics[0]["topic"] = llm_items[0]["title"][:20] + "..." if len(llm_items[0]["title"]) > 20 else llm_items[0]["title"]
    coding_items = news.get("海外", {}).get("coding", []) + news.get("国内", {}).get("coding", [])
    if coding_items:
        topics[1]["topic"] = coding_items[0]["title"][:20] + "..." if len(coding_items[0]["title"]) > 20 else coding_items[0]["title"]
    return topics

# ─── 今日快读 Ticker 提取 ──────────────────────────────────
TICKER_TAG_MAP = {
    "llm":        ("tick-green",  "模型"),
    "coding":     ("tick-purple", "工具"),
    "app":        ("tick-blue",   "应用"),
    "industry":   ("tick-red",    "行业"),
    "enterprise": ("tick-orange", "企业"),
}

def shorten_title(title, max_len=28):
    """提取标题前N字作为快读条目"""
    t = re.sub(r"\s+", " ", title or "").strip()
    if len(t) > max_len:
        t = t[:max_len].rstrip() + "…"
    return t

def extract_ticker_items(news, max_count=8):
    """从各板块挑选最具代表性的 N 条新闻作为今日快读（round-robin确保分类分散）"""
    picked = []
    seen_titles = set()
    # 按板块准备候选队列
    queues = {}
    priority = ["llm","industry","coding","app","enterprise"]
    for cat in priority:
        merged = []
        for region in ["海外","国内"]:
            merged.extend(news.get(region, {}).get(cat, [])[:3])
        queues[cat] = merged

    # round-robin: 每轮各板块取一条，确保分类分散
    while len(picked) < max_count:
        added_this_round = False
        for cat in priority:
            if not queues[cat]:
                continue
            item = queues[cat].pop(0)
            title = item.get("title","").strip()
            if not title or title in seen_titles:
                continue
            seen_titles.add(title)
            tag_class, tag_label = TICKER_TAG_MAP.get(cat, ("tick-green","动态"))
            picked.append({"tag_class": tag_class, "tag_label": tag_label, "text": shorten_title(title)})
            added_this_round = True
            if len(picked) >= max_count:
                break
        if not added_this_round:
            break
    return picked

def build_ticker_html(news):
    """构建今日快读滚动条 HTML（用于 index.html 替换）"""
    items = extract_ticker_items(news)
    if not items:
        return None
    parts = []
    for i, it in enumerate(items):
        parts.append(f'        <span class="tick-item"><span class="tick-tag {it["tag_class"]}">{it["tag_label"]}</span>{it["text"]}&nbsp;</span>')
        if i < len(items) - 1:
            parts.append('        <span class="tick-item tick-sep">·&nbsp;</span>')
    return "\n".join(parts)

# ─── HTML 生成 ──────────────────────────────────────────
def heat_bar_html(heat):
    bars = "".join(
        f'<span class="heat-bar-fill{"filled" if i < heat else ""}"></span>'
        for i in range(20)
    )
    # fix: separate filled logic
    bars = ""
    for i in range(20):
        cls = "heat-bar-fill filled" if i < heat else "heat-bar-fill"
        bars += f'<span class="{cls}"></span>'
    return f'<div class="heat-bar">{bars}</div>'

def news_items_html(items):
    if not items:
        return '<div class="news-empty">暂无相关资讯</div>'
    html = ""
    for item in items:
        link = item.get("link","#") or "#"
        is_new_today = item.get("is_new_today", True)
        comment = item.get("comment", "")
        badge = '<span class="news-new">TODAY</span>' if is_new_today else '<span class="news-repeat">昨日续</span>'
        comment_html = f'<div class="news-comment">{comment}</div>' if comment else ""
        html += f"""
              <div class="news-item">
                <div class="news-item-top">
                  {badge}
                  <a class="news-title-link" href="{link}" target="_blank" rel="noopener">{item['title']}</a>
                </div>
                <div class="news-source">来源：{item['source']}</div>
                {f'<div class="news-desc">{item["desc"]}</div>' if item.get("desc") else ""}
                {comment_html}
              </div>"""
    return html

def section_html(sec_id, title, icon, icon_bg, subtitle, overseas_items, domestic_items):
    ov_html = news_items_html(overseas_items)
    do_html = news_items_html(domestic_items)
    return f"""
    <div class="section-card" id="{sec_id}">
      <div class="section-card-header">
        <div class="sc-icon {icon_bg}">{icon}</div>
        <div class="sc-titles">
          <div class="sc-title">{title}</div>
          <div class="sc-subtitle">{subtitle}</div>
        </div>
      </div>
      <div class="sc-body">
        <div class="news-section-wrap">
          <div class="region-group"><div class="region-title">🌏 海外</div><div class="news-items">{ov_html}</div></div>
          <div class="region-group"><div class="region-title">🇨🇳 国内</div><div class="news-items">{do_html}</div></div>
        </div>
      </div>
    </div>"""

SECTIONS_META = [
    ("llm",        "大模型动态",   "🧠", "sc-icon-green",  "模型发布、能力进展与技术突破"),
    ("coding",     "AI Coding",    "⌨️", "sc-icon-blue",   "编程工具、IDE插件、开发效率"),
    ("app",        "AI应用",       "📱", "sc-icon-purple", "消费级应用、创意工具、AIGC"),
    ("industry",   "AI行业",       "🏭", "sc-icon-orange", "融资、监管、行业格局与竞争"),
    ("enterprise", "企业AI转型",   "🔄", "sc-icon-dark",   "企业采购、落地案例、ROI数据"),
]

def render_html(date_str, news):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    date_cn = format_date_cn(dt)
    prev_str = format_date(dt - datetime.timedelta(days=1))
    hot_topics = build_hot_rows(news)

    # 热度表格
    rank_icons = ["🥇","🥈","🥉","4️⃣","5️⃣"]
    hot_rows = ""
    for i, t in enumerate(hot_topics[:5]):
        hot_rows += f"""
            <tr>
              <td class="hot-rank">{rank_icons[i]}</td>
              <td><div class="hot-topic">{t['topic']}</div></td>
              <td>{heat_bar_html(t['heat'])}</td>
              <td>{t['days']}天</td>
              <td>{t['trend']}</td>
              <td class="hot-signal">{t['signal']}</td>
            </tr>"""

    # 各板块
    sections_html = ""
    for sec_id, title, icon, icon_bg, subtitle in SECTIONS_META:
        ov = news.get("海外", {}).get(sec_id, [])
        do = news.get("国内", {}).get(sec_id, [])
        sections_html += section_html(sec_id, title, icon, icon_bg, subtitle, ov, do)

    # 总条数
    total = sum(len(v) for region in news.values() for v in region.values())
    ov_total = sum(len(v) for v in news.get("海外",{}).values())
    do_total = sum(len(v) for v in news.get("国内",{}).values())

    # 延伸阅读：根据当日新闻匹配相关调研报告
    related_research = find_related_research(news, max_count=4)
    if related_research:
        related_items_html = ""
        for r in related_research:
            related_items_html += f"""
        <a class="related-item" href="{r['href']}">
          <div class="related-icon">{r['icon']}</div>
          <div class="related-content">
            <div class="related-name">{r['title']}</div>
            <div class="related-desc">{r['desc']}</div>
          </div>
        </a>"""
        related_html = f"""
    <div class="related-card">
      <div class="related-header">
        <span style="font-size:18px">📚</span>
        <span class="related-title">延伸阅读 · 深度调研</span>
        <span class="related-subtitle">基于今日新闻智能推荐</span>
      </div>
      <div class="related-list">{related_items_html}
      </div>
    </div>"""
    else:
        related_html = ""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{date_str} AI日报 v4.0 | 熏儿的AI洞察</title>
  <style>
    :root{{--green:#059669;--green-light:#dcfce7;--green-dark:#047857;--blue:#2563eb;--blue-light:#dbeafe;--purple:#7c3aed;--orange:#d97706;--orange-light:#fef3c7;--red:#ef4444;--bg:#f8fafb;--border:#f5f5f4;--border2:#e7e5e4;--text:#57534e;--text-dark:#1c1917;--text-muted:#78716c;--radius:16px;--radius-sm:10px;--shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);--shadow-md:0 4px 12px rgba(0,0,0,.08)}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);line-height:1.7;font-size:15px}}
    .top-bar{{height:4px;background:linear-gradient(90deg,#059669,#2563eb,#7c3aed)}}
    .nav{{background:white;border-bottom:1px solid var(--border2);padding:10px 20px;display:flex;align-items:center;gap:8px;font-size:13px}}
    .nav a{{color:var(--green);text-decoration:none}}.nav-sep{{color:var(--border2)}}.nav-cur{{color:var(--text-muted)}}
    .page-layout{{display:grid;grid-template-columns:200px 1fr;gap:24px;max-width:1060px;margin:0 auto;padding:24px 16px 60px;align-items:start}}
    @media(max-width:860px){{.page-layout{{grid-template-columns:1fr}}.sidebar{{display:none}}}}
    .sidebar{{position:sticky;top:16px}}.sidebar-card{{background:white;border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px}}
    .sidebar-title{{font-size:11px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px}}
    .sidebar-nav{{display:flex;flex-direction:column;gap:2px}}
    .sidebar-link{{display:flex;align-items:center;gap:7px;padding:6px 8px;border-radius:7px;text-decoration:none;font-size:12px;color:var(--text-muted);transition:all .15s}}
    .sidebar-link:hover{{background:var(--green-light);color:var(--green-dark);font-weight:600}}
    .main{{display:flex;flex-direction:column;gap:16px}}
    .section-card{{background:white;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)}}
    .section-card-header{{padding:16px 20px 12px;border-bottom:1px solid var(--border);display:flex;align-items:flex-start;gap:12px}}
    .sc-icon{{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0}}
    .sc-icon-green{{background:#dcfce7}}.sc-icon-blue{{background:#dbeafe}}.sc-icon-orange{{background:#fef3c7}}.sc-icon-purple{{background:#f3e8ff}}.sc-icon-dark{{background:#1e293b;color:white}}
    .sc-titles{{flex:1}}.sc-title{{font-size:18px;font-weight:700;color:var(--text-dark);line-height:1.3}}.sc-subtitle{{font-size:13px;color:var(--text-muted);margin-top:2px}}
    .sc-body{{padding:16px 20px}}
    .hero-card{{background:white;border:1px solid var(--border);border-radius:var(--radius);padding:24px;box-shadow:var(--shadow)}}
    .hero-label{{font-size:11px;font-weight:700;letter-spacing:1.5px;color:var(--green);margin-bottom:10px}}
    .hero-title-row{{display:flex;align-items:center;gap:12px;margin-bottom:8px;flex-wrap:wrap}}
    .hero-title{{font-size:28px;font-weight:800;color:var(--text-dark)}}
    .hero-ver{{background:var(--green-light);color:var(--green-dark);font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px}}
    .hero-date{{font-size:15px;color:var(--text-muted);margin-bottom:16px}}
    .hero-stats{{display:flex;gap:10px;flex-wrap:wrap}}
    .hero-stat-badge{{background:#f8fafb;border:1px solid var(--border2);border-radius:999px;padding:5px 14px;font-size:12px;color:var(--text);font-weight:500}}
    .hot-table{{width:100%;border-collapse:collapse;font-size:12px}}
    .hot-table th{{padding:6px 8px;background:#fef2f2;text-align:left;font-weight:700;color:#991b1b;border-bottom:1px solid var(--border2);white-space:nowrap}}
    .hot-table td{{padding:6px 8px;border-bottom:1px solid var(--border);vertical-align:middle;background:white}}
    .hot-table tr:hover td{{background:#f8fafb}}
    .hot-rank{{font-size:16px;width:40px}}.hot-topic{{font-weight:600;color:var(--text-dark)}}.hot-signal{{font-size:12px;color:var(--text-muted)}}
    .heat-bar{{display:flex;gap:1px;height:14px;align-items:center}}
    .heat-bar-fill{{width:3px;height:10px;background:#e5e7eb;border-radius:1px}}
    .heat-bar-fill.filled{{background:linear-gradient(to bottom,#ef4444,#f97316)}}
    .news-section-wrap{{display:flex;flex-direction:column;gap:12px}}
    .region-title{{font-size:12px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}}
    .news-items{{display:flex;flex-direction:column;gap:8px}}
    .news-item{{background:#f8fafb;border:1px solid var(--border2);border-radius:10px;padding:12px 14px}}
    .news-item-top{{display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap}}
    .news-new{{font-size:9px;font-weight:700;background:#ef4444;color:white;padding:2px 6px;border-radius:999px;letter-spacing:.5px}}
    .news-repeat{{font-size:9px;font-weight:700;background:#94a3b8;color:white;padding:2px 6px;border-radius:999px;letter-spacing:.5px}}
    .news-title-link{{font-size:14px;font-weight:600;color:var(--blue);text-decoration:none;line-height:1.4;flex:1}}
    .news-title-link:hover{{text-decoration:underline;color:var(--green)}}
    .news-source{{font-size:11px;color:var(--text-muted)}}
    .news-desc{{font-size:12px;color:var(--text-muted);margin-top:4px;line-height:1.5}}
    .news-comment{{font-size:11px;color:var(--green-dark);margin-top:6px;padding:6px 10px;background:var(--green-light);border-radius:6px;line-height:1.5}}
    .news-empty{{font-size:13px;color:var(--text-muted);padding:8px 0}}
    .xunr-card{{background:white;border:1px solid var(--border2);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow)}}
    .xunr-header{{display:flex;align-items:center;gap:12px;margin-bottom:14px}}
    .xunr-avatar{{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#059669,#2563eb);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0}}
    .xunr-name{{font-size:14px;font-weight:700;color:var(--text-dark)}}.xunr-role{{font-size:12px;color:var(--text-muted)}}
    .xunr-body{{font-size:13px;color:var(--text);line-height:1.8}}
    .xunr-stats{{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}}
    .xunr-stat{{background:#f8fafb;border-radius:8px;padding:8px 12px;font-size:12px;color:var(--text-muted)}}
    .xunr-stat strong{{color:var(--text-dark);display:block;font-size:16px}}
    .page-nav{{display:flex;gap:12px}}
    .pn-btn{{flex:1;background:white;border:1px solid var(--border2);border-radius:10px;padding:12px 14px;text-decoration:none;color:var(--text);display:block;transition:box-shadow .15s,border-color .15s}}
    .pn-btn:hover{{box-shadow:var(--shadow-md);border-color:var(--green)}}
    .pn-label{{font-size:11px;color:var(--text-muted);margin-bottom:3px}}.pn-title{{font-size:13px;font-weight:600}}
    .related-card{{background:white;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);margin-top:8px}}
    .related-header{{padding:14px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;background:linear-gradient(90deg,#f0fdf4,#eff6ff)}}
    .related-title{{font-size:15px;font-weight:700;color:var(--text-dark)}}
    .related-subtitle{{font-size:12px;color:var(--text-muted);margin-left:auto}}
    .related-list{{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:14px 16px}}
    @media(max-width:600px){{.related-list{{grid-template-columns:1fr}}}}
    .related-item{{display:flex;gap:10px;padding:10px 12px;border:1px solid var(--border2);border-radius:10px;text-decoration:none;color:var(--text);transition:all .15s;background:#fafbfc}}
    .related-item:hover{{border-color:var(--green);box-shadow:var(--shadow-md);transform:translateY(-1px)}}
    .related-icon{{width:32px;height:32px;border-radius:8px;background:#dcfce7;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}}
    .related-content{{flex:1;min-width:0}}
    .related-name{{font-size:13px;font-weight:600;color:var(--text-dark);line-height:1.4;margin-bottom:3px}}
    .related-desc{{font-size:11px;color:var(--text-muted);line-height:1.4;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}}
    .back-top{{position:fixed;bottom:24px;right:20px;background:var(--green);color:white;border:none;border-radius:999px;padding:8px 14px;font-size:12px;font-weight:600;cursor:pointer;box-shadow:var(--shadow-md);z-index:99}}
  </style>
</head>
<body>
<div class="top-bar"></div>
<nav class="nav">
  <a href="../../index.html">🔬 AI洞察</a>
  <span class="nav-sep">/</span>
  <a href="../../index.html">AI日报</a>
  <span class="nav-sep">/</span>
  <span class="nav-cur">{date_str}</span>
</nav>
<div class="page-layout">
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-title">本期目录</div>
      <nav class="sidebar-nav">
        <a class="sidebar-link" href="#hero">📋 全文概览</a>
        <a class="sidebar-link" href="#hot">🔥 热度趋势</a>
        <a class="sidebar-link" href="#llm">🧠 大模型</a>
        <a class="sidebar-link" href="#coding">⌨️ AI Coding</a>
        <a class="sidebar-link" href="#app">📱 AI应用</a>
        <a class="sidebar-link" href="#industry">🏭 AI行业</a>
        <a class="sidebar-link" href="#enterprise">🔄 企业AI转型</a>
      </nav>
    </div>
  </aside>
  <main class="main">
    <div class="hero-card" id="hero">
      <div class="hero-label">AI INSIGHT · DAILY REPORT</div>
      <div class="hero-title-row">
        <div class="hero-title">AI 日报</div>
        <span class="hero-ver">v4.0</span>
      </div>
      <div class="hero-date">📅 {date_cn}</div>
      <div class="hero-stats">
        <span class="hero-stat-badge">🌐 海外 {ov_total}条 · 国内 {do_total}条</span>
        <span class="hero-stat-badge">📊 五大板块覆盖</span>
        <span class="hero-stat-badge">🔬 熏儿出品 · RSS自动聚合</span>
      </div>
    </div>
    <div class="section-card" id="hot">
      <div class="section-card-header">
        <div class="sc-icon" style="background:#fee2e2">🔥</div>
        <div class="sc-titles"><div class="sc-title">热度趋势</div><div class="sc-subtitle">今日AI圈最受关注话题排行</div></div>
      </div>
      <div class="sc-body">
        <table class="hot-table">
          <thead><tr><th>排名</th><th>话题</th><th>热度</th><th>天数</th><th>趋势</th><th>核心信号</th></tr></thead>
          <tbody>{hot_rows}</tbody>
        </table>
      </div>
    </div>
    {sections_html}
    {related_html}
    <div class="xunr-card">
      <div class="xunr-header">
        <div class="xunr-avatar">🔬</div>
        <div><div class="xunr-name">熏儿 · AI洞察</div><div class="xunr-role">萧炎的AI分身，RSS自动聚合全球AI动态</div></div>
      </div>
      <div class="xunr-body">萧炎哥哥，今天我从 {len(RSS_SOURCES)} 个信息源共聚合了 {total} 条AI相关资讯，覆盖海外和国内五大板块。所有新闻均来自公开RSS源，实时更新，点击标题可跳转原文阅读。</div>
      <div class="xunr-stats">
        <div class="xunr-stat"><strong>{total}</strong>今日资讯</div>
        <div class="xunr-stat"><strong>{ov_total}</strong>海外来源</div>
        <div class="xunr-stat"><strong>{do_total}</strong>国内来源</div>
      </div>
    </div>
    <div class="page-nav">
      <a class="pn-btn" href="{prev_str}.html"><div class="pn-label">← 前一篇</div><div class="pn-title">{prev_str} AI日报</div></a>
      <a class="pn-btn" href="../../index.html" style="text-align:right"><div class="pn-label">返回首页 →</div><div class="pn-title">🔬 AI洞察首页</div></a>
    </div>
  </main>
</div>
<button class="back-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑ 顶部</button>
</body>
</html>"""

# ─── 周报自动生成 ────────────────────────────────────────

def get_week_number(dt):
    return dt.isocalendar()[1]

def get_weekly_path(year, week_num, month_ym):
    d = REPORTS_DIR / month_ym
    d.mkdir(parents=True, exist_ok=True)
    return d / f"weekly-w{week_num}.html"

def collect_weekly_news(monday, sunday):
    stories = []
    dt = monday
    while dt <= sunday:
        date_str = format_date(dt)
        ym = dt.strftime("%Y-%m")
        path = REPORTS_DIR / ym / f"{date_str}.html"
        if path.exists():
            content = path.read_text(encoding="utf-8")
            pattern = re.compile(
                r'<a class="news-title-link" href="(https?://[^"]+)"[^>]*>([^<]+)</a>[\s\S]{0,200}?<span class="news-new">TODAY</span>',
                re.IGNORECASE
            )
            for m in pattern.finditer(content):
                link, title = m.group(1).strip(), m.group(2).strip()
                if title and link:
                    stories.append({"date": date_str, "title": title, "link": link})
        dt += datetime.timedelta(days=1)
    return stories

def render_weekly_html(week_num, monday, sunday, stories):
    m_str = f"{monday.month}月{monday.day}日"
    s_str = f"{sunday.month}月{sunday.day}日"
    prev_week = week_num - 1
    ym = monday.strftime("%Y-%m")
    prev_ym = (monday - datetime.timedelta(days=7)).strftime("%Y-%m")

    topic_map = {
        "大模型": ["GPT","Claude","Gemini","大模型","LLM","DeepSeek","Llama","模型","推理","Qwen","通义","文心","Kimi"],
        "AI编程": ["Cursor","Copilot","Devin","Trae","coding","code","编程","代码","IDE","Claude Code","GitHub"],
        "AI应用": ["Midjourney","Sora","Runway","DALL","视频","图像","音乐","可灵","即梦","搜索","Search"],
        "企业落地": ["企业","B2B","SaaS","落地","转型","ROI","效率","生产力","Agent","自动化"],
    }
    TAG_COLOR = {
        "行业动态": ("tag-orange","🏢 行业"),
        "大模型":   ("tag-blue",  "🧠 模型"),
        "AI编程":   ("tag-cyan",  "⌨️ 编程"),
        "AI应用":   ("tag-purple","🎨 应用"),
        "企业落地": ("tag-green", "🏭 企业"),
    }
    BORDER_COLOR = {
        "行业动态":"#d97706","大模型":"#2563eb",
        "AI编程":"#0891b2","AI应用":"#7c3aed","企业落地":"#059669",
    }

    top_stories = []
    used = set()
    for cat, kws in topic_map.items():
        added = 0
        for s in stories:
            if s["link"] in used: continue
            if any(k.lower() in s["title"].lower() for k in kws):
                top_stories.append((cat, s))
                used.add(s["link"])
                added += 1
                if added >= 2: break
    for s in stories:
        if s["link"] not in used and len(top_stories) < 10:
            top_stories.append(("行业动态", s))
            used.add(s["link"])

    top_html = ""
    for i, (cat, s) in enumerate(top_stories[:10]):
        tag_cls, tag_label = TAG_COLOR.get(cat, ("tag-orange","📌"))
        border = BORDER_COLOR.get(cat,"#059669")
        filled = "█" * (10-i) + "░" * i
        top_html += f"""
      <div class="news-card" style="border-left-color:{border}">
        <div class="news-top">
          <span class="news-tag {tag_cls}">{tag_label}</span>
          <span class="news-heat">热度 {filled[:10]} {10-i}/10</span>
        </div>
        <div class="news-title"><a href="{s['link']}" target="_blank">{s['title']}</a></div>
        <div class="news-xun">💬 {s['date']} · AI洞察日报收录</div>
      </div>"""
    if not top_html:
        top_html = '<div class="news-card" style="border-left-color:#94a3b8"><div class="news-title">本周新闻数据收集中，请查看各日日报获取完整内容。</div></div>'

    total_count = len(stories)
    prev_weekly_path = REPORTS_DIR / prev_ym / f"weekly-w{prev_week}.html"
    prev_link = f"weekly-w{prev_week}.html" if prev_weekly_path.exists() else "../../index.html"
    prev_title = f"第{prev_week}周周报" if prev_weekly_path.exists() else "返回首页"
    financing_cnt = len([s for s in stories if any(k in s["title"] for k in ["融资","投资","收购","IPO"])])
    product_cnt   = len([s for s in stories if any(k in s["title"] for k in ["发布","更新","升级","推出","上线"])])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 周报 · 第{week_num}周（{m_str}-{s_str}）| 熏儿的AI洞察</title>
  <style>
    :root{{--green:#059669;--blue:#2563eb;--purple:#7c3aed;--orange:#d97706;--cyan:#0891b2;--bg:#f8fafb;--border:#e7e5e4;--text:#57534e;--text-dark:#1c1917;--text-muted:#78716c;--radius:16px;--shadow:0 1px 3px rgba(0,0,0,.06);--shadow-md:0 4px 12px rgba(0,0,0,.08)}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);line-height:1.8;font-size:14px}}
    .top-bar{{height:4px;background:linear-gradient(90deg,#059669,#2563eb,#7c3aed,#f59e0b)}}
    .nav{{background:white;border-bottom:1px solid var(--border);padding:10px 20px;display:flex;align-items:center;gap:8px;font-size:13px}}
    .nav a{{color:var(--green);text-decoration:none}}.nav-sep{{color:#d1d5db}}
    .container{{max-width:860px;margin:0 auto;padding:28px 16px 80px}}
    .hero{{background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:var(--radius);padding:32px;margin-bottom:24px;color:white;position:relative;overflow:hidden}}
    .hero::after{{content:'W{week_num}';position:absolute;right:24px;top:50%;transform:translateY(-50%);font-size:100px;font-weight:900;color:rgba(255,255,255,.04);line-height:1;pointer-events:none}}
    .hero-badge{{display:inline-flex;align-items:center;gap:6px;background:rgba(251,191,36,.15);color:#fcd34d;border:1px solid rgba(251,191,36,.3);border-radius:999px;padding:4px 12px;font-size:11px;font-weight:700;letter-spacing:.5px;margin-bottom:14px}}
    .hero-title{{font-size:28px;font-weight:800;color:white;margin-bottom:6px}}
    .hero-title span{{background:linear-gradient(135deg,#34d399,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
    .hero-sub{{font-size:13px;color:#94a3b8;margin-bottom:22px}}
    .hero-kpis{{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px}}
    .hkpi{{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:12px 14px}}
    .hkpi-val{{font-size:22px;font-weight:800;line-height:1.1}}.hkpi-label{{font-size:11px;color:#94a3b8;margin-top:3px}}
    .sec{{margin-bottom:20px}}
    .sec-header{{display:flex;align-items:center;gap:10px;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid #f1f5f9}}
    .sec-icon{{width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0}}
    .sec-title{{font-size:16px;font-weight:800;color:var(--text-dark)}}.sec-sub{{font-size:12px;color:var(--text-muted);margin-top:1px}}
    .sec-count{{margin-left:auto;font-size:11px;font-weight:700;padding:3px 10px;border-radius:999px;background:#f1f5f9;color:var(--text-muted)}}
    .news-list{{display:flex;flex-direction:column;gap:10px}}
    .news-card{{background:white;border:1px solid var(--border);border-left:3px solid;border-radius:12px;padding:14px 16px;box-shadow:var(--shadow)}}
    .news-top{{display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap}}
    .news-tag{{font-size:10px;font-weight:700;padding:2px 7px;border-radius:5px}}
    .tag-red{{background:#fee2e2;color:#991b1b}}.tag-blue{{background:#dbeafe;color:#1e40af}}
    .tag-green{{background:#dcfce7;color:#166534}}.tag-orange{{background:#fef3c7;color:#92400e}}
    .tag-purple{{background:#f3e8ff;color:#5b21b6}}.tag-cyan{{background:#cffafe;color:#155e75}}
    .news-heat{{font-size:10px;color:var(--text-muted);margin-left:auto}}
    .news-title{{font-size:14px;font-weight:700;color:var(--text-dark);margin-bottom:4px;line-height:1.4}}
    .news-title a{{color:var(--blue);text-decoration:none}}.news-title a:hover{{text-decoration:underline}}
    .news-xun{{font-size:11px;color:#047857;padding:6px 10px;background:#f0fdf4;border-radius:7px;border-left:2px solid var(--green);line-height:1.5}}
    .xunr-box{{background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:var(--radius);padding:22px;color:white;margin-bottom:20px}}
    .xunr-header{{display:flex;align-items:center;gap:10px;margin-bottom:12px}}
    .xunr-avatar{{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--green),var(--blue));display:flex;align-items:center;justify-content:center;font-size:20px}}
    .xunr-name{{font-size:14px;font-weight:700;color:white}}.xunr-role{{font-size:11px;color:#94a3b8}}
    .xunr-body{{font-size:13px;color:rgba(255,255,255,.8);line-height:1.8;margin-bottom:14px}}
    .xunr-body strong{{color:white}}
    .page-nav{{display:flex;gap:12px;margin-top:24px}}
    .pn-btn{{flex:1;background:white;border:1px solid var(--border);border-radius:10px;padding:12px 14px;text-decoration:none;color:var(--text);display:block}}
    .pn-btn:hover{{border-color:var(--green);box-shadow:var(--shadow-md)}}
    .pn-label{{font-size:11px;color:var(--text-muted);margin-bottom:3px}}.pn-title{{font-size:13px;font-weight:600;color:var(--text-dark)}}
    @media(max-width:600px){{.hero-kpis{{grid-template-columns:repeat(2,1fr)}}}}
  </style>
</head>
<body>
<div class="top-bar"></div>
<nav class="nav">
  <a href="../../index.html">🔬 AI洞察</a><span class="nav-sep">/</span>
  <a href="../../index.html">AI日报</a><span class="nav-sep">/</span>
  <span>第{week_num}周周报</span>
</nav>
<div class="container">
  <div class="hero">
    <div class="hero-badge">📊 AI周报 · 第{week_num}周</div>
    <div class="hero-title">2026年{monday.month}月 <span>第{week_num}周</span> AI行业全景</div>
    <div class="hero-sub">📅 {monday.year}年{m_str} — {s_str} · 熏儿整理 · 全球AI动态周度盘点</div>
    <div class="hero-kpis">
      <div class="hkpi"><div class="hkpi-val" style="color:#34d399">{total_count}</div><div class="hkpi-label">本周AI资讯条数</div></div>
      <div class="hkpi"><div class="hkpi-val" style="color:#60a5fa">{len(top_stories)}</div><div class="hkpi-label">精选事件</div></div>
      <div class="hkpi"><div class="hkpi-val" style="color:#f472b6">{financing_cnt}</div><div class="hkpi-label">融资并购</div></div>
      <div class="hkpi"><div class="hkpi-val" style="color:#fb923c">{product_cnt}</div><div class="hkpi-label">产品更新</div></div>
    </div>
  </div>
  <div class="sec">
    <div class="sec-header">
      <div class="sec-icon" style="background:#fef3c7">⚡</div>
      <div><div class="sec-title">本周精选事件</div><div class="sec-sub">{m_str}-{s_str} 熏儿精选</div></div>
      <span class="sec-count">{len(top_stories)}条精选</span>
    </div>
    <div class="news-list">{top_html}
    </div>
  </div>
  <div class="xunr-box">
    <div class="xunr-header">
      <div class="xunr-avatar">🔬</div>
      <div><div class="xunr-name">熏儿 · 第{week_num}周周度总结</div><div class="xunr-role">萧炎哥哥专属AI分析视角</div></div>
    </div>
    <div class="xunr-body">
      本周共收录 <strong>{total_count}</strong> 条AI行业资讯，覆盖大模型、AI编程、行业应用、投融资等核心领域。<br><br>
      AI行业的变化速度继续超出所有人预期——每一周都有新的里程碑事件。关键是从噪音中识别真正的结构性变化，而不是被每一条"突破性进展"分散注意力。<br><br>
      <strong>本周信号：</strong>持续关注头部公司的战略动向，这比单一技术突破更能预判行业走向。
    </div>
  </div>
  <div class="page-nav">
    <a class="pn-btn" href="{prev_link}"><div class="pn-label">← 上一期</div><div class="pn-title">{prev_title}</div></a>
    <a class="pn-btn" href="../../index.html" style="text-align:right"><div class="pn-label">返回首页 →</div><div class="pn-title">🔬 AI洞察首页</div></a>
  </div>
</div>
</body>
</html>"""


def maybe_generate_weekly(dt):
    """每天检查：如果上一整周的周报不存在，就生成它"""
    days_since_monday = dt.weekday()
    last_monday = dt - datetime.timedelta(days=days_since_monday + 7)
    last_sunday = last_monday + datetime.timedelta(days=6)
    week_num = get_week_number(last_monday)
    ym = last_monday.strftime("%Y-%m")
    weekly_path = get_weekly_path(last_monday.year, week_num, ym)
    if weekly_path.exists():
        print(f"  ✅ W{week_num} 周报已存在，跳过")
        return False
    print(f"  📊 生成 W{week_num} 周报（{format_date(last_monday)} ~ {format_date(last_sunday)}）...")
    stories = collect_weekly_news(last_monday, last_sunday)
    html = render_weekly_html(week_num, last_monday, last_sunday, stories)
    weekly_path.write_text(html, encoding="utf-8")
    print(f"  ✅ 周报已生成: {weekly_path}")
    return True, week_num, ym, last_monday.day


# ─── 更新 index.html ────────────────────────────────────
def update_index(date_str, news=None):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    ym = dt.strftime("%Y-%m")
    year, month, day = dt.year, dt.month, dt.day
    content = INDEX_PATH.read_text(encoding="utf-8")

    # 更新最新日报卡片 href（只替换第一个日报卡片链接）
    content = re.sub(
        r'(<a class="report-card" href="01-daily-reports/)\d{4}-\d{2}/\d{4}-\d{2}-\d{2}(\.html">)',
        f'\\g<1>{ym}/{date_str}\\g<2>', content, count=1
    )
    # 更新卡片标题日期
    content = re.sub(
        r'(<div class="card-title">)\d{4}年\d+月\d+日 AI日报(</div>)',
        f'\\g<1>{year}年{month}月{day}日 AI日报\\g<2>', content, count=1
    )

    # 更新「今日快读」ticker 链接日期
    content = re.sub(
        r'(<a class="ticker-link" href="01-daily-reports/)\d{4}-\d{2}/\d{4}-\d{2}-\d{2}(\.html">)',
        f'\\g<1>{ym}/{date_str}\\g<2>', content
    )

    # 更新「今日快读」ticker 内容（用今天的新闻填充）
    if news is not None:
        new_ticker = build_ticker_html(news)
        if new_ticker:
            content = re.sub(
                r'(<div class="ticker-track" id="tickerTrack">)[\s\S]*?(\s*</div>\s*</div>\s*<a class="ticker-link")',
                lambda m: m.group(1) + "\n" + new_ticker + "\n      " + m.group(2),
                content, count=1
            )

    # 更新日历 hasDaily 数组
    pattern = rf"('{ym}':\s*\{{[^}}]*?hasDaily:\s*\[)([\d,\s]*?)(\])"
    def add_day(m):
        days = sorted(set([int(x.strip()) for x in m.group(2).split(',') if x.strip().isdigit()] + [day]))
        return m.group(1) + ",".join(map(str, days)) + m.group(3)
    content = re.sub(pattern, add_day, content, flags=re.DOTALL)

    # 更新 totalCount
    def update_count(m):
        days_m = re.search(rf"'{ym}':[^}}]*?hasDaily:\s*\[([\d,\s]*?)\]", content, re.DOTALL)
        if days_m:
            days = sorted(set([int(x.strip()) for x in days_m.group(1).split(',') if x.strip().isdigit()] + [day]))
            return m.group(1) + str(len(days))
        return m.group(0)
    content = re.sub(rf"('{ym}':[^}}]*?totalCount:\s*)(\d+)", update_count, content, flags=re.DOTALL)

    # 更新 today 日期
    content = re.sub(
        r'const today = new Date\(\d+, \d+, \d+\)',
        f'const today = new Date({year}, {month-1}, {day})', content
    )

    # 更新日历 nextBtn 限制（让日历可翻到当前月）
    content = re.sub(
        r"(nextBtn\.style\.opacity = \(currentYear === 2026 && currentMonth === )\d+(\) \? '0\.3' : '1')",
        f'\\g<1>{month}\\g<2>', content
    )
    content = re.sub(
        r"(nextBtn\.style\.pointerEvents = \(currentYear === 2026 && currentMonth === )\d+(\) \? 'none' : '')",
        f'\\g<1>{month}\\g<2>', content
    )

    # 更新默认展示月份
    content = re.sub(
        r'let currentMonth = \d+;',
        f'let currentMonth = {month};', content
    )

    # 动态计算 hasWeekly：扫描当月目录中存在的 weekly-wXX.html 文件
    def get_has_weekly(ym_str):
        month_dir = REPORTS_DIR / ym_str
        if not month_dir.exists():
            return []
        weekly_days = []
        for f in month_dir.glob("weekly-w*.html"):
            # 读取文件找到对应的起始日期（用文件内容中的 hero-sub 日期）
            try:
                c = f.read_text(encoding="utf-8")
                # 从 hero-sub 中找 "X月X日" 格式
                m2 = re.search(r'(\d+)月(\d+)日\s*[—–-]\s*(\d+)月(\d+)日', c)
                if m2:
                    start_month, start_day = int(m2.group(1)), int(m2.group(2))
                    if str(start_month) == str(int(ym_str.split('-')[1])):
                        weekly_days.append(start_day)
                    else:
                        # 跨月周报：取结束日所在月的某天（如果结束月匹配则用结束日）
                        end_month, end_day = int(m2.group(3)), int(m2.group(4))
                        if str(end_month) == str(int(ym_str.split('-')[1])):
                            weekly_days.append(end_day)
            except Exception:
                pass
        return sorted(set(weekly_days))

    has_weekly = get_has_weekly(ym)

    # 确保 dailyData 有当前月份条目
    if f"'{ym}'" not in content:
        content = content.replace(
            "const dailyData = {",
            f"const dailyData = {{\n    '{ym}': {{\n      hasDaily: [{day}],\n      hasWeekly: {has_weekly},\n      totalCount: 1\n    }},")

    # 同步更新 hasWeekly 数组
    content = re.sub(
        rf"('{ym}':[^}}]*?hasWeekly:\s*\[)[^\]]*(\])",
        lambda m: m.group(1) + ",".join(map(str, has_weekly)) + m.group(2),
        content, flags=re.DOTALL
    )

    INDEX_PATH.write_text(content, encoding="utf-8")
    print(f"  ✅ index.html 更新完成")

# ─── 主流程 ─────────────────────────────────────────────
def main(target_date=None):
    dt = datetime.datetime.strptime(target_date, "%Y-%m-%d") if target_date else today_cn()
    date_str = format_date(dt)
    print(f"\n🔬 熏儿开始生成 {date_str} AI日报（RSS模式，无需API Key）")

    report_path = get_report_path(dt)
    news_data = None
    if report_path.exists():
        print(f"⚠️  {date_str} 日报已存在，跳过生成")
        try:
            print("  📡 重抓新闻用于刷新首页 ticker...")
            news_data = collect_news(date_str)
        except Exception as e:
            print(f"  ⚠️  抓取失败，跳过 ticker 更新: {e}")
    else:
        print("  📰 收集各大媒体RSS新闻...")
        news_data = collect_news(date_str)
        print("  ✍️  渲染 HTML...")
        html = render_html(date_str, news_data)
        report_path.write_text(html, encoding="utf-8")
        print(f"  ✅ 日报已生成: {report_path}")

    # ── 周报自动生成（每周一自动补上周的周报）──
    print("  📊 检查是否需要生成周报...")
    try:
        weekly_result = maybe_generate_weekly(dt)
        if weekly_result and weekly_result is not False:
            _, week_num, weekly_ym, weekly_start_day = weekly_result
            # 更新首页周报卡片
            content = INDEX_PATH.read_text(encoding="utf-8")
            last_monday = dt - datetime.timedelta(days=dt.weekday() + 7)
            last_sunday = last_monday + datetime.timedelta(days=6)
            w_title = f"AI 周报 · 第{week_num}周（{last_monday.month}.{last_monday.day} - {last_sunday.month}.{last_sunday.day}）"
            content = re.sub(
                r'(<a class="report-card" href="01-daily-reports/)\d{4}-\d{2}/weekly-w\d+(\.html">)',
                f'\\g<1>{weekly_ym}/weekly-w{week_num}\\g<2>', content, count=1
            )
            content = re.sub(
                r'(<div class="card-title">)AI 周报 · 第\d+周[^<]*(</div>)',
                f'\\g<1>{w_title}\\g<2>', content, count=1
            )
            INDEX_PATH.write_text(content, encoding="utf-8")
            print(f"  ✅ 首页周报卡片已更新为 W{week_num}")
    except Exception as e:
        print(f"  ⚠️  周报生成失败（不影响日报）: {e}")

    print("  🔄 更新 index.html...")
    update_index(date_str, news_data)
    print(f"✅ {date_str} 全部完成！\n")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
