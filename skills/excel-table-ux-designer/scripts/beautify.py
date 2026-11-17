# -*- coding: utf-8 -*-
"""
Excel 表格排版改造器 / Excel Table Layout Refiner
=================================================
在体检报告基础上执行排版改造。**强制先备份，再动表。**

用法:
    python beautify.py <file.xlsx>                      # 默认：自动判模式 + 修 P0/P1
    python beautify.py <file.xlsx> --fix P0,P1,P2       # 指定修复级别
    python beautify.py <file.xlsx> --mode config        # 强制配置表模式（保守）
    python beautify.py <file.xlsx> --mode report        # 强制汇报表模式（视觉）
    python beautify.py <file.xlsx> --dry-run            # 只列改动计划，不写文件
    python beautify.py <file.xlsx> --out new.xlsx       # 另存，不覆盖原文件
    python beautify.py <file.xlsx> --header-style dark  # 深色表头（配白字）
    python beautify.py <file.xlsx> --no-backup          # 不做备份（不推荐）

安全边界:
    · 合并单元格：只报告，不自动拆分（可能破坏数据结构）
    · 数据值：默认不改。数字存文本仅在 --convert-numeric 时转换
    · 透视表/图表/VBA：openpyxl 无法完整往返，检测到会警告
"""
import os
import sys
import re
import shutil
import argparse
from datetime import datetime
from collections import Counter, defaultdict

try:
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.formatting.rule import Rule, FormulaRule
    from openpyxl.styles.differential import DifferentialStyle
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    sys.exit("缺少 openpyxl。请先安装：pip install openpyxl")

# ── 设计令牌（来源: references/research/02 §4.5 实测 WCAG 对比度）──────────────
PALETTE = {
    "light": {
        "header_bg": "FFF0F0F0",   # Ant gray-3
        "header_fg": "FF262626",   # 13.28:1 AAA
        "divider":   "FFD9D9D9",   # Ant default border
        "body_fg":   "FF161616",   # 18.10:1 AAA
        "muted_fg":  "FF525252",   #  7.81:1 AAA
        "zebra":     "FFF4F4F4",   # Carbon Gray10
        "accent":    "FF0F62FE",   # Carbon Blue60, 5.00:1 AA
    },
    "dark": {
        "header_bg": "FF393939",   # Carbon Gray80
        "header_fg": "FFFFFFFF",   # 11.55:1 AAA
        "divider":   "FF8D8D8D",
        "body_fg":   "FF161616",
        "muted_fg":  "FF525252",
        "zebra":     "FFF4F4F4",
        "accent":    "FF0F62FE",
    },
}
FILL_WARN  = "FFFFEB9C"   # 空值标黄
FILL_ERROR = "FFFFC7CE"   # 重复值标红
FONT_CN    = "微软雅黑"
FONT_NUM   = "Consolas"
SZ_HEADER, SZ_BODY, SZ_NOTE = 11, 11, 9
ROW_H_HEADER, ROW_H_BODY = 22, 18

CN_RE = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")
LABAN_TYPE_WORDS = {"int", "long", "float", "double", "bool", "string", "text",
                    "datetime", "date", "time", "enum", "bean", "list", "map",
                    "array", "short", "byte"}


# ── 通用工具 ────────────────────────────────────────────────────────────────
def disp_width(v):
    if v is None:
        return 0
    w = 0
    for ch in str(v):
        w += 2 if CN_RE.match(ch) else 1
    return w


def is_num_text(cell):
    if cell.value is None or cell.data_type != "s":
        return False
    s = str(cell.value).strip()
    if not s:
        return False
    c = s.replace(",", "").replace("，", "").rstrip("%")
    if not c:
        return False
    try:
        float(c)
        return True
    except ValueError:
        return False


def has_any_border(border):
    """未设置的边读回是 None，不是 Side 对象，必须逐边安全判断。"""
    if border is None:
        return False
    for side_name in ("left", "right", "top", "bottom"):
        side = getattr(border, side_name, None)
        if side is not None and getattr(side, "style", None):
            return True
    return False


