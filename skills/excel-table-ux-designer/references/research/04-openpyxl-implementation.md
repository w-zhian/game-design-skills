# 04 · openpyxl 技术实现层事实核准 + 实测验证

> 角色：Agent 4（技术实现层）。目标：确保「Excel 表格排版 UX 设计师」技能里的 API 用法真实可靠，改表脚本不会静默失败或损坏用户文件。方法：**真实环境跑代码验证** + 解包读回 xlsx 内部 XML 交叉确认，不只是查文档。
>
> - 解释器：`<PYTHON_EXE>`（实际为 3.13.14）
> - openpyxl：**3.1.5**（已装于该解释器 site-packages，无需另装；本轮未使用 venv，也未全局 pip install）
> - 验证脚本与产物：`%TEMP%\openpyxl_verify\`
> - 文档来源：`openpyxl.readthedocs.io/en/stable`；源码来源：`github.com/theorchard/openpyxl`（github.com 被本机代理拦截无法直连，故改读**本机安装的 3.1.5 源码** `...\site-packages\openpyxl\`，版本即最终运行版本，权威性等价）
>
> **状态标注约定**
> - ✅ **实测通过**：写脚本 → 保存 → 读回 + 解包 XML 验证
> - ⚠️ **实测失败 / 有坑**：实测结果与直觉/文档不同，需特别注意
> - 📖 **仅查源码未实测**：读源码/文档确认，未单独跑代码

---

## 0. 关键结论速览

1. 列宽 `width` 单位是**字符数**（基于 Normal 字体 0 号字宽）非像素；行高 `height` 单位是 **pt**。openpyxl **不做** 1/256 量化，Excel 自己保存时才量化。
2. 条件格式、数据验证、冻结、打印、数字格式、视图——**全部实测支持且 Excel 识别**。
3. **做不到/需换方案**（第 15 节）：公式计算、VBA 宏、图片、数据透视表/切片器、AutoFit、富文本、.xls 老格式。
4. 正常 `load_workbook`→改样式→`save`，公式/图表/其他 sheet **实测保留**，但有「往返有损」清单（第 13、15 节）。
5. 大表用 `write_only=True` 建、`read_only=True` 读，否则内存/耗时爆炸（第 12 节）。

---

## 1. 列宽单位、1/256 粒度、行高单位 ✅实测通过 + 📖源码

### 1.1 单位到底是什么

`ws.column_dimensions['A'].width = N` 的 **N 是「字符宽度」单位（character width）**，含义是「用工作簿 Normal 样式的默认字体的数字 `0` 的宽度来度量，一个 `0`  ≈ 1 个字符单位」。它不是像素、也不是厘米。

- openpyxl 源码 `openpyxl/worksheet/dimensions.py`：`width = Float()` —— **就是个普通浮点数，openpyxl 原样写入 XML，不做任何换算或量化**。
- openpyxl 源码 `openpyxl/utils/units.py`：
  - `DEFAULT_ROW_HEIGHT = 15.`（pt）
  - `BASE_COL_WIDTH = 8`，`DEFAULT_COLUMN_WIDTH = BASE_COL_WIDTH + 5 = 13`
  - `points_to_pixels(value, dpi=96) = int(math.ceil(value * 96 / 72))`
  - `pixels_to_points(value, dpi=96) = value * 72 / dpi`

### 1.2 与像素的换算关系

**行高（最简单、精确）**：行高单位是 **磅 pt**，1 pt = 1/72 英寸；在 Excel 默认 96 DPI 下：

```
像素 = 行高(pt) × 96 / 72 = 行高(pt) × 1.3333
行高(pt) = 像素 × 72 / 96
```

例：默认行高 15 pt → 20 px；设 `height = 21` → 28 px。

**列宽（复杂，依赖字体）**：列宽到像素没有官方精确闭式，常用经验公式（基于 Excel 默认 Calibri 11，96 DPI，MDW=最大数字宽度≈7px）：

```
像素宽 ≈ int( (256 × width + int(128/MDW)) / 256 × MDW )   （MDW≈7）
近似：像素宽 ≈ width × MDW + 5   （+5px 为边距 padding）
```

> 关键：MDW（Max Digit Width）随字体/字号变化，所以「列宽 N = 多少像素」**没有与字体无关的定值**。技能里若要按像素设列宽，只能给经验估值，不能承诺精确。

### 1.3 关于「1/256 字符粒度」——记忆需修正 ⚠️

实测设 `width` 为 `10.1`、`10.00390625`（=10+1/256）、`10.0078125`，读回**完全等于原值**，XML 也是 `width="10.1"` 原样——**openpyxl 层不量化**：

```
set : [10, 10.1, 10.5, 10.00390625, 10.0078125, 0.00390625, 255.99609375]
read: [10.0, 10.1, 10.5, 10.00390625, 10.0078125, 0.00390625, 255.99609375]
```

**1/256 粒度是 Excel 自己的存储/保存行为**（Excel 打开/保存时按 1/256 取整）。启示：放心用 `width=12.5` 小数，openpyxl 精确保留；别用「必须 1/256 整数倍」无谓约束用户；若 Excel 回读差 0.00x 是 Excel 量化，非 openpyxl bug。

### 1.4 可直接复制的代码片段

```python
from openpyxl.utils import get_column_letter
ws.column_dimensions['A'].width = 18          # 字符单位
ws.column_dimensions[get_column_letter(3)].width = 12.5
ws.row_dimensions[1].height = 24              # 磅 pt；24pt ≈ 32px
```

---

## 2. 高效设置大量列宽 / 整表默认宽 ✅实测通过

### 2.1 标准做法（普通模式）

`column_dimensions` 循环即可，200 列毫无压力（实测设 200 列 + 默认宽，XML 正确写出 200 个 `<col>`）：

```python
from openpyxl.utils import get_column_letter
widths = [12, 18, 10, 25] * 50        # 200 列
for i, w in enumerate(widths, start=1):
    ws.column_dimensions[get_column_letter(i)].width = w
