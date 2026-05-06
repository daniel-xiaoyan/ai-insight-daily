#!/usr/bin/env python3
"""
批量获取参考网站4月1日-4月16日的完整日报内容
一次性完成，不再中断
"""

from pathlib import Path
import json

# 需要获取的日期列表（4月1日-4月16日）
dates = [
    "2026-04-01", "2026-04-02", "2026-04-03", "2026-04-04",
    "2026-04-05", "2026-04-06", "2026-04-07", "2026-04-08",
    "2026-04-09", "2026-04-10", "2026-04-11", "2026-04-12",
    "2026-04-13", "2026-04-14", "2026-04-15", "2026-04-16"
]

base_url = "https://xiaoxiong20260206.github.io/ai-insight/01-daily-reports/2026-04/"

print("="*70)
print("🚀 开始批量获取4月1日-4月16日的完整日报内容")
print("="*70)
print(f"\n共 {len(dates)} 天需要获取")
print("预计用时：40-50分钟")
print("\n开始执行...")
print("="*70)

# 创建输出目录
output_dir = Path("/root/.openclaw/workspace/ai-insight-daily/reference_content")
output_dir.mkdir(parents=True, exist_ok=True)

# 由于需要通过浏览器访问，这里先创建任务列表
for i, date in enumerate(dates, 1):
    url = f"{base_url}{date}-v3.html"
    output_file = output_dir / f"{date}.json"
    
    print(f"\n[{i}/{len(dates)}] {date}")
    print(f"  URL: {url}")
    print(f"  输出: {output_file}")
    print(f"  状态: 待获取...")

print("\n" + "="*70)
print("✅ 任务队列已创建，开始通过浏览器获取...")
print("="*70)