def detect_mode(ws):
    """判定 sheet 是配置表还是汇报表。"""
    a1 = ws.cell(1, 1).value
    if isinstance(a1, str) and a1.strip().startswith("##"):
        return "config", "A1 以 ## 开头（Luban 风格标记）"
    # 首行全是 ASCII 标识符 + 第二行含类型名 → 强配置表特征
    row1 = [ws.cell(1, c).value for c in range(1, min(ws.max_column or 0, 12) + 1)]
    row1s = [str(v) for v in row1 if v not in (None, "")]
    row2 = [str(ws.cell(2, c).value or "").lower() for c in range(1, min(ws.max_column or 0, 12) + 1)]
    ascii_ids = row1s and all(re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", s) for s in row1s)
    typed = sum(1 for v in row2 if v.split("(")[0].split("#")[0] in LABAN_TYPE_WORDS) >= 2
    if ascii_ids and typed:
        return "config", "首行为 ASCII 字段名且第二行为类型行"
    if ascii_ids and len(row1s) >= 5:
        return "config", "首行全为 ASCII 字段名（疑似配置表，保守处理）"
    return "report", "普通数据/汇报表"


def find_header_row(ws, max_scan=10):
    """定位「人看的表头行」。配置表要跳过 ## 标记行，取 ##var 行。"""
    # 先找 ##var
    for r in range(1, min(max_scan, ws.max_row or 1) + 1):
        v = ws.cell(r, 1).value
        if isinstance(v, str) and "##var" in v:
            return r
    for r in range(1, min(max_scan, ws.max_row or 1) + 1):
        vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column or 0, 30) + 1)]
        if len([v for v in vals if v not in (None, "")]) >= 2:
            return r
    return 1


def marker_rows(ws, limit=6):
    """配置表标记行下标集合（##var/##type/##group/##comment 等）。"""
    out = set()
    for r in range(1, min(limit, ws.max_row or 1) + 1):
        v = ws.cell(r, 1).value
        if isinstance(v, str) and v.strip().startswith("##"):
            out.add(r)
    return out


def backup(path):
    stem, ext = os.path.splitext(path)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = f"{stem}.backup-{ts}{ext}"
    shutil.copy2(path, dst)
    return dst


def preflight_risks(path, wb):
    """改造前风险检查：返回需告知用户的警告列表。"""
    warns = []
    ext = os.path.splitext(path)[1].lower()
    if ext == ".xlsm":
        warns.append("文件为 .xlsm（含宏）：必须以 keep_vba 加载并保持 .xlsm 后缀，否则宏会丢失")
    if ext == ".xls":
        warns.append(".xls 老格式：openpyxl 不支持，请先另存为 .xlsx")
    for ws in wb.worksheets:
        try:
            if getattr(ws, "_charts", None):
                warns.append(f"「{ws.title}」含图表对象：常规图表可往返，复杂图表可能降级")
        except Exception:
            pass
        try:
            if getattr(ws, "_images", None):
                warns.append(f"「{ws.title}」含图片/形状：openpyxl 往返有损，可能丢失")
        except Exception:
            pass
        try:
            if getattr(ws, "_pivots", None):
                warns.append(f"「{ws.title}」含数据透视表：openpyxl 支持极差，基本会丢")
        except Exception:
            pass
    return warns


# ── 各修复步骤 ──────────────────────────────────────────────────────────────
def step_widths(ws, header_row, mrows, mode, changes):
    """按内容估算设列宽；同类列统一宽度。"""
    max_col = min(ws.max_column or 0, 300)
    if max_col == 0:
        return
    need = {}
    for c in range(1, max_col + 1):
        w = 0
        for r in range(1, min(ws.max_row or 1, 500) + 1):
            w = max(w, disp_width(ws.cell(r, c).value))
        # +2 字符 padding，与诊断器口径保持一致
        need[c] = min(w + 2, 60)

    # 分档：把需求宽度归入 4 档，保证视觉整齐
    def bucket(w):
        if w <= 8:
            return 8
        if w <= 14:
            return 14
        if w <= 22:
            return 20
        if w <= 34:
            return 30
        return min(w, 50)

    # 同类列（表头前 2 字符相同）取该组最大需求
    group_max = defaultdict(int)
    col_group = {}
    for c in range(1, max_col + 1):
        hv = str(ws.cell(header_row, c).value or "")
        g = hv[:2].strip() or f"__col{c}"
        col_group[c] = g
        group_max[g] = max(group_max[g], need[c])

    old = {}
    for c in range(1, max_col + 1):
        letter = get_column_letter(c)
        cd = ws.column_dimensions.get(letter)
        old[c] = cd.width if cd else None
        new_w = bucket(group_max[col_group[c]]) if group_max[col_group[c]] > 0 else bucket(need[c])
        ws.column_dimensions[letter].width = new_w
    n_changed = sum(1 for c in old if old[c] is None or abs((old[c] or 0) - ws.column_dimensions[get_column_letter(c)].width) > 0.5)
    if n_changed:
        changes.append(f"列宽：按内容分 4 档重设 {n_changed} 列（同类列已统一）")