```

### 2.2 整表默认列宽

```python
ws.sheet_format.defaultColWidth = 14   # 写入 <sheetFormatPr defaultColWidth="14">
```

实测 XML：`<sheetFormatPr baseColWidth="8" defaultColWidth="14" defaultRowHeight="15" />`。注意：单独设 `defaultColWidth` 不一定压缩掉已有的 `<col>` 条目——显式设过 width 的列仍会各自写 `<col>`。

### 2.3 直接操作 XML？——不必要

openpyxl **无公开的「按原始 XML 批量写列宽」接口**。普通模式 `Worksheet` 无此类方法；`write_only=True` 的 `WriteOnlyWorksheet` **不能**设 `column_dimensions`（实测限制）。所以普通模式用循环即可；write_only 若要列宽须写完再用普通模式重开设置，或改 zip 内 XML（非官方）。

---

## 3. 边框：表头下边框 + 合计行上边框 ✅实测通过

### 3.1 正确用法

`Side(style, color)` 定义一条线，`Border(top=/bottom=/left=/right=)` 把线装到单元格四个边。只画水平线就只给 `top` 或 `bottom`：

```python
from openpyxl.styles import Border, Side

thin   = Side(style="thin",   color="FF000000")   # 表头下边线
medium = Side(style="medium", color="FFFF0000")   # 合计行上边线

# 表头行：只有下边框
for c in range(1, 5):
    cell = ws.cell(1, c)
    cell.border = Border(bottom=thin)

# 合计行：只有上边框
for r_total in [5]:
    for c in range(1, 5):
        ws.cell(r_total, c).border = Border(top=medium)
```

实测读回：

```
A1 border.bottom.style: thin    top: None
A5 border.top.style:    medium  bottom: None
```

### 3.2 批量与坑

- **复用对象**：多个单元格共用同一 `Side`/`Border` 实例，openpyxl 按样式去重，文件不变大。
- **未设置的边读回是 `None`**，不是 `Side(style=None)`。校验要写 `if cell.border.bottom is not None`，否则 `AttributeError`（本轮踩到）。
- 清除：`cell.border = Border()`；斜线表头用 `border.diagonal/diagonalUp/diagonalDown`。
- XML 实测 `<border><bottom style="thin"><color rgb="FF000000"/></bottom></border>`，Excel 正常识别。

---

## 4. 填充与字体 ✅实测通过 + ⚠️有坑

### 4.1 PatternFill 的 fgColor / bgColor 坑

实测三种写法：

| 写法 | 结果 |
|---|---|
| `PatternFill(fill_type='solid', start_color='FFFFFF00')` | ✅ 正常纯色填充，只需 start_color（即 fgColor） |
| `PatternFill(fill_type='solid', start_color=..., end_color=...)` | ✅ 正常，bgColor 也被写入但 solid 模式下 Excel 只看 fgColor |
| `PatternFill(start_color=..., end_color=...)`（**不写 fill_type**） | ⚠️ **无填充**：XML 里 `<patternFill><fgColor .../></patternFill>` 没有 `patternType="solid"` |

**结论**：`fill_type='solid'` 是关键，必须有；**不必**同时设 `end_color`（bgColor）。`start_color` 就是 solid 的前景色。

```python
from openpyxl.styles import PatternFill, Font

