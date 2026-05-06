#!/usr/bin/env python3
"""
AI洞察 · 每日自动生成日报脚本
由 熏儿 自动维护，每天北京时间 10:00 运行
"""

import os
import sys
import json
import re
import datetime
from pathlib import Path
from openai import OpenAI

# ─── 配置 ──────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
REPORTS_DIR = REPO_ROOT / "01-daily-reports"
INDEX_PATH = REPO_ROOT / "index.html"
DATA_PATH = REPO_ROOT / "data.json"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"

# 星期映射
WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# ─── 日期工具 ──────────────────────────────────────────
def today_cn():
    """返回北京时间今天的 datetime"""
    utc_now = datetime.datetime.utcnow()
    beijing = utc_now + datetime.timedelta(hours=8)
    return beijing

def format_date(dt):
    return dt.strftime("%Y-%m-%d")

def format_date_cn(dt):
    wd = WEEKDAYS[dt.weekday()]
    return f"{dt.year}年{dt.month}月{dt.day}日 · {wd}"

def get_month_dir(dt):
    return REPORTS_DIR / dt.strftime("%Y-%m")

def get_report_path(dt):
    return get_month_dir(dt) / f"{format_date(dt)}.html"

# ─── AI 内容生成 ────────────────────────────────────────
def build_prompt(date_str: str) -> str:
    return f"""你是「熏儿」，萧炎的AI洞察数字分身，负责每天整理全球AI行业最重要的动态。
今天日期：{date_str}

请生成今天的《AI日报》内容，以严格的JSON格式返回，字段如下：

{{
  "date": "{date_str}",
  "hot_topics": [
    {{
      "rank": 1,
      "topic": "话题名称",
      "heat": 15,
      "days": 1,
      "trend": "热门",
      "signal": "核心信号描述（15字内）"
    }}
  ],
  "overview": [
    {{
      "section": "大模型",
      "icon": "🧠",
      "headline": "板块最重要一句话（20字内）",
      "summary": "2-3句摘要"
    }}
  ],
  "sections": [
    {{
      "id": "llm",
      "title": "大模型动态",
      "icon": "🧠",
      "icon_bg": "sc-icon-green",
      "subtitle": "模型发布、能力进展与技术突破",
      "overseas": [
        {{
          "title": "新闻标题",
          "source": "来源媒体",
          "is_new": true,
          "finding": "核心发现：...",
          "impact": "影响判断：..."
        }}
      ],
      "domestic": [
        {{
          "title": "新闻标题",
          "source": "来源媒体",
          "is_new": true,
          "finding": "核心发现：...",
          "impact": ""
        }}
      ],
      "focus_title": "💡 深度聚焦 · 主题",
      "focus_paras": ["段落1", "段落2"],
      "takeaway": "一句话TAKEAWAY结论",
      "insight_title": "板块核心洞察标题",
      "insight_body": "核心洞察正文（2-3句）",
      "insight_points": [
        "🔥 **关键词**：洞察结论",
        "⚡ **关键词**：洞察结论"
      ]
    }}
  ],
  "data_points": [
    {{"metric": "指标名", "value": "数值", "note": "说明"}}
  ],
  "tomorrow": [
    {{"title": "明日关注标题", "desc": "具体说明"}}
  ],
  "xunr_note": "熏儿自述（100字内，第一人称，幽默+洞察风格）",
  "stats": {{
    "total": 16,
    "overseas": 8,
    "domestic": 8,
    "sections": 5,
    "focus": 3
  }}
}}

要求：
- hot_topics 包含5条，heat值1-20递减（第1条15-18，第5条5-8），体现差异
- sections 必须包含5个：llm/coding/app/industry/enterprise
- coding的icon_bg用sc-icon-blue，app用sc-icon-purple，industry用sc-icon-orange，enterprise用sc-icon-dark
- 内容要反映{date_str}前后真实发生的AI行业重要事件
- 如果不确定具体事件，用合理推断补充，保持专业性
- 返回纯JSON，不要markdown代码块"""

def call_openai(prompt: str) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4000,
    )
    raw = response.choices[0].message.content.strip()
    # 去掉可能的 markdown 代码块
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

