#!/usr/bin/env python3
"""
AI洞察日报 - 全自动生成器
一键生成专业级日报HTML
"""

import json
import os
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

# 搜索配置
SEARCH_QUERIES = {
    "overseas_llm": [
        "OpenAI GPT new model",
        "Anthropic Claude announcement",
        "Google Gemini update",
        "Meta AI Llama news",
    ],
    "overseas_coding": [
        "Cursor AI coding tool",
        "GitHub Copilot new features",
        "Claude Code update",
        "AI programming tool",
    ],
    "overseas_app": [
        "AI Agent platform enterprise",
        "OpenAI Cloudflare",
        "Google Workspace Gemini",
    ],
    "overseas_industry": [
        "AI startup funding",
        "Sam Altman OpenAI",
        "Cognition AI Devin",
    ],
    "domestic_llm": [
        "百度文心一言 更新",
        "阿里通义千问 新功能", 
        "月之暗面 Kimi 更新",
        "智谱AI GLM 新模型",
        "DeepSeek 更新",
    ],
    "domestic_coding": [
        "AI编程工具 国内",
        "代码生成工具 更新",
    ],
    "domestic_app": [
        "AI应用 产品发布 国内",
        "智能体平台 国内",
    ],
    "domestic_industry": [
        "AI融资 投资 国内",
        "AI行业 国内",
    ],
}

def search_web(query: str, count: int = 3) -> List[Dict]:
    """简单网页搜索"""
    results = []
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
            matches = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>', html)
            
            for link, title in matches[:count]:
                title = title.replace('&#x27;', "'").replace('&quot;', '"')
                results.append({"title": title, "url": link})
    except:
        pass
    return results

def collect_news() -> Dict:
    """采集新闻"""
    today = datetime.now().strftime("%Y-%m-%d")
    news = {"date": today, "items": []}
    
    print(f"🔍 采集 {today} 新闻...")
    
    for category, queries in SEARCH_QUERIES.items():
        region = "海外" if category.startswith("overseas") else "国内"
        section = category.split("_")[1]
        
        for query in queries:
            results = search_web(query, 2)
            for r in results:
                news["items"].append({
                    **r,
                    "region": region,
                    "section": section,
                    "query": query
                })
            time.sleep(0.5)
    
    # 去重
    seen = set()
    unique = []
    for item in news["items"]:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)
    news["items"] = unique
    
    print(f"✅ 采集到 {len(unique)} 条新闻")
    return news

def generate_sample_content(news: Dict) -> Dict:
    """生成示例日报内容（实际使用AI生成）"""
    today = news["date"]
    
    # 按板块分组
    llm_o = [n for n in news["items"] if n["section"] == "llm" and n["region"] == "海外"][:3]
    llm_d = [n for n in news["items"] if n["section"] == "llm" and n["region"] == "国内"][:3]
    coding_o = [n for n in news["items"] if n["section"] == "coding" and n["region"] == "海外"][:2]
    coding_d = [n for n in news["items"] if n["section"] == "coding" and n["region"] == "国内"][:2]
    app_o = [n for n in news["items"] if n["section"] == "app" and n["region"] == "海外"][:2]
    app_d = [n for n in news["items"] if n["section"] == "app" and n["region"] == "国内"][:2]
    ind_o = [n for n in news["items"] if n["section"] == "industry" and n["region"] == "海外"][:2]
    ind_d = [n for n in news["items"] if n["section"] == "industry" and n["region"] == "国内"][:2]
    
    return {
        "date": today,
        "overview": [
            {"emoji": "🧠", "section": "大模型", "summary": f"{'、'.join([n['title'][:20] for n in llm_o[:2]])}..."},
            {"emoji": "⌨️", "section": "AI Coding", "summary": "Cursor、Claude Code等工具持续更新"},
            {"emoji": "📱", "section": "AI应用", "summary": "企业级AI Agent部署门槛持续降低"},
            {"emoji": "🏭", "section": "AI行业", "summary": "AI初创公司融资热度不减"},
        ],
        "heat_trends": [
            {"rank": "🥇", "topic": "大模型竞争", "heat": "9", "days": "5", "trend": "🔥 热门"},
            {"rank": "🥈", "topic": "AI编程工具", "heat": "8", "days": "3", "trend": "📈 上升"},
            {"rank": "🥉", "topic": "企业AI转型", "heat": "7", "days": "2", "trend": "➡️ 稳定"},
        ],
        "llm": {"overseas": llm_o, "domestic": llm_d},
        "coding": {"overseas": coding_o, "domestic": coding_d},
        "app": {"overseas": app_o, "domestic": app_d},
        "industry": {"overseas": ind_o, "domestic": ind_d},
        "stats": {
            "total": len(news["items"]),
            "overseas": len([n for n in news["items"] if n["region"] == "海外"]),
            "domestic": len([n for n in news["items"] if n["region"] == "国内"]),
        }
    }

