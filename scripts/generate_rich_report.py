#!/usr/bin/env python3
"""
AI洞察日报 - 丰富版生成器
生成类似示例的美观日报HTML
"""

import json
from datetime import datetime
from pathlib import Path

def generate_rich_report(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 加载分析数据
    analysis_path = Path(__file__).parent.parent / "data" / "analysis" / f"{date_str}_analysis.json"
    raw_path = Path(__file__).parent.parent / "data" / "raw" / f"{date_str}_raw.json"
    
    if not raw_path.exists():
        print(f"未找到 {date_str} 的数据")
        return
    
    with open(raw_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # AI整理的重点内容（基于采集的资讯手动整理）
    highlights = [
        {
            "title": "百度文心5.0发布",
            "summary": "文心一言App升级至5.0版本并更名为「文心」，新增魔法漫画、全形式AI搜索、创意修图、视频生成等功能，覆盖搜索、创作、视频通话等多场景。",
            "url": "https://www.ithome.com/0/894/189.htm",
            "tag": "产品升级"
        },
        {
            "title": "月之暗面Kimi K2更新",
            "summary": "Kimi K2模型上下文长度扩展至256K，API输出速度提升至60-100 Token/s，Agentic Coding能力在真实编程任务中表现进一步提升。",
            "url": "https://www.ithome.com/0/880/609.htm",
            "tag": "模型升级"
        },
        {
            "title": "智谱GLM-5.1发布",
            "summary": "智谱最新旗舰模型GLM-5.1代码能力大幅增强，长程任务显著提升，可单次持续自主工作长达8小时，综合能力对齐Claude Opus 4.6。",
            "url": "https://docs.bigmodel.cn/cn/guide/models/text/glm-5.1",
            "tag": "新模型"
        },
        {
            "title": "MiniMax 2.7开源",
            "summary": "稀宇科技开源最新大模型MiniMax 2.7/M2.7，号称全球首个带自我进化能力的大模型，仅10B激活参数（总参230B）在Artificial Analysis榜单表现优异。",
            "url": "https://platform.minimaxi.com/docs/release-notes/models",
            "tag": "开源模型"
        },
        {
            "title": "Google NotebookLM整合Gemini",
            "summary": "Google将NotebookLM功能整合进Gemini notebooks，20亿Gmail用户将陆续获得AI升级体验。",
            "url": "https://www.digitaltrends.com/computing/notebooklm-arrives-inside-gemini-notebooks-starting-today/",
            "tag": "产品整合"
        }
    ]
    
    # AI Coding 动态
    coding_news = [
        {
            "title": "智谱GLM-5.1：工程级代码能力",
            "summary": "GLM-5.1在真实开发场景中表现优异，能够完成从规划、执行到迭代优化的完整闭环，交付工程级成果。",
            "url": "https://docs.bigmodel.cn/cn/guide/models/text/glm-5.1",
            "source": "智谱AI"
        },
        {
            "title": "Kimi K2：Agentic Coding能力提升",
            "summary": "月之暗面优化Kimi K2在真实编程任务中的Agentic Coding能力，支持更复杂的代码理解和生成任务。",
            "url": "https://www.ithome.com/0/880/609.htm",
            "source": "月之暗面"
        }
    ]
    
    # 大模型发布
    model_news = [
        {
            "title": "百度文心5.0",
            "summary": "品牌回归「文心」，新增魔法漫画、全形式AI搜索、视频生成、创意修图等多模态功能。",
            "url": "https://www.ithome.com/0/894/189.htm",
            "company": "百度"
        },
        {
            "title": "智谱GLM-5.1",
            "summary": "745B大模型，200K上下文，代码能力对齐Claude Opus 4.6，支持8小时长程自主执行。",
            "url": "https://docs.bigmodel.cn/cn/guide/models/text/glm-5.1",
            "company": "智谱AI"
        },
        {
            "title": "MiniMax-M2.7",
            "summary": "10B激活参数（总参230B），全球首个带自我进化能力，正式开源。",
            "url": "https://platform.minimaxi.com/docs/release-notes/models",
            "company": "MiniMax"
        },
        {
            "title": "Mistral 3",
            "summary": "Mistral最新一代模型发布，持续挑战OpenAI和Google的市场地位。",
            "url": "https://mistral.ai/news/mistral-3",
            "company": "Mistral AI"
        },
        {
            "title": "Grok 5（预览）",
            "summary": "xAI Grok 5预计6T参数规模，向AGI目标迈进，具体发布时间待定。",
            "url": "https://www.nxcode.io/resources/news/grok-5-release-date-6t-parameters-agi-xai-complete-guide-2026",
            "company": "xAI"
        }
    ]
    
    # AI产品与应用
    product_news = [
        {
            "title": "百度「文心」App全面升级",
            "summary": "新增魔法漫画生成、全形式AI搜索、创意修图、视频生成、视频通话等功能，覆盖更多使用场景。",
            "url": "https://www.ithome.com/0/894/189.htm"
        },
        {
            "title": "NotebookLM入驻Gemini",
            "summary": "Google将NotebookLM功能整合进Gemini notebooks，提升笔记和知识管理能力。",
            "url": "https://www.digitaltrends.com/computing/notebooklm-arrives-inside-gemini-notebooks-starting-today/"
        },
        {
            "title": "Gmail 20亿用户AI升级",
            "summary": "Google为Gmail带来AI升级，所有用户将陆续获得新功能体验。",
            "url": "https://www.forbes.com/sites/zakdoffman/2026/04/10/googles-gmail-upgrade-decision-2-billion-users-must-act-now/"
        }
    ]
    
    # 汇总表格数据
    summary_table = [
        {"company": "百度", "type": "产品升级", "highlight": "文心5.0发布，新增魔法漫画、AI搜索", "importance": "⭐⭐⭐⭐"},
        {"company": "月之暗面", "type": "模型更新", "highlight": "Kimi K2上下文扩展至256K", "importance": "⭐⭐⭐⭐"},
        {"company": "智谱AI", "type": "新模型", "highlight": "GLM-5.1发布，8小时长程自主执行", "importance": "⭐⭐⭐⭐⭐"},
        {"company": "MiniMax", "type": "开源", "highlight": "M2.7开源，首个自我进化大模型", "importance": "⭐⭐⭐⭐"},
        {"company": "Mistral", "type": "新模型", "highlight": "Mistral 3发布", "importance": "⭐⭐⭐"},
        {"company": "Google", "type": "产品整合", "highlight": "NotebookLM整合Gemini", "importance": "⭐⭐⭐"},
        {"company": "xAI", "type": "预告", "highlight": "Grok 5参数规模将达6T", "importance": "⭐⭐⭐"},
    ]
    
    # 生成HTML
    html = generate_html(date_str, highlights, coding_news, model_news, product_news, summary_table, raw_data)
    
    # 保存
    reports_dir = Path(__file__).parent.parent / "site" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = reports_dir / f"{date_str}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 丰富版日报已生成: {output_path}")
    return output_path

def generate_html(date_str, highlights, coding_news, model_news, product_news, summary_table, raw_data):
    """生成美观的日报HTML"""
    
    # 今日要点卡片
    highlights_html = ""
    for h in highlights:
        highlights_html += f'''
        <div class="highlight-card" onclick="window.open('{h['url']}', '_blank')">
            <div class="highlight-tag">{h['tag']}</div>
            <h3>{h['title']}</h3>
            <p>{h['summary']}</p>
        </div>
        '''
    
    # AI Coding 动态
    coding_html = ""
    for item in coding_news:
        coding_html += f'''
        <div class="news-card">
            <div class="news-header">
                <h4>{item['title']}</h4>
                <span class="news-source">{item['source']}</span>
            </div>
            <p class="news-desc">{item['summary']}</p>
        </div>
        '''
    
    # 大模型发布
    model_html = ""
    for item in model_news:
        model_html += f'''
        <div class="news-card">
            <div class="news-header">
                <h4>{item['title']}</h4>
                <span class="company-badge">{item['company']}</span>
            </div>
            <p class="news-desc">{item['summary']}</p>
        </div>
        '''
    
    # 产品与应用
    product_html = ""
    for item in product_news:
        product_html += f'''
        <div class="news-card">
            <h4>{item['title']}</h4>
            <p class="news-desc">{item['summary']}</p>
        </div>
        '''
    
    # 汇总表格
    table_rows = ""
    for row in summary_table:
        table_rows += f'''
        <tr>
            <td><strong>{row['company']}</strong></td>
            <td><span class="type-tag">{row['type']}</span></td>
            <td>{row['highlight']}</td>
            <td class="center">{row['importance']}</td>
        </tr>
        '''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{date_str} AI洞察日报</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --accent-pink: #ec4899;
            --accent-cyan: #06b6d4;
            --accent-orange: #f97316;
            --bg-dark: #0f0f1a;
            --bg-card: #1a1a2e;
            --bg-card-hover: #252545;
            --text-primary: #ffffff;
            --text-secondary: #a0a0b8;
            --border: #2a2a45;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* 头部Banner */
        .header-banner {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
        }}
        
        .header-banner::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 300px;
            height: 300px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
        }}
        
        .header-content {{
            position: relative;
            z-index: 1;
        }}
        
        .header-title {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .header-date {{
            font-size: 1rem;
            opacity: 0.9;
            margin-bottom: 16px;
        }}
        
        .header-summary {{
            background: rgba(255,255,255,0.15);
            border-radius: 12px;
            padding: 16px 20px;
            font-size: 0.95rem;
            line-height: 1.8;
        }}
        
        /* 板块标题 */
        .section {{
            margin-bottom: 32px;
        }}
        
        .section-title {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--border);
        }}
        
        .section-icon {{
            font-size: 1.4rem;
        }}
        
        /* 今日要点 */
        .highlights {{
            display: grid;
            gap: 16px;
        }}
        
        .highlight-card {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .highlight-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(238, 90, 111, 0.3);
        }}
        
        .highlight-card:nth-child(2) {{
            background: linear-gradient(135deg, var(--accent-cyan) 0%, #0891b2 100%);
        }}
        
        .highlight-card:nth-child(2):hover {{
            box-shadow: 0 10px 30px rgba(6, 182, 212, 0.3);
        }}
        
        .highlight-card:nth-child(3) {{
            background: linear-gradient(135deg, var(--accent-orange) 0%, #ea580c 100%);
        }}
        
        .highlight-card:nth-child(3):hover {{
            box-shadow: 0 10px 30px rgba(249, 115, 22, 0.3);
        }}
        
        .highlight-tag {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            margin-bottom: 10px;
        }}
        
        .highlight-card h3 {{
            font-size: 1.1rem;
            margin-bottom: 8px;
        }}
        
        .highlight-card p {{
            font-size: 0.9rem;
            opacity: 0.95;
            line-height: 1.6;
        }}
        
        /* 新闻卡片 */
        .news-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 12px;
            transition: all 0.2s;
        }}
        
        .news-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--primary);
        }}
        
        .news-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 10px;
        }}
        
        .news-card h4 {{
            font-size: 1rem;
            color: var(--text-primary);
            font-weight: 600;
        }}
        
        .news-source {{
            font-size: 0.75rem;
            color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.15);
            padding: 4px 10px;
            border-radius: 20px;
            white-space: nowrap;
        }}
        
        .company-badge {{
            font-size: 0.75rem;
            color: var(--accent-pink);
            background: rgba(236, 72, 153, 0.15);
            padding: 4px 10px;
            border-radius: 20px;
            white-space: nowrap;
        }}
        
        .news-desc {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.7;
        }}
        
        /* 汇总表格 */
        .summary-table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-card);
            border-radius: 12px;
            overflow: hidden;
        }}
        
        .summary-table th {{
            background: var(--primary);
            color: white;
            padding: 14px 16px;
            text-align: left;
            font-weight: 500;
            font-size: 0.85rem;
        }}
        
        .summary-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid var(--border);
            font-size: 0.9rem;
        }}
        
        .summary-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .summary-table tr:hover td {{
            background: rgba(99, 102, 241, 0.1);
        }}
        
        .type-tag {{
            display: inline-block;
            background: var(--primary);
            color: white;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
        }}
        
        .center {{
            text-align: center;
        }}
        
        /* 页脚 */
        .footer {{
            text-align: center;
            padding: 30px;
            color: var(--text-secondary);
            border-top: 1px solid var(--border);
            margin-top: 40px;
        }}
        
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: var(--primary);
            text-decoration: none;
            margin-bottom: 20px;
            font-size: 0.9rem;
        }}
        
        .back-link:hover {{
            color: var(--accent-cyan);
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">← 返回首页</a>
        
        <!-- 头部Banner -->
        <div class="header-banner">
            <div class="header-content">
                <h1 class="header-title">🤖 AI 洞察日报</h1>
                <div class="header-date">{date_str} | 自动采集 · AI整理</div>
                <div class="header-summary">
                    今日共采集 {len(raw_data['sources']['overseas']) + len(raw_data['sources']['domestic'])} 条AI行业资讯，
                    国内大厂密集更新：百度文心5.0、月之暗面Kimi K2、智谱GLM-5.1、MiniMax 2.7开源等重大动态值得关注。
                </div>
            </div>
        </div>
        
        <!-- 今日要点 -->
        <div class="section">
            <h2 class="section-title"><span class="section-icon">🎯</span> 今日要点</h2>
            <div class="highlights">
                {highlights_html}
            </div>
        </div>
        
        <!-- AI Coding 动态 -->
        <div class="section">
            <h2 class="section-title"><span class="section-icon">💻</span> AI Coding 动态</h2>
            {coding_html}
        </div>
        
        <!-- 大模型发布 -->
        <div class="section">
            <h2 class="section-title"><span class="section-icon">🚀</span> 大模型发布/更新</h2>
            {model_html}
        </div>
        
        <!-- AI产品与应用 -->
        <div class="section">
            <h2 class="section-title"><span class="section-icon">✨</span> AI 产品与应用</h2>
            {product_html}
        </div>
        
        <!-- 汇总表格 -->
        <div class="section">
            <h2 class="section-title"><span class="section-icon">📊</span> 今日动态汇总</h2>
            <table class="summary-table">
                <thead>
                    <tr>
                        <th>公司/产品</th>
                        <th>动态类型</th>
                        <th>要点简述</th>
                        <th class="center">重要度</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>🤖 萧炎的AI洞察 · 自动追踪 · 每日洞察</p>
            <p style="font-size: 0.8rem; margin-top: 8px; opacity: 0.7;">生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </div>
</body>
</html>'''
    
    return html

if __name__ == "__main__":
    import sys
    date = sys.argv[1] if len(sys.argv) > 1 else None
    generate_rich_report(date)
