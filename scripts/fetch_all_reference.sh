#!/bin/bash
# 自动批量获取参考网站日报内容的脚本
# 后台执行，不再中断

echo "开始批量获取4月1日-4月17日的完整日报内容..."
echo "预计用时：6-8小时"
echo ""

# 创建保存目录
mkdir -p /root/.openclaw/workspace/ai-insight-daily/reference_html

dates=(
    "2026-04-01" "2026-04-02" "2026-04-03" "2026-04-04"
    "2026-04-05" "2026-04-06" "2026-04-07" "2026-04-08"
    "2026-04-09" "2026-04-10" "2026-04-11" "2026-04-12"
    "2026-04-13" "2026-04-14" "2026-04-15"
)

base_url="https://xiaoxiong20260206.github.io/ai-insight/01-daily-reports/2026-04/"

for date in "${dates[@]}"; do
    url="${base_url}${date}-v3.html"
    output_file="/root/.openclaw/workspace/ai-insight-daily/reference_html/${date}.html"
    
    echo "[$date] 正在获取: $url"
    
    # 使用curl获取HTML
    curl -s "$url" -o "$output_file" --max-time 30
    
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        echo "  ✓ 已保存: $output_file ($(wc -c < "$output_file") bytes)"
    else
        echo "  ✗ 获取失败: $date"
    fi
    
    # 等待5秒，避免请求过快
    sleep 5
done

echo ""
echo "批量获取完成！"
echo "文件保存在: /root/.openclaw/workspace/ai-insight-daily/reference_html/"
