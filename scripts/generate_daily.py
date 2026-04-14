#!/usr/bin/env python3
"""
AI洞察日报生成器 - 根目录版
直接生成到仓库根目录，适配GitHub Pages默认设置
"""

import json
import os
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# 搜索配置
SEARCH_QUERIES = {
    "overseas_llm": ["OpenAI GPT", "Anthropic Claude", "Google Gemini", "Meta Llama", "xAI Grok"],
    "overseas_coding": ["Cursor AI", "GitHub Copilot", "Claude Code", "AI programming"],
    "overseas_app": ["AI Agent", "OpenAI Cloudflare", "Google Workspace Gemini"],
    "overseas_industry": ["AI startup funding", "Sam Altman", "Cognition AI"],
    "domestic_llm": ["百度文心一言", "阿里通义千问", "月之暗面 Kimi", "智谱AI GLM", "DeepSeek"],
    "domestic_coding": ["AI编程工具 国内", "代码生成 国内"],
    "domestic_app": ["AI应用 国内", "智能体平台 国内"],
    "domestic_industry": ["AI融资 国内", "AI行业 国内"],
}

def search_web(query: str, count: int = 3) -> List[Dict]:
    """搜索网页"""
    results = []
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
            matches = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)"([^>]*)>([^<]+)</a>', html)
            
            for link, _, title in matches[:count]:
                title = title.replace('&#x27;', "'").replace('&quot;', '"').replace('&amp;', '&')
                results.append({"title": title, "url": link})
    except Exception as e:
        print(f"    ⚠️ {e}")
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
                news["items"].append({**r, "region": region, "section": section})
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