def step_row_heights(ws, header_row, mrows, mode, changes):
    if mode != "report":
        return
    max_row = min(ws.max_row or 0, 5000)
    for r in range(1, max_row + 1):
        if r == header_row:
            ws.row_dimensions[r].height = ROW_H_HEADER
        elif ws.row_dimensions[r].height in (None,) or ws.row_dimensions[r].height == 15:
            ws.row_dimensions[r].height = ROW_H_BODY
    changes.append(f"行高：表头 {ROW_H_HEADER}pt、正文 {ROW_H_BODY}pt")


def step_header_style(ws, header_row, mrows, mode, changes, header_style="light", font_cn=FONT_CN):
    """表头样式。config 模式只加粗 + 下边框，不加底色，避免污染程序读取。"""
    pal = PALETTE[header_style]
    max_col = min(ws.max_column or 0, 300)
    n = 0
    for c in range(1, max_col + 1):
        cell = ws.cell(header_row, c)
        if cell.value in (None, ""):
            continue
        cell.font = Font(
            name=font_cn,
            size=SZ_HEADER, bold=True,
            color=pal["header_fg"] if mode == "report" else "FF000000",
        )
        if mode == "report":
            cell.fill = PatternFill("solid", start_color=pal["header_bg"])
        cell.alignment = Alignment(
            horizontal="center" if disp_width(cell.value) <= 6 else "left",
            vertical="center", wrap_text=False,
        )
        cell.border = Border(bottom=Side(style="medium", color=pal["divider"]))
        n += 1
    changes.append(f"表头：{n} 列加粗"
                   + ("+ 浅灰底 #F0F0F0 + 下分隔线" if mode == "report" else "+ 下分隔线（未加底色，保持程序可读）"))


def step_clear_full_grid(ws, header_row, mrows, mode, changes):
    """清掉自绘全表边框，只在表头下与合计行上留线。"""
    if mode != "report":
        return
    max_row = min(ws.max_row or 0, 5000)
    max_col = min(ws.max_column or 0, 300)
    cleared = 0
    for r in range(1, max_row + 1):
        if r == header_row:
            continue
        for c in range(1, max_col + 1):
            cell = ws.cell(r, c)
            if has_any_border(cell.border):
                cell.border = Border()
                cleared += 1
    # 合计行上边框
    total_rows = []
    for r in range(max_row, max(header_row, 1), -1):
        for c in range(1, min(max_col, 6) + 1):
            v = ws.cell(r, c).value
            if isinstance(v, str) and re.search(r"合计|总计|小计|总[计数]|Total", v):
                total_rows.append(r)
                break
        if total_rows:
            break
    for r in total_rows:
        for c in range(1, max_col + 1):
            cell = ws.cell(r, c)
            cell.border = Border(top=Side(style="thin", color=PALETTE["light"]["divider"]))
            cell.font = Font(name=cell.font.name if cell.font and cell.font.name else FONT_CN,
                             size=cell.font.size if cell.font and cell.font.size else SZ_BODY,
                             bold=True)
    if cleared:
        changes.append(f"边框：清除 {cleared} 个单元格的四边框，改为「表头下 + 合计行上」两条横线")
    if total_rows:
        changes.append(f"合计行：第 {total_rows[0]} 行加上边框并加粗")


LEGEND_RE = re.compile(
    r"图例|图注|说明[:：]|legend|红\s*[=＝]|黄\s*[=＝]|绿\s*[=＝]|蓝\s*[=＝]|灰\s*[=＝]|"
    r"表示|代表|标记为|标注|highlight|color\s*code",
    re.I,
)


def find_legend(ws, data_start):
    """检测表头上方是否存在图例说明。

    血泪来源：真实测试里 A1 明写「客户分级：红=战略 黄=重点 绿=一般」，
    脚本仍按「颜色 >3 种」把 15 个格子清空了 —— 用户的业务语义被抹掉。
    用户用颜色承载语义这件事，脚本无法从色值本身判断，只能从图例文字判断。
    """
    for r in range(1, min(data_start, 8) + 1):
        vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column or 0, 12) + 1)]
        line = " ".join(str(v) for v in vals if v not in (None, ""))
        if line and LEGEND_RE.search(line):
            return r, line[:80]
    return None, None


