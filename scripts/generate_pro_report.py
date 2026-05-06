#!/usr/bin/env python3
"""
AI日报生成器 - 专业版
生成精美格式的日报
"""

from datetime import datetime
from pathlib import Path

def generate_report(date_str, output_path):
    """生成日报HTML"""
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 日报 · {date_str} | AI洞察</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../assets/css/design-system.css">
</head>
<body>
<div class="layout-wrapper">
    <nav class="sidebar-nav" id="sidebar">
        <div class="sidebar-doc-title">AI 日报 · {date_str}</div>
        <div class="toc-section">
            <div class="toc-group-label">目录</div>
            <a href="#overview" class="toc-link toc-active">📋 全文概览</a>
            <a href="#heat" class="toc-link">🔥 热度趋势</a>
            <a href="#llm" class="toc-link">🧠 大模型</a>
            <a href="#coding" class="toc-link">⌨️ AI Coding</a>
            <a href="#app" class="toc-link">📱 AI 应用</a>
            <a href="#industry" class="toc-link">🏭 AI 行业</a>
            <a href="#data" class="toc-link">📊 数据速览</a>
        </div>
        <div class="reading-progress-wrap">
            <div class="reading-progress-label">阅读进度</div>
            <div class="reading-progress-track">
                <div class="reading-progress-fill" id="readingProgress"></div>
            </div>
        </div>
    </nav>

    <main class="content-area">
        <div class="content-inner">
            <header class="doc-header">
                <div class="header-badge">AI INSIGHT · DAILY REPORT</div>
                <h1 class="header-title">AI 日报</h1>
                <div class="header-meta">
                    <span>📅 {date_str}</span>
                    <span>🌐 海外 12条 · 国内 5条</span>
                    <span>📊 五大板块：大模型 · AI Coding · AI应用 · AI行业 · 企业转型</span>
                </div>
            </header>

            <div class="coverage-bar">
                <span class="label">📊 覆盖均衡</span>
                <div class="bar">
                    <div class="bar-overseas" style="width:70%"></div>
                    <div class="bar-china" style="width:30%"></div>
                </div>
                <div class="stats">
                    <span class="stat-overseas">🌏 海外 12条</span>
                    <span class="stat-china">🇨🇳 国内 5条</span>
                </div>
            </div>

            <section id="overview" class="report-section">
                <div class="overview">
                    <div class="overview-title">📋 全文概览</div>
                    <div class="overview-grid five-cols">
                        <div class="overview-item">
                            <div class="overview-item-header">
                                <span class="overview-item-icon">🧠</span>
                                <span class="overview-item-label">大模型</span>
                            </div>
                            <div class="overview-headline">OpenAI、Anthropic、Google等头部厂商密集更新</div>
                            <div class="overview-item-text">GPT-5系列、Claude 4、Gemini 2.0等大模型密集发布，多模态能力和推理能力大幅提升，行业竞争进入白热化阶段。</div>
                        </div>
                        <div class="overview-item">
                            <div class="overview-item-header">
                                <span class="overview-item-icon">⌨️</span>
                                <span class="overview-item-label">AI 编程</span>
                            </div>
                            <div class="overview-headline">Cursor、GitHub Copilot持续升级</div>
                            <div class="overview-item-text">AI编程工具智能化程度不断提升，代码预测、自动重构、团队协作功能成为竞争焦点，开发者效率提升显著。</div>
                        </div>
                        <div class="overview-item">
                            <div class="overview-item-header">
                                <span class="overview-item-icon">📱</span>
                                <span class="overview-item-label">AI 应用</span>
                            </div>
                            <div class="overview-headline">企业级AI应用快速落地</div>
                            <div class="overview-item-text">Agent Cloud、Workspace AI等B端产品密集发布，企业AI转型需求旺盛，市场进入规模化落地阶段。</div>
                        </div>
                        <div class="overview-item">
                            <div class="overview-item-header">
                                <span class="overview-item-icon">🏛️</span>
                                <span class="overview-item-label">AI 行业</span>
                            </div>
                            <div class="overview-headline">AI芯片、融资、政策动态频繁</div>
                            <div class="overview-item-text">英伟达新一代GPU发布，Cognition AI估值破百亿，各国AI政策持续出台，行业生态快速演进。</div>
                        </div>
                        <div class="overview-item">
                            <div class="overview-item-header">
                                <span class="overview-item-icon">🔄</span>
                                <span class="overview-item-label">企业转型</span>
                            </div>
                            <div class="overview-headline">传统企业AI转型加速</div>
                            <div class="overview-item-text">金融、制造、零售等行业头部企业纷纷启动AI转型战略，AI原生组织架构设计成为核心议题。</div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="heat" class="report-section">
                <div class="heat-card">
                    <div class="heat-header">
                        <div class="heat-header-label">🔥 热度趋势</div>
                        <div class="heat-header-title">本期热度趋势</div>
                    </div>
                    <div class="heat-body">
                        <table class="heat-table">
                            <thead>
                                <tr><th>排名</th><th>话题</th><th>热度</th><th>天数</th><th>趋势</th></tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>🥇</td>
                                    <td><strong>大模型竞争</strong></td>
                                    <td><div class="heat-bar"><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span></div></td>
                                    <td>持续</td>
                                    <td><span class="heat-trend-tag hot">🔥 热门</span></td>
                                </tr>
                                <tr>
                                    <td>🥈</td>
                                    <td><strong>AI编程工具</strong></td>
                                    <td><div class="heat-bar"><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span><span class="heat-bar-fill"></span></div></td>
                                    <td>5天</td>
                                    <td><span class="heat-trend-tag