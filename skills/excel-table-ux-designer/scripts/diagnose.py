# -*- coding: utf-8 -*-
"""
Excel 表格排版体检器 / Excel Table Layout Auditor
=================================================
只读扫描，绝不修改原文件。输出分级问题清单（P0/P1/P2），每项含位置、影响、改法。

用法:
    python diagnose.py <file.xlsx>                # 人读报告
    python diagnose.py <file.xlsx> --json         # 机器读（供后续脚本消费）
    python diagnose.py <file.xlsx> --sheet 表名    # 只看某个 sheet
    python diagnose.py <file.xlsx> --max-rows 5000 # 大表抽样上限

依赖: openpyxl >= 3.0
设计依据: references/research/01~04（Few/Tufte 对齐与墨水比、WCAG 对比度、
         Luban 配置表契约、openpyxl 实测 API 行为）
"""
import sys
import json
import re
import argparse
from collections import Counter, defaultdict

try:
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter
except ImportError:
    sys.exit("缺少 openpyxl。请先安装：pip install openpyxl")

# ── 常量：Excel 默认值（来源: Microsoft 官方文档）────────────────────────────
EXCEL_DEFAULT_COL_WIDTH = 8.43   # 字符单位
EXCEL_DEFAULT_ROW_HEIGHT = 15.0  # pt
DEFAULT_COL_WIDTH_OPENPYXL = 13.0  # openpyxl 写入时的默认值（8+5）

# 判定阈值
LARGE_ROW_THRESHOLD = 40         # 超过此行数应冻结表头
LARGE_COL_THRESHOLD = 12         # 超过此列数应冻结首列
WIDE_TABLE_THRESHOLD = 25        # 超过此列数视为宽表
MAX_FILL_KINDS = 3               # 底色种类上限（表头+斑马纹+强调）
MAX_FONT_KINDS = 2               # 字体家族种类上限
MAX_SIZE_KINDS = 4               # 字号档位上限

CN_CHAR_RE = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")

# 分类维度列：值天然重复，不能按「主键重复」处理
NON_KEY_COL_RE = re.compile(
    r"年份|年度|^年$|月份|^月$|日期|^日$|季度|季度|周次|分类|类型|类别|等级|级别|"
    r"区域|地区|省份|城市|状态|部门|团队|组$|渠道|来源|平台|品类|标签",
    re.I,
)
# 像主键的列名。注意用 lookaround 而非 \bid\b：
# 「物料ID」里「料」与「I」之间没有 word boundary，\bid\b 匹配不到中文紧邻的 ID。
ID_COL_RE = re.compile(
    r"(?<![a-z])id(?![a-z])|编号|序号|代码|编码|uuid|guid",
    re.I,
)


# ── 工具函数 ────────────────────────────────────────────────────────────────
def display_width(value):
    """估算字符串在 Excel 中占用的字符宽度（中文/全角算 2）。"""
    if value is None:
        return 0
    s = str(value)
    w = 0
    for ch in s:
        w += 2 if CN_CHAR_RE.match(ch) else 1
    return w


def is_numeric_text(cell):
    """判断是否为「数字被存成文本」。"""
    if cell.value is None:
        return False
    if cell.data_type != "s":
        return False
    s = str(cell.value).strip()
    if not s:
        return False
    # 允许千分位、小数点、负号、百分号
    cleaned = s.replace(",", "").replace("，", "").rstrip("%")
    if not cleaned:
        return False
    try:
        float(cleaned)
        return True
    except ValueError:
        return False


def col_letter(idx):
    return get_column_letter(idx)


def has_any_border(border):
    """安全判断边框是否有任何一条边（未设置的边读回是 None，不是 Side 对象）。"""
    if border is None:
        return False
    for side_name in ("left", "right", "top", "bottom"):
        side = getattr(border, side_name, None)
        if side is not None and getattr(side, "style", None):
            return True
    return False


def compress_ranges(indices):
    """把 [1,2,3,5,7,8] 压成 "A-C, E, G-H"。"""
    if not indices:
        return ""
    idxs = sorted(set(indices))
    parts, start, prev = [], idxs[0], idxs[0]
    for i in idxs[1:]:
        if i == prev + 1:
            prev = i
            continue
        parts.append((start, prev))
        start = prev = i
    parts.append((start, prev))
    out = []
    for a, b in parts:
        out.append(col_letter(a) if a == b else f"{col_letter(a)}-{col_letter(b)}")
    return ", ".join(out)