def step_fill_normalize(ws, header_row, mrows, mode, changes, max_kinds=3, data_start=None):
    """收敛底色种类。**检测到图例就一律不动。**"""
    if mode != "report":
        return
    ds = data_start or (header_row + 1)
    max_row = min(ws.max_row or 0, 5000)
    max_col = min(ws.max_column or 0, 300)
    kinds = Counter()
    for r in range(1, max_row + 1):
        for c in range(1, max_col + 1):
            cell = ws.cell(r, c)
            if cell.value in (None, ""):
                continue
            if cell.fill and cell.fill.fill_type == "solid":
                rgb = cell.fill.start_color.rgb
                if isinstance(rgb, str) and rgb not in ("00000000",):
                    kinds[rgb[-6:].upper()] += 1
    if len(kinds) <= max_kinds:
        return

    # ★ 先查图例：有图例 = 颜色是信息，不是噪音
    lr, ltext = find_legend(ws, ds)
    if lr:
        changes.append(
            f"底色：发现图例（第 {lr} 行「{ltext}」），**保留全部 {len(kinds)} 种颜色未做清理**"
            f"——颜色在这里承载业务语义，不能当装饰删掉"
        )
        return

    cleared = 0
    for r in range(header_row + 1, max_row + 1):
        if r in mrows:
            continue
        for c in range(1, max_col + 1):
            cell = ws.cell(r, c)
            if cell.value in (None, ""):
                continue
            if cell.fill and cell.fill.fill_type == "solid":
                cell.fill = PatternFill(fill_type=None)
                cleared += 1
    if cleared:
        changes.append(
            f"底色：未发现图例，清除数据区 {cleared} 个单元格的自定义填充"
            f"（原 {len(kinds)} 种 → 收敛为表头色 1 种）"
            f"；若这些颜色其实有语义，请用备份还原并在表头加一行图例，我会保留"
        )


def step_zebra(ws, header_row, mrows, mode, changes, enable):
    """斑马纹。仅宽表启用（调研：窄表用斑马纹反而增加困惑）。"""
    if mode != "report" or not enable:
        return
    max_col = min(ws.max_column or 0, 300)
    max_row = min(ws.max_row or 0, 5000)
    if max_col < 20:
        changes.append("斑马纹：跳过（表宽 < 20 列，窄表加隔行底色反而干扰阅读）")
        return
    fill = PatternFill("solid", start_color=PALETTE["light"]["zebra"])
    n = 0
    for r in range(header_row + 1, max_row + 1):
        if (r - header_row) % 2 == 0:
            continue
        for c in range(1, max_col + 1):
            cell = ws.cell(r, c)
            if cell.fill is None or cell.fill.fill_type != "solid":
                cell.fill = fill
                n += 1
    changes.append(f"斑马纹：{n} 个单元格加 #F4F4F4 隔行底色（宽表防串行）")


def is_num_text_val(s):
    """判断裸值是否为「长得像数字的文本」。"""
    if not isinstance(s, str):
        return False
    t = s.strip().replace(",", "").replace("，", "").rstrip("%")
    if not t:
        return False
    try:
        float(t)
        return True
    except ValueError:
        return False


def step_alignment(ws, header_row, mrows, mode, changes):
    """数值右对齐、文本左对齐、日期左对齐。

    ⚠️ 关键：即使未开启 --convert-numeric，也要把「数字存成文本」的列按数值列对待，
    否则会被误判成文本列而左对齐 —— 那是在加重问题而不是修问题。
    """
    max_col = min(ws.max_column or 0, 200)
    max_row = min(ws.max_row or 0, 5000)
    right_n = left_n = 0
    for c in range(1, max_col + 1):
        # 采样判断列类型
        vals = []
        for r in range(header_row + 1, min(max_row, header_row + 300) + 1):
            if r in mrows:
                continue
            v = ws.cell(r, c).value
            if v not in (None, ""):
                vals.append(v)
        if len(vals) < 3:
            continue
        num = sum(1 for v in vals
                  if (isinstance(v, (int, float)) and not isinstance(v, bool))
                  or is_num_text_val(v))
        is_num_col = num / len(vals) >= 0.8
        for r in range(header_row + 1, max_row + 1):
            if r in mrows:
                continue
            cell = ws.cell(r, c)
            if cell.value in (None, ""):
                continue
            if is_num_col:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                right_n += 1
            else:
                # 短代码（≤4 字符）允许居中，其余左对齐
                if disp_width(cell.value) <= 4:
                    continue
                cell.alignment = Alignment(horizontal="left", vertical="center")
                left_n += 1
    if right_n or left_n:
        changes.append(f"对齐：{right_n} 个数值格右对齐、{left_n} 个文本格左对齐（短代码保留居中）")


