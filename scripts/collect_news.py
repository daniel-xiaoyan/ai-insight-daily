#!/usr/bin/env python3
"""
AI资讯搜索采集脚本（GitHub Actions优化版）
使用多个搜索引擎获取AI大模型相关资讯
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

# 预设新闻源（当搜索失败时作为备选）
PRESET_NEWS = [
    {
        "title": "OpenAI GPT-5 Development Updates",
        "url": "https://openai.com/blog",
        "snippet": "OpenAI continues to advance their GPT model series with new capabilities",
        "source": "OpenAI Blog",
        "category": "overseas"
    },
    {
        "title": "Anthropic Claude Latest Features",
        "url": "https://www.anthropic.com/news",
        "snippet": "Claude AI assistant updates and new capabilities",
        "source": "Anthropic",
        "category": "overseas"
    },
    {
        "title": "Google Gemini AI News",
        "url": "https://blog.google/technology/ai/",
        "snippet": "Latest updates on Gemini models and AI products",
        "source": "Google Blog",
        "category": "overseas"
    },
    {
        "title": "百度文心大模型动态",
        "url": "https://yiyan.baidu.com/",
        "snippet": "百度文心一言最新功能更新和模型发布",
        "source": "百度",
        "category": "domestic"
    },
    {
        "title": "月之暗面 Kimi 更新日志",
        "url": "https://www.moonshot.cn/",
        "snippet": "Kimi大模型最新能力和功能更新",
        "source": "月之暗面",
        "category": "domestic"
    },
    {
        "title": "智谱AI GLM模型发布",
        "url": "https://www.zhipuai.cn/",
        "snippet": "智谱GLM系列大模型最新动态",
        "source": "智谱AI",
        "category": "domestic"
    },
    {
        "title": "阿里通义千问更新",
        "url": "https://tongyi.aliyun.com/",
        "snippet": "阿里通义千问大模型最新功能",
        "source": "阿里云",
        "category": "domestic"
    }
]

def is_github_actions() -> bool:
    """检查是否在GitHub Actions环境中运行"""
    return os.environ.get('GITHUB_ACTIONS') == 'true'

def search_with_requests(url: str, headers: dict, timeout: int = 15) -> str:
    """使用urllib进行搜索请求"""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"    ⚠️ 请求失败: {e}")
        return ""

def search_duckduckgo(query: str, count: int = 5) -> List[Dict]:
    """使用DuckDuckGo搜索"""
    results = []
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        html = search_with_requests(url, headers)
        if not html:
            return results
        
        # 解析搜索结果
        result_blocks = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>', html)
        
        for i, (link, title) in enumerate(result_blocks[:count]):
            # 清理HTML实体
            title = title.replace('&#x27;', "'").replace('&quot;', '"').replace('&amp;', '&')
            
            results.append({
                "title": title,
                "url": link,
                "snippet": "",
                "source": "DuckDuckGo",
                "query": query
            })
            
    except Exception as e:
        print(f"    ⚠️ DuckDuckGo搜索失败: {e}")
    
    return results

def search_bing(query: str, count: int = 5) -> List[Dict]:
    """使用Bing搜索"""
    results = []
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.bing.com/search?q={encoded_query}&count={count}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
        }
        
        html = search_with_requests(url, headers)
        if not html:
            return results
        
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
        print(f"    ⚠️ Bing搜索失败: {e}")
    
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
    
    # 在GitHub Actions中，搜索可能受限，使用更保守的策略
    is_ci = is_github_actions()
    if is_ci:
        print("  ℹ️ 检测到GitHub Actions环境，使用优化搜索策略")
    
    # 海外资讯
    print("\n📰 搜索海外AI资讯...")
    for query in SEARCH_QUERIES["overseas"]:
        print(f"  - 搜索: {query}")
        results = search_duckduckgo(query, count=3)
        if not results:
            results = search_bing(query, count=3)
        all_news["sources"]["overseas"].extend(results)
        
        # GitHub Actions中减少请求频率
        delay = 2 if is_ci else 1
        time.sleep(delay)
    
    # 国内资讯
    print("\n🇨🇳 搜索国内AI资讯...")
    for query in SEARCH_QUERIES["domestic"]:
        print(f"  - 搜索: {query}")
        results = search_duckduckgo(query, count=3)
        if not results:
            results = search_bing(query, count=3)
        all_news["sources"]["domestic"].extend(results)
        time.sleep(2 if is_ci else 1)
    
    # 综合资讯
    print("\n🌐 搜索综合AI资讯...")
    for query in SEARCH_QUERIES["general"]:
        print(f"  - 搜索: {query}")
        results = search_duckduckgo(query, count=3)
        if not results:
            results = search_bing(query, count=3)
        all_news["sources"]["general"].extend(results)
        time.sleep(2 if is_ci else 1)
    
    # 如果搜索结果太少，添加预设新闻源作为补充
    total_results = sum(len(v) for v in all_news["sources"].values())
    if total_results < 5:
        print(f"\n⚠️ 搜索结果较少 ({total_results} 条)，添加预设新闻源...")
        for preset in PRESET_NEWS:
            category = preset.get("category", "general")
            if category in all_news["sources"]:
                all_news["sources"][category].append({
                    "title": preset["title"],
                    "url": preset["url"],
                    "snippet": preset["snippet"],
                    "source": preset["source"],
                    "query": "preset"
                })
    
    # 去重（基于URL）
    seen_urls = set()
    for category in all_news["sources"]:
        unique_results = []
        for item in all_news["sources"][category]:
            url = item.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(item)
        all_news["sources"][category] = unique_results
    
    # 保存原始数据
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    raw_path = data_dir / f"{today}_raw.json"
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    total_count = sum(len(v) for v in all_news["sources"].values())
    print(f"\n✅ 原始数据已保存: {raw_path}")
    print(f"📊 共采集 {total_count} 条资讯")
    print(f"   - 海外: {len(all_news['sources']['overseas'])} 条")
    print(f"   - 国内: {len(all_news['sources']['domestic'])} 条")
    print(f"   - 综合: {len(all_news['sources']['general'])} 条")
    
    return all_news

def main():
    """主函数"""
    print("=" * 50)
    print("🤖 萧炎的AI洞察 - 资讯采集器")
    print("=" * 50)
    
    news_data = collect_daily_news()
    
    print("\n💡 下一步操作:")
    print("1. 运行 analyze_news.py 分析资讯")
    print("2. 运行 generate_rich_report.py 生成日报")

if __name__ == "__main__":
    main()
