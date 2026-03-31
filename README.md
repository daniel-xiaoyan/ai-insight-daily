# 🤖 萧炎的AI洞察

系统化追踪 AI 行业动态，每日输出大模型领域洞察，帮助你保持对 AI 行业的全局视野。

## 📊 追踪范围

| 类别 | 范围 |
|------|------|
| 🌍 海外大厂 | OpenAI, Anthropic, Google DeepMind, Meta AI, xAI, Mistral |
| 🇨🇳 国内大厂 | 字节、阿里、百度、腾讯、智谱、月之暗面、MiniMax 等 |
| 🎯 重点关注 | 大模型发布、AI Agent、AI Coding、多模态、产品更新 |

## 🚀 快速开始

### 1. 部署到 GitHub Pages

```bash
# Fork 本仓库到你的 GitHub
# 然后启用 GitHub Pages:
# Settings -> Pages -> Source -> GitHub Actions
```

### 2. 本地开发

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/ai-insight-daily.git
cd ai-insight-daily

# 生成今日日报结构
python scripts/generate_report.py

# 收集资讯（需要配合AI助手使用）
python scripts/collect_news.py
```

### 3. 自动化配置

项目已配置 GitHub Actions，每天自动：
- 生成日报模板
- 部署到 GitHub Pages
- 更新时间索引

## 📁 项目结构

```
ai-insight-daily/
├── .github/workflows/    # GitHub Actions 配置
├── site/                 # 静态网站文件
│   ├── index.html       # 首页
│   └── reports/         # 日报页面
├── scripts/             # 自动化脚本
│   ├── generate_report.py   # 生成日报结构
│   └── collect_news.py      # 资讯采集
├── data/                # 数据文件
│   ├── index.json       # 日报索引
│   └── raw/             # 原始采集数据
└── docs/                # 文档
```

## 📝 日报生成流程

```
┌─────────────────┐
│  定时触发/手动   │
└────────┬────────┘
         ▼
┌─────────────────┐
│  搜索AI资讯     │
│  (多引擎采集)   │
└────────┬────────┘
         ▼
┌─────────────────┐
│  AI分析整理     │
│  (分类/摘要)    │
└────────┬────────┘
         ▼
┌─────────────────┐
│  生成HTML页面   │
└────────┬────────┘
         ▼
┌─────────────────┐
│  部署到Pages    │
└─────────────────┘
```

## 🔧 数据源配置

编辑 `scripts/collect_news.py` 中的 `SEARCH_QUERIES` 来自定义搜索关键词：

```python
SEARCH_QUERIES = {
    "overseas": [
        "OpenAI GPT new model",
        "Anthropic Claude update",
        # 添加你关注的
    ],
    "domestic": [
        "字节跳动大模型",
        "阿里通义千问",
        # 添加你关注的
    ]
}
```

## 🎨 自定义样式

修改 `site/index.html` 中的 CSS 变量来自定义主题色：

```css
:root {
    --bg-primary: #0a0a0f;    /* 主背景色 */
    --accent: #6366f1;         /* 主题色 */
    --accent-light: #818cf8;   /* 高亮色 */
}
```

## 📅 更新日志

- **2026-03-31**: 项目初始化，基础框架搭建完成
- 更多更新见 [CHANGELOG.md](CHANGELOG.md)

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License
