#!/usr/bin/env python3
"""
批量修改日报文件中的日期信息
确保每个文件显示正确的日期
"""

from pathlib import Path
import re

reports_dir = Path("/root/.openclaw/workspace/ai-insight-daily/reports/2026-04")

# 获取所有HTML文件
html_files = sorted(reports_dir.glob("2026-04-*.html"))

print(f"找到 {len(html_files)} 个日报文件")
print("开始修改日期信息...\n")

for html_file in html_files:
    date_str = html_file.stem  # 2026-04-01
    day = date_str.split("-")[2]  # 01
    
    # 读取文件
    content = html_file.read_text(encoding='utf-8')
    
    # 修改侧边栏标题
    content = re.sub(
        r'AI 日报 · 2026-04-\d{2}',
        f'AI 日报 · {date_str}',
        content
    )
    
    # 修改页面标题 (title标签)
    content = re.sub(
        r'<title>AI 日报 · 2026-04-\d{2}',
        f'<title>AI 日报 · {date_str}',
        content
    )
    
    # 修改meta description
    content = re.sub(
        r'AI洞察日报 2026-04-\d{2}',
        f'AI洞察日报 {date_str}',
        content
    )
    
    # 修改header中的日期显示
    # 格式：2026年4月16日 周四
    content = re.sub(
        r'2026年4月\d{1,2}日',
        f'2026年4月{int(day)}日',
        content
    )
    
    # 保存文件
    html_file.write_text(content, encoding='utf-8')
    
    print(f"✅ {date_str}: 日期信息已更新")

print(f"\n🎉 完成！共修改 {len(html_files)} 个文件")
