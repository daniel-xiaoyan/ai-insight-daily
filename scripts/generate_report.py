#!/usr/bin/env python3
"""
AI Insight Daily - 数据采集与日报生成脚本
自动搜索AI大模型相关资讯，生成结构化日报
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import re

# 数据源配置
SOURCES = {
    "overseas_companies": [
        "OpenAI", "Anthropic", "Google DeepMind", "Meta AI", "xAI", "Mistral AI", "Cohere", "AI21 Labs"
    ],
    "domestic_companies": [
        "字节跳动", "阿里通义", "百度文心", "腾讯混元", "智谱AI", "月之暗面", "MiniMax", "零一万物", "百川智能"
    ],
    "key_people": [
        "Sam Altman", "Dario Amodei", "Demis Hassabis", "Yann LeCun", "李开复", "王小川", "杨植麟", "闫俊杰"
    ],
    "topics": [
        "大模型", "LLM", "GPT", "Claude", "Gemini", "Llama", "AI Agent", "AI Coding", "多模态", "推理模型"
    ]
}

def get_today() -> str:
    """获取今日日期"""
    return datetime.now().strftime("%Y-%m-%d")

def get_current_week() -> str:
    """获取当前周数"""
    return datetime.now().strftime("%Y-W%W")

def load_raw_news(date: str) -> Dict:
    """加载采集的原始资讯数据"""
    raw_path = Path(__file__).parent.parent / "data" / "raw" / f"{date}_raw.json"
    if raw_path.exists():
        return json.loads(raw_path.read_text(encoding='utf-8'))
    return {"sources": {"overseas": [], "domestic": [], "general": []}}

def categorize_news(news_items: List[Dict]) -> Dict[str, List[Dict]]:
    """将新闻分类到不同板块"""
    categories = {
        "海外大模型": [],
        "国内大厂": [],
        "AI应用": [],
        "产品发布": [],
        "投融资": []
    }
    
    overseas_keywords = ["openai", "anthropic", "google", "meta", "claude", "gpt", "gemini", "llama", "xai", "mistral"]
    domestic_keywords = ["字节", "阿里", "百度", "腾讯", "智谱", "月之暗面", "minimax", "kimi", "通义", "文心", "混元"]
    product_keywords = ["发布", "推出", "上线", "更新", "新版", "release", "launch", "announce"]
    
    for item in news_items:
        title_lower = item.get("title", "").lower()
        
        # 判断国内/海外
        is_domestic = any(kw in title_lower or kw in item.get("query", "") for kw in domestic_keywords)
        is_overseas = any(kw in title_lower or kw in item.get("query", "") for kw in overseas_keywords)
        
        # 判断是否为产品发布
        is_product = any(kw in title_lower for kw in product_keywords)
        
        if is_domestic:
            categories["国内大厂"].append(item)
        elif is_overseas:
            categories["海外大模型"].append(item)
        
        if is_product:
            categories["产品发布"].append(item)
        
        # AI应用（默认分到应用类）
        if item not in categories["海外大模型"] and item not in categories["国内大厂"]:
            categories["AI应用"].append(item)
    
    return categories

def generate_daily_report_template(date: str) -> Dict:
    """生成日报模板，包含实际采集的数据"""
    raw_data = load_raw_news(date)
    
    # 合并所有资讯
    all_news = []
    for category, items in raw_data.get("sources", {}).items():
        all_news.extend(items)
    
    # 分类
    categorized = categorize_news(all_news)
    
    # 生成TOP新闻（最多5条）
    top_news = all_news[:5] if all_news else []
    
    # 生成摘要
    summary = f"今日共采集 {len(all_news)} 条AI行业资讯，"
    if categorized["海外大模型"]:
        summary += f"海外大模型动态 {len(categorized['海外大模型'])} 条，"
    if categorized["国内大厂"]:
        summary += f"国内大厂更新 {len(categorized['国内大厂'])} 条，"
    summary += "值得关注。"
    
    return {
        "date": date,
        "type": "daily",
        "title": f"{date} AI洞察日报",
        "summary": summary,
        "sections": {
            "海外大模型": categorized["海外大模型"][:5],
            "国内大厂": categorized["国内大厂"][:5],
            "AI应用": categorized["AI应用"][:5],
            "产品发布": categorized["产品发布"][:5],
            "投融资": categorized["投融资"][:3]
        },
        "top_news": top_news,
        "stats": {
            "total_news": len(all_news),
            "overseas": len(categorized["海外大模型"]),
            "domestic": len(categorized["国内大厂"])
        },
        "generated_at": datetime.now().isoformat()
    }

def generate_weekly_report_template(week: str, start_date: str, end_date: str) -> Dict:
    """生成周报模板"""
    return {
        "week": week,
        "type": "weekly",
        "title": f"AI洞察周报 · {week}（{start_date} - {end_date}）",
        "summary": "",
        "highlights": [],
        "trends": {
            "模型发布": [],
            "产品更新": [],
            "融资动态": [],
            "行业观点": []
        },
        "key_companies": {},
        "generated_at": datetime.now().isoformat()
    }

def create_report_html(report_data: Dict, output_path: Path):
    """生成日报HTML页面"""
    
    # 生成板块HTML
    sections_html = ""
    for section_name, items in report_data["sections"].items():
        if items:
            items_html = ""
            for item in items:
                title = item.get("title", "无标题")
                url = item.get("url", "#")
                snippet = item.get("snippet", "")
                source = item.get("source", "")
                
                items_html += f"""
                <div class="news-item">
                    <div class="news-title">
                        <a href="{url}" target="_blank">{title}</a>
                    </div>
                    <div class="news-summary">{snippet}</div>
                    <div class="news-meta">
                        <span class="tag">{source}</span>
                    </div>
                </div>
                """
            
            sections_html += f"""
            <div class="section">
                <h2>{section_name}</h2>
                {items_html}
            </div>
            """
    
    # 如果没有内容，显示提示
    if not sections_html:
        sections_html = """
        <div class="section">
            <p style="color: var(--text-secondary); text-align: center; padding: 40px;">
                今日暂未采集到资讯，请稍后再来查看~ 🕐
            </p>
        </div>
        """
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_data['title']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a25;
            --text-primary: #ffffff;
            --text-secondary: #a0a0b0;
            --accent: #6366f1;
            --accent-light: #818cf8;
            --border: #2a2a3a;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.8;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        header {{
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 40px;
        }}
        h1 {{
            font-size: 1.8rem;
            margin-bottom: 10px;
        }}
        .meta {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        .summary {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            color: var(--text-secondary);
        }}
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            color: var(--accent);
            text-decoration: none;
            margin-bottom: 20px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section h2 {{
            font-size: 1.3rem;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--accent);
            display: inline-block;
        }}
        .news-item {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .news-item:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
        }}
        .news-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .news-title a {{
            color: var(--text-primary);
            text-decoration: none;
        }}
        .news-title a:hover {{
            color: var(--accent-light);
        }}
        .news-summary {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin-bottom: 10px;
        }}
        .news-meta {{
            display: flex;
            gap: 15px;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        .tag {{
            background: var(--accent);
            color: white;
            padding: 2px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
        }}
        .stat-item {{
            text-align: center;
            padding: 15px 25px;
            background: var(--bg-card);
            border-radius: 10px;
        }}
        .stat-number {{
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--accent);
        }}
        .stat-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        footer {{
            text-align: center;
            padding: 30px 0;
            color: var(--text-secondary);
            border-top: 1px solid var(--border);
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">← 返回首页</a>
        <header>
            <h1>{report_data['title']}</h1>
            <div class="meta">生成于 {report_data['generated_at'][:10]} · 自动采集</div>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{report_data['stats']['total_news']}</div>
                    <div class="stat-label">总资讯</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{report_data['stats']['overseas']}</div>
                    <div class="stat-label">海外</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{report_data['stats']['domestic']}</div>
                    <div class="stat-label">国内</div>
                </div>
            </div>
        </header>
        
        <div class="summary">
            📋 {report_data['summary']}
        </div>
        
        <div class="content">
            {sections_html}
        </div>
        
        <footer>
            <p>🤖 萧炎的AI洞察 · 自动追踪 · 每日洞察</p>
            <p style="font-size: 0.8rem; margin-top: 10px;">数据采集于 {report_data['generated_at'][:19]}</p>
        </footer>
    </div>
</body>
</html>"""
    
    output_path.write_text(html_content, encoding='utf-8')
    print(f"✅ 已生成报告页面: {output_path}")