# ─── HTML 生成 ──────────────────────────────────────────
def heat_bar_html(heat: int) -> str:
    bars = ""
    for i in range(20):
        cls = "heat-bar-fill filled" if i < heat else "heat-bar-fill"
        bars += f'<span class="{cls}"></span>'
    return f'<div class="heat-bar">{bars}</div>'

def trend_class(trend: str) -> str:
    if "热" in trend:
        return "trend-hot"
    elif "上" in trend:
        return "trend-up"
    return "trend-stable"

def news_items_html(items: list) -> str:
    html = ""
    for item in items:
        new_badge = '<span class="news-new">NEW</span>' if item.get("is_new") else ""
        expand_btns = ""
        expand_contents = ""
        if item.get("finding"):
            expand_btns += '<button class="news-expand-btn" onclick="toggleExpand(this)">💡 核心发现</button>'
            expand_contents += f'<div class="news-expand-content">{item["finding"]}</div>'
        if item.get("impact"):
            expand_btns += '<button class="news-expand-btn" onclick="toggleExpand(this)">📊 影响判断</button>'
            expand_contents += f'<div class="news-expand-content">{item["impact"]}</div>'
        html += f"""
              <div class="news-item">
                <div class="news-item-top">
                  {new_badge}
                  <a class="news-title-link" href="#">{item['title']}</a>
                </div>
                <div class="news-source">来源：{item.get('source', '')}</div>
                <div class="news-expands">{expand_btns}</div>
                {expand_contents}
              </div>"""
    return html

def section_html(sec: dict) -> str:
    overseas = news_items_html(sec.get("overseas", []))
    domestic = news_items_html(sec.get("domestic", []))
    region_html = ""
    if overseas:
        region_html += f'<div class="region-group"><div class="region-title">🌏 海外</div><div class="news-items">{overseas}</div></div>'
    if domestic:
        region_html += f'<div class="region-group"><div class="region-title">🇨🇳 国内</div><div class="news-items">{domestic}</div></div>'

    focus_paras = "".join(f'<div class="focus-box-p">{p}</div>' for p in sec.get("focus_paras", []))
    insight_points = "".join(f'<div class="ic-point">{p}</div>' for p in sec.get("insight_points", []))

    return f"""
    <div class="section-card" id="{sec['id']}">
      <div class="section-card-header">
        <div class="sc-icon {sec['icon_bg']}">{sec['icon']}</div>
        <div class="sc-titles">
          <div class="sc-title">{sec['title']}</div>
          <div class="sc-subtitle">{sec.get('subtitle', '')}</div>
        </div>
      </div>
      <div class="sc-body">
        <div class="news-section-wrap">{region_html}</div>
        <div class="focus-box">
          <div class="focus-box-title">{sec.get('focus_title', '💡 深度聚焦')}</div>
          <div class="focus-box-paras">{focus_paras}</div>
          <div class="takeaway-box">
            <div class="takeaway-label">💡 TAKEAWAY</div>
            <div class="takeaway-text">{sec.get('takeaway', '')}</div>
          </div>
        </div>
        <div class="insight-callout">
          <div class="ic-header">
            <div class="ic-emoji-wrap">{sec['icon']}</div>
            <div class="ic-title">{sec.get('insight_title', sec['title'] + '：核心洞察')}</div>
          </div>
          <div class="ic-body">
            {sec.get('insight_body', '')}
            <div class="ic-points">{insight_points}</div>
          </div>
        </div>
      </div>
    </div>"""

