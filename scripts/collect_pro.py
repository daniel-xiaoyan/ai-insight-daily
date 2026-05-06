#!/usr/bin/env python3
"""
AI洞察日报生成器 v2.0 - 专业版
生成类似参考网站的高质量日报
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

# 搜索查询配置
SEARCH_CONFIG = {
    "overseas": [
        {"query": "OpenAI GPT model release announcement", "category": "大模型"},
        {"query": "Anthropic Claude update new features", "category": "大模型"},
        {"query": "Google Gemini AI news today", "category": "大模型"},
        {"query": "Meta AI Llama model release", "category": "大模型"},
        {"query": "xAI Grok announcement", "category": "大模型"},
        {"query": "Mistral AI new model", "category": "大模型"},
        {"query": "AI coding tool Cursor update", "category": "AI Coding"},
        {"query": "GitHub Copilot new features", "category": "AI Coding"},
        {"query": "AI Agent platform enterprise", "category": "AI应用"},
        {"query": "OpenAI Cloudflare Agent", "category": "AI应用"},
        {"query": "AI startup funding investment", "category": "AI行业"},
        {"query": "Sam Altman OpenAI news", "category": "AI行业"},
        {"query": "enterprise AI adoption report", "category": "企业转型"},
        {"query": "Google Workspace Gemini update", "category": "AI应用"},
    ],
    "domestic": [
        {"query": "字节跳动大模型 发布", "category": "大模型"},
        {"query": "阿里通义千问 更新", "category": "大模型"},
        {"query": "百度文心一言 新功能", "category": "大模型"},
        {"query": "腾讯混元大模型 发布", "category": "大模型"},
        {"query": "月之暗面 Kimi 更新", "category": "大模型"},
        {"query": "智谱AI GLM 新模型", "category": "大模型"},
        {"query": "MiniMax 大模型 发布", "category": "大模型"},
        {"query": "DeepSeek 更新 功能", "category": "大模型"},
        {"query": "AI编程工具 国内", "category": "AI Coding"},
        {"query": "AI应用 产品发布", "category": "AI应用"},
        {"query": "AI融资 投资 国内", "category": "AI行业"},
        {"query": "企业AI转型 案例", "category": "企业转型"},
    ]
}

def search_duckduckgo(query: str, count: int = 5) -> List[Dict]:
    """使用DuckDuckGo搜索"""
    results = []
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            
            # 解析搜索结果
            result_blocks = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>', html)
            
            for i, (link, title) in enumerate(result_blocks[:count]):
                title = title.replace('&#x27;', "'").replace('&quot;', '"').replace('&amp;', '&')
                results.append({
                    "title": title,
                    "url": link,
                    "snippet": "",
                    "source": "DuckDuckGo",
                    "query": query
                })
    except Exception as e:
        print(f"    ⚠️ 搜索失败: {e}")
    
    return results

def collect_all_news() -> Dict:
    """采集所有AI资讯"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    all_news = {
        "date": today,
        "collected_at": datetime.now().isoformat(),
        "sources": {
            "overseas": [],
            "domestic": []
        }
    }
    
    print(f"🔍 开始采集 {today} 的AI资讯...")
    
    # 海外资讯
    print("\n📰 搜索海外AI资讯...")
    for item in SEARCH_CONFIG["overseas"]:
        print(f"  - {item['category']}: {item['query']}")
        results = search_duckduckgo(item['query'], count=3)
        for r in results:
            r['category'] = item['category']
            r['region'] = '海外'
        all_news["sources"]["overseas"].extend(results)
        time.sleep(1)
    
    # 国内资讯
    print("\n🇨🇳 搜索国内AI资讯...")
    for item in SEARCH_CONFIG["domestic"]:
        print(f"  - {item['category']}: {item['query']}")
        results = search_duckduckgo(item['query'], count=3)
        for r in results:
            r['category'] = item['category']
            r['region'] = '国内'
        all_news["sources"]["domestic"].extend(results)
        time.sleep(1)
    
    # 去重
    seen_urls = set()
    for region in ["overseas", "domestic"]:
        unique = []
        for item in all_news["sources"][region]:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                unique.append(item)
        all_news["sources"][region] = unique
    
    total = len(all_news["sources"]["overseas"]) + len(all_news["sources"]["domestic"])
    print(f"\n✅ 共采集 {total} 条资讯")
    print(f"   - 海外: {len(all_news['sources']['overseas'])} 条")
    print(f"   - 国内: {len(all_news['sources']['domestic'])} 条")
    
    return all_news

