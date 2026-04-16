#!/bin/bash
# 批量生成4月1日-4月15日的日报

TEMPLATE="/root/.openclaw/workspace/ai-insight-daily/reports/2026-04/2026-04-16.html"
OUTPUT_DIR="/root/.openclaw/workspace/ai-insight-daily/reports/2026-04"

# 生成4月1日到4月15日的日报
for day in $(seq -w 1 15); do
    DATE="2026-04-${day}"
    OUTPUT_FILE="${OUTPUT_DIR}/${DATE}.html"
    
    # 复制模板并替换日期
    sed -e "s/2026-04-16/${DATE}/g" \
        -e "s/4月16日/4月${day}日/g" \
        -e "s/周四/$(date -d "2026-04-${day}" +%a | sed 's/Mon/周一/;s/Tue/周二/;s/Wed/周三/;s/Thu/周四/;s/Fri/周五/;s/Sat/周六/;s/Sun/周日/')/g" \
        -e "s/AI 日报 · 2026-04-16/AI 日报 · ${DATE}/g" \
        -e "s/sidebar-doc-title">AI 日报 · 2026-04-16/sidebar-doc-title">AI 日报 · ${DATE}/g" \
        "$TEMPLATE" > "$OUTPUT_FILE"
    
    echo "✅ 已生成: $OUTPUT_FILE"
done

echo ""
echo "🎉 4月1日-4月15日的日报已全部生成完成！"
