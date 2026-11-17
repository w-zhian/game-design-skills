# openpyxl 技术手册（全部实测）

> 环境：Python 3.13 / openpyxl **3.1.5** / Windows。
> 每条标注：✅ 实测通过 ｜ ⚠️ 有坑 ｜ ❌ 做不到。
> 来源：`research/04-openpyxl-implementation.md`（550 行，含 XML 解包交叉验证）。

---

## 1. 单位（最容易错的地方）

| 项 | 单位 | 说明 |
|---|---|---|
| `ws.column_dimensions['A'].width` | **字符数**（不是像素） | 基准是 Normal 字体里 `0` 的宽度 |
| `ws.row_dimensions[1].height` | **pt**（磅） | 1pt = 1/72 英寸；96DPI 下 px = pt × 1.3333 |
| Excel 默认列宽 | 8.43 | 官方值 |
| Excel 默认行高 | 15.0 pt | 官方值 |
| Excel 列宽范围 | 0（隐藏）～ 255 | — |
| Excel 行高范围 | 0（隐藏）～ 409 | — |

**列宽 → 像素**没有与字体无关的定值（依存于 MDW），只能给经验估算：

```python
# 近似（Calibri 11 / 96DPI），不要承诺精确
px ≈ int((256 * width + int(128 / 7)) / 256 * 7)   # MDW ≈ 7
```

**1/256 量化是 Excel 的行为，不是 openpyxl 的** ✅
实测设 `width=10.00390625` 原样保存，openpyxl 不做量化。
→ 放心用 `width=12.5` 小数；Excel 打开后差 0.00x 是 Excel 自己取整。

```python
from openpyxl.utils import get_column_letter
ws.column_dimensions['A'].width = 18
ws.column_dimensions[get_column_letter(3)].width = 12.5
ws.row_dimensions[1].height = 24
```

---

## 2. 边框：只画水平线 ✅

```python
from openpyxl.styles import Border, Side

# 表头下：只有下边框
cell.border = Border(bottom=Side(style="medium", color="FFD9D9D9"))

# 合计行上：只有上边框
cell.border = Border(top=Side(style="thin", color="FFD9D9D9"))

# 清空全部边框
cell.border = Border()
```

⚠️ **读回时未设置的边是 `None`，不是 Side 对象**：
```python
# 错误写法 —— 会 AttributeError: 'NoneType' object has no attribute 'style'
if cell.border.top.style: ...

# 正确写法
def has_any_border(b):
    if b is None: return False
    for s in ("left","right","top","bottom"):
        side = getattr(b, s, None)
        if side is not None and getattr(side, "style", None):
            return True
    return False
```
（这个坑在真实回归测试中触发过一次，已固化到两个脚本里。）

---

## 3. 填充与字体 ⚠️

```python
from openpyxl.styles import PatternFill, Font

# 正确：fill_type 必填 + 8 位 ARGB
cell.fill = PatternFill(fill_type="solid", start_color="FFF0F0F0")
# 清除填充
cell.fill = PatternFill(fill_type=None)

cell.font = Font(name="微软雅黑", size=11, bold=True, color="FF262626")
```

⚠️ **颜色必须是 8 位 ARGB**（`FF` + RGB）。写 6 位会被解释成别的颜色或报错。
⚠️ `fill_type='solid'` 不写则填充不生效。

---

## 4. 条件格式 ✅

```python
from openpyxl.formatting.rule import Rule, FormulaRule, CellIsRule, DataBarRule, ColorScaleRule
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.styles import PatternFill

# 重复值标红（openpyxl 没有 DuplicateValuesRule 便捷类，用通用 Rule）
ws.conditional_formatting.add(
    "A2:A1000",
    Rule(type="duplicateValues",
         dxf=DifferentialStyle(fill=PatternFill("solid", start_color="FFFFC7CE"))),
)

# 空值标黄 ⚠️ 公式按「选区左上角」写，列绝对、行相对
ws.conditional_formatting.add(
    "A2:A1000",
    FormulaRule(formula=["LEN($A2)=0"],
                fill=PatternFill("solid", start_color="FFFFEB9C")),
)

# 数据条（汇报表性价比最高）
ws.conditional_formatting.add("B2:B100", DataBarRule(start_type="min", end_type="max", color="FF638EC6"))

# 数值比较
ws.conditional_formatting.add("C2:C100",
    CellIsRule(operator="greaterThan", formula=["100"], fill=PatternFill("solid", start_color="FFFFC7CE")))
```

