#!/bin/bash
# 获取深度调研、追踪体系、知识库的所有页面

echo "开始获取深度调研、追踪体系、知识库页面..."

BASE_URL="https://xiaoxiong20260206.github.io/ai-insight"
OUTPUT_DIR="/root/.openclaw/workspace/ai-insight-daily/reference_html"

# 创建目录
mkdir -p $OUTPUT_DIR/deep-research
mkdir -p $OUTPUT_DIR/tracking
mkdir -p $OUTPUT_DIR/knowledge-base

# 深度调研首页
echo "获取深度调研首页..."
curl -s "$BASE_URL/02-deep-research/" -o "$OUTPUT_DIR/deep-research/index.html"

# AI Agent落地指南
echo "获取AI Agent落地指南..."
curl -s "$BASE_URL/02-deep-research/topics/ai-agent-guide/index.html" -o "$OUTPUT_DIR/deep-research/ai-agent-guide.html"

# 追踪体系
echo "获取追踪体系..."
curl -s "$BASE_URL/03-tracking/" -o "$OUTPUT_DIR/tracking/index.html" 

# 知识库
echo "获取知识库..."
curl -s "$BASE_URL/04-knowledge-base/" -o "$OUTPUT_DIR/knowledge-base/index.html"

echo "完成！"