# 标识类列：不能加千分位（年份 2026 → "2,026"、ID 1000123 → "1,000,123" 都是明显错误）
# 用 lookaround 而非 \bid\b：「物料ID」里「料」与「I」之间没有 word boundary
ID_LIKE_RE = re.compile(
    r"(?<![a-z])id(?![a-z])|编号|序号|代码|编码|号码|号$|no\.?$|code|key|"
    r"年份|年度|^年$|phone|电话|手机|邮编|卡号|身份证|批次|version|版本",
    re.I,
)
# 金额/数量类：明确是数值标量，才配 #,##0
SCALAR_RE = re.compile(
    r"额|量|数|价|费|收|支|成本|利润|销量|流水|库存|gmv|amount|revenue|price|cost|qty|count|total",
    re.I,
)
# 分类维度列：值天然重复，不能当主键做「重复值标红」
NON_KEY_COL_RE = re.compile(
    r"年份|年度|^年$|月份|^月$|日期|^日$|季度|周次|分类|类型|类别|等级|级别|"
    r"区域|地区|省份|城市|状态|部门|团队|组$|渠道|来源|平台|品类|标签",
    re.I,
)


def step_number_format(ws, header_row, mrows, mode, changes):
    """按列推断数字格式，使小数位一致。"""
    if mode != "report":
        return
    max_col = min(ws.max_column or 0, 200)
    max_row = min(ws.max_row or 0, 5000)
    applied = 0
    skipped_id = []
    for c in range(1, max_col + 1):
        vals = []
        for r in range(header_row + 1, min(max_row, header_row + 300) + 1):
            v = ws.cell(r, c).value
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                vals.append(v)
        if len(vals) < 3:
            continue
        all_int = all(float(v).is_integer() for v in vals)
        max_abs = max(abs(float(v)) for v in vals)
        hdr = str(ws.cell(header_row, c).value or "")

        if re.search(r"率|比例|占比|rate|ratio|percent", hdr, re.I):
            fmt = "0.0%"
        elif ID_LIKE_RE.search(hdr):
            # 标识/年份：原样显示，绝不加千分位
            fmt = "0"
            skipped_id.append(hdr or get_column_letter(c))
        elif all_int and not SCALAR_RE.search(hdr) \
                and all(len(str(abs(int(v)))) == 4 and 1900 <= abs(v) <= 2100 for v in vals):
            # 列名没有数值含义、值全是 1900-2100 的四位整数 → 极高概率是年份
            fmt = "0"
            skipped_id.append(hdr or get_column_letter(c))
        elif all_int:
            fmt = "#,##0"
        elif max_abs < 1:
            fmt = "0.00"
        else:
            fmt = "#,##0.00"
        for r in range(header_row + 1, max_row + 1):
            cell = ws.cell(r, c)
            if isinstance(cell.value, (int, float)) and not isinstance(cell.value, bool):
                if cell.number_format in ("General", "general", None):
                    cell.number_format = fmt
                    applied += 1
    if applied:
        changes.append(f"数字格式：处理 {applied} 个数值格（小数 #,##0.00 / 整数 #,##0 / 比率 0.0%）")
    if skipped_id:
        changes.append(f"数字格式：{len(skipped_id)} 个标识/年份列（{', '.join(skipped_id[:5])}）"
                       f"保持原样显示，未加千分位")


def step_convert_numeric(ws, header_row, mrows, mode, changes, enabled):
    """数字存文本 → 转真数值（可选，默认关闭）。"""
    if not enabled:
        return
    max_col = min(ws.max_column or 0, 200)
    max_row = min(ws.max_row or 0, 5000)
    converted = 0
    for c in range(1, max_col + 1):
        cells = [ws.cell(r, c) for r in range(header_row + 1, max_row + 1)]
        cand = [x for x in cells if is_num_text(x)]
        if not cand or len(cand) / max(len([x for x in cells if x.value not in (None, "")]), 1) < 0.8:
            continue
        for cell in cand:
            s = str(cell.value).strip().replace(",", "").replace("，", "").rstrip("%")
            try:
                f = float(s)
                cell.value = int(f) if f.is_integer() and "%" not in str(cell.value) else f
                cell.data_type = "n"
                converted += 1
            except ValueError:
                pass
    if converted:
        changes.append(f"数字类型：{converted} 个「数字存成文本」单元格转为真数值")


def step_freeze(ws, header_row, mrows, mode, changes):
    max_row = ws.max_row or 0
    max_col = ws.max_column or 0
    # 配置表有多行标记（##var/##type/##group/##comment），要全部钉住
    freeze_row = (max(mrows) + 1) if mrows else (header_row + 1)
    if max_row <= 40 and max_col <= 12:
        return
    if max_col > 12:
        ws.freeze_panes = f"B{freeze_row}"
        changes.append(f"冻结窗格：{ws.freeze_panes}（同时冻结表头与前 1 列）")
    else:
        ws.freeze_panes = f"A{freeze_row}"
        changes.append(f"冻结窗格：{ws.freeze_panes}（冻结表头）")