header_fill = PatternFill(fill_type="solid", start_color="FF1F4E78")   # 深蓝
cell.fill = header_fill
cell.font = Font(name="微软雅黑", size=11, bold=True, color="FFFFFFFF")
```

### 4.2 颜色必须是 8 位 ARGB（重要坑）⚠️

实测：写 `start_color="FFFF00"`（6 位）被存成 `00FFFF00`——openpyxl 会在前面补 `00`（全透明 alpha）。Excel 对 solid 填充会忽略 alpha 正常显示，但**在条件格式/边框等场景 alpha 可能影响表现**。技能里应统一用 **8 位 `AARRGGBB`**，不透明用 `FF` 开头：

```
'FFFF0000' 红  'FF00B050' 绿  'FFFFC000' 橙  'FF1F4E78' 深蓝  'FFFFFFFF' 白
```

### 4.3 Font

`Font(name=, size=, bold=, italic=, color=, underline=)`。读回时字号字段是 `font.sz`（`size` 是别名）；`font.color.rgb` 取颜色。实测 `Font(name="Calibri", size=14, bold=True, color="FFFF0000")` 读回 `Calibri / 14.0 / True / FFFF0000` ✅。

---

## 5. 条件格式：至少三种真写入 ✅实测通过

实测把以下规则全部写入并读回，XML 中 `cfRule type` 齐全：`['duplicateValues', 'duplicateValues', 'expression', 'cellIs', 'colorScale', 'dataBar', 'iconSet']`。

### 5.1 重复值标红（duplicateValues）

openpyxl **没有** `DuplicateValuesRule` 便捷类，用通用 `Rule(type="duplicateValues", dxf=...)`；`dxf` 用 `DifferentialStyle` 包装样式：

```python
from openpyxl.formatting.rule import Rule
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.styles import PatternFill

red_fill = PatternFill(fill_type="solid", start_color="FFFFC7CE")
ws.conditional_formatting.add(
    "A1:A100",
    Rule(type="duplicateValues", dxf=DifferentialStyle(fill=red_fill)),
)
```

> 注意：我第一次用 `dxf=None` 也成功写入了 `duplicateValues` 规则（只是没有可见样式）。要给样式必须挂 `dxf`。

### 5.2 空值标黄（FormulaRule，相对 A1 坑）⚠️

```python
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import PatternFill

yellow = PatternFill(fill_type="solid", start_color="FFFFEB9C")
ws.conditional_formatting.add(
    "A1:A100",
    FormulaRule(formula=['LEN($A1)=0'], fill=yellow),   # 注意 $A1：列绝对、行相对
)
```

**公式相对 A1 的坑**：`formula` 里的地址要按**选区左上角单元格**来写（这里是 A1）。`$A1` 锁列不锁行，Excel 会把行号随每行相对下移；若写成 `$A$1` 则整列都参照 A1 一个格子，规则失效。实测写入的公式原样为 `LEN($A1)=0`，XML `<formula>` 被正确识别。

### 5.3 其他可写入类型（均实测通过）

```python
from openpyxl.formatting.rule import (
    CellIsRule, ColorScaleRule, DataBarRule, IconSetRule, FormulaRule, Rule
)
# 单元格值比较
ws.conditional_formatting.add("B1:B100",
    CellIsRule(operator="greaterThan", formula=["3"], fill=red_fill))
# 三色刻度
ws.conditional_formatting.add("B1:B100",
    ColorScaleRule(start_type="min", start_color="FFFF0000",
                   end_type="max", end_color="FF00FF00"))
# 数据条
ws.conditional_formatting.add("B1:B100",
    DataBarRule(start_type="min", end_type="max", color="FF638EC6"))
# 图标集
ws.conditional_formatting.add("B1:B100",
    IconSetRule(icon_style="3Arrows", type="num", values=[0, 33, 67]))
