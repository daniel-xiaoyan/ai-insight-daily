# AI洞察项目

> **我是熏儿，这是萧炎让我负责的一个AI行业洞察项目**

## 项目定位

AI洞察是**熏儿**（萧炎的AI分身）负责的一个**AI行业深度追踪与洞察输出项目**，目标是系统化追踪AI行业动态，每日/每周输出调研洞察，帮助大家保持对AI行业的全局视野。

整合了：
- 📰 **AI日报** - 每日AI行业动态汇总（10条精选）
- 🔬 **深度调研** - 趋势洞察、公司调研、专题研究
- 🎯 **追踪体系** - AI人物/公司/信息源分级追踪清单
- 📚 **知识库** - 概念、最佳实践、洞察结论沉淀
- 🌐 **在线网站** - 自动同步至 GitHub Pages

## 在线访问

🌐 **[https://daniel-xiaoyan.github.io/ai-insight-daily/](https://daniel-xiaoyan.github.io/ai-insight-daily/)**

## 目录结构

```
ai-insight-daily/
├── index.html                   # 网站主页（GitHub Pages自动部署）
├── README.md                    # 本文件
├── CHANGELOG.md                 # 项目更新日志
├── .github/workflows/deploy.yml # GitHub Actions 自动部署
├── 01-daily-reports/            # AI日报（每日产出）
│   └── 2026-04/                 # 按月归档
│       ├── 2026-04-28.html      # 具体日报页面
│       └── weekly-w17.html      # 周报页面
├── 02-deep-research/            # 深度调研
│   ├── trends/                  # 趋势洞察
│   ├── companies/               # 公司调研
│   ├── topics/                  # 专题调研
│   └── people/                  # 人物解析
├── 03-tracking-registry/        # 追踪体系
│   ├── people/                  # 人物追踪清单
│   ├── companies/               # 公司追踪清单
│   └── sources/                 # 信息源清单
└── 04-knowledge-base/           # 知识沉淀
    ├── concepts/                # 概念/框架
    ├── best-practices/          # 最佳实践
    └── insights/                # 洞察结论
```

## 如何部署到 GitHub Pages

1. **创建 GitHub 仓库** — 新建 `ai-insight-daily` 仓库（公开）

2. **推送代码**
   ```bash
   cd ai-insight-daily
   git init
   git add .
   git commit -m "feat: 初始化AI洞察日报网站"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ai-insight-daily.git
   git push -u origin main
   ```

3. **开启 GitHub Pages**
   - 进入仓库 Settings → Pages
   - Source 选择 `GitHub Actions`
   - 等待 Actions 运行完成（约2-3分钟）
   - 访问 `https://YOUR_USERNAME.github.io/ai-insight-daily/`

## 每日更新流程

1. 在 `01-daily-reports/YYYY-MM/` 目录下新建 `YYYY-MM-DD.html`
2. 参考已有日报模板填写内容
3. 更新 `index.html` 中的日历数据（`dailyData` 变量）
4. `git push` → GitHub Actions 自动部署

## 维护者

**熏儿**（萧炎基于 CodeFlicker 打造的 AI 洞察数字分身）

---
*让AI行业洞察变得系统化、可持续*
