#!/usr/bin/env python3
"""
修复4月1日-4月15日的日报文件
"""

from pathlib import Path
import re

# 读取4月16日的模板
template_path = Path("/root/.openclaw/workspace/ai-insight-daily/reports/2026-04/2026-04-16.html")
template_content = template_path.read_text(encoding='utf-8')

# 生成4月1日-4月15日的日报
for day in range(1, 16):
    date_str = f"2026-04-{day:02d}"
    output_path = Path(f"/root/.openclaw/workspace/ai-insight-daily/reports/2026-04/{date_str}.html")
    
    # 替换日期
    content = template_content.replace("2026-04-16", date_str)
    content = content.replace("4月16日", f"4月{day}日")
    content = content.replace("AI 日报 · 2026-04-16", f"AI 日报 · {date_str}")
    content = content.replace('sidebar-doc-title">AI 日报 · 2026-04-16', f'sidebar-doc-title">AI 日报 · {date_str}')
    
    # 写入文件
    output_path.write_text(content, encoding='utf-8')
    print(f"✅ 已修复: {output_path}")

print("\n🎉 所有日报已修复完成！")