def generate_html(news: Dict) -> str:
    """生成日报HTML"""
    date = news["date"]
    year, month, _ = date.split("-")
    
    # 分组
    llm_o = [n for n in news["items"] if n["section"] == "llm" and n["region"] == "海外"][:4]
    llm_d = [n for n in news["items"] if n["section"] == "llm" and n["region"] == "国内"][:4]
    coding_o = [n for n in news["items"] if n["section"] == "coding" and n["region"] == "海外"][:3]
    coding_d = [n for n in news["items"] if n["section"] == "coding" and n["region"] == "国内"][:3]
    app_o = [n for n in news["items"] if n["section"] == "app" and n["region"] == "海外"][:3]
    app_d = [n for n in news["items"] if n["section"] == "app" and n["region"] == "国内"][:3]
    ind_o = [n for n in news["items"] if n["section"] == "industry" and n["region"] == "海外"][:3]
    ind_d = [n for n in news["items"] if n["section"] == "industry" and n["region"] == "国内"][:3]
    
    total_o = len([n for n in news["items"] if n["region"] == "海外"])
    total_d = len([n for n in news["items"] if n["region"] == "国内"])
    
    def news_card(item: Dict) -> str:
        if not item:
            return ""
        return f'''
        <div class="news-item">
            <span class="tag-new">NEW</span>
            <a href="{item["url"]}" class="news-title" target="_blank">{item["title"]}</a>
            <div class="news-content">{item["title"][:40]}...</div>
        </div>'''
    
    def section_items(items: List[Dict]) -> str:
        if not items:
            return '<p class="no-data">暂无数据</p>'
        return "".join([news_card(i) for i in items])
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI洞察日报 · {date}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ --primary: #10b981; --bg: #f8fafc; --card: #fff; --text: #1e293b; --text2: #64748b; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, var(--primary) 0%, #34d399 100%); border-radius: 16px; padding: 40px; text-align: center; color: white; margin-bottom: 24px; }}
        .header h1 {{ font-size: 2rem; margin-bottom: 8px; }}
        .header-meta {{ opacity: 0.9; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }}
        .stat-card {{ background: var(--card); border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 1.8rem; font-weight: bold; color: var(--primary); }}
        .stat-label {{ font-size: 0.85rem; color: var(--text2); }}
        .section {{ background: var(--card); border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .section-title {{ font-size: 1.3rem; font-weight: 600; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px solid #e2e8f0; display: flex; align-items: center; gap: 8px; }}
        .region-tabs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .region-title {{ font-weight: 600; margin-bottom: 12px; color: var(--text2); }}
        .news-item {{ background: #f8fafc; border-radius: 8px; padding: 16px; margin-bottom: 12px; }}
        .tag-new {{ display: inline-block; background: var(--primary); color: white; font-size: 0.7rem; padding: 2px 8px; border-radius: 4px; margin-bottom: 8px; }}
        .news-title {{ font-weight: 600; color: var(--text); text-decoration: none; display: block; margin-bottom: 6px; }}
        .news-title:hover {{ color: var(--primary); }}
        .news-content {{ font-size: 0.9rem; color: var(--text2); }}
        .no-data {{ color: var(--text2); font-style: italic; padding: 20px; text-align: center; }}
        .footer {{ text-align: center; padding: 40px 20px; color: var(--text2); }}
        @media (max-width: 768px) {{ .stats {{ grid-template-columns: 1fr; }} .region-tabs {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI 洞察日报</h1>
            <div class="header-meta">📅 {date} | 🌐 海外 {total_o} 条 · 国内 {total_d} 条</div>
        </div>
        
        <div class="stats">
            <div class="stat-card"><div class="stat-number">{len(news["items"])}</div><div class="stat-label">总资讯</div></div>
            <div class="stat-card"><div class="stat-number">{total_o}</div><div class="stat-label">海外动态</div></div>
            <div class="stat-card"><div class="stat-number">{total_d}</div><div class="stat-label">国内动态</div></div>
        </div>
        
        <div class="section">
            <h2 class="section-title">🧠 大模型</h2>
            <div class="region-tabs">
                <div><div class="region-title">🌏 海外</div>{section_items(llm_o)}</div>
                <div><div class="region-title">🇨🇳 国内</div>{section_items(llm_d)}</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">⌨️ AI Coding</h2>
            <div class="region-tabs">
                <div><div class="region-title">🌏 海外</div>{section_items(coding_o)}</div>
                <div><div class="region-title">🇨🇳 国内</div>{section_items(coding_d)}</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📱 AI应用</h2>
            <div class="region-tabs">
                <div><div class="region-title">🌏 海外</div>{section_items(app_o)}</div>
                <div><div class="region-title">🇨🇳 国内</div>{section_items(app_d)}</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">🏭 AI行业</h2>
            <div class="region-tabs">
                <div><div class="region-title">🌏 海外</div>{section_items(ind_o)}</div>
                <div><div class="region-title">🇨🇳 国内</div>{section_items(ind_d)}</div>
            </div>
        </div>
        
        <div class="footer">
            <p>🤖 萧炎的AI洞察 · 每日自动更新</p>
            <p style="font-size: 0.8rem; margin-top: 8px;">生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </div>
</body>
</html>'''
    return html

def main():
    """主函数 - 生成日报到根目录"""
    print("=" * 50)
    print("🤖 AI洞察日报生成器")
    print("=" * 50)
    
    # 采集新闻
    news = collect_news()
    
    # 生成HTML
    html = generate_html(news)
    
    # 保存到根目录的 reports/2026-04/ 文件夹
    base_dir = Path(__file__).parent.parent
    report_dir = base_dir / "reports" / news["date"][:7]  # reports/2026-04/
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"{news['date']}.html"
    report_path.write_text(html, encoding='utf-8')
    
    print(f"\n✅ 日报已生成: {report_path}")
    print(f"📊 共 {len(news['items'])} 条资讯")
    
    # 同时生成最新日报的副本到根目录
    latest_path = base_dir / "daily-report.html"
    latest_path.write_text(html, encoding='utf-8')
    print(f"✅ 最新日报: {latest_path}")

if __name__ == "__main__":
    main()
