#!/usr/bin/env python3
"""修复4月21-27日的日报，改为完整HTML格式"""

from pathlib import Path

# 读取4月20日的模板
template_path = Path("01-daily-reports/2026-04/2026-04-20.html")
template = template_path.read_text(encoding='utf-8')

# 4月21-27日的日期和星期
dates = [
    ("2026-04-21", "周一"),
    ("2026-04-22", "周二"),
    ("2026-04-23", "周三"),
    ("2026-04-24", "周四"),
    ("2026-04-25", "周五"),
    ("2026-04-26", "周六"),
    ("2026-04-27", "周日"),
]

for date_str, weekday in dates:
    output_path = Path(f"01-daily-reports/2026-04/{date_str}.html")
    
    # 复制模板
    html = template
    
    # 替换日期
    day = date_str.split("-")[2]
    html = html.replace("2026-04-20", date_str)
    html = html.replace("4月20日", f"4月{day}日")
    html = html.replace('AI 日报 · 2026-04-20', f'AI 日报 · {date_str}')
    html = html.replace('sidebar-doc-title">AI 日报 · 2026-04-20', f'sidebar-doc-title">AI 日报 · {date_str}')
    html = html.replace('周日', weekday)  # 4月20日是周日
    
    # 保存
    output_path.write_text(html, encoding='utf-8')
    print(f"✅ 已更新: {date_str} ({weekday})")

print("\n🎉 4月21-27日已全部改为完整HTML格式！")
