#!/usr/bin/env python3
"""
更新首页深度调研链接脚本
自动将新生成的报告添加到首页时间轴
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = SCRIPT_DIR.parent.parent
INDEX_FILE = PROJECT_DIR / "index.html"


def get_all_research_files():
    """获取所有完整版调研报告"""
    research_dir = PROJECT_DIR / "02-deep-research"
    files = []
    
    for category in ["trends", "topics", "companies", "people"]:
        cat_dir = research_dir / category
        if cat_dir.exists():
            for f in cat_dir.glob("*-complete.html"):
                # 解析文件信息
                stat = f.stat()
                files.append({
                    "path": str(f.relative_to(PROJECT_DIR)),
                    "name": f.stem.replace("-complete", "").replace("-", " "),
                    "category": category,
                    "mtime": stat.st_mtime,
                    "date": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
                })
    
    # 按修改时间排序
    files.sort(key=lambda x: x["mtime"], reverse=True)
    return files


def update_index_stats(total_count):
    """更新首页统计数字"""
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 更新深度调研数量
    content = re.sub(
        r'<div class="stat-number stat-green">\d+</div>\s*<div class="stat-label">深度调研</div>',
        f'<div class="stat-number stat-green">{total_count}</div>\n      <div class="stat-label">深度调研</div>',
        content
    )
    
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 首页统计已更新：深度调研 {total_count} 篇")


def main():
    print("📊 分析深度调研文件...")
    
    files = get_all_research_files()
    print(f"   找到 {len(files)} 篇完整版报告")
    
    # 更新首页统计
    update_index_stats(len(files))
    
    # 输出报告列表
    print("\n📋 报告列表:")
    for i, f in enumerate(files[:10], 1):
        print(f"   {i}. [{f['category']}] {f['name']}")
    
    if len(files) > 10:
        print(f"   ... 还有 {len(files) - 10} 篇")


if __name__ == "__main__":
    main()