def step_gridlines(ws, header_row, mrows, mode, changes):
    if ws.sheet_view.showGridLines:
        ws.sheet_view.showGridLines = False
        changes.append("网格线：已关闭（改用结构线分隔）")


def step_font_unify(ws, header_row, mrows, mode, changes, font_cn=FONT_CN):
    if mode != "report":
        return
    max_col = min(ws.max_column or 0, 200)
    max_row = min(ws.max_row or 0, 5000)
    for c in range(1, max_col + 1):
        # 判断是否数字列
        vals = [ws.cell(r, c).value for r in range(header_row + 1, min(max_row, header_row + 100) + 1)]
        vals = [v for v in vals if v not in (None, "")]
        is_num = vals and sum(1 for v in vals if isinstance(v, (int, float))) / len(vals) >= 0.8
        fname = FONT_NUM if is_num else font_cn
        for r in range(header_row + 1, max_row + 1):
            if r in mrows:
                continue
            cell = ws.cell(r, c)
            if cell.value in (None, ""):
                continue
            cur = cell.font
            cell.font = Font(
                name=fname,
                size=(cur.size if cur and cur.size and cur.size in (SZ_BODY, SZ_NOTE) else SZ_BODY),
                bold=(cur.bold if cur else False),
                italic=(cur.italic if cur else False),
                color=(cur.color if cur and cur.color and cur.color.rgb else PALETTE["light"]["body_fg"]),
            )
    changes.append(f"字体：中文列统一 {font_cn}、数字列统一 {FONT_NUM}，字号收敛为 {SZ_BODY}pt")


def step_cond_format(ws, header_row, mrows, mode, changes, data_start=None):
    """条件格式：重复值标红（唯一键列）+ 空值标黄（前若干列）。"""
    max_row = min(ws.max_row or 0, 5000)
    if max_row < 3:
        return
    # 配置表有 4 行标记，数据从 max(mrows)+1 开始；否则从表头下一行开始
    data_first = data_start if data_start else ((max(mrows) + 1) if mrows else (header_row + 1))
    if data_first > max_row:
        return
    added = []

    # 主键列：必须是「像主键 + 几乎全唯一」的列。
    # 早期版本直接取首列，导致「年份」列（2026 出现两次）被误加重复值标红。
    key_col = None
    for c in range(1, min(ws.max_column or 1, 6) + 1):
        vals = [ws.cell(r, c).value for r in range(data_first, max_row + 1)]
        vals = [v for v in vals if v not in (None, "")]
        if len(vals) < 3:
            continue
        hdr = str(ws.cell(header_row, c).value or "")
        if NON_KEY_COL_RE.search(hdr):
            continue                      # 分类维度列，跳过
        uniq_ratio = len(set(vals)) / len(vals)
        if ID_LIKE_RE.search(hdr) or uniq_ratio >= 0.95:
            key_col = c
            break

    if key_col:
        kletter = get_column_letter(key_col)
        ws.conditional_formatting.add(
            f"{kletter}{data_first}:{kletter}{max_row}",
            Rule(type="duplicateValues",
                 dxf=DifferentialStyle(fill=PatternFill("solid", start_color=FILL_ERROR))),
        )
        added.append(f"{kletter} 列（{ws.cell(header_row, key_col).value}）重复值标红")
    else:
        added.append("未找到唯一键列，跳过重复值校验（避免对年份/分类列误标红）")

    # 空值标黄：只对前 6 列，避免大面积刷黄
    for c in range(1, min(ws.max_column or 1, 6) + 1):
        letter = get_column_letter(c)
        ws.conditional_formatting.add(
            f"{letter}{data_first}:{letter}{max_row}",
            FormulaRule(formula=[f"AND(LEN(${letter}{data_first})=0,ROW()>{header_row})"],
                        fill=PatternFill("solid", start_color=FILL_WARN)),
        )
    added.append("前 6 列空值标黄")
    changes.append("条件格式：" + "、".join(added) + "（常驻预警，非一次性上色）")


def _set_fit_to_width(ws):
    """设置「按 1 页宽缩放」，绕过 openpyxl 的 property 转发。

    ⚠️ 两层坑：
    1. `ps.fitToPage = True` 转发到 `sheet_properties.pageSetUpPr.fitToPage`，
       某些文件该值为 None → AttributeError。
    2. 更隐蔽的是 `PageSetup._parent` 本身可能是 None，此时连
       `sheet_properties` 都取不到（错误信息形如
       "'NoneType' object has no attribute 'sheet_properties'"）。
       真机压测 200 列 × 3000 行的表时踩到，小样本不复现。

    所以这里直接操作 worksheet 的 sheet_properties，并保留降级路径。
    """
    try:
        from openpyxl.worksheet.properties import PageSetupProperties
        wspr = ws.sheet_properties
        if wspr is None:
            return False
        if wspr.pageSetUpPr is None:
            wspr.pageSetUpPr = PageSetupProperties()
        wspr.pageSetUpPr.fitToPage = True
        ps = ws.page_setup
        ps.fitToWidth = 1
        ps.fitToHeight = 0
        return True
    except Exception:
        return False