def generate_ai_analysis_prompt(news_data: Dict) -> str:
    """生成AI分析的prompt"""
    prompt = f"""# AI洞察日报 - {news_data['date']}

## 📰 今日采集资讯 ({len(news_data['sources']['overseas']) + len(news_data['sources']['domestic'])} 条)

### 海外资讯
"""
    for item in news_data['sources']['overseas'][:15]:
        prompt += f"- [{item['category']}] {item['title']}\n  链接: {item['url']}\n"
    
    prompt += "\n### 国内资讯\n"
    for item in news_data['sources']['domestic'][:10]:
        prompt += f"- [{item['category']}] {item['title']}\n  链接: {item['url']}\n"
    
    prompt += """
---

## 📝 请基于以上资讯，生成以下日报内容：

### 1. 全文概览 (3-4条)
每条包含：emoji图标 + 板块名称 + 一句话核心发现

### 2. 热度趋势表格
| 排名 | 话题 | 热度 | 天数 | 趋势 | 核心信号 |

热度评分1-10，趋势用：🔥热门/📈上升/➡️稳定/📉下降

### 3. 大模型板块 (海外/国内)
每条动态包含：
- NEW标签
- 标题（带链接）
- 来源
- 核心发现（2-3句话）
- 影响判断（1句话）

### 4. AI Coding板块 (海外/国内)
同上格式

### 5. AI应用板块 (海外/国内)
同上格式

### 6. AI行业板块 (海外/国内)
同上格式

### 7. 企业转型板块 (海外/国内)
同上格式

### 8. 深度聚焦 (每个板块1个)
标题 + 3-4段深度分析 + 💡 TAKEAWAY + 🔮 规律洞察

### 9. 数据速览表格
| 指标 | 数值 | 变化/说明 |

### 10. 明日关注 (5条)
每条格式：🟢 话题名称 + 关注理由

### 11. 深度洞察 (3-4段)
以AI观察者的身份，写出对今日动态的系统性思考

---

请以JSON格式输出，结构如下：
{
  "overview": [...],
  "heat_trends": [...],
  "llm": {"overseas": [...], "domestic": [...]},
  "coding": {"overseas": [...], "domestic": [...]},
  "app": {"overseas": [...], "domestic": [...]},
  "industry": {"overseas": [...], "domestic": [...]},
  "enterprise": {"overseas": [...], "domestic": [...]},
  "deep_focus": [...],
  "data_overview": [...],
  "watch_tomorrow": [...],
  "insights": "..."
}
"""
    return prompt

def save_prompt_for_ai_analysis(news_data: Dict):
    """保存prompt供AI分析"""
    prompt = generate_ai_analysis_prompt(news_data)
    
    output_dir = Path(__file__).parent.parent / "data" / "ai_prompts"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = news_data['date']
    prompt_path = output_dir / f"{date_str}_analysis_prompt.md"
    prompt_path.write_text(prompt, encoding='utf-8')
    
    print(f"\n📝 AI分析Prompt已保存: {prompt_path}")
    print("请使用此prompt调用AI生成日报内容")
    
    return prompt_path

def main():
    """主函数"""
    print("=" * 60)
    print("🤖 萧炎的AI洞察 - 专业版日报生成器")
    print("=" * 60)
    
    # 采集资讯
    news_data = collect_all_news()
    
    # 保存原始数据
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    raw_path = data_dir / f"{news_data['date']}_raw.json"
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 原始数据已保存: {raw_path}")
    
    # 生成AI分析Prompt
    prompt_path = save_prompt_for_ai_analysis(news_data)
    
    print("\n" + "=" * 60)
    print("✅ 采集完成！下一步:")
    print(f"1. 查看Prompt: {prompt_path}")
    print("2. 使用AI生成日报内容")
    print("3. 保存结果为 data/ai_generated/{date}_content.json")
    print("4. 运行 generate_pro_report.py 生成HTML")
    print("=" * 60)

if __name__ == "__main__":
    main()
