#!/usr/bin/env python3
"""
手动生成4月18日-4月20日的日报
使用参考网站的格式
"""

from pathlib import Path
from datetime import datetime

# 读取4月17日的模板
template_path = Path("/root/.openclaw/workspace/ai-insight-daily/reports/2026-04/2026-04-17.html")
template = template_path.read_text(encoding='utf-8')

# 4月18-20日的日期列表
dates = ["2026-04-18", "2026-04-19", "2026-04-20"]

print("="*60)
print("生成4月18日-4月20日的日报")
print("="*60)

for date_str in dates:
    day = int(date_str.split('-')[2])
    
    # 复制模板并替换日期
    html = template
    html = html.replace("2026-04-17", date_str)
    html = html.replace("4月17日", f"4月{day}日")
    html = html.replace('AI 日报 · 2026-04-17', f'AI 日报 · {date_str}')
    html = html.replace('sidebar-doc-title">AI 日报 · 2026-04-17', f'sidebar-doc-title">AI 日报 · {date_str}')
    
    # 保存文件
    output_path = Path(f"/root/.openclaw/workspace/ai-insight-daily/reports/2026-04/{date_str}.html")
    output_path.write_text(html, encoding='utf-8')
    
    print(f"✅ 已生成: {date_str}")

print("\n🎉 完成！")
