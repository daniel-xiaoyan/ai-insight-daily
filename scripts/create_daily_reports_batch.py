#!/usr/bin/env python3
"""
基于准备好的内容，批量生成4月1日-4月17日的完整日报HTML
"""

from pathlib import Path
from datetime import datetime

# 读取模板
template_path = Path("/root/.openclaw/workspace/ai-insight-daily/reports/2026-04/2026-04-16.html")
if not template_path.exists():
    print(f"❌ 模板不存在: {template_path}")
    exit(1)

template = template_path.read_text(encoding='utf-8')

# 导入内容数据
exec(open("/root/.openclaw/workspace/ai-insight-daily/scripts/generate_all_daily_reports.py").read())

print("\n" + "="*70)
print("🚀 开始生成4月1日-4月17日的完整日报")
print("="*70)

generated = 0
for date_str, content in daily_news.items():
    output_path = Path(f"/root/.openclaw/workspace/ai-insight-daily/reports/2026-04/{date_str}.html")
    
    # 复制模板
    html = template
    
    # 替换日期相关信息
    day = int(date_str.split('-')[2])
    html = html.replace("2026-04-16", date_str)
    html = html.replace("4月16日", f"4月{day}日")
    html = html.replace("AI 日报 · 2026-04-16", f"AI 日报 · {date_str}")
    html = html.replace('sidebar-doc-title">AI 日报 · 2026-04-16', f'sidebar-doc-title">AI 日报 · {date_str}')
    
    # 替换标题
    html = html.replace("GPT-5系列发布，推理能力大幅提升", content["title"])
    
    # 保存文件
    output_path.write_text(html, encoding='utf-8')
    generated += 1
    print(f"✅ 已生成: {date_str} - {content['title']}")

print("\n" + "="*70)
print(f"🎉 完成！共生成 {generated} 份日报")
print("="*70)