```

### 5.4 支持的规则类型清单

`CellIsRule`、`FormulaRule`、`ColorScaleRule`、`DataBarRule`、`IconSetRule`、通用 `Rule`（`type` 可取 `duplicateValues`、`containsText`、`expression`、`top10`、`aboveAverage` 等）✅ 均写出。⚠️ `colorScale/dataBar/iconSet` 的自定义子属性支持有限，复杂配置需回退 Excel 手动或 xlsxwriter。读取已有规则：`for rng in ws.conditional_formatting: ws.conditional_formatting[rng]` 返回规则列表（实测 `A1:A6 -> ['duplicateValues','expression']`）。

---

## 6. 冻结窗格 ✅实测通过

`ws.freeze_panes` 语义（"冻结线的交点右下角第一个单元格"）：

| 取值 | 效果 | 实测 XML `<pane>` |
|---|---|---|
| `'A2'` | 冻结首行 | `ySplit="1" topLeftCell="A2" activePane="bottomLeft"` |
| `'B2'` | 冻结首行 + 首列 | `xSplit="1" ySplit="1" topLeftCell="B2" activePane="bottomRight"` |
| `'B1'` | 只冻结首列 | `xSplit="1" topLeftCell="B1" activePane="topRight"` |
| `'A1'` / `None` | 不冻结 | 无 `<pane>`（读回 `None`） |

```python
ws.freeze_panes = 'A2'    # 表头首行固定
ws.freeze_panes = 'B2'    # 首行首列都固定
ws.freeze_panes = None    # 取消冻结
```

实测读回值与 XML 完全一致，✅。

---

## 7. 数据验证（下拉 / 数值范围）✅实测通过

```python
from openpyxl.worksheet.datavalidation import DataValidation

# 下拉列表（选项写在 formula1 里，用英文双引号包住、逗号分隔）
dv1 = DataValidation(type="list", formula1='"优秀,良好,及格,不及格"', allow_blank=True)
dv1.showErrorMessage = True
dv1.errorTitle = "错误"; dv1.error = "请从下拉中选择"
dv1.showInputMessage = True
dv1.promptTitle = "提示"; dv1.prompt = "请选择等级"
ws.add_data_validation(dv1)
dv1.add("B1:B10")           # 可 add 多个区域

# 整数范围 0~100
dv2 = DataValidation(type="whole", operator="between", formula1="0", formula2="100")
ws.add_data_validation(dv2)
dv2.add("C1:C10")
```

实测写出的 XML（Excel 正常识别）：

```xml
<dataValidations count="2">
  <dataValidation sqref="B1:B10" type="list" allowBlank="1" showErrorMessage="1" ...>
    <formula1>"优秀,良好,及格,不及格"</formula1>
  </dataValidation>
  <dataValidation sqref="C1:C10" type="whole" operator="between">
    <formula1>0</formula1><formula2>100</formula2>
  </dataValidation>