def step_print(ws, header_row, mrows, mode, changes):
    """打印设置。任何一项失败都只降级，不允许中断整个改造流程。"""
    max_row = ws.max_row or 0
    max_col = ws.max_column or 0
    if max_col < 8 and max_row < 40:
        return
    notes = []
    try:
        ps = ws.page_setup
        ps.orientation = "landscape" if max_col > 10 else (ps.orientation or "portrait")
        ps.paperSize = 9  # A4
    except Exception as e:
        changes.append(f"打印：页面方向/纸张设置失败（{type(e).__name__}），已跳过")
        return

    if not _set_fit_to_width(ws):
        try:
            ws.page_setup.scale = 80
            notes.append("按页宽缩放不可用，已降级为固定 80% 缩放")
        except Exception:
            notes.append("缩放设置失败，请手动在页面布局里调整")

    try:
        # 配置表要把全部标记行都作为重复标题行，否则第 2 页只剩 ##var 没有类型
        title_end = max(mrows) if mrows else header_row
        ws.print_title_rows = f"$1:${title_end}"
    except Exception:
        notes.append("重复标题行设置失败")
    try:
        ws.print_area = f"A1:{get_column_letter(min(max_col, 16384))}{min(max_row, 1048576)}"
        ws.page_margins.left = ws.page_margins.right = 0.4
        ws.page_margins.top = ws.page_margins.bottom = 0.5
        ws.oddFooter.center.text = "第 &P 页 / 共 &N 页"
        ws.oddFooter.right.text = "&F  &A"
    except Exception:
        notes.append("打印区域/页脚设置失败")

    changes.append("打印：A4 " + ("横向" if ps.orientation == "landscape" else "纵向")
                   + "、重复标题行、页脚含页码/文件名/sheet 名"
                   + ("；" + "；".join(notes) if notes else ""))


def step_hidden_warn(ws, header_row, mrows, mode, changes):
    hidden = [l for l, cd in ws.column_dimensions.items() if cd.hidden]
    if hidden:
        changes.append(f"⚠ 保留 {len(hidden)} 个隐藏列未处理（{', '.join(hidden[:8])}）——"
                       f"若其中含关键字段请取消隐藏；程序按位置读取时隐藏列仍会生效")


def _safe(step_fn, *args, changes=None, label=""):
    """执行单个改造步骤。失败只记录，不中断整个流程。

    设计原则：宁可少改一项，也不能让脚本半途崩溃留下半成品文件。
    """
    try:
        step_fn(*args)
        return True
    except Exception as e:
        if changes is not None:
            changes.append(f"⚠ 步骤「{label or step_fn.__name__}」失败已跳过（{type(e).__name__}: {e}）")
        return False