def update_index_html():
    """更新首页index.html，添加今日日报链接"""
    today = get_today()
    index_path = Path(__file__).parent.parent / "index.html"
    
    if index_path.exists():
        content = index_path.read_text(encoding='utf-8')
        
        # 检查是否已包含今日链接
        if today not in content:
            # 在报告列表前插入今日报告链接
            new_report_link = f'''
            <a href="reports/{today}.html" class="report-card">
                <div class="report-date">{today}</div>
                <div class="report-title">AI洞察日报</div>
                <div class="report-badge new">NEW</div>
            </a>'''
            
            # 简单地在第一个report-card前插入
            content = content.replace(
                '<div class="report-list">',
                f'<div class="report-list">\n{new_report_link}'
            )
            
            index_path.write_text(content, encoding='utf-8')
            print(f"✅ 首页已更新，添加 {today} 日报链接")

def main():
    """主函数"""
    today = get_today()
    data_dir = Path(__file__).parent.parent / "data"
    site_dir = Path(__file__).parent.parent / "site"
    reports_dir = site_dir / "reports"
    
    # 创建目录
    data_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    
    print("=" * 50)
    print("🤖 萧炎的AI洞察 - 日报生成器")
    print("=" * 50)
    
    # 检查是否有采集的数据
    raw_path = data_dir / "raw" / f"{today}_raw.json"
    if raw_path.exists():
        print(f"📊 发现采集数据: {raw_path}")
    else:
        print(f"⚠️ 未找到今日采集数据，将生成空模板")
    
    # 生成今日日报
    daily_report = generate_daily_report_template(today)
    daily_json_path = data_dir / f"{today}.json"
    daily_json_path.write_text(json.dumps(daily_report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✅ 日报数据已保存: {daily_json_path}")
    
    # 生成日报HTML
    daily_html_path = reports_dir / f"{today}.html"
    create_report_html(daily_report, daily_html_path)
    
    # 更新首页
    update_index_html()
    
    # 更新索引
    index_path = data_dir / "index.json"
    index_data = {"reports": [], "last_update": today}
    if index_path.exists():
        index_data = json.loads(index_path.read_text(encoding='utf-8'))
    
    # 检查是否已存在今日报告
    existing = [r for r in index_data['reports'] if r.get('date') == today]
    if not existing:
        index_data['reports'].insert(0, daily_report)
        index_data['last_update'] = today
        index_path.write_text(json.dumps(index_data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"✅ 索引已更新: {index_path}")
    
    print(f"\n📈 今日统计:")
    print(f"   - 总资讯: {daily_report['stats']['total_news']} 条")
    print(f"   - 海外: {daily_report['stats']['overseas']} 条")
    print(f"   - 国内: {daily_report['stats']['domestic']} 条")
    print(f"\n🌐 网站已生成，准备部署到GitHub Pages")

if __name__ == "__main__":
    main()