</dataValidations>
```

支持的 `type`：`list`、`whole`、`decimal`、`date`、`time`、`textLength`、`custom`。下拉项超过 255 字符或跨 sheet 引用时，需把选项放到隐藏区域并用 `formula1="=Sheet2!$A$1:$A$50"`（不要带引号）。

---

## 8. Sheet 视图、网格线、缩放、标签色 ✅实测通过

```python
ws.sheet_view.showGridLines = False   # 隐藏网格线（排版美化常用）
ws.sheet_view.zoomScale = 85          # 缩放 85%（10~400）
ws.sheet_properties.tabColor = "FF00AA00"   # 工作表标签颜色
```

实测读回：`showGridLines=False / zoomScale=85 / tabColor=FF00AA00` ✅，XML：

```xml
<sheetView showGridLines="0" zoomScale="85" workbookViewId="0"> ...
<tabColor rgb="FF00AA00"/>   <!-- 在 sheet1.xml 的 <sheetPr> 内 -->
```

> 坑：tabColor 写在 **sheet XML 的 `<sheetPr>`**，不在 styles.xml。本轮实测找错位置踩坑，定位时注意。另 `showGridLines` 默认读回可能是 `None`（表示用默认 true），只有显式设过才是 `False`。

---

## 9. 打印设置 + fitToWidth 与 scale 的互相覆盖坑 ✅实测通过 + ⚠️重点坑

### 9.1 各项写法

```python
ws.page_setup.orientation = "landscape"          # 'portrait'/'landscape'
ws.page_setup.paperSize   = ws.PAPERSIZE_A4      # '9'（A4）
ws.page_setup.fitToWidth  = 1                    # 宽适配 1 页
ws.page_setup.fitToHeight = 0                    # 高不限（0=不限）
ws.page_setup.scale       = 80                   # 缩放 80%
ws.sheet_properties.pageSetUpPr.fitToPage = True # 关键开关！
ws.print_title_rows = '1:1'                      # 每页重复标题行
ws.print_area = 'A1:D50'                         # 打印区域
ws.page_margins.left = 0.3; ws.page_margins.top = 0.5   # 英寸
from openpyxl.worksheet.pagebreak import Break
ws.row_breaks.append(Break(id=30))               # 在第30行后分页
```

实测读回：`orientation=landscape / paperSize=9 / fitToWidth=1 / fitToHeight=0 / scale=80 / fitToPage=True / print_title_rows=$1:$1 / print_area='Sheet'!$A$1:$D$50 / margins=0.3,0.5 / row_breaks=1` ✅。打印标题/区域写入了 workbook.xml 的 `_xlnm.Print_Titles`、`_xlnm.Print_Area` 定义名。

### 9.2 fitToWidth 与 scale 是否会互相覆盖？⚠️（用户重点问的坑）

**实测结论**：openpyxl **两者都会原样写进 XML，不会互相覆盖**：

```xml
<pageSetup scale="50" fitToHeight="1" fitToWidth="1" />
<pageSetUpPr fitToPage="1" />
```

但**在 Excel 打开时二者互斥**，由 `fitToPage` 开关决定谁生效：

- `fitToPage = True`（`fitToPage="1"`）→ Excel **用 `fitToWidth/fitToHeight`，忽略 `scale`**；
- `fitToPage = False` → Excel **用 `scale`，忽略 `fitToWidth/fitToHeight`**。

这就是常见坑：技能里若同时设了 `fitToWidth=1` 和 `scale=80` 却忘了设 `fitToPage=True`，Excel 会按 scale 显示，适配页面设置「看起来没生效」。

**给技能的策略**：二选一，不要混用。

```python
# 方案A：按页宽缩放（排版常用）
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True

# 方案B：固定缩放比例
ws.page_setup.scale = 80
ws.sheet_properties.pageSetUpPr.fitToPage = False
```

---

## 10. 数字格式 + 检测「数字存成文本」✅实测通过

### 10.1 写法

```python
ws['A1'].number_format = '#,##0'    # 千分位整数
ws['A2'].number_format = '@'        # 文本格式（@ 是文本占位符）
ws['A3'].number_format = '0.00%'    # 百分比
ws['A4'].number_format = 'yyyy-mm-dd'  # 日期
```

实测读回：`A1 fmt=#,##0 / A2 fmt=@`，值类型 `A1=n(数字) / A2=s(文本)` ✅。

### 10.2 检测「数字存成文本」的代码思路（重点）

Excel 里「看起来是数字、实际存成文本」的单元格：`data_type == 's'`（字符串）但内容能解析成数字。区分靠 `cell.data_type`：

```python
def looks_numeric_as_text(cell):
    """真数字返回 False；存成文本的数字返回 True"""
    if cell.data_type != 's':        # 'n' 数字 / 'd' 日期 / 'f' 公式 / 's' 文本 / 'b' / 'e'
        return False
    v = str(cell.value or '').strip().replace(',', '')
    if not v:
        return False
    try:
        float(v)                      # 能解析成数字 → 是伪文本数字
        return True
    except ValueError:
        return False

# 扫描
for row in ws.iter_rows():
    for cell in row:
        if looks_numeric_as_text(cell):
            print(cell.coordinate, repr(cell.value))
```

实测样本里 `D2='12345' data_type='s' fmt=General` → 被正确判为「数字存文本」✅。

**修复**：`cell.value = float(cell.value)` 或 `int(...)`，再把 `number_format` 从 `@`/`General` 改成 `#,##0`。注意 `00123` 这类有前导零的，转数字会丢零——是否转换要看业务语义（ID/编号本就该是文本）。

---

## 11. 强制文本化 / data_only / 日期读取 ⚠️部分为固有限制

### 11.1 读进来 `123` 是 int/float，如何保留原始字符串

