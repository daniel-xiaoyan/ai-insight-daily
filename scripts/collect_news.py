#!/usr/bin/env python3
"""
AI资讯搜索采集脚本
使用多个搜索引擎获取AI大模型相关资讯
"""

import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import urllib.request
import urllib.parse

# 搜索查询模板
SEARCH_QUERIES = {
    "overseas": [
        "OpenAI GPT new model release 2025",
        "Anthropic Claude update announcement",
        "Google Gemini AI news today",
        "Meta AI Llama model release",
        "AI coding tool Cursor update",
        "Mistral AI new model",
        "xAI Grok announcement"
    ],
    "domestic": [
        "字节跳动大模型 发布",
        "阿里通义千问 更新",
        "百度文心一言 新功能",
        "腾讯混元大模型 发布",
        "月之暗面 Kimi 更新",
        "智谱AI GLM 新模型",
        "MiniMax 大模型 发布"
    ],
    "general": [
        "AI大模型 今日资讯",
        "人工智能 最新动态",
        "LLM large language model news today"
    ]
}

def search_duckduckgo(query: str, count: int = 5) -> List[Dict]:
    """
    使用DuckDuckGo搜索（无需API key，适合GitHub Actions）
    """
    results = []
    try:
        # 编码查询词
        encoded_query = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            
            # 解析搜索结果
            # DuckDuckGo HTML结果的简单解析
            result_blocks = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>', html)
            snippets = re.findall(r'<a class="result__snippet"[^>]*>([^<]+)</a>', html)
            
            for i, (link, title) in enumerate(result_blocks[:count]):
                snippet = snippets[i] if i < len(snippets) else ""
                # 清理HTML标签
                snippet = re.sub(r'<[^>]+>', '', snippet)
                results.append({
                    "title": re.sub(r'<[^>]+>', '', title),
                    "url": link,
                    "snippet": snippet,
                    "source": "DuckDuckGo",
                    "query": query
                })
                
    except Exception as e:
        print(f"  ⚠️ 搜索失败: {e}")
    
    return results

def search_bing(query: str, count: int = 5) -> List[Dict]:
    """
    使用Bing搜索（备选方案）
    """
    results = []
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.bing.com/search?q={encoded_query}&count={count}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            
            # 简单解析Bing结果
            titles = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(?!.*Next)(?!.*Previous)([^<]{10,200})</a>', html)
            
            for link, title in titles[:count]:
                if link.startswith('http') and not link.startswith('https://www.bing.com'):
                    clean_title = re.sub(r'<[^>]+>', '', title)
                    results.append({
                        "title": clean_title,
                        "url": link,
                        "snippet": "",
                        "source": "Bing",
                        "query": query
                    })
                    
    except Exception as e:
        print(f"  ⚠️ Bing搜索失败: {e}")
    
    return results

def collect_daily_news() -> Dict:
    """采集今日AI资讯"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    all_news = {
        "date": today,
        "collected_at": datetime.now().isoformat(),
        "sources": {
            "overseas": [],
            "domestic": [],
            "general": []
        }
    }
    
    print(f"🔍 开始采集 {today} 的AI资讯...")
    
    # 海外资讯
    print("\n📰 搜索海外AI资讯...")
    for query in SEARCH_QUERIES["overseas"]:
        print(f"  - 搜索: {query}")
        results = search_duckduckgo(query, count=3)
        if not results:
            results = search_bing(query, count=3)
        all_news["sources"]["overseas"].extend(results)
        time.sleep(1)  # 避免请求过快
    
    # 国内资讯
    print("\n🇨🇳 搜索国内AI资讯...")
    for query in SEARCH_QUERIES["domestic"]:
        print(f"  - 搜索: {query}")
        results = search_duckduckgo(query, count=3)
        if not results:
            results = search_bing(query, count=3)
        all_news["sources"]["domestic"].extend(results)
        time.sleep(1)
    
    # 综合资讯
    print("\n🌐 搜索综合AI资讯...")
    for query in SEARCH_QUERIES["general"]:
        print(f"  - 搜索: {query}")
        results = search_duckduckgo(query, count=3)
        if not results:
            results = search_bing(query, count=3)
        all_news["sources"]["general"].extend(results)
        time.sleep(1)
    
    # 去重（基于URL）
    seen_urls = set()
    for category in all_news["sources"]:
        unique_results = []
        for item in all_news["sources"][category]:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                unique_results.append(item)
        all_news["sources"][category] = unique_results
    
    # 保存原始数据
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    raw_path = data_dir / f"{today}_raw.json"
    raw_path.write_text(json.dumps(all_news, ensure_ascii=False, indent=2), encoding='utf-8')
    
    total_count = sum(len(v) for v in all_news["sources"].values())
    print(f"\n✅ 原始数据已保存: {raw_path}")
    print(f"📊 共采集 {total_count} 条资讯")
    
    return all_news

def generate_ai_summary_prompt(news_data: Dict) -> str:
    """
    生成用于AI分析总结的prompt
    """
    prompt = f"""请根据以下AI行业资讯，生成一份简洁的AI洞察日报摘要。

日期: {news_data['date']}

采集到的资讯:

"""
    
    for category, items in news_data["sources"].items():
        if items:
            prompt += f"\n【{category}】\n"
            for i, item in enumerate(items[:10], 1):  # 每类最多10条
                prompt += f"{i}. {item['title']}\n"
                if item['snippet']:
                    prompt += f"   摘要: {item['snippet'][:100]}...\n"
                prompt += f"   链接: {item['url']}\n\n"
    
    prompt += """
请生成以下内容:
1. 今日要点总结（3-5条，每条一句话）
2. 海外大模型动态（要点）
3. 国内大厂动态（要点）
4. 值得关注的产品/技术

格式为JSON:
{
  "summary": "整体总结",
  "highlights": ["要点1", "要点2", ...],
  "overseas": ["动态1", "动态2", ...],
  "domestic": ["动态1", "动态2", ...],
  "products": ["产品1", "产品2", ...]
}
"""
    
    return prompt

def main():
    """主函数"""
    print("=" * 50)
    print("🤖 萧炎的AI洞察 - 资讯采集器")
    print("=" * 50)
    
    news_data = collect_daily_news()
    
    # 生成AI分析的prompt
    prompt = generate_ai_summary_prompt(news_data)
    
    # 保存prompt供后续使用
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    prompt_path = data_dir / f"{news_data['date']}_prompt.txt"
    prompt_path.write_text(prompt, encoding='utf-8')
    
    print(f"\n📝 AI分析Prompt已保存: {prompt_path}")
    print("\n💡 下一步操作:")
    print("1. 查看 raw/ 目录下的原始数据")
    print("2. 使用AI助手分析prompt文件并生成日报内容")
    print("3. 运行 generate_report.py 生成日报页面")

if __name__ == "__main__":
    main()
