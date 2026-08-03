---
name: article-curation
version: 1.0.0
description: >-
  Daily curation of game design articles from GameRes forum board 6 (游戏策划).
  Fetches the latest threads via API, filters by relevance to system / combat /
  level / numerical module design (low priority for 文案/剧情/叙事), scores
  quality, reads and summarizes top candidates, and writes a deduplicated daily
  digest. Use for: 每日文章摘取, 论坛文章收集, 游戏设计文章日报, GameRes 摘取,
  定时文章收集, 策划学习材料整理.
  Do NOT use for: original game design work (use numerical-planning,
  combat-design, system-design, gameplay-design instead).
---

# Article Curation (GameRes 每日文章摘取)

Curate high-quality game design articles from the GameRes 游戏策划 forum
(`https://www.gameres.com/forum/b/6`) into a daily digest.

## Focus Scope

Priority topics (HIGH):

- **系统设计**: 系统拆解, 模块划分, UI流程, 系统依赖, 养成系统, 经济循环架构
- **战斗设计**: 伤害模型, 技能设计, Boss设计, 战斗节奏, 打击感, 职业平衡
- **关卡设计**: 关卡节奏, 难度曲线, 地图设计, 关卡结构, 引导设计
- **数值模块设计**: 数值框架, 公式, 成长曲线, 产出消耗, 概率/保底, 平衡性

Low priority (LOW, only include if exceptionally deep):

- 文案, 剧情, 叙事, 对白, 世界观包装

Exclude entirely:

- 招聘/求职, 广告/推广, 纯资讯转载无观点, 闲聊灌水, 纯求助提问帖

## Data Access

Forum list API (no login, no anti-bot observed):

```
GET https://www.gameres.com/api/v1/forum/boards/6?page_size=20&sort=dateline&cursor={unix_ts}
```

- `sort=dateline` = 最新发帖; `cursor` = unix timestamp of the last item of the
  previous page (omit for the first page).
- `page_size` 上限为 50，超过会返回 422。
- Article URL format: `https://www.gameres.com/forum/t/{id}` — body is readable
  without login.
- Fallback if the API fails: open `/forum/b/6` with the Browser tool and click
  "加载更多" to paginate.

## Archive Index (历史老文章索引)

全量历史索引已于 2026-08 生成：`digests/gameres-archive-index.md`（27088 帖，
按本技能标准评分，四大方向各 Top 40），原始数据在 `digests/gameres-archive.json`。
重跑脚本：工作区根目录 `crawl_gameres.py`（抓取+评分）与
`build_gameres_index.py`（生成索引）。日报中若发现与索引重复的老文，
直接引用索引条目即可。

## Workflow

Copy this checklist and track progress:

```
Task Progress:
- [ ] Step 1: Load state (last cursor + seen URLs)
- [ ] Step 2: Fetch new threads since last cursor
- [ ] Step 3: Filter and score candidates
- [ ] Step 4: Read and summarize top 3-5 articles
- [ ] Step 5: Write digest and update state
```

**Step 1: Load state**
Read `digests/state.json` (fields: `last_cursor`, `last_run`) and
`digests/seen-urls.txt` under the current workspace. If missing, this is the
first run: initialize state after Step 5 with the newest thread timestamp.

**Step 2: Fetch new threads**
Call the list API (WebFetch or curl). Collect threads whose `dateline` is newer
than `last_cursor`. If none, stop and report "今日无新帖".

**Step 3: Filter and score**
Apply the criteria in [references/curation-criteria.md](references/curation-criteria.md).
Keep candidates scoring >= 6/10, up to 5 articles. Prefer method/framework
articles (干货/深度/复盘) over opinion-only posts.

**Step 4: Read and summarize**
Open each selected article URL. Extract:

- 核心观点 (1-2 sentences)
- 关键方法/框架/公式 (3-5 bullets, keep original terms)
- 可借鉴点: one sentence on how this applies to our own design work

**Step 5: Write digest and update state**
Write `digests/gameres-{YYYY-MM-DD}.md` using the output template below.
Append all processed article URLs to `digests/seen-urls.txt` (dedup guard).
Update `digests/state.json` with the newest thread's `dateline` and today's date.

## Output Template

```markdown
# GameRes 策划文章日报 — {YYYY-MM-DD}

> 来源：GameRes 游戏策划版块（forum/b/6）｜新帖 {N} 篇，收录 {M} 篇

## 1. {文章标题}
- **链接**: {url}
- **作者/时间**: {author} · {date}｜浏览 {views} · 回复 {replies}
- **方向**: {系统设计 | 战斗设计 | 关卡设计 | 数值设计}
- **核心观点**: ...
- **关键方法**:
  - ...
- **可借鉴点**: ...

## 落选但值得留意（可选）
- {标题} — {一句话说明为什么没收录但值得看} ({url})
```

## Rules

- Never fabricate article content; every bullet must come from the fetched page.
- If an article is paywalled/login-gated, record it in 落选 list with the reason.
- Keep each article summary under 15 lines; depth over breadth.
