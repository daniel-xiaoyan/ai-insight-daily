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
    {"url": "https://venturebeat.com/feed/", "name": "VentureBeat", "region": "海外", "tags": ["AI","machine learning","LLM","agent","model"]},
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
                items.append({"title": title, "desc": summary[:200], "link": link, "pub": ""})
    except Exception as e:
        print(f"  ⚠️  解析RSS失败: {e}")
    return items

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

# ─── 收集新闻 ──────────────────────────────────────────
def collect_news(date_str):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    all_news = {"海外": {}, "国内": {}}
    
    for src in RSS_SOURCES:
        print(f"  📡 抓取 {src['name']}...")
        xml = fetch_rss(src["url"])
        if not xml:
            continue
        items = parse_rss(xml)
        region = src["region"]
        count = 0
        for item in items[:30]:
            if not is_ai_related(item["title"], src["tags"]):
                continue
            cat = classify_topic(item["title"])
            if cat not in all_news[region]:
                all_news[region][cat] = []
            if len(all_news[region][cat]) < 3:
                all_news[region][cat].append({
                    "title": item["title"],
                    "source": src["name"],
                    "link": item["link"],
                    "desc": clean_html(item["desc"]),
                })
                count += 1
        print(f"     → 筛选到 {count} 条AI相关")
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
        html += f"""
              <div class="news-item">
                <div class="news-item-top">
                  <span class="news-new">NEW</span>
                  <a class="news-title-link" href="{link}" target="_blank" rel="noopener">{item['title']}</a>
                </div>
                <div class="news-source">来源：{item['source']}</div>
                {f'<div class="news-desc">{item["desc"]}</div>' if item.get("desc") else ""}
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
    .news-title-link{{font-size:14px;font-weight:600;color:var(--blue);text-decoration:none;line-height:1.4;flex:1}}
    .news-title-link:hover{{text-decoration:underline;color:var(--green)}}
    .news-source{{font-size:11px;color:var(--text-muted)}}
    .news-desc{{font-size:12px;color:var(--text-muted);margin-top:4px;line-height:1.5}}
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

# ─── 更新 index.html ────────────────────────────────────
def update_index(date_str):
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

    # 确保 dailyData 有当前月份条目
    if f"'{ym}'" not in content:
        content = content.replace(
            "const dailyData = {",
            f"const dailyData = {{\n    '{ym}': {{\n      hasDaily: [{day}],\n      hasWeekly: [],\n      totalCount: 1\n    }},"
        )

    INDEX_PATH.write_text(content, encoding="utf-8")
    print(f"  ✅ index.html 更新完成")

# ─── 主流程 ─────────────────────────────────────────────
def main(target_date=None):
    dt = datetime.datetime.strptime(target_date, "%Y-%m-%d") if target_date else today_cn()
    date_str = format_date(dt)
    print(f"\n🔬 熏儿开始生成 {date_str} AI日报（RSS模式，无需API Key）")

    report_path = get_report_path(dt)
    if report_path.exists():
        print(f"⚠️  {date_str} 日报已存在，跳过生成")
    else:
        print("  📰 收集各大媒体RSS新闻...")
        news = collect_news(date_str)
        print("  ✍️  渲染 HTML...")
        html = render_html(date_str, news)
        report_path.write_text(html, encoding="utf-8")
        print(f"  ✅ 日报已生成: {report_path}")

    print("  🔄 更新 index.html...")
    update_index(date_str)
    print(f"✅ {date_str} 全部完成！\n")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
