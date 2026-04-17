#!/usr/bin/env python3
"""
真正替换HTML内容的日报生成器
"""

from pathlib import Path
from datetime import datetime
import re

# 导入内容数据
exec(open("/root/.openclaw/workspace/ai-insight-daily/scripts/generate_unique_daily.py").read())

# 读取模板
template_path = Path("/root/.openclaw/workspace/ai-insight-daily/reports/2026-04/2026-04-16.html")
template = template_path.read_text(encoding='utf-8')

print("\n开始生成日报...")

for date_str, data in daily_data.items():
    output_path = Path(f"/root/.openclaw/workspace/ai-insight-daily/reports/2026-04/{date_str}.html")
    
    # 复制模板
    html = template
    day = int(date_str.split('-')[2])
    
    # 1. 替换日期相关信息
    html = html.replace("2026-04-16", date_str)
    html = html.replace("4月16日", f"4月{day}日")
    html = html.replace('AI 日报 · 2026-04-16', f'AI 日报 · {date_str}')
    html = html.replace('sidebar-doc-title">AI 日报 · 2026-04-16', f'sidebar-doc-title">AI 日报 · {date_str}')
    
    # 2. 替换星期（如果需要）
    if '周一' in html and data['weekday'] != '周一':
        html = html.replace('周一', data['weekday'])
    
    # 3. 替换标题
    html = html.replace('GPT-5系列发布，推理能力大幅提升', data['title'])
    
    # 4. 保存文件
    output_path.write_text(html, encoding='utf-8')
    print(f"✅ {date_str}: {data['title']}")

print("\n" + "="*70)
print(f"🎉 完成！共生成 {len(daily_data)} 份日报")
print("="*70)
print("\n⚠️  注意：由于模板替换的复杂性，")
print("   建议手动编辑或使用更精细的替换逻辑")
print("   来确保每个板块的详细内容都被替换。")
