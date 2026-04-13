#!/usr/bin/env python3
"""
AI日报内容分析器
分析采集到的资讯，生成结构化内容供AI整理
"""

import json
from datetime import datetime
from pathlib import Path

def analyze_news(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 加载原始数据
    raw_path = Path(__file__).parent.parent / "data" / "raw" / f"{date_str}_raw.json"
    if not raw_path.exists():
        print(f"未找到 {date_str} 的数据")
        return
    
    with open(raw_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 整理所有资讯
    all_news = []
    for category, items in data['sources'].items():
        for item in items:
            item['category'] = category
            all_news.append(item)
    
    # 按主题分类
    themes = {
        "AI Coding": ["coding", "code", "cursor", "claude", "programming", "ide", "github"],
        "大模型发布": ["model", "gpt", "llama", "gemini", "claude", "glm", "kimi", "发布", "开源"],
        "AI Agent": ["agent", "autonomous", "mcp", "computer-use"],
        "产品更新": ["update", "upgrade", "version", "app", "功能", "升级"],
        "多模态": ["image", "video", "audio", "multimodal", "vision", "图片", "视频"],
        "搜索/知识": ["search", "knowledge", "notebook", "rag", "搜索"],
        "硬件/芯片": ["gpu", "chip", "hardware", "nvidia", "芯片"],
    }
    
    classified = {k: [] for k in themes.keys()}
    classified["其他"] = []
    
    for item in all_news:
        title_lower = item.get('title', '').lower()
        query_lower = item.get('query', '').lower()
        text = title_lower + ' ' + query_lower
        
        matched = False
        for theme, keywords in themes.items():
            if any(kw in text for kw in keywords):
                classified[theme].append(item)
                matched = True
                break
        
        if not matched:
            classified["其他"].append(item)
    
    # 识别重点公司动态
    companies = {
        "OpenAI": [],
        "Anthropic/Claude": [],
        "Google/Gemini": [],
        "Meta/Llama": [],
        "xAI/Grok": [],
        "Mistral": [],
        "百度/文心": [],
        "阿里/通义": [],
        "字节": [],
        "月之暗面/Kimi": [],
        "智谱/GLM": [],
        "MiniMax": [],
    }
    
    company_keywords = {
        "OpenAI": ["openai", "gpt", "chatgpt"],
        "Anthropic/Claude": ["anthropic", "claude"],
        "Google/Gemini": ["google", "gemini", "gmail"],
        "Meta/Llama": ["meta", "llama"],
        "xAI/Grok": ["xai", "grok", "musk"],
        "Mistral": ["mistral"],
        "百度/文心": ["baidu", "百度", "文心", "文小言"],
        "阿里/通义": ["alibaba", "阿里", "通义", "qwen"],
        "字节": ["bytedance", "字节", "doubao", "豆包"],
        "月之暗面/Kimi": ["moonshot", "月之暗面", "kimi"],
        "智谱/GLM": ["zhipu", "智谱", "glm"],
        "MiniMax": ["minimax", "稀宇"],
    }
    
    for item in all_news:
        title_lower = item.get('title', '').lower()
        query_lower = item.get('query', '').lower()
        text = title_lower + ' ' + query_lower
        
        for company, keywords in company_keywords.items():
            if any(kw in text for kw in keywords):
                companies[company].append(item)
    
    # 生成分析报告
    report = {
        "date": date_str,
        "total_news": len(all_news),
        "by_theme": {k: len(v) for k, v in classified.items() if v},
        "by_company": {k: len(v) for k, v in companies.items() if v},
        "highlights": []
    }
    
    # 提取可能的重点（标题较长的、包含版本号的等）
    for item in all_news:
        title = item.get('title', '')
        # 包含数字版本号的可能是重要发布
        if any(x in title for x in ['5.0', '4.0', '3.0', '2.0', 'K2', 'K3', 'V4', 'V5', '发布', '开源', '上线']):
            report['highlights'].append({
                'title': title,
                'url': item.get('url', ''),
                'company': item.get('query', '')
            })
    
    # 生成AI分析Prompt
    prompt = f"""# AI洞察日报 - {date_str}

## 📊 今日采集概况
- 总资讯数: {report['total_news']} 条
- 海外资讯: {len(data['sources']['overseas'])} 条
- 国内资讯: {len(data['sources']['domestic'])} 条

## 🏢 重点公司动态统计
"""
    for company, count in sorted(report['by_company'].items(), key=lambda x: -x[1]):
        if count > 0:
            prompt += f"- {company}: {count} 条\n"
    
    prompt += f"\n## 📁 主题分类\n"
    for theme, count in sorted(report['by_theme'].items(), key=lambda x: -x[1]):
        if count > 0:
            prompt += f"- {theme}: {count} 条\n"
    
    prompt += f"\n## 🔥 可能的重点资讯\n"
    for h in report['highlights'][:10]:
        prompt += f"- {h['title']}\n"
    
    prompt += f"\n## 📰 所有原始资讯\n\n"
    
    # 按分类列出详细资讯
    for category in ['overseas', 'domestic']:
        cat_name = '海外' if category == 'overseas' else '国内'
        prompt += f"### {cat_name}资讯 ({len(data['sources'][category])} 条)\n\n"
        for item in data['sources'][category]:
            title = item.get('title', '无标题')
            url = item.get('url', '')
            query = item.get('query', '')
            prompt += f"**{title}**\n"
            prompt += f"- 搜索关键词: {query}\n"
            prompt += f"- 链接: {url}\n\n"
    
    prompt += """
---

## 📝 请基于以上资讯，生成以下日报内容：

### 1️⃣ 今日要点（3-5条）
提炼今日最重要的AI行业动态，每条一句话，突出影响力和重要性。

### 2️⃣ AI Coding 动态
整理与AI编程相关的资讯，包括：
- Cursor、Claude Code等工具更新
- AI辅助编程能力提升
- 新的AI编程产品/功能

### 3️⃣ 大模型发布/更新
- 新模型发布（含版本号、主要特性）
- 现有模型重要更新
- 开源模型动态

### 4️⃣ AI产品与应用
- 面向消费者的AI产品更新
- 企业级AI应用
- 多模态能力（图文视频）

### 5️⃣ 融资与商业
- 公司融资动态
- 商业合作/收购
- 市场份额/营收数据

### 6️⃣ 汇总表格
| 公司/产品 | 动态类型 | 要点简述 | 重要度 |
|---------|---------|---------|-------|

请用简洁专业的语言输出，适合AI从业者快速阅读了解行业动态。
"""
    
    # 保存分析报告
    output_dir = Path(__file__).parent.parent / "data" / "analysis"
    output_dir.mkdir(exist_ok=True)
    
    analysis_path = output_dir / f"{date_str}_analysis.json"
    with open(analysis_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    prompt_path = output_dir / f"{date_str}_ai_prompt.md"
    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"✅ 分析报告已保存: {analysis_path}")
    print(f"✅ AI分析Prompt已保存: {prompt_path}")
    print(f"\n📊 统计:")
    print(f"  - 总资讯: {report['total_news']} 条")
    print(f"  - 主题分类: {len([k for k,v in classified.items() if v])} 个")
    print(f"  - 涉及公司: {len([k for k,v in companies.items() if v])} 家")
    print(f"  - 重点候选: {len(report['highlights'])} 条")
    
    return report, prompt

if __name__ == "__main__":
    import sys
    date = sys.argv[1] if len(sys.argv) > 1 else None
    analyze_news(date)