# ── 单项检测器 ──────────────────────────────────────────────────────────────
class Issue:
    def __init__(self, level, code, title, where, impact, fix, count=0):
        self.level = level      # P0 / P1 / P2
        self.code = code
        self.title = title
        self.where = where
        self.impact = impact
        self.fix = fix
        self.count = count

    def as_dict(self):
        return {
            "level": self.level, "code": self.code, "title": self.title,
            "where": self.where, "impact": self.impact, "fix": self.fix,
            "count": self.count,
        }


def scan_sheet(ws, max_rows=5000):
    """扫描单个 sheet，返回 (issues, stats)。"""
    issues = []
    stats = {}

    # 实际数据边界
    max_row = ws.max_row or 0
    max_col = ws.max_column or 0
    stats["rows"] = max_row
    stats["cols"] = max_col

    # 空 sheet 直接跳过（避免对 1x1 空表误报「整列空白」）
    nonempty = sum(
        1
        for r in range(1, min(max_row, 200) + 1)
        for c in range(1, min(max_col, 50) + 1)
        if ws.cell(r, c).value not in (None, "")
    )
    if max_row == 0 or max_col == 0 or nonempty < 2:
        stats["empty_sheet"] = True
        return issues, stats

    sample_rows = min(max_row, max_rows)
    stats["sampled_rows"] = sample_rows
    stats["truncated"] = max_row > max_rows

    # 定位表头行（第一个含 >=2 个非空单元格的行；跳过以 ## 开头的配置表标记行）
    header_row = None
    for r in range(1, min(sample_rows, 10) + 1):
        vals = [ws.cell(r, c).value for c in range(1, min(max_col, 30) + 1)]
        nonempty = [v for v in vals if v not in (None, "")]
        if len(nonempty) >= 2:
            header_row = r
            break
    stats["header_row"] = header_row

    # 数据区起点：Luban 表必须跳过全部标记行（##var/##type/##group/##comment）
    # 否则标记行会被当成数据，污染主键/空值/数字格式等所有统计
    cfg_markers = set()
    a1v = ws.cell(1, 1).value
    if isinstance(a1v, str) and a1v.strip().startswith("##"):
        for r in range(1, min(10, max_row) + 1):
            v = ws.cell(r, 1).value
            if isinstance(v, str) and v.strip().startswith("##"):
                cfg_markers.add(r)
    data_start = (max(cfg_markers) + 1) if cfg_markers else ((header_row or 1) + 1)
    stats["data_start_row"] = data_start
    stats["cfg_marker_rows"] = sorted(cfg_markers)

    # ── 1. 冻结窗格 ────────────────────────────────────────────────────────
    frozen = ws.freeze_panes
    stats["freeze_panes"] = frozen
    need_row_freeze = max_row > LARGE_ROW_THRESHOLD
    need_col_freeze = max_col > LARGE_COL_THRESHOLD
    if need_row_freeze and not frozen:
        issues.append(Issue(
            "P1", "FREEZE_NONE", "未冻结表头",
            f"整表 {max_row} 行 × {max_col} 列，未设置冻结窗格",
            "下滑 40 行后表头消失，读者只能靠记忆对列；这是大表最高频的阅读障碍",
            f"冻结到表头下一行（本表应为 {col_letter(1)}{data_start}）；"
            f"列多则再冻主键列 → {col_letter(2)}{data_start}",
        ))
    elif frozen:
        # 冻结位置是否合理
        m = re.match(r"([A-Z]+)(\d+)", frozen)
        if m:
            fcol = 0
            for ch in m.group(1):
                fcol = fcol * 26 + (ord(ch) - 64)
            frow = int(m.group(2)) - 1
            stats["frozen_cols"] = fcol - 1
            stats["frozen_rows"] = frow
            if need_row_freeze and frow < (header_row or 1):
                issues.append(Issue(
                    "P2", "FREEZE_TOO_HIGH", "冻结位置偏上",
                    f"冻结于 {frozen}，冻结行数 {frow}，表头在第 {header_row} 行",
                    "表头仍会随滚动消失，冻结未真正生效",
                    f"改为冻结到表头下一行：{col_letter(fcol)}{data_start}",
                ))

    # ── 2. 列宽 ────────────────────────────────────────────────────────────
    width_info, unset_cols, narrow_cols = {}, [], []
    for c in range(1, min(max_col, 300) + 1):
        letter = col_letter(c)
        cd = ws.column_dimensions.get(letter)
        w = cd.width if cd is not None else None
        width_info[letter] = w
        if w is None:
            unset_cols.append(c)
            continue
        # 内容所需宽度估算
        need = 0
        for r in range(1, sample_rows + 1):
            need = max(need, display_width(ws.cell(r, c).value))
        need = min(need + 2, 60)
        if need > 0 and w + 0.5 < need and w < 50:
            narrow_cols.append((c, round(w, 1), need))
    stats["unset_width_cols"] = len(unset_cols)
    stats["narrow_cols"] = len(narrow_cols)

    if unset_cols and max_col > 3:
        issues.append(Issue(
            "P1", "COL_WIDTH_UNSET", "列宽全部沿用默认值",
            f"{len(unset_cols)} 列未设置列宽（默认 {EXCEL_DEFAULT_COL_WIDTH} 字符）",
            "宽内容被截断成 #### 或与邻列视觉粘连；长文本列尤其严重",
            "按内容分级设宽：ID 列 8-10、名称列 14-20、备注列 30-40（同类列必须同宽）",
            count=len(unset_cols),
        ))
    if narrow_cols:
        examples = "；".join(
            f"{col_letter(c)}（当前 {w}，约需 {n}）" for c, w, n in narrow_cols[:6]
        )
        issues.append(Issue(
            "P1", "COL_WIDTH_NARROW", "列宽小于内容所需",
            f"{len(narrow_cols)} 列内容被挤压：{examples}",
            "内容显示不全，读者要双击单格才能看全，破坏整列扫描节奏",
            "按「该列最长内容 + 2 字符」设宽；中文按 2 字符计",
            count=len(narrow_cols),
        ))

    # 同类列宽是否一致（用表头前 2 个字符判断同类）
    if header_row and max_col >= 4:
        groups = defaultdict(list)
        for c in range(1, max_col + 1):
            hv = ws.cell(header_row, c).value
            if hv:
                groups[str(hv)[:2]].append((c, width_info.get(col_letter(c))))
        inconsistent = [
            g for g, items in groups.items()
            if len(items) > 1 and len({w for _, w in items if w is not None}) > 1
        ]
        if inconsistent:
            issues.append(Issue(
                "P2", "COL_WIDTH_INCONSISTENT", "同类列宽度不统一",
                f"{len(inconsistent)} 组同名前缀列的宽度不一致，如：{'、'.join(inconsistent[:4])}",
                "视觉上列组被打散，读者难以感知「这几列是一组」",
                "按语义分组后，同组列统一宽度（3-4 档宽度即可，不要出现 20 种）",
                count=len(inconsistent),
            ))

    # ── 3. 表头样式 ────────────────────────────────────────────────────────
    if header_row:
        hdr_cells = [ws.cell(header_row, c) for c in range(1, max_col + 1)
                     if ws.cell(header_row, c).value not in (None, "")]
        if hdr_cells:
            bold_ratio = sum(1 for c in hdr_cells if c.font and c.font.bold) / len(hdr_cells)
            fill_ratio = sum(
                1 for c in hdr_cells
                if c.fill and c.fill.fill_type == "solid"
                and (c.fill.start_color.rgb or c.fill.start_color.index) not in (None, "00000000")
            ) / len(hdr_cells)
            stats["header_bold_ratio"] = round(bold_ratio, 2)
            stats["header_fill_ratio"] = round(fill_ratio, 2)
            if bold_ratio < 0.5 and fill_ratio < 0.5:
                issues.append(Issue(
                    "P1", "HEADER_PLAIN", "表头与数据无视觉区分",
                    f"表头行（第 {header_row} 行）仅 {bold_ratio:.0%} 加粗、{fill_ratio:.0%} 有底色",
                    "读者视线无法快速锁定列语义，每读一列都要回溯表头",
                    "表头两选一：浅灰底 #F0F0F0 + 深字 #262626（对比度 13.3:1），"
                    "或加粗 + 单条下边框 #D9D9D9",
                ))
            elif bold_ratio >= 0.5 and fill_ratio >= 0.9:
                pass  # 好

    # ── 4. 对齐 ────────────────────────────────────────────────────────────
    numeric_cols, centered_text_cols, centered_numeric_cols = [], [], []
    for c in range(1, min(max_col, 120) + 1):
        vals = [ws.cell(r, c) for r in range(data_start, sample_rows + 1)]
        vals = [v for v in vals if v.value not in (None, "")]
        if len(vals) < 3:
            continue
        num_cnt = sum(1 for v in vals if isinstance(v.value, (int, float)) and not isinstance(v.value, bool))
        txt_cnt = len(vals) - num_cnt
        aligns = Counter((v.alignment.horizontal or "general") for v in vals)
        top_align = aligns.most_common(1)[0][0]
        if num_cnt / len(vals) >= 0.8:
            if top_align == "center":
                centered_numeric_cols.append(c)
            elif top_align in ("left",):
                numeric_cols.append(c)
        elif txt_cnt / len(vals) >= 0.8:
            if top_align == "center":
                centered_text_cols.append(c)
    stats["centered_numeric_cols"] = len(centered_numeric_cols)
    stats["left_numeric_cols"] = len(numeric_cols)

    if centered_numeric_cols:
        issues.append(Issue(
            "P0", "ALIGN_NUM_CENTER", "数值列居中（破坏小数位对齐）",
            f"{len(centered_numeric_cols)} 个数值列居中：{compress_ranges(centered_numeric_cols)}",
            "各数位数不同时无法上下位比较大小，扫读速度显著下降——"
            "这是数值表最影响效率的单一问题",
            "改为右对齐 + 统一小数位（number_format 如 #,##0.00），使小数点纵向对齐",
            count=len(centered_numeric_cols),
        ))
    if numeric_cols:
        issues.append(Issue(
            "P2", "ALIGN_NUM_LEFT", "数值列左对齐",
            f"{len(numeric_cols)} 个数值列左对齐：{compress_ranges(numeric_cols)}",
            "个位数与千位数右端不齐，比较大小需逐位读数",
            "改右对齐",
            count=len(numeric_cols),
        ))
    if centered_text_cols and len(centered_text_cols) > max_col * 0.4:
        issues.append(Issue(
            "P2", "ALIGN_TEXT_CENTER", "文本列大面积居中",
            f"{len(centered_text_cols)}/{max_col} 列文本居中：{compress_ranges(centered_text_cols[:15])}",
            "居中的长文本左右起点均不固定，整列扫描时眼睛每次都要重新找起点",
            "文本/日期改左对齐；仅短代码类（≤4 字符）可居中",
            count=len(centered_text_cols),
        ))

    # ── 5. 数字存成文本 ────────────────────────────────────────────────────
    numeric_text_cells = []
    for c in range(1, min(max_col, 120) + 1):
        for r in range(data_start, sample_rows + 1):
            cell = ws.cell(r, c)
            if is_numeric_text(cell):
                numeric_text_cells.append(cell.coordinate)
    if numeric_text_cells:
        cols_affected = sorted({re.match(r"([A-Z]+)", c).group(1) for c in numeric_text_cells})
        issues.append(Issue(
            "P0", "NUM_AS_TEXT", "数字被存成文本",
            f"{len(numeric_text_cells)} 个单元格，涉及列 {', '.join(cols_affected[:10])}"
            f"（如 {', '.join(numeric_text_cells[:5])}）",
            "SUM/AVERAGE 结果为 0、排序按字符序（'10' < '9'）、右对齐设置无效、"
            "条件格式数值规则失效；且这些问题不会报警",
            "转真数值（优先级最高，必须先修这个再谈格式）：分列→完成，或脚本批量转换",
            count=len(numeric_text_cells),
        ))

    # ── 6. 合并单元格 ──────────────────────────────────────────────────────
    merges = list(ws.merged_cells.ranges)
    stats["merged_ranges"] = len(merges)
    if merges:
        # 区分：跨行合并（多用于数据区，最危险）vs 仅跨列（多用于标题）
        row_spanning = [m for m in merges if m.max_row > m.min_row]
        col_spanning = [m for m in merges if m.max_row == m.min_row]
        if row_spanning:
            issues.append(Issue(
                "P0", "MERGE_ROWSPAN", "数据区跨行合并单元格",
                f"{len(row_spanning)} 处跨行合并：{', '.join(str(m) for m in row_spanning[:5])}",
                "值只留在左上角格，其余为空——筛选、排序、SUM、透视表、"
                "以及任何脚本读取都会漏数（openpyxl 读合并区非左上格为 None）",
                "数据区禁用跨行合并：拆开并向下填充值；配置表若为工具链预设的子结构合并，"
                "需先确认程序读取逻辑再决定是否保留",
                count=len(row_spanning),
            ))
        if col_spanning:
            issues.append(Issue(
                "P2", "MERGE_COLSPAN", "跨列合并（建议改用居中跨列）",
                f"{len(col_spanning)} 处跨列合并：{', '.join(str(m) for m in col_spanning[:5])}",
                "合并后无法单独设置被合并格的对齐/宽度，复制粘贴时易错位",
                "标题类改用「设置单元格格式 → 对齐 → 水平对齐：跨列居中」"
                "（Center Across Selection），保持单元格独立",
                count=len(col_spanning),
            ))

    # ── 7. 网格线 ──────────────────────────────────────────────────────────
    grid_on = ws.sheet_view.showGridLines
    stats["gridlines_visible"] = grid_on
    if grid_on and max_row > 15 and max_col > 4:
        fill_any = any(
            ws.cell(r, c).fill and ws.cell(r, c).fill.fill_type == "solid"
            for r in range(1, min(sample_rows, 20) + 1)
            for c in range(1, min(max_col, 10) + 1)
        )
        issues.append(Issue(
            "P2", "GRIDLINES_ON", "默认网格线与自定义边框叠加",
            "工作表网格线可见" + ("，同时存在单元格填充" if fill_any else ""),
            "灰网格线是纯装饰性墨水，会与真正的边框争夺注意力；"
            "打印时还会出现无意义的细线",
            "视图 → 取消勾选「网格线」，改用表头下边框 + 合计行上边框做结构分隔",
        ))

    # ── 8. 底部/右侧边框滥用 ───────────────────────────────────────────────
    all_borders = 0
    for r in range(1, min(sample_rows, 60) + 1):
        for c in range(1, min(max_col, 30) + 1):
            if has_any_border(ws.cell(r, c).border):
                all_borders += 1
    cells_scanned = min(sample_rows, 60) * min(max_col, 30)
    stats["bordered_cell_ratio"] = round(all_borders / max(cells_scanned, 1), 2)
    if cells_scanned and all_borders / cells_scanned > 0.85:
        issues.append(Issue(
            "P1", "BORDER_FULL_GRID", "自绘全表边框（视觉像一张网）",
            f"约 {all_borders}/{cells_scanned} 个单元格四边都有边框，覆盖率 "
            f"{all_borders / cells_scanned:.0%}",
            "每格都被框住时，边框不再传递结构信息，退化等同于网格线，且视觉噪音大；"
            "这是「做了美化反而更难读」的典型",
            "只保留两条横线：表头下、合计行上（细线 #D9D9D9）；"
            "宽表可每 3-5 行加一条更淡的分隔线",
        ))

    # ── 9. 底色与字体种类 ──────────────────────────────────────────────────
    fills, fonts, sizes = Counter(), Counter(), Counter()
    for r in range(1, min(sample_rows, 200) + 1):
        for c in range(1, min(max_col, 40) + 1):
            cell = ws.cell(r, c)
            if cell.value in (None, ""):
                continue
            if cell.fill and cell.fill.fill_type == "solid":
                rgb = cell.fill.start_color.rgb
                if isinstance(rgb, str):
                    fills[rgb[-6:].upper()] += 1
            if cell.font:
                fonts[cell.font.name or "?"] += 1
                sizes[cell.font.size] += 1
    stats["fill_kinds"] = len(fills)
    stats["font_kinds"] = len(fonts)
    stats["size_kinds"] = len(sizes)
    stats["top_fills"] = fills.most_common(6)
    if len(fills) > MAX_FILL_KINDS:
        issues.append(Issue(
            "P1", "FILL_TOO_MANY", "底色种类过多",
            f"{len(fills)} 种填充色：{', '.join(f'#{k}' for k, _ in fills.most_common(6))}",
            "颜色一多就失去语义——读者无法判断哪种颜色代表什么，"
            "颜色从「信息」退化为「噪音」",
            f"砍到 ≤{MAX_FILL_KINDS} 种：表头底 + 斑马纹 + 一个强调色；"
            "其余改用文字/符号表达",
            count=len(fills),
        ))
    if len(fonts) > MAX_FONT_KINDS:
        issues.append(Issue(
            "P2", "FONT_TOO_MANY", "字体家族过多",
            f"{len(fonts)} 种字体：{', '.join(k for k, _ in fonts.most_common(5))}",
            "不同字体基线/字高不同，导致同一行内文字上下跳动；"
            "且字体缺失触发回退会让列宽跳动",
            f"统一到 ≤{MAX_FONT_KINDS} 种：中文主体一种（微软雅黑/等线），"
            "数字列一种等宽（Consolas）",
            count=len(fonts),
        ))
    if len(sizes) > MAX_SIZE_KINDS:
        issues.append(Issue(
            "P2", "SIZE_TOO_MANY", "字号档位过多",
            f"{len(sizes)} 档字号：{sorted(x for x in sizes if x)}",
            "字号是层级信号，档位超过 3-4 档后层级信息过载，读者不再感知大小差异",
            "收敛为 3 档：表头/正文/注释（如 11 / 11 / 9 pt）",
            count=len(sizes),
        ))

    # ── 10. 打印与呈现 ────────────────────────────────────────────────────
    ps = ws.page_setup
    stats["print_title_rows"] = ws.print_title_rows
    stats["orientation"] = ps.orientation
    stats["fitToWidth"] = ps.fitToWidth
    stats["scale"] = ps.scale
    stats["print_area"] = ws.print_area
    wide = max_col > WIDE_TABLE_THRESHOLD
    if wide and not ws.print_title_rows:
        issues.append(Issue(
            "P1", "PRINT_NO_TITLE", "宽表未设重复标题行",
            f"{max_col} 列的表，print_title_rows 为空",
            "打印/转 PDF 跨页后第二页起没有表头，读者不知道每列是什么",
            f"页面布局 → 打印标题 → 顶端标题行填 ${header_row or 1}:${header_row or 1}",
        ))
    if wide and ps.orientation != "landscape":
        issues.append(Issue(
            "P1", "PRINT_PORTRAIT", "宽表用纵向纸",
            f"{max_col} 列，页面方向为 {ps.orientation or 'portrait'}",
            "列被压到极窄或横向截断，打印后不可读",
            "改为横向（landscape），并设 fitToWidth=1（按 1 页宽缩放）",
        ))
    if not ws.print_area and max_row > 100:
        issues.append(Issue(
            "P2", "PRINT_NO_AREA", "未设打印区域",
            f"{max_row} 行，未指定 print_area",
            "打印时会带出表外的空白行/备注栏，或截断边缘列",
            "选中数据区 → 页面布局 → 打印区域 → 设置打印区域",
        ))

    # ── 11. 条件格式 / 数据验证 ────────────────────────────────────────────
    cf_count = 0
    try:
        for rng in ws.conditional_formatting:
            cf_count += len(ws.conditional_formatting[rng])
    except Exception:
        cf_count = 0
    try:
        dv_count = len(ws.data_validations.dataValidation) if ws.data_validations else 0
    except Exception:
        dv_count = 0
    stats["cond_format_rules"] = cf_count
    stats["data_validations"] = dv_count

    # ── 12. 重复主键（首列）──────────────────────────────────────────────
    if max_row > 3:
        key_col = 1
        # 若首列全空则顺延
        for c in range(1, min(max_col, 5) + 1):
            vals = [ws.cell(r, c).value for r in range(data_start, sample_rows + 1)]
            if sum(1 for v in vals if v not in (None, "")) >= max(1, len(vals) * 0.9):
                key_col = c
                break
        vals = [ws.cell(r, key_col).value for r in range(data_start, sample_rows + 1)]
        vals = [v for v in vals if v not in (None, "")]
        dup = [k for k, n in Counter(vals).items() if n > 1]
        stats["dup_keys"] = len(dup)
        if dup:
            hdr_txt = str(ws.cell(header_row or 1, key_col).value or "")
            # 主键应当「几乎全唯一」。判断三件事：
            # ① 列名像不像主键；② 是否明确是分类维度（年份/类型/部门…）；③ 重复占比
            non_key = bool(NON_KEY_COL_RE.search(hdr_txt))
            id_like = bool(ID_COL_RE.search(hdr_txt))
            dup_rows = sum(n for n in Counter(vals).values() if n > 1) - len(dup)
            dup_ratio = dup_rows / max(len(vals), 1)

            if non_key:
                # 年份/类型/部门这类维度列，重复是正常的，不该按 P0 报
                issues.append(Issue(
                    "P2", "DUP_NONKEY", "首列是分类维度列，值天然重复",
                    f"{col_letter(key_col)} 列（{hdr_txt}）有 {len(dup)} 个重复值，"
                    f"重复行占比 {dup_ratio:.0%}",
                    "该列看起来是「年份/类型/部门」这类分类维度，本来就会重复；"
                    "真正的风险是：如果它是主键，重复会导致导出覆盖",
                    "确认这列是否为主键。若不是，把它从首列移开或用真正的唯一键做冻结锚点；"
                    "若是，必须修掉重复",
                ))
            elif id_like or dup_ratio <= 0.15:
                issues.append(Issue(
                    "P0", "DUP_KEY", "疑似主键列存在重复值",
                    f"{col_letter(key_col)} 列（{hdr_txt}）有 {len(dup)} 个重复值："
                    f"{', '.join(str(d) for d in dup[:8])}",
                    "若为主键：导出时覆盖或报错，游戏内数据丢失；"
                    "若非主键，则该列不宜放在首位并冻结",
                    "加条件格式「重复值」标红做常驻预警；"
                    "Luban 配置表此项为硬性检查项（map 表主键必须唯一）",
                    count=len(dup),
                ))
            else:
                issues.append(Issue(
                    "P1", "DUP_HIGH", "首列重复值过多，可能不是主键",
                    f"{col_letter(key_col)} 列 {len(vals)} 行里有 {len(dup)} 个值重复"
                    f"（重复行占比 {dup_ratio:.0%}）",
                    "主键应当几乎全唯一。重复占比这么高，说明它更可能是分类列；"
                    "若真当主键用，导出会大面积覆盖",
                    "确认主键定义；真正的主键应换成唯一列，并对它做重复校验",
                    count=len(dup),
                ))

    # ── 13. 空行 / 空列 / 隐藏列 ──────────────────────────────────────────
    empty_cols = []
    for c in range(1, max_col + 1):
        if all(ws.cell(r, c).value in (None, "") for r in range(1, min(sample_rows, 500) + 1)):
            empty_cols.append(c)
    if empty_cols:
        issues.append(Issue(
            "P2", "EMPTY_COLS", "存在整列空白",
            f"{len(empty_cols)} 列整列无数据：{compress_ranges(empty_cols)}",
            "打断列组连续性，也让「按位置读取」的脚本偏移；打印时出现大片空白",
            "删除，或作为分组间隔列明确设窄（宽度 2-3）",
            count=len(empty_cols),
        ))

    hidden_cols = []
    for letter, cd in ws.column_dimensions.items():
        if cd.hidden:
            hidden_cols.append(letter)
    if hidden_cols:
        issues.append(Issue(
            "P2", "HIDDEN_COLS", "存在隐藏列",
            f"{len(hidden_cols)} 列被隐藏：{', '.join(hidden_cols[:10])}",
            "若其中含关键字段：读者会以为表里没有这个信息；"
            "程序按位置读取时仍会读隐藏列（隐藏≠删除），易造成「界面上看不到但确实生效」的隐蔽 bug",
            "关键字段不要隐藏；确需隐藏时在表头区加醒目标注「含隐藏列 N 个」",
            count=len(hidden_cols),
        ))

    # ── 14. 数字格式一致性 ────────────────────────────────────────────────
    if header_row:
        fmt_by_col = {}
        for c in range(1, min(max_col, 60) + 1):
            fmt_by_col[c] = Counter(
                ws.cell(r, c).number_format
                for r in range(data_start, min(sample_rows, data_start + 200) + 1)
                if isinstance(ws.cell(r, c).value, (int, float))
            )
        mixed, id_cols = [], []
        for c, fmts in fmt_by_col.items():
            if not fmts:
                continue
            top = fmts.most_common(1)[0][0]
            if top not in ("General", "general"):
                continue
            hdr = str(ws.cell(header_row, c).value or "")
            # 年份/编号/ID 列本来就该是 General 或 "0"，不该要求统一的数值格式
            if ID_COL_RE.search(hdr) or NON_KEY_COL_RE.search(hdr):
                id_cols.append(c)
            else:
                mixed.append(c)
        if len(mixed) > 3:
            issues.append(Issue(
                "P1", "NUMFMT_GENERAL", "数值列未设数字格式",
                f"{len(mixed)} 个数值列保持 General 格式：{compress_ranges(mixed[:15])}"
                + (f"（另有 {len(id_cols)} 个标识/年份列不需设，已排除）" if id_cols else ""),
                "小数位数参差（1.5 与 1.53846 混排），无法小数点对齐；"
                "大数没有千分位，位数难数",
                "统一格式：金额 #,##0 / 比率 0.0% / 系数 0.00；"
                "同一列小数位必须一致。注意：年份/ID/编号列**不要**加千分位",
                count=len(mixed),
            ))

    # ── 15. Luban 配置表契约（仅当疑似配置表）────────────────────────────
    a1 = ws.cell(1, 1).value
    is_luban = isinstance(a1, str) and a1.strip().startswith("##")
    stats["looks_like_luban"] = is_luban
    if is_luban:
        markers = {}
        for r in range(1, min(6, max_row) + 1):
            v = ws.cell(r, 1).value
            if isinstance(v, str) and v.strip().startswith("##"):
                markers[v.strip()] = r
        stats["luban_markers"] = markers
        missing = [k for k in ("##var", "##type") if not any(
            k in str(mk) for mk in markers)]
        if missing:
            issues.append(Issue(
                "P0", "LUBAN_HEADER", "配置表缺少必需的标记行",
                f"A1 以 ## 开头（疑似 Luban 表），但未找到 {'、'.join(missing)} 行；现有序："
                f"{', '.join(f'{k}@第{v}行' for k, v in markers.items())}",
                "Luban 依赖 ##var（字段名）与 ##type（类型）定位数据区；"
                "缺任一行会导致整表导出失败或字段全错位",
                "补齐标记行：##var / ##type / ##group / ##comment；类型名不得汉化（int 不能写成「整数」）",
            ))
        # 检查注释列是否加 #
        if header_row and False:
            pass
    elif max_col >= 4 and max_row >= 3:
        # 可能是配置表但 A1 不是 ##（配置表通常行数不多但列多，故不设高行数门槛）
        first_row_strs = [str(ws.cell(1, c).value or "") for c in range(1, min(max_col, 8) + 1)]
        looks_tabular = all(re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", s) for s in first_row_strs if s)
        if looks_tabular and any(first_row_strs):
            issues.append(Issue(
                "P2", "LUBAN_A1", "疑似配置表但 A1 未按约定标记",
                f"A1 = {ws.cell(1, 1).value!r}，首行字段名均为 ASCII 标识符",
                "若本表由 Luban/类似工具链读取，A1 不以 ## 开头会导致整表被跳过导出——"
                "表现为「表改了但游戏里没生效」",
                "确认工具链：若是 Luban 表，A1 改为 ## 并在下方补 ##var/##type 行；"
                "若纯人工登记表，可忽略此项",
            ))

    return issues, stats


def run(path, sheet_name=None, max_rows=5000):
    wb = load_workbook(path, data_only=False)
    result = {"file": path, "sheets": []}
    targets = [sheet_name] if sheet_name else wb.sheetnames
    for name in targets:
        if name not in wb.sheetnames:
            raise SystemExit(f"找不到 sheet: {name}")
        ws = wb[name]
        issues, stats = scan_sheet(ws, max_rows=max_rows)
        result["sheets"].append({
            "name": name,
            "stats": stats,
            "issues": [i.as_dict() for i in issues],
            "issue_count": {
                "P0": sum(1 for i in issues if i.level == "P0"),
                "P1": sum(1 for i in issues if i.level == "P1"),
                "P2": sum(1 for i in issues if i.level == "P2"),
            },
        })
    wb.close()
    return result


def render(result):
    """把结果渲染成人读报告。"""
    L = []
    L.append("═" * 66)
    L.append("  Excel 排版体检报告")
    L.append("═" * 66)
    L.append(f"文件: {result['file']}")
    L.append(f"Sheet 数: {len(result['sheets'])}")
    total = {"P0": 0, "P1": 0, "P2": 0}
    for sh in result["sheets"]:
        total["P0"] += sh["issue_count"]["P0"]
        total["P1"] += sh["issue_count"]["P1"]
        total["P2"] += sh["issue_count"]["P2"]
    L.append(f"问题总数: P0×{total['P0']}  P1×{total['P1']}  P2×{total['P2']}")
    L.append("")

    level_name = {
        "P0": "P0 硬伤 —— 会算错数 / 会读漏 / 会导出失败",
        "P1": "P1 效率 —— 看得见，但每次都要多花力气",
        "P2": "P2 打磨 —— 风格一致性与观感",
    }

    for sh in result["sheets"]:
        st = sh["stats"]
        L.append(f"── Sheet「{sh['name']}」" + "─" * 40)
        if st.get("empty_sheet"):
            L.append("   （空表，已跳过）")
            L.append("")
            continue
        if st.get("rows"):
            L.append(f"   规模: {st['rows']:,} 行 × {st['cols']} 列"
                     + (f"（抽样前 {st['sampled_rows']:,} 行）" if st.get("truncated") else ""))
        L.append(f"   表头行: 第 {st.get('header_row')} 行   "
                 f"数据起: 第 {st.get('data_start_row')} 行   "
                 f"冻结: {st.get('freeze_panes') or '无'}")
        L.append(f"   底色种类: {st.get('fill_kinds')}   字体: {st.get('font_kinds')} 种"
                 + (f"   标记行: {st.get('cfg_marker_rows')}" if st.get("cfg_marker_rows") else ""))
        L.append("")
        if not sh["issues"]:
            L.append("   ✓ 未发现明显排版问题")
            L.append("")
            continue
        for level in ("P0", "P1", "P2"):
            bucket = [i for i in sh["issues"] if i["level"] == level]
            if not bucket:
                continue
            L.append(f"   【{level_name[level]}】")
            for i in bucket:
                L.append(f"   [{i['code']}] {i['title']}")
                L.append(f"      · 位置: {i['where']}")
                L.append(f"      · 影响: {i['impact']}")
                L.append(f"      · 改法: {i['fix']}")
                L.append("")
        L.append("")
    L.append("═" * 66)
    L.append("说明: 本报告为只读扫描，未改动原文件。")
    L.append("      改造请用 beautify.py，它会先自动备份再动表。")
    L.append("═" * 66)
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Excel 表格排版体检器（只读）")
    ap.add_argument("file", help="xlsx/xlsm 路径")
    ap.add_argument("--sheet", default=None, help="只检查指定 sheet")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--max-rows", type=int, default=5000, help="每表抽样行数上限")
    ap.add_argument("-o", "--out", default=None, help="把报告写入文件")
    args = ap.parse_args()

    result = run(args.file, args.sheet, args.max_rows)
    text = json.dumps(result, ensure_ascii=False, indent=2) if args.json else render(result)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"报告已写入: {args.out}")
    else:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        print(text)


if __name__ == "__main__":
    main()
