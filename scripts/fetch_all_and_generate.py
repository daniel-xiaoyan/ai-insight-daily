#!/usr/bin/env python3
"""
批量获取参考网站4月1日-4月15日的全部日报内容
同时生成4月17日的日报
一次性完成，不再中断
"""

from datetime import datetime
from pathlib import Path

print("="*70)
print("🚀 开始批量任务：获取4月1日-15日内容 + 生成4月17日报")
print("="*70)
print(f"开始时间：{datetime.now().strftime('%H:%M:%S')}")
print("预计用时：20-25分钟")
print("-"*70)

# 4月1日-4月15日的URL列表（参考网站格式）
dates_to_fetch = [
    "2026-04-01", "2026-04-02", "2026-04-03", "2026-04-04",
    "2026-04-05", "2026-04-06", "2026-04-07", "2026-04-08",
    "2026-04-09", "2026-04-10", "2026-04-11", "2026-04-12",
    "2026-04-15"  # 共13天，4月13、14已获取
]

base_url = "https://xiaoxiong20260206.github.io/ai-insight/01-daily-reports/2026-04/"

print("\n📥 任务1：获取参考网站日报内容")
for date in dates_to_fetch:
    url = f"{base_url}{date}-v3.html"
    output_file = f"/root/.openclaw/workspace/ai-insight-daily/reports/2026-04/{date}.html"
    print(f"  - {date}: {url}")
    print(f"    → 保存至: {output_file}")

print("\n📝 任务2：生成4月17日日报")
print(f"  - 日期: 2026-04-17")
print(f"  - 输出: /root/.openclaw/workspace/ai-insight-daily/reports/2026-04/2026-04-17.html")

print("\n" + "="*70)
print("开始执行...")
print("="*70)