⚠️ **`FormulaRule` 的公式相对坑**：写成 `$A$2` 会让整列都参照 A2 一个格，规则失效。
正确是 `$A2`（锁列不锁行），且地址要按**选区左上角单元格**来写。

支持的规则类型：`duplicateValues` / `expression` / `cellIs` / `colorScale` / `dataBar` / `iconSet` / `containsText` / `top10` / `aboveAverage`，
个别子属性支持有限。

读取已有规则：
```python
for rng in ws.conditional_formatting:
    rules = ws.conditional_formatting[rng]   # list
```

---

## 5. 冻结窗格 ✅

```python
ws.freeze_panes = "A2"   # 冻结第 1 行
ws.freeze_panes = "B2"   # 冻结第 1 行 + 第 1 列
ws.freeze_panes = "B1"   # 只冻结第 1 列
ws.freeze_panes = None   # 取消
```

语义：**冻结线的交点在所填单元格的左上角**。填 `B2` = 冻结上方 1 行 + 左侧 1 列。

---

## 6. 数据验证（下拉 / 范围）✅

```python
from openpyxl.worksheet.datavalidation import DataValidation

dv = DataValidation(type="list", formula1='"是,否,待定"', allow_blank=True)
dv.prompt = "请选择状态"
dv.error = "只能选：是 / 否 / 待定"
ws.add_data_validation(dv)
dv.add("D2:D1000")

dv_num = DataValidation(type="whole", operator="between", formula1="0", formula2="100")
ws.add_data_validation(dv_num)
dv_num.add("E2:E1000")
```

⚠️ 注意：纯文本粘贴**不会触发**数据验证（Excel 原生行为，非 openpyxl 问题）。

---

## 7. 视图 / 网格线 / 缩放 ✅

```python
ws.sheet_view.showGridLines = False
ws.sheet_view.zoomScale = 90
ws.sheet_properties.tabColor = "0F62FE"     # sheet 标签色（6 位即可）
```

---

## 8. 打印设置 ⚠️（fitToWidth 与 scale 互斥）

```python
ps = ws.page_setup
ps.orientation = "landscape"    # 横向
ps.paperSize = 9                # A4
ps.fitToPage = True             # ← 这个开关决定谁生效
ps.fitToWidth = 1
ps.fitToHeight = 0

ws.print_title_rows = "$1:$1"   # 每页重复第 1 行
ws.print_area = "A1:H200"
ws.page_margins.left = ws.page_margins.right = 0.4
ws.oddFooter.center.text = "第 &P 页 / 共 &N 页"
ws.oddFooter.right.text = "&F  &A"    # 文件名 + sheet 名
```

**坑 1：`fitToWidth` 与 `scale` 互相覆盖**，谁生效由 `fitToPage` 决定：
- 要「按 1 页宽缩放」→ `fitToPage=True` + `fitToWidth=1`，**不要**设 `scale`
- 要「固定 80% 缩放」→ `fitToPage=False` + `scale=80`，**不要**设 `fitToWidth`

同时设两个 → 结果不可预期，是改表脚本最常见的静默失败。

**坑 2（实测踩到，小表不复现）：`ps.fitToPage = True` 会崩**

```
AttributeError: 'NoneType' object has no attribute 'sheet_properties'
```

原因有两层：
1. `fitToPage` 不是 `PageSetup` 自己的属性，而是转发到 `sheet_properties.pageSetUpPr.fitToPage`；
2. 更隐蔽的是 `PageSetup._parent` 本身可能是 `None`（加载某些被保存过的文件时），
   此时连 `sheet_properties` 都取不到。

`200 列 × 3000 行` 的实表上必现，小样本 100% 复现不了。
**正确写法：绕过 property 转发，直接操作 worksheet：**

```python
from openpyxl.worksheet.properties import PageSetupProperties

def set_fit_to_width(ws):
    try:
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
        ws.page_setup.scale = 80      # 降级
        return False
```