def render_html(data: dict, date_str: str) -> str:
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    date_cn = format_date_cn(dt)
    prev_date = format_date(dt - datetime.timedelta(days=1))
    month_dir = dt.strftime("%Y-%m")

    # 热度趋势
    hot_rows = ""
    rank_icons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    for i, t in enumerate(data.get("hot_topics", [])[:5]):
        tc = trend_class(t.get("trend", ""))
        hot_rows += f"""
            <tr>
              <td class="hot-rank">{rank_icons[i]}</td>
              <td><div class="hot-topic">{t['topic']}</div></td>
              <td>{heat_bar_html(t['heat'])}</td>
              <td>{t.get('days', 1)}天</td>
              <td><span class="trend-badge {tc}">{t.get('trend', '')}</span></td>
              <td class="hot-signal">{t.get('signal', '')}</td>
            </tr>"""

    # 全文概览
    ov_cards = ""
    for ov in data.get("overview", []):
        ov_cards += f"""
          <div class="ov-card">
            <div class="ov-card-header"><span class="ov-icon">{ov['icon']}</span><span class="ov-name">{ov['section']}</span></div>
            <div class="ov-headline">{ov['headline']}</div>
            <div class="ov-summary">{ov['summary']}</div>
          </div>"""

    # 各板块
    sections_html = ""
    for sec in data.get("sections", []):
        sections_html += section_html(sec)

    # 数据速览
    data_rows = ""
    for dp in data.get("data_points", []):
        data_rows += f'<tr><td class="data-metric">{dp["metric"]}</td><td class="data-value">{dp["value"]}</td><td class="data-note">{dp.get("note","")}</td></tr>'

    # 明日关注
    tomorrow_items = ""
    for t in data.get("tomorrow", []):
        tomorrow_items += f"""
          <div class="tomorrow-item">
            <div class="tomorrow-dot"></div>
            <div class="tomorrow-content">
              <div class="tomorrow-title">{t['title']}</div>
              <div class="tomorrow-desc">{t['desc']}</div>
            </div>
          </div>"""

    stats = data.get("stats", {})

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{date_str} AI日报 v4.0 | 熏儿的AI洞察</title>
  <style>
    :root {{
      --green: #059669; --green-light: #dcfce7; --green-dark: #047857;
      --blue: #2563eb; --blue-light: #dbeafe;
      --purple: #7c3aed;
      --orange: #d97706; --orange-light: #fef3c7;
      --red: #ef4444;
      --bg: #f8fafb;
      --card: #ffffff;
      --border: #f5f5f4;
      --border2: #e7e5e4;
      --text: #57534e;
      --text-dark: #1c1917;
      --text-muted: #78716c;
      --radius: 16px;
      --radius-sm: 10px;
      --shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
      --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; font-size: 15px; }}
    .top-bar {{ height: 4px; background: linear-gradient(90deg,#059669,#2563eb,#7c3aed); }}
    .nav {{ background: white; border-bottom: 1px solid var(--border2); padding: 10px 20px; display: flex; align-items: center; gap: 8px; font-size: 13px; }}
    .nav a {{ color: var(--green); text-decoration: none; }}
    .nav a:hover {{ text-decoration: underline; }}
    .nav-sep {{ color: var(--border2); }}
    .nav-cur {{ color: var(--text-muted); }}
    .page-layout {{ display: grid; grid-template-columns: 200px 1fr; gap: 24px; max-width: 1060px; margin: 0 auto; padding: 24px 16px 60px; align-items: start; }}
    @media (max-width: 860px) {{ .page-layout {{ grid-template-columns: 1fr; }} .sidebar {{ display: none; }} }}
    .sidebar {{ position: sticky; top: 16px; }}
    .sidebar-card {{ background: white; border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 14px; }}
    .sidebar-title {{ font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }}
    .sidebar-nav {{ display: flex; flex-direction: column; gap: 2px; }}
    .sidebar-link {{ display: flex; align-items: center; gap: 7px; padding: 6px 8px; border-radius: 7px; text-decoration: none; font-size: 12px; color: var(--text-muted); transition: all 0.15s; }}
    .sidebar-link:hover, .sidebar-link.active {{ background: var(--green-light); color: var(--green-dark); font-weight: 600; }}
    .sidebar-link .sicon {{ font-size: 14px; flex-shrink: 0; }}
    .main {{ display: flex; flex-direction: column; gap: 16px; }}
    .section-card {{ background: white; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow); }}
    .section-card-header {{ padding: 16px 20px 12px; border-bottom: 1px solid var(--border); display: flex; align-items: flex-start; gap: 12px; }}
    .sc-icon {{ width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }}
    .sc-icon-green {{ background: #dcfce7; }} .sc-icon-blue {{ background: #dbeafe; }} .sc-icon-orange {{ background: #fef3c7; }} .sc-icon-red {{ background: #fee2e2; }} .sc-icon-purple {{ background: #f3e8ff; }} .sc-icon-dark {{ background: #1e293b; }}
    .sc-titles {{ flex: 1; }}
    .sc-title {{ font-size: 18px; font-weight: 700; color: var(--text-dark); line-height: 1.3; }}
    .sc-subtitle {{ font-size: 13px; color: var(--text-muted); margin-top: 2px; }}
    .sc-body {{ padding: 16px 20px; }}
    .hero-card {{ background: white; border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow); }}
    .hero-label {{ font-size: 11px; font-weight: 700; letter-spacing: 1.5px; color: var(--green); margin-bottom: 10px; }}
    .hero-title-row {{ display: flex; align-items: center; gap: 12px; margin-bottom: 8px; flex-wrap: wrap; }}
    .hero-title {{ font-size: 28px; font-weight: 800; color: var(--text-dark); }}
    .hero-ver {{ background: var(--green-light); color: var(--green-dark); font-size: 12px; font-weight: 700; padding: 3px 10px; border-radius: 999px; }}
    .hero-date {{ font-size: 15px; color: var(--text-muted); margin-bottom: 16px; }}
    .hero-stats {{ display: flex; gap: 10px; flex-wrap: wrap; }}
    .hero-stat-badge {{ background: #f8fafb; border: 1px solid var(--border2); border-radius: 999px; padding: 5px 14px; font-size: 12px; color: var(--text); font-weight: 500; }}
    .hero-cover-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 16px; }}
    @media (max-width: 600px) {{ .hero-cover-grid {{ grid-template-columns: 1fr; }} }}
    .cover-chip {{ background: #f8fafb; border-radius: 10px; padding: 12px; text-align: center; border: 1px solid var(--border2); }}
    .cover-chip-emoji {{ font-size: 22px; margin-bottom: 4px; }}
    .cover-chip-label {{ font-size: 12px; font-weight: 600; color: var(--text-dark); }}
    .cover-chip-num {{ font-size: 11px; color: var(--text-muted); margin-top: 2px; }}
    .overview-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
    @media (max-width: 600px) {{ .overview-grid {{ grid-template-columns: 1fr; }} }}
    .ov-card {{ background: #f8fafb; border-radius: 10px; padding: 14px; border: 1px solid var(--border2); }}
    .ov-card-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }}
    .ov-icon {{ font-size: 18px; }}
    .ov-name {{ font-size: 13px; font-weight: 700; color: var(--text-dark); }}
    .ov-headline {{ font-size: 13px; font-weight: 600; color: var(--blue); margin-bottom: 5px; line-height: 1.4; }}
    .ov-summary {{ font-size: 12px; color: var(--text-muted); line-height: 1.5; }}
    .hot-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    .hot-table th {{ padding: 6px 8px; background: #fef2f2; text-align: left; font-weight: 700; color: #991b1b; border-bottom: 1px solid var(--border2); white-space: nowrap; }}
    .hot-table td {{ padding: 6px 8px; border-bottom: 1px solid var(--border); vertical-align: middle; background: white; }}
    .hot-table tr:last-child td {{ border-bottom: none; }}
    .hot-table tr:hover td {{ background: #f8fafb; }}
    .hot-rank {{ font-size: 16px; width: 40px; }}
    .hot-topic {{ font-weight: 600; color: var(--text-dark); }}
    .heat-bar {{ display: flex; gap: 1px; height: 14px; align-items: center; }}
    .heat-bar-fill {{ width: 3px; height: 10px; background: #e5e7eb; border-radius: 1px; }}
    .heat-bar-fill.filled {{ background: linear-gradient(to bottom, #ef4444, #f97316); }}
    .trend-badge {{ font-size: 11px; padding: 2px 8px; border-radius: 999px; font-weight: 600; display: inline-flex; align-items: center; gap: 3px; }}
    .trend-hot {{ background: transparent; color: var(--text); }}
    .trend-up {{ background: transparent; color: var(--text); }}
    .trend-stable {{ background: #eff6ff; color: var(--blue); }}
    .hot-signal {{ font-size: 12px; color: var(--text-muted); }}
    .hot-summary {{ margin-top: 14px; font-size: 13px; color: var(--text); line-height: 1.6; background: #f8fafb; padding: 12px; border-radius: 8px; }}
    .news-section-wrap {{ display: flex; flex-direction: column; gap: 12px; }}
    .region-group {{}}
    .region-title {{ font-size: 12px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }}
    .news-items {{ display: flex; flex-direction: column; gap: 8px; }}
    .news-item {{ background: #f8fafb; border: 1px solid var(--border2); border-radius: 10px; padding: 12px 14px; }}
    .news-item-top {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; flex-wrap: wrap; }}
    .news-new {{ font-size: 9px; font-weight: 700; background: #ef4444; color: white; padding: 2px 6px; border-radius: 999px; letter-spacing: 0.5px; }}
    .news-title-link {{ font-size: 14px; font-weight: 600; color: var(--blue); text-decoration: none; line-height: 1.4; flex: 1; }}
    .news-title-link:hover {{ text-decoration: underline; color: var(--green); }}
    .news-source {{ font-size: 11px; color: var(--text-muted); }}
    .news-expands {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; }}
    .news-expand-btn {{ font-size: 11px; padding: 3px 10px; border-radius: 999px; border: 1px solid var(--border2); background: white; cursor: pointer; color: var(--text-muted); transition: all 0.15s; }}
    .news-expand-btn:hover {{ background: var(--green-light); color: var(--green-dark); border-color: #86efac; }}
    .news-expand-content {{ display: none; margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border2); font-size: 13px; color: var(--text); line-height: 1.6; }}
    .news-expand-content.open {{ display: block; }}
    .focus-box {{ background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 12px; padding: 18px; margin-top: 12px; color: white; }}
    .focus-box-title {{ font-size: 14px; font-weight: 700; margin-bottom: 12px; color: #e2e8f0; }}
    .focus-box-paras {{ display: flex; flex-direction: column; gap: 10px; }}
    .focus-box-p {{ font-size: 13px; color: rgba(255,255,255,0.75); line-height: 1.7; }}
    .takeaway-box {{ background: rgba(5,150,105,0.2); border-left: 3px solid #10b981; border-radius: 6px; padding: 12px 14px; margin-top: 12px; }}
    .takeaway-label {{ font-size: 10px; font-weight: 700; color: #86efac; letter-spacing: 1px; margin-bottom: 4px; }}
    .takeaway-text {{ font-size: 13px; font-weight: 600; color: white; line-height: 1.5; }}
    .insight-callout {{ background: white; border: 1px solid var(--border); border-radius: 16px; overflow: hidden; margin-top: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
    .ic-header {{ background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); padding: 14px 20px; display: flex; align-items: center; gap: 10px; }}
    .ic-emoji-wrap {{ width: 32px; height: 32px; border-radius: 50%; background: #fef3c7; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }}
    .ic-title {{ font-size: 15px; font-weight: 700; color: var(--text); }}
    .ic-body {{ padding: 14px 20px; font-size: 15px; color: var(--text); line-height: 1.65; }}
    .ic-body strong {{ color: var(--text-dark); }}
    .ic-points {{ display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }}
    .ic-point {{ font-size: 15px; color: var(--text); line-height: 1.65; }}
    .data-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    .data-table td {{ padding: 8px 12px; border-bottom: 1px solid var(--border); }}
    .data-table tr:last-child td {{ border-bottom: none; }}
    .data-metric {{ color: var(--text-muted); }}
    .data-value {{ font-weight: 700; color: var(--text-dark); font-size: 15px; }}
    .data-note {{ color: var(--text-muted); font-size: 12px; }}
    .tomorrow-items {{ display: flex; flex-direction: column; gap: 10px; }}
    .tomorrow-item {{ display: flex; gap: 12px; align-items: flex-start; }}
    .tomorrow-dot {{ width: 10px; height: 10px; border-radius: 50%; background: var(--green); margin-top: 6px; flex-shrink: 0; }}
    .tomorrow-title {{ font-size: 14px; font-weight: 600; color: var(--text-dark); }}
    .tomorrow-desc {{ font-size: 13px; color: var(--text-muted); line-height: 1.5; margin-top: 2px; }}
    .xunr-card {{ background: white; border: 1px solid var(--border2); border-radius: var(--radius); padding: 20px; box-shadow: var(--shadow); }}
    .xunr-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }}
    .xunr-avatar {{ width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #059669, #2563eb); display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; }}
    .xunr-name {{ font-size: 14px; font-weight: 700; color: var(--text-dark); }}
    .xunr-role {{ font-size: 12px; color: var(--text-muted); }}
    .xunr-body {{ font-size: 13px; color: var(--text); line-height: 1.8; }}
    .xunr-stats {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }}
    .xunr-stat {{ background: #f8fafb; border-radius: 8px; padding: 8px 12px; font-size: 12px; color: var(--text-muted); }}
    .xunr-stat strong {{ color: var(--text-dark); display: block; font-size: 16px; }}
    .page-nav {{ display: flex; gap: 12px; }}
    .pn-btn {{ flex: 1; background: white; border: 1px solid var(--border2); border-radius: 10px; padding: 12px 14px; text-decoration: none; color: var(--text); display: block; transition: box-shadow 0.15s, border-color 0.15s; }}
    .pn-btn:hover {{ box-shadow: var(--shadow-md); border-color: var(--green); }}
    .pn-label {{ font-size: 11px; color: var(--text-muted); margin-bottom: 3px; }}
    .pn-title {{ font-size: 13px; font-weight: 600; }}
    .back-top {{ position: fixed; bottom: 24px; right: 20px; background: var(--green); color: white; border: none; border-radius: 999px; padding: 8px 14px; font-size: 12px; font-weight: 600; cursor: pointer; box-shadow: var(--shadow-md); transition: transform 0.15s; z-index: 99; }}
    .back-top:hover {{ transform: translateY(-2px); }}
  </style>
</head>
<body>
<div class="top-bar"></div>
<nav class="nav">
  <a href="../../index.html">🔬 AI洞察</a>
  <span class="nav-sep">/</span>
  <a href="../../index.html">AI日报</a>
  <span class="nav-sep">/</span>
  <span class="nav-cur">{date_str}</span>
</nav>
<div class="page-layout">
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-title">本期目录</div>
      <nav class="sidebar-nav">
        <a class="sidebar-link" href="#hero"><span class="sicon">📋</span> 全文概览</a>
        <a class="sidebar-link" href="#overview"><span class="sicon">📋</span> 板块摘要</a>
        <a class="sidebar-link" href="#hot"><span class="sicon">🔥</span> 热度趋势</a>
        <a class="sidebar-link" href="#llm"><span class="sicon">🧠</span> 大模型</a>
        <a class="sidebar-link" href="#coding"><span class="sicon">⌨️</span> AI Coding</a>
        <a class="sidebar-link" href="#app"><span class="sicon">📱</span> AI应用</a>
        <a class="sidebar-link" href="#industry"><span class="sicon">🏭</span> AI行业</a>
        <a class="sidebar-link" href="#enterprise"><span class="sicon">🔄</span> 企业AI转型</a>
        <a class="sidebar-link" href="#data"><span class="sicon">📊</span> 数据速览</a>
        <a class="sidebar-link" href="#tomorrow"><span class="sicon">📌</span> 明日关注</a>
      </nav>
    </div>
  </aside>
  <main class="main">
    <div class="hero-card" id="hero">
      <div class="hero-label">AI INSIGHT · DAILY REPORT</div>
      <div class="hero-title-row">
        <div class="hero-title">AI 日报</div>
        <span class="hero-ver">v4.0</span>
      </div>
      <div class="hero-date">📅 {date_cn}</div>
      <div class="hero-stats">
        <span class="hero-stat-badge">🌐 海外 {stats.get('overseas',8)}条 · 国内 {stats.get('domestic',8)}条</span>
        <span class="hero-stat-badge">📊 五大板块覆盖</span>
        <span class="hero-stat-badge">🔬 熏儿出品</span>
      </div>
      <div class="hero-cover-grid">
        <div class="cover-chip"><div class="cover-chip-emoji">📊</div><div class="cover-chip-label">覆盖均衡</div><div class="cover-chip-num">5个板块</div></div>
        <div class="cover-chip"><div class="cover-chip-emoji">🌏</div><div class="cover-chip-label">海外动态</div><div class="cover-chip-num">{stats.get('overseas',8)}条资讯</div></div>
        <div class="cover-chip"><div class="cover-chip-emoji">🇨🇳</div><div class="cover-chip-label">国内动态</div><div class="cover-chip-num">{stats.get('domestic',8)}条资讯</div></div>
      </div>
    </div>
    <div class="section-card" id="overview">
      <div class="section-card-header">
        <div class="sc-icon sc-icon-blue">📋</div>
        <div class="sc-titles"><div class="sc-title">全文概览</div><div class="sc-subtitle">各板块核心摘要，快速了解今日AI动态</div></div>
      </div>
      <div class="sc-body"><div class="overview-grid">{ov_cards}</div></div>
    </div>
    <div class="section-card" id="hot">
      <div class="section-card-header">
        <div class="sc-icon sc-icon-red">🔥</div>
        <div class="sc-titles"><div class="sc-title">热度趋势</div><div class="sc-subtitle">今日AI圈最受关注话题排行 · 持续天数 · 趋势变化</div></div>
      </div>
      <div class="sc-body">
        <table class="hot-table">
          <thead><tr><th>排名</th><th>话题</th><th>热度</th><th>天数</th><th>趋势</th><th>核心信号</th></tr></thead>
          <tbody>{hot_rows}</tbody>
        </table>
      </div>
    </div>
    {sections_html}
    <div class="section-card" id="data">
      <div class="section-card-header">
        <div class="sc-icon sc-icon-blue">📊</div>
        <div class="sc-titles"><div class="sc-title">数据速览</div><div class="sc-subtitle">今日AI圈关键数字</div></div>
      </div>
      <div class="sc-body"><table class="data-table"><tbody>{data_rows}</tbody></table></div>
    </div>
    <div class="section-card" id="tomorrow">
      <div class="section-card-header">
        <div class="sc-icon sc-icon-green">📌</div>
        <div class="sc-titles"><div class="sc-title">明日关注</div><div class="sc-subtitle">值得持续追踪的信号</div></div>
      </div>
      <div class="sc-body"><div class="tomorrow-items">{tomorrow_items}</div></div>
    </div>
    <div class="xunr-card">
      <div class="xunr-header">
        <div class="xunr-avatar">🔬</div>
        <div><div class="xunr-name">熏儿 · AI洞察</div><div class="xunr-role">萧炎的AI分身，负责每日AI洞察输出</div></div>
      </div>
      <div class="xunr-body">{data.get('xunr_note', '')}</div>
      <div class="xunr-stats">
        <div class="xunr-stat"><strong>{stats.get('total',16)}</strong>今日处理资讯</div>
        <div class="xunr-stat"><strong>{stats.get('sections',5)}</strong>覆盖板块</div>
        <div class="xunr-stat"><strong>{stats.get('focus',3)}</strong>深度聚焦</div>
      </div>
    </div>
    <div class="page-nav">
      <a class="pn-btn" href="{prev_date}.html"><div class="pn-label">← 前一篇</div><div class="pn-title">{prev_date} AI日报</div></a>
      <a class="pn-btn" href="../../index.html" style="text-align:right"><div class="pn-label">返回首页 →</div><div class="pn-title">🔬 AI洞察首页</div></a>
    </div>
  </main>
</div>
<button class="back-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑ 回到顶部</button>
<script>
  function toggleExpand(btn) {{
    const item = btn.closest('.news-item');
    const contents = item.querySelectorAll('.news-expand-content');
    const btns = item.querySelectorAll('.news-expand-btn');
    const idx = Array.from(btns).indexOf(btn);
    const target = contents[idx];
    if (!target) return;
    const isOpen = target.classList.contains('open');
    contents.forEach(c => c.classList.remove('open'));
    if (!isOpen) target.classList.add('open');
  }}
  const sections = document.querySelectorAll('[id]');
  const sideLinks = document.querySelectorAll('.sidebar-link');
  const obs = new IntersectionObserver(entries => {{
    entries.forEach(e => {{
      if (e.isIntersecting) {{
        sideLinks.forEach(l => l.classList.remove('active'));
        const a = document.querySelector('.sidebar-link[href="#' + e.target.id + '"]');
        if (a) a.classList.add('active');
      }}
    }});
  }}, {{threshold: 0.3}});
  sections.forEach(s => obs.observe(s));
</script>
</body>
</html>"""

# ─── 更新 index.html ────────────────────────────────────
def update_index(date_str: str):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    ym = dt.strftime("%Y-%m")
    year, month = dt.year, dt.month

    content = INDEX_PATH.read_text(encoding="utf-8")

    # 1. 更新最新日报卡片标题
    # 日期标题
    content = re.sub(
        r'(<div class="card-title">)\d{4}年\d+月\d+日 AI日报(</div>)',
        f'\\g<1>{year}年{month}月{dt.day}日 AI日报\\g<2>',
        content, count=1
    )
    # href
    content = re.sub(
        r'(href="01-daily-reports/\d{4}-\d{2}/)\d{4}-\d{2}-\d{2}(\.html")',
        f'\\g<1>{date_str}\\g<2>',
        content, count=1
    )

    # 2. 更新日历 dailyData
    # 找到对应月份的 hasDaily 数组并追加当天
    day = dt.day
    pattern = rf"('{ym}':\s*\{{[^}}]*hasDaily:\s*\[)([\d,\s]*?)(\])"
    def add_day_to_array(m):
        days_str = m.group(2)
        days = [int(x.strip()) for x in days_str.split(',') if x.strip().isdigit()]
        if day not in days:
            days.append(day)
            days.sort()
        return m.group(1) + ",".join(map(str, days)) + m.group(3)
    new_content = re.sub(pattern, add_day_to_array, content, flags=re.DOTALL)

    # 3. 更新 totalCount
    new_count_pattern = rf"('{ym}':\s*\{{[^}}]*totalCount:\s*)(\d+)"
    def update_count(m):
        ym_block_start = content.find(f"'{ym}':")
        if ym_block_start == -1:
            return m.group(0)
        block = content[ym_block_start:ym_block_start+300]
        days_match = re.search(r'hasDaily:\s*\[([\d,\s]*?)\]', block)
        if days_match:
            days = [int(x.strip()) for x in days_match.group(1).split(',') if x.strip().isdigit()]
            if day not in days:
                days.append(day)
            return m.group(1) + str(len(days))
        return m.group(0)
    new_content = re.sub(new_count_pattern, update_count, new_content)

    # 4. 更新统计卡片数字（4月日报 / 5月日报）
    month_label = f"{month}月日报"
    new_content = re.sub(
        rf'(<div class="stat-number stat-purple">)\d+(</div>\s*<div class="stat-label">{month_label})',
        lambda m: m.group(1) + str(day) + m.group(2),
        new_content
    )

    # 5. 更新 today date in renderCalendar
    new_content = re.sub(
        r'const today = new Date\(\d+, \d+, \d+\)',
        f'const today = new Date({year}, {month-1}, {day})',
        new_content
    )

    INDEX_PATH.write_text(new_content, encoding="utf-8")
    print(f"✅ 更新 index.html 完成 (日历+卡片)")

# ─── 更新 data.json ─────────────────────────────────────
def update_data_json(date_str: str, data: dict):
    existing = {}
    if DATA_PATH.exists():
        try:
            existing = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    existing[date_str] = {
        "title": f"{date_str} AI日报",
        "hot_count": len(data.get("hot_topics", [])),
        "generated_at": datetime.datetime.utcnow().isoformat(),
    }
    DATA_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")

# ─── 主流程 ─────────────────────────────────────────────
def main(target_date: str = None):
    dt = datetime.datetime.strptime(target_date, "%Y-%m-%d") if target_date else today_cn()
    date_str = format_date(dt)
    print(f"🔬 熏儿开始生成 {date_str} AI日报...")

    # 创建目录
    month_dir = get_month_dir(dt)
    month_dir.mkdir(parents=True, exist_ok=True)

    report_path = get_report_path(dt)
    if report_path.exists():
        print(f"⚠️  {date_str} 日报已存在，跳过生成")
    else:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY 未设置")
        print("  📡 调用 OpenAI 生成内容...")
        prompt = build_prompt(date_str)
        data = call_openai(prompt)
        print("  ✍️  渲染 HTML...")
        html = render_html(data, date_str)
        report_path.write_text(html, encoding="utf-8")
        print(f"  ✅ 日报已生成: {report_path}")
        update_data_json(date_str, data)

    print("  🔄 更新 index.html...")
    update_index(date_str)
    print(f"✅ {date_str} 全部完成！")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    main(target)
