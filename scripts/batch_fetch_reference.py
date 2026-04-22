#!/usr/bin/env python3
"""
批量获取参考网站4月1日-4月15日的日报内容
由于需要访问15个页面并提取完整HTML，这需要15-20分钟
"""

import time
from pathlib import Path

# 日期列表
dates = [f"2026-04-{day:02d}" for day in range(1, 16)]

print("="*60)
print("📥 批量获取参考网站日报内容")
print("="*60)
print(f"\n目标：获取4月1日-4月15日共15天的日报")
print(f"预计时间：15-20分钟")
print(f"\n开始时间：{time.strftime('%H:%M:%S')}")
print("-"*60)

# 由于需要通过浏览器访问，这里记录需要获取的URL
base_url = "https://xiaoxiong20260206.github.io/ai-insight/01-daily-reports/2026-04/"

for i, date in enumerate(dates, 1):
    url = f"{base_url}{date}-v3.html"
    print(f"\n[{i}/15] {date}")
    print(f"    URL: {url}")
    print(f"    状态: 待获取...")
    
print("\n" + "="*60)
print("✅ 任务队列已创建")
print("="*60)
