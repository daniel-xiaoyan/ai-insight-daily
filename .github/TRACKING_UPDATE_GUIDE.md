# 追踪体系更新规范

## 更新频率

**每月月初（1-3日）** 进行一次全量更新

## 更新内容

### 1. 模型版本更新

需要更新的关键版本信息：

| 公司/项目 | 最新版本（2026年5月） | 需要确认的渠道 |
|----------|---------------------|--------------|
| DeepSeek | V4 (2026-04-24) | GitHub Release, 官网博客 |
| OpenAI | GPT-5 (2026-03-15) | OpenAI Blog |
| Anthropic | Claude 4 (2026-02-28) | Anthropic Blog |
| Google | Gemini 3 (2026-04-01) | Google AI Blog |
| Meta | Llama 4 (2026-03-20) | Meta AI Blog |
| 字节跳动 | 豆包 V3 (2026-04-15) | 豆包官网 |
| 阿里 | 通义千问 Qwen-3 (2026-03-10) | 通义官网 |

### 2. 追踪条目更新

每次更新需要：

1. **版本号检查** - 确认每个模型/产品的最新版本
2. **能力更新** - 更新核心能力描述（如上下文长度、多模态能力等）
3. **新增条目** - 添加新晋重要人物/公司
4. **详情页同步** - 更新对应的详情页面

### 3. 详情页模板

每个追踪条目应有对应的详情页，路径规范：

```
03-tracking/
├── companies/
│   ├── deepseek.html
│   ├── openai.html
│   ├── anthropic.html
│   └── bytedance.html
├── people/
│   ├── sam-altman.html
│   ├── darius-amodei.html
│   └── jason-wei.html
└── sources/
    ├── rss-feeds.html
    └── newsletters.html
```

详情页必须包含：

1. 公司/人物概况
2. 核心产品/贡献
3. 技术演进时间线
4. 竞争格局分析
5. 追踪重点说明
6. 信息源列表
7. 近期动态
8. 关键洞察

## 更新流程

### 自动化部分

GitHub Actions 可在每月1日触发提醒：

```yaml
name: Monthly Tracking Update Reminder
on:
  schedule:
    - cron: '0 0 1 * *'  # UTC 00:00 = 北京时间 08:00
  workflow_dispatch:

jobs:
  remind:
    runs-on: ubuntu-latest
    steps:
      - name: Create reminder issue
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '🔄 月度追踪体系更新',
              body: `
## 本月更新任务

- [ ] 检查所有模型版本号
- [ ] 更新核心能力描述
- [ ] 检查新增重要人物/公司
- [ ] 更新详情页面内容

请按照 [更新规范](/.github/TRACKING_UPDATE_GUIDE.md) 执行更新。
              `,
              labels: ['maintenance', 'tracking-update']
            })
```

### 手动部分

需要人工完成：

1. 搜索最新版本信息（通过官方渠道）
2. 更新 `index.html` 中的追踪表格
3. 更新对应的详情页面
4. 提交推送更改

## 质量标准

更新必须满足：

- ✅ 版本号准确（与官方发布一致）
- ✅ 能力描述准确（基于实际测试/报告）
- ✅ 链接有效（所有详情页可访问）
- ✅ 时间戳更新（元数据中的更新时间）

---

**最后更新**：2026年5月11日
**维护者**：熏儿
