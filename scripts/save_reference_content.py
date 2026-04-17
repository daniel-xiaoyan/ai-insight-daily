#!/usr/bin/env python3
"""
保存参考网站的完整日报内容
建立真实内容数据库
"""

from pathlib import Path
import json

# 4月17日完整内容（已获取）
april_17_content = {
    "date": "2026-04-17",
    "title": "Claude Opus 4.7与GPT-Rosalind同日竞技，AI算力涨价潮终结20年降价史",
    "overview": [
        {"icon": "🚀", "label": "大模型", "headline": "三巨头同日竞技", "text": "Claude Opus 4.7与GPT-Rosalind同日发布，Gemini 2.5系列全面GA"},
        {"icon": "🤖", "label": "AI应用", "headline": "Agent产品元年开启", "text": "AWS、Norton、LILT密集发布Agent产品，AI从对话走向自主执行"},
        {"icon": "💼", "label": "产业动态", "headline": "AI算力涨价潮来袭", "text": "阿里云、腾讯云、百度云同日调价，终结云计算20年降价史"},
        {"icon": "🇨🇳", "label": "国内动态", "headline": "深圳大模型备案提速", "text": "4款深圳大模型通过广东省备案，国产AI合规发展进入新阶段"},
        {"icon": "🛠️", "label": "开发者工具", "headline": "AI编程助手竞争白热化", "text": "Gemini Code Assist与OpenAI Codex密集更新"}
    ],
    "coverage": {"overseas": 9, "domestic": 5},
    "sections": {
        "llm": {
            "overseas": [
                {"tag": "NEW", "title": "Claude Opus 4.7发布：安全对齐能力再升级", "source": "Anthropic", "findings": "Anthropic发布Claude Opus 4.7，在网络安全评估中展现更强的安全对齐能力，延续代码理解和长文本处理优势", "impact": ""},
                {"tag": "NEW", "title": "GPT-5.3 Instant Mini上线：更快响应替代GPT-5", "source": "OpenAI", "findings": "OpenAI推出GPT-5.3 Instant Mini，以更快的响应速度替代此前的GPT-5版本", "impact": ""},
                {"tag": "NEW", "title": "GPT-Rosalind亮相：面向专业工作场景", "source": "OpenAI", "findings": "OpenAI发布GPT-Rosalind，专为专业工作场景设计，同日与Claude Opus 4.7形成正面竞争", "impact": ""},
                {"tag": "NEW", "title": "Gemini 2.5 Pro/Flash全面可用", "source": "Google", "findings": "Google Gemini 2.5 Pro和Flash模型正式GA，Gemini 3.1 Flash TTS Preview同步发布", "impact": ""}
            ],
            "domestic": []
        }
    }
}

# 保存为JSON
output_dir = Path("/root/.openclaw/workspace/ai-insight-daily/reference_content")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "2026-04-17.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(april_17_content, f, ensure_ascii=False, indent=2)

print("✅ 4月17日内容已保存")
print(f"文件: {output_file}")
print("\n⏱️  继续获取其他日期...")