**配套纪律**：每个改造步骤都要用 try/except 包住，失败只记录不中断。
一个美化步骤出错不该让整份文件停留在「改了一半」的状态。
`beautify.py` 里的 `_safe()` 就是干这个的。

---

## 9. 数字格式与「数字存文本」检测 ✅

```python
cell.number_format = "@"        # 文本
cell.number_format = "#,##0"    # 千分位整数
cell.number_format = "0.00"     # 两位小数
cell.number_format = "0.0%"     # 百分比
```

**检测「数字存成文本」**（诊断器的核心判据）：

```python
def is_numeric_text(cell):
    if cell.value is None or cell.data_type != "s":
        return False
    s = str(cell.value).strip().replace(",", "").replace("，", "").rstrip("%")
    if not s:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False
```

⚠️ **转换前必须问用户**：手机号、身份证、以 `0` 开头的编号、超长数字编号，
转成数值会丢前导零或变科学计数法。这是唯一会改单元格值的操作。

---

## 10. 大表性能 ✅

| 模式 | 用法 | 限制 |
|---|---|---|
| `read_only=True` | 只读扫描大表 | 不能随机访问，样式读不全 |
| `write_only=True` | 从零生成大表 | 不能设 `column_dimensions`、不能合并、只能 `append()` |
| 普通模式 | 改格式（本技能主要用法） | 3 万行 × 200 列量级要注意内存 |

改格式必须用普通模式（要读样式）。**做抽样上限**（`diagnose.py --max-rows`）。

---

## 11. 不破坏原文件 ✅（有损清单）

```python
wb = load_workbook(path, keep_vba=(ext == ".xlsm"))
# ... 改样式 ...
wb.save(path)   # 或另存
```

✅ **实测保住的**：公式（未重算，原样保留）、常规图表、其他 sheet 的数据与格式、sheet 顺序。

⚠️ **会丢/降级的（必须提前告知用户）**：

| 对象 | 情况 |
|---|---|
| VBA 宏 | 默认丢；需 `keep_vba=True` 且存回 `.xlsm` |
| 图片 / 形状 / 文本框 | 往返有损或丢失 |
| 数据透视表 / 切片器 | 基本会丢 |
| 复杂图表（自定义布局） | 降级 |
| 富文本（单元格内多段样式） | 支持有限 |
| 共享/数组公式 | 往返不完整 |
| `.xls` 老格式 | 不支持，需先另存 `.xlsx` |

**策略**：改前自动备份 → 检测到上述对象主动警告 → 不确定就只报告不修改。

---

## 12. ❌ openpyxl 做不到的事（不要承诺）

| 能力 | 替代方案 |
|---|---|
| 计算公式结果 | win32com（需装 Excel）／LibreOffice headless／让用户先保存 |
| `data_only=True` 读缓存值 | 只在 Excel 保存过之后有效，新生成的文件读出 `None` |
| AutoFit 自动列宽 | 按内容估算（`disp_width` 中文算 2 格），或 win32com `Columns.AutoFit` |
| 图片 / 形状 | win32com / xlsxwriter（新建时） |
| 数据透视表 / 切片器 | win32com / 手动 |
| 复杂图表 | xlsxwriter（新建）/ win32com |
| `.xls` | xlrd 读 / xlwt 写 / 先另存 |
| 保留 VBA 并新建宏 | 只能 `keep_vba` 保留，不能新建 |

`win32com` 前提：Windows + 已装 Excel + 能起 COM 进程。沙箱环境常被拦，用前先测。

---

## 13. 快速自测

```bash
python scripts/make_sample.py %TEMP%/ugly.xlsx          # 造一个"故意很烂"的表
python scripts/diagnose.py %TEMP%/ugly.xlsx -o before.txt
python scripts/beautify.py %TEMP%/ugly.xlsx --convert-numeric
python scripts/diagnose.py %TEMP%/ugly.xlsx -o after.txt
```

期望：样本打出的问题经改造后，**P0 只剩「合并单元格」和「重复主键」**（这两个是刻意不自动修的），
字体从 5 种降到 2 种，底色从 6 种降到 1 种。

改了脚本之后必须跑这一套，否则可能在用户文件上静默失败。