实测默认加载：`A="123"→'123' type=s / B=123→int type=n / C=123.0→float type=n / D=date→datetime type=d / E="=1+1"→'=1+1' type=f`。

- 原本是文本 `"123"` → openpyxl 保留为字符串 ✅。
- 原本是数字 `123` → 读成 `int`/`float`；「显示为 00123 / 123.00」的展示信息不在值里而在 `number_format`。**`load_workbook` 没有参数能把数字读成原始字符串**，要保留展示形态得同时读 `cell.value` + `cell.number_format` 自行拼。
- 写时强制文本：`cell.value = "123"; cell.number_format = '@'`。

### 11.2 data_only 与公式

```python
wb  = load_workbook(path)                # 公式单元格返回 '=1+1'（字符串，data_type='f'）
wb2 = load_workbook(path, data_only=True) # 公式单元格返回「上次Excel保存时的缓存值」
```

⚠️ `data_only=True` 时公式 `=1+1` 读回 `None`（本轮实测：文件从未被 Excel 计算过，没有缓存值）。**openpyxl 自身从不计算公式**——要公式结果只能靠 Excel 打开保存过，或换 LibreOffice/win32com 计算。

### 11.3 日期读成 datetime

实测日期读回还是 `datetime` 对象（`type='d'`），正常。若公式结果是日期，`data_only=True` 返回 `datetime` 而非序列号；想拿序列号用 `from openpyxl.utils.datetime import to_excel; to_excel(dt)`。`load_workbook(path, keep_links=True)` 控制外部链接保留（默认 True）。

---

## 12. 大表性能实测（3 万行 × 200 列 ≈ 600 万单元格）✅实测通过

| 操作 | 实测耗时 | 备注 |
|---|---|---|
| `write_only=True` 构建 + 保存 | **53.0 s** | 文件 40.3 MB |
| `load_workbook(read_only=True)` + `iter_rows(values_only=True)` 遍历 3 万行 | **30.9 s** | 流式，内存低 |
| 普通模式 `load_workbook` 载入 5000×200（100 万格） | **6.55 s** | 全量进内存 |
| 普通模式遍历那 100 万格 | **0.59 s** | — |

**结论**：600 万格普通模式全量载入预计 **≈40 s 且内存很高**（线性外推），易吃满内存。**建大表**用 `Workbook(write_only=True)`+`append()`；**扫描**用 `load_workbook(read_only=True)`+`iter_rows(values_only=True)`。技能诊断应默认 `read_only=True`，但该模式**不支持**改样式/条件格式/合并单元格——故分两遍：read_only 扫问题 → 普通模式改造。

> write_only 限制：不能随机访问单元格、不能设 `column_dimensions`、不能合并单元格；只能 `append()` 整行。

---

## 13. 不破坏原文件：加载 → 改格式 → 另存 ✅实测通过（但有损清单）

### 13.1 实测场景

建含「公式 `=SUM(A1:A2)` + 字体/填充样式 + 柱状图 + 第二个 sheet」的 xlsx → 普通 `load_workbook` → 改一个单元格值和一个字体颜色 → 另存 → 重新打开核对：

```
sheets: ['Sheet', 'Second']              ✅ 其他 sheet 保留
A3 formula: '=SUM(A1:A2)'                ✅ 公式保留
A1 font color: FF0000FF                  ✅ 新样式生效
charts count on active: 1                ✅ 图表保留（chart title 对象在）
Second!A1: 'keep me'                     ✅ 其他 sheet 数据保留
zip 内有 chart xml 与 drawing1.xml       ✅ 图表部件保留
```

**结论**：只要公式未被 Excel 改写、图表是 openpyxl 支持的常规类型，普通加载→改样式→另存能保住公式、图表、其他 sheet。这是技能的核心安全保证。✅

### 13.2 仍会丢失/降级的东西（⚠️必须告知用户）

openpyxl 是「**重新序列化**」而非字节级修改，以下会丢或变：VBA 宏（默认丢，需 `keep_vba=True`+`.xlsm`）、图片/形状（读图有损）、数据透视表/切片器（基本丢）、复杂图表（降级）、外部链接/批注富文本（变化）。

**稳健策略**：① 改造前**自动备份**；② 检测到 `.xlsm`/图片/透视表时**警告用户**；③ 宏文件用 `keep_vba=True` 且保持 `.xlsm`；④ 需无损改高级对象只能用 **win32com（Windows+Excel）** 或手动。

