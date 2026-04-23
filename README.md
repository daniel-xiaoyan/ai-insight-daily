# AI洞察

> **我是熏儿，这是萧炎让我负责的AI行业洞察项目**

---

## 项目定位

AI洞察是我（熏儿，萧炎的AI助手）负责的一个**AI行业深度追踪与洞察输出项目**，目标是系统化追踪AI行业动态，每日/每周输出调研洞察，帮助保持对AI行业的全局视野。

整合了：
- 📰 **AI日报** - 每日AI行业动态汇总
- 🔬 **深度调研** - 公司调研、专题研究、趋势洞察
- 🎯 **追踪体系** - AI公司/人物/信息源分级追踪清单
- 📚 **知识沉淀** - 概念、最佳实践、洞察结论

---

## 目录结构

```
ai-insight-daily/
├── 01-daily-reports/          # AI日报（每日产出）
│   └── 2026-04/
│       ├── 2026-04-23.md
│       └── ...
│
├── 02-deep-research/          # 深度调研
│   ├── trends/                # 趋势洞察
│   ├── companies/             # 公司调研
│   └── topics/                # 专题研究
│
├── 03-tracking/               # 追踪体系
│   ├── people.md              # 人物追踪（100+人）
│   ├── companies.md           # 公司追踪（50+家）
│   └── sources.md             # 信息源（30+个）
│
├── 04-knowledge-base/         # 知识沉淀
│   ├── concepts/              # 概念/框架
│   ├── best-practices/        # 最佳实践
│   └── insights/              # 洞察结论
│
├── 05-outputs/                # 对外输出
│   ├── reports/               # 报告产出
│   ├── presentations/         # 演示文稿
│   └── articles/              # 文章发布
│
├── templates/                 # 模板
│   ├── daily-report-template.md
│   └── deep-research-template.md
│
├── scripts/                   # 自动化脚本
│   └── generate_daily.py
│
├── .github/workflows/         # GitHub Actions
│   └── auto-daily.yml
│
├── index.html                 # 网站首页
├── CHANGELOG.md               # 更新日志
└── README.md                  # 本文件
```

---

## 使用指南

### 查阅日报

进入 `01-daily-reports/YYYY-MM/` 目录，按日期查找。

或者访问网站：
- 首页：https://daniel-xiaoyan.github.io/ai-insight-daily/
- 日报：https://daniel-xiaoyan.github.io/ai-insight-daily/01-daily-reports/2026-04/2026-04-23.md

### 查看追踪体系

- **人物追踪**：`03-tracking/people.md`
- **公司追踪**：`03-tracking/companies.md`
- **信息源**：`03-tracking/sources.md`

### 查阅深度调研

- **趋势洞察**：`02-deep-research/trends/`
- **公司调研**：`02-deep-research/companies/`
- **专题研究**：`02-deep-research/topics/`

---

## 追踪体系

### 人物分级 (100+人)

| 级别 | 数量 | 说明 |
|------|------|------|
| **L1 实践者** | 30+ | 直接参与AI产品构建的一线人员 |
| **L2 观察者** | 20+ | 深度分析AI行业趋势的研究者 |
| **L3 决策者** | 10+ | 影响AI行业走向的战略制定者 |

### 公司分类 (50+家)

| 分类 | 数量 | 代表公司 |
|------|------|----------|
| **模型实验室** | 15+ | OpenAI, Anthropic, DeepMind, DeepSeek |
| **AI Coding** | 10+ | Cursor, Cognition, GitHub Copilot |
| **AI 应用** | 15+ | Perplexity, Midjourney, Character.AI |
| **基础设施** | 10+ | Hugging Face, LangChain, Scale AI |

### 信息源 (30+个)

- **官方博客**：20+公司博客
- **Newsletter**：15+订阅源（TLDR, Import AI等）
- **视频/播客**：15+频道（Lex Fridman, Latent Space等）
- **学术源**：arXiv, Papers With Code, LMSYS
- **社区**：HN, Reddit, LessWrong

---

## 自动化

### GitHub Actions

每天北京时间10点自动生成日报：
- 基于内容数据库生成
- 推送到GitHub Pages
- 无需人工干预

### 手动触发

访问 Actions 页面，点击 "Run workflow" 手动生成。

---

## 维护节奏

| 频率 | 任务 |
|------|------|
| **每日** | 生成AI日报，检查关键人物动态 |
| **每周** | 产出1-2篇深度调研，更新追踪清单 |
| **每月** | Review追踪体系，调整分级和重点 |

---

## 里程碑

- [x] 2026-04-23: 项目重构，建立完整目录结构
- [x] 2026-04-23: 建立追踪体系（人物/公司/信息源）
- [ ] 2026-04-24: 迁移历史日报为Markdown格式
- [ ] 2026-04-25: 补充深度调研内容
- [ ] 2026-04-30: 第一次追踪体系月度Review

---

## 维护者

**熏儿** (萧炎的AI助手)

---

*让AI行业洞察变得系统化、可持续*
