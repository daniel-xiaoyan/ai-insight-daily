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
        "OpenAI", "Anthropic", "Google DeepMind", "Meta AI", 
        "xAI", "Mistral AI", "Cohere", "AI21 Labs"
    ],
    "domestic_companies": [
        "字节跳动", "阿里通义", "百度文心", "腾讯混元", 
        "智谱AI", "月之暗面", "MiniMax", "零一万物", "百川智能"
    ],
    "key_people": [
        "Sam Altman", "Dario Amodei", "Demis Hassabis", "Yann LeCun",
        "李开复", "王小川", "杨植麟", "闫俊杰"
    ],
    "topics": [
        "大模型", "LLM", "GPT", "Claude", "Gemini", "Llama",
        "AI Agent", "AI Coding", "多模态", "推理模型"
    ]
}

def get_today() -> str:
    """获取今日日期"""
    return datetime.now().strftime("%Y-%m-%d")

def get_current_week() -> str:
    """获取当前周数"""
    return datetime.now().strftime("%Y-W%W")

def generate_daily_report_template(date: str) -> Dict:
    """生成日报模板"""
    return {
        "date": date,
        "type": "daily",
        "title": f"{date} AI洞察日报",
        "summary": "",
        "sections": {
            "海外大模型": [],
            "国内大厂": [],
            "AI应用": [],
            "产品发布": [],
            "投融资": []
        },
        "top_news": [],
        "stats": {
            "total_news": 0,
            "overseas": 0,
            "domestic": 0
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
        }}
        .news-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .news-summary {{
            color: var(--text-secondary);
            font-size: 0.95rem;
        }}
        .news-meta {{
            display: flex;
            gap: 15px;
            margin-top: 10px;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        .tag {{
            background: var(--accent);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
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
            <div class="meta">生成于 {report_data['generated_at'][:10]}</div>
        </header>
        
        <div class="content">
            <!-- 动态内容区域 -->
            <p style="color: var(--text-secondary); text-align: center; padding: 40px;">
                日报内容将通过自动化脚本填充...
            </p>
        </div>
        
        <footer>
            <p>🤖 萧炎的AI洞察 · 自动追踪 · 每日洞察</p>
        </footer>
    </div>
</body>
</html>"""
    
    output_path.write_text(html_content, encoding='utf-8')
    print(f"✅ 已生成报告页面: {output_path}")

def main():
    """主函数"""
    today = get_today()
    data_dir = Path(__file__).parent.parent / "data"
    site_dir = Path(__file__).parent.parent / "site"
    reports_dir = site_dir / "reports"
    
    # 创建目录
    data_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    
    # 生成今日日报
    daily_report = generate_daily_report_template(today)
    daily_json_path = data_dir / f"{today}.json"
    daily_json_path.write_text(json.dumps(daily_report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✅ 日报数据已保存: {daily_json_path}")
    
    # 生成日报HTML
    daily_html_path = reports_dir / f"{today}.html"
    create_report_html(daily_report, daily_html_path)
    
    # 更新首页数据索引
    index_path = data_dir / "index.json"
    index_data = {"reports": [], "last_update": today}
    if index_path.exists():
        index_data = json.loads(index_path.read_text(encoding='utf-8'))
    
    if today not in [r.get('date') for r in index_data['reports']]:
        index_data['reports'].insert(0, daily_report)
        index_data['last_update'] = today
        index_path.write_text(json.dumps(index_data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"✅ 索引已更新: {index_path}")
    
    print("\n📊 下一步操作:")
    print("1. 运行搜索脚本采集资讯")
    print("2. 使用AI生成日报内容")
    print("3. 提交并部署到GitHub Pages")

if __name__ == "__main__":
    main()