def generate_html(content: Dict) -> str:
    """生成专业日报HTML"""
    date = content["date"]
    year, month, day = date.split("-")
    
    # 构建目录导航
    nav_html = "".join([
        f'<a href="#overview">📋 全文概览</a>',
        f'<a href="#heat">🔥 热度趋势</a>',
        f'<a href="#llm">🧠 大模型</a>',
        f'<a href="#coding">⌨️ AI Coding</a>',
        f'<a href="#app">📱 AI应用</a>',
        f'<a href="#industry">🏭 AI行业</a>',
        f'<a href="#data">📊 数据速览</a>',
    ])
    
    # 概览卡片
    overview_cards = "".join([
        f'''<div class="overview-card">
            <div class="overview-icon">{item["emoji"]}</div>
            <div class="overview-section">{item["section"]}</div>
            <div class="overview-summary">{item["summary"]}</div>
        </div>''' for item in content["overview"]
    ])
    
    # 热度趋势表格
    heat_rows = "".join([
        f'''<tr>
            <td>{row["rank"]}</td>
            <td><strong>{row["topic"]}</strong></td>
            <td>{"🔥" * int(row["heat"])}</td>
            <td>{row["days"]}天</td>
            <td>{row["trend"]}</td>
        </tr>''' for row in content["heat_trends"]
    ])
    
    # 生成板块内容
    def generate_section_items(items: List[Dict], region: str) -> str:
        if not items:
            return f'<p class="no-data">暂无{region}资讯</p>'
        return "".join([
            f'''<div class="news-item">
                <span class="tag-new">NEW</span>
                <a href="{item["url"]}" class="news-title" target="_blank">{item["title"]}</a>
                <div class="news-source">{item.get("source", "来源")}</div>
                <div class="news-content">
                    <p><strong>核心发现：</strong>根据相关报道，{item["title"][:50]}...</p>
                </div>
            </div>''' for item in items
        ])
    
    llm_html = f'''
    <div class="region-tabs">
        <div class="region-section">
            <div class="region-title">🌏 海外</div>
            {generate_section_items(content["llm"]["overseas"], "海外")}
        </div>
        <div class="region-section">
            <div class="region-title">🇨🇳 国内</div>
            {generate_section_items(content["llm"]["domestic"], "国内")}
        </div>
    </div>'''
    
    coding_html = f'''
    <div class="region-tabs">
        <div class="region-section">
            <div class="region-title">🌏 海外</div>
            {generate_section_items(content["coding"]["overseas"], "海外")}
        </div>
        <div class="region-section">
            <div class="region-title">🇨🇳 国内</div>
            {generate_section_items(content["coding"]["domestic"], "国内")}
        </div>
    </div>'''
    
    app_html = f'''
    <div class="region-tabs">
        <div class="region-section">
            <div class="region-title">🌏 海外</div>
            {generate_section_items(content["app"]["overseas"], "海外")}
        </div>
        <div class="region-section">
            <div class="region-title">🇨🇳 国内</div>
            {generate_section_items(content["app"]["domestic"], "国内")}
        </div>
    </div>'''
    
    industry_html = f'''
    <div class="region-tabs">
        <div class="region-section">
            <div class="region-title">🌏 海外</div>
            {generate_section_items(content["industry"]["overseas"], "海外")}
        </div>
        <div class="region-section">
            <div class="region-title">🇨🇳 国内</div>
            {generate_section_items(content["industry"]["domestic"], "国内")}
        </div>
    </div>'''
    
    # 数据表格
    data_rows = f'''
    <tr><td>总采集资讯</td><td><strong>{content["stats"]["total"]}</strong></td><td>海外+国内</td></tr>
    <tr><td>海外资讯</td><td><strong>{content["stats"]["overseas"]}</strong></td><td>OpenAI、Anthropic等</td></tr>
    <tr><td>国内资讯</td><td><strong>{content["stats"]["domestic"]}</strong></td><td>百度、阿里、月之暗面等</td></tr>
    '''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI洞察日报 · {date}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --primary: #10b981;
            --primary-light: #34d399;
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #1e293b;
            --text-secondary: #64748b;
            --border: #e2e8f0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            border-radius: 16px;
            padding: 40px;
            text-align: center;
            color: white;
            margin-bottom: 24px;
        }}
        .header-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            margin-bottom: 16px;
        }}
        .header h1 {{ font-size: 2rem; margin-bottom: 8px; }}
        .header-meta {{ opacity: 0.9; font-size: 0.95rem; }}
        
        /* Stats */
        .stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: var(--card);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .stat-number {{ font-size: 1.8rem; font-weight: bold; color: var(--primary); }}
        .stat-label {{ font-size: 0.85rem; color: var(--text-secondary); margin-top: 4px; }}
        
        /* Nav */
        .nav {{
            background: var(--card);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 24px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .nav a {{
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            color: var(--text-secondary);
            font-size: 0.9rem;
            transition: all 0.2s;
        }}
        .nav a:hover {{
            background: var(--primary);
            color: white;
        }}
        
        /* Section */
        .section {{
            background: var(--card);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .section-title {{
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--border);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        /* Overview */
        .overview-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }}
        .overview-card {{
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid var(--primary);
        }}
        .overview-icon {{ font-size: 1.5rem; margin-bottom: 8px; }}
        .overview-section {{ font-weight: 600; margin-bottom: 4px; }}
        .overview-summary {{ font-size: 0.9rem; color: var(--text-secondary); }}
        
        /* Table */
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}
        th {{
            background: var(--primary);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 500;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid var(--border);
        }}
        tr:hover td {{ background: #f8fafc; }}
        
        /* News Items */
        .region-tabs {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .region-title {{
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--text-secondary);
        }}
        .news-item {{
            background: #f8fafc;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        }}
        .tag-new {{
            display: inline-block;
            background: var(--primary);
            color: white;
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: 4px;
            margin-bottom: 8px;
        }}
        .news-title {{
            font-weight: 600;
            color: var(--text);
            text-decoration: none;
            display: block;
            margin-bottom: 6px;
        }}
        .news-title:hover {{ color: var(--primary); }}
        .news-source {{
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 8px;
        }}
        .news-content {{
            font-size: 0.9rem;
            color: var(--text-secondary);
        }}
        .no-data {{
            color: var(--text-secondary);
            font-style: italic;
            padding: 20px;
            text-align: center;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
        }}
        
        @media (max-width: 768px) {{
            .stats {{ grid-template-columns: 1fr; }}
            .overview-grid {{ grid-template-columns: 1fr; }}
            .region-tabs {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-badge">AI INSIGHT · DAILY REPORT</div>
            <h1>AI 洞察日报</h1>
            <div class="header-meta">📅 {date} | 🌐 海外 {content["stats"]["overseas"]} 条 · 国内 {content["stats"]["domestic"]} 条</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{content["stats"]["total"]}</div>
                <div class="stat-label">总资讯</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{content["stats"]["overseas"]}</div>
                <div class="stat-label">海外动态</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{content["stats"]["domestic"]}</div>
                <div class="stat-label">国内动态</div>
            </div>
        </div>
        
        <nav class="nav">{nav_html}</nav>
        
        <section class="section" id="overview">
            <h2 class="section-title">📋 全文概览</h2>
            <div class="overview-grid">{overview_cards}</div>
        </section>
        
        <section class="section" id="heat">
            <h2 class="section-title">🔥 热度趋势</h2>
            <table>
                <thead>
                    <tr><th>排名</th><th>话题</th><th>热度</th><th>天数</th><th>趋势</th></tr>
                </thead>
                <tbody>{heat_rows}</tbody>
            </table>
        </section>
        
        <section class="section" id="llm">
            <h2 class="section-title">🧠 大模型</h2>
            {llm_html}
        </section>
        
        <section class="section" id="coding">
            <h2 class="section-title">⌨️ AI Coding</h2>
            {coding_html}
        </section>
        
        <section class="section" id="app">
            <h2 class="section-title">📱 AI应用</h2>
            {app_html}
        </section>
        
        <section class="section" id="industry">
            <h2 class="section-title">🏭 AI行业</h2>
            {industry_html}
        </section>
        
        <section class="section" id="data">
            <h2 class="section-title">📊 数据速览</h2>
            <table>
                <thead>
                    <tr><th>指标</th><th>数值</th><th>说明</th></tr>
                </thead>
                <tbody>{data_rows}</tbody>
            </table>
        </section>
        
        <div class="footer">
            <p>🤖 萧炎的AI洞察 · 自动追踪 · 每日更新</p>
            <p style="font-size: 0.8rem; margin-top: 8px;">生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </div>
</body>
</html>'''
    
    return html

def main():
    """主函数"""
    print("=" * 50)
    print("🤖 AI洞察日报生成器")
    print("=" * 50)
    
    # 采集新闻
    news = collect_news()
    
    # 生成内容
    content = generate_sample_content(news)
    
    # 生成HTML
    html = generate_html(content)
    
    # 保存
    output_dir = Path(__file__).parent.parent / "site" / "reports" / "2026-04"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    date = news["date"]
    output_path = output_dir / f"{date}-v1.html"
    output_path.write_text(html, encoding='utf-8')
    
    print(f"\n✅ 日报已生成: {output_path}")
    print(f"📊 共 {content['stats']['total']} 条资讯")

if __name__ == "__main__":
    main()