# ── 主流程 ──────────────────────────────────────────────────────────────────
def refine(path, mode="auto", levels=("P0", "P1", "P2"), out=None,
           header_style="light", do_backup=True, dry_run=False,
           convert_numeric=False, zebra=None, font_cn=FONT_CN, skip_font=False):
    warns = []
    wb = load_workbook(path, keep_vba=os.path.splitext(path)[1].lower() == ".xlsm")
    warns += preflight_risks(path, wb)

    report = []
    for ws in wb.worksheets:
        a1 = ws.cell(1, 1).value
        if ws.max_row in (None, 0, 1) and ws.max_column in (None, 0, 1) and a1 in (None, ""):
            report.append((ws.title, "空表", [], []))
            continue

        m, reason = detect_mode(ws)
        use_mode = m if mode == "auto" else mode
        header_row = find_header_row(ws)
        mrows = marker_rows(ws) if use_mode == "config" else set()
        # 数据区起点：配置表要跳过全部 ## 标记行（与 diagnose.py 口径一致）
        data_start = (max(mrows) + 1) if mrows else (header_row + 1)

        changes = []
        # 列宽：任何模式都修（纯视觉，不影响程序）
        _safe(step_widths, ws, header_row, mrows, use_mode, changes,
              changes=changes, label="列宽")
        # P0
        _safe(step_convert_numeric, ws, header_row, mrows, use_mode, changes, convert_numeric,
              changes=changes, label="数字类型转换")
        _safe(step_alignment, ws, header_row, mrows, use_mode, changes,
              changes=changes, label="对齐")
        # P1
        _safe(step_header_style, ws, header_row, mrows, use_mode, changes, header_style, font_cn,
              changes=changes, label="表头样式")
        _safe(step_clear_full_grid, ws, header_row, mrows, use_mode, changes,
              changes=changes, label="边框精简")
        _safe(step_fill_normalize, ws, header_row, mrows, use_mode, changes, 3, data_start,
              changes=changes, label="底色收敛")
        _safe(step_row_heights, ws, header_row, mrows, use_mode, changes,
              changes=changes, label="行高")
        _safe(step_zebra, ws, header_row, mrows, use_mode, changes,
              zebra if zebra is not None else True,
              changes=changes, label="斑马纹")
        _safe(step_freeze, ws, header_row, mrows, use_mode, changes,
              changes=changes, label="冻结窗格")
        _safe(step_gridlines, ws, header_row, mrows, use_mode, changes,
              changes=changes, label="网格线")
        _safe(step_print, ws, header_row, mrows, use_mode, changes,
              changes=changes, label="打印设置")
        _safe(step_cond_format, ws, header_row, mrows, use_mode, changes, data_start,
              changes=changes, label="条件格式")
        # P2
        if "P2" in levels:
            _safe(step_number_format, ws, header_row, mrows, use_mode, changes,
                  changes=changes, label="数字格式")
            if not skip_font:
                _safe(step_font_unify, ws, header_row, mrows, use_mode, changes, font_cn,
                      changes=changes, label="字体统一")
        _safe(step_hidden_warn, ws, header_row, mrows, use_mode, changes,
              changes=changes, label="隐藏列提示")

        report.append((ws.title, f"{use_mode}（{reason}）", changes, []))

    bpath = None
    if not dry_run:
        target = out if out else path
        if do_backup and not out:
            bpath = backup(path)
        try:
            wb.save(target)
        except Exception as e:
            wb.close()
            raise SystemExit(
                f"保存失败：{type(e).__name__}: {e}\n"
                f"原文件未被改动" + (f"，备份在 {bpath}" if bpath else "")
            )
    wb.close()
    return report, warns, bpath


def render(report, warns, bpath, dry_run):
    L = []
    L.append("═" * 66)
    L.append("  Excel 排版改造" + ("（预演，未写文件）" if dry_run else "完成"))
    L.append("═" * 66)
    if bpath:
        L.append(f"备份: {bpath}")
        L.append("")
    if warns:
        L.append("⚠ 风险提示")
        for w in warns:
            L.append(f"   · {w}")
        L.append("")
    for title, mode_desc, changes, _ in report:
        L.append(f"── Sheet「{title}」  模式: {mode_desc}")
        if not changes:
            L.append("   （无改动）")
        for ch in changes:
            L.append(f"   ✓ {ch}")
        L.append("")
    L.append("═" * 66)
    L.append("提示: 请打开文件复核；若效果不满意，直接用备份还原。")
    L.append("═" * 66)
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Excel 表格排版改造器（先备份再动表）")
    ap.add_argument("file")
    ap.add_argument("--mode", choices=["auto", "config", "report"], default="auto")
    ap.add_argument("--fix", default="P0,P1,P2", help="要修的级别，如 P0,P1,P2")
    ap.add_argument("--out", default=None, help="另存路径（不覆盖原文件，也不备份）")
    ap.add_argument("--header-style", choices=["light", "dark"], default="light")
    ap.add_argument("--font-cn", default=FONT_CN, help=f"中文字体（默认 {FONT_CN}，可改 等线/宋体）")
    ap.add_argument("--no-font", action="store_true", help="不统一字体（保留原字体）")
    ap.add_argument("--convert-numeric", action="store_true",
                    help="把「数字存成文本」转成真数值（会改数据，需确认）")
    ap.add_argument("--no-zebra", action="store_true", help="禁用斑马纹")
    ap.add_argument("--no-backup", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="只列改动计划")
    ap.add_argument("-o", "--report", default=None, help="把改动清单写入文本文件")
    args = ap.parse_args()

    levels = tuple(x.strip().upper() for x in args.fix.split(",") if x.strip())
    report, warns, bpath = refine(
        args.file, mode=args.mode, levels=levels, out=args.out,
        header_style=args.header_style, do_backup=not args.no_backup,
        dry_run=args.dry_run, convert_numeric=args.convert_numeric,
        zebra=False if args.no_zebra else None,
        font_cn=args.font_cn, skip_font=args.no_font,
    )
    text = render(report, warns, bpath, args.dry_run)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"清单已写入: {args.report}")
    else:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        print(text)


if __name__ == "__main__":
    main()