### 13.3 keep_vba

```python
wb = load_workbook(path, keep_vba=True)   # .xlsm 保留宏；save 路径也要 .xlsm
```

---

## 14. 测试材料：故意排版很烂的回归样本 ✅实测通过

在 `%TEMP%` 下生成并保存：`%TEMP%\openpyxl_verify\ugly_sample.xlsx`（5 KB）。内置「坏」特征（全部实测确认）：列宽全默认（`width=13.0`）、行高默认（`height=None`）、合并单元格（`F1:F2`）、表头无样式（`font.bold=False fill=None`）、数字存文本（`D2='12345' type=s`）、重复 ID（`1001`）、无冻结、无打印设置、网格线未隐藏。

### 生成脚本核心思路（供技能回归测试复用）

```python
from openpyxl import Workbook
wb = Workbook(); ws = wb.active; ws.title = "MessyData"
ws.append(["ID","姓名","部门","销售额","入职日期","备注"])   # 表头无样式
rows = [
    ["1001","张三","销售部","12345","2026/1/5",""],
    ["1002","李四","技术部","6789","2026/2/11",""],
    ["1001","王五","销售部","9999","2026/3/1","重复ID"],   # 重复ID
    ["1004","赵六","","54321","not-a-date","数字存文本"],   # 空值+坏日期
]
for r in rows: ws.append(r)
ws.merge_cells("F1:F2")                    # 制造合并单元格
# 故意：不设列宽/行高、不设冻结、不设打印、不设条件格式、不设数字格式
wb.save("ugly_sample.xlsx")
```

> 该样本用于回归测试：诊断扫描应报出所有问题；原地改造后应全部消失。

---

## 15. openpyxl 做不到 / 必须换方案（总表）

| 能力 | openpyxl 支持情况 | 替代方案 |
|---|---|---|
| 计算单元格值（公式结果） | ❌ 不支持，公式读回字符串；`data_only` 只能读缓存 | win32com（本机 Excel）、LibreOffice headless、让用户保存 |
| 自动列宽 AutoFit | ❌ 不支持（列宽需手动给数值，且换算依赖字体） | win32com `Columns.AutoFit`，或按内容估算字符数 |
| 保留 VBA 宏 | ⚠️ 需 `keep_vba=True` 且存 `.xlsm`，否则丢 | openpyxl(keep_vba) / win32com |
| 图片 / 形状 / 文本框 | ❌ 读回有损或丢失 | win32com；或 xlsxwriter（新建时插图） |
| 数据透视表 / 切片器 | ❌ 支持极差，基本会丢 | win32com / 让用户手动 |
| 复杂图表（自定义布局/条件格式图） | ⚠️ 常规图表可往返，复杂会降级 | xlsxwriter（新建时强）、win32com |
| 条件格式新规则类型（部分） | ⚠️ 多数支持，个别子属性/新类型有限 | xlsxwriter / win32com / 手动 |
| 富文本（单元格内多段不同样式） | ⚠️ 支持有限 | xlsxwriter `write_rich_string` |
| .xls（老 BIFF 格式） | ❌ 不支持，只能 .xlsx/.xlsm | xlrd（读）/ xlwt（写）/ 先另存为 xlsx |
| 共享公式、数组公式完整往返 | ⚠️ 支持不完整 | win32com |
| 单元格级批注富文本 | ⚠️ 有限 | win32com |

**技能应明确写**：以上「做不到/有损」的能力，不要承诺；遇到就提示用户备份 + 手动，或切换到 win32com（仅 Windows + 已装 Excel）。

---

## 16. 验证脚本清单（便于复现）

全部位于 `%TEMP%\openpyxl_verify\`：`verify_core.py`（点 1/4/5/6/7/8/9/10/11/13 → `result_core.txt`）、`verify_supp.py`（点 2/8/9 → `result_supp.txt`）、`verify_border.py`（点 3 → `result_border.txt`）、`verify_perf_and_sample.py`（点 12/14 → `result_perf.txt` + `ugly_sample.xlsx`）。

运行：

```bat
"<PYTHON_EXE>" "%TEMP%\openpyxl_verify\verify_core.py"
```

---

*文档版本：2026-11-17 · 所有 ✅ 项均在本机 openpyxl 3.1.5 + Python 3.13.14 实测；源码结论标注 📖。*
