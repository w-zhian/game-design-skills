# 03 · 游戏配置表的工程排版实践调研

> 调研目标：为「Excel 表格排版 UX 设计师」技能内置一套**与 Luban 导出流水线兼容**的配置表排版规范。
> 调研者：Agent 3（工程排版实践）。
> 调研日期：2026-11-17。
> 每条结论后标注 `— 来源: <URL>（类型：硬约束/惯例/观点）`。

---

## 0. 方法论与来源分级

### 0.1 三类结论的定义

- **硬约束**：工具链在代码/文档中强制要求、不满足就报错或被忽略的规则。来自官方仓库 README、官方文档站、官方 Manual。
- **惯例**：社区/行业长期使用、但工具本身不强制的排版习惯。来自工具文档中的"建议/推荐"、示例工程、三方生态项目。
- **观点**：行业分享（GDC 演讲等）中演讲者主张的做法，属于经验之谈而非规范。
- 凡未找到可靠公开来源者，明确写「**未找到可靠公开来源**」，不臆造。 — 来源: 本调研方法约定（类型：惯例）

### 0.2 来源取舍

- Luban 官方规范以 **GitHub `focus-creative-games/luban`** 与**官方文档站 `datable.cn/docs`** 为准（当前文档版本 5.x）。 — 来源: https://github.com/focus-creative-games/luban （类型：硬约束）
- 严格排除：知乎、微信公众号、百度百科/知道、CSDN 洗稿文。本报告未采用上述来源。
- 交叉验证采用：GitHub 官方仓库/文档、厂商公开技术站、GDC Vault 演讲页、微软官方支持文档、独立开发者 GitHub 项目 README。
- 注意：检索中出现的 `wxb1990/luban`、`funturn/luban`、`AILHC/luban`、`wumohai/luban`、`Peoley199/luban` 均为 **fork/镜像**，非官方源；本报告仅在需说明历史写法差异时提及，不作为规范依据。 — 来源: https://github.com/focus-creative-games/luban （类型：硬约束）

### 0.3 重要版本提示

- Luban 自 5.0.0 起文档与能力升级为 "AI Native"（官方 Skills、`-c schema-json`、`--errorFormat json`、`Luban.Agent` CLI、MCP Server），本报告以 5.x 文档为准。 — 来源: https://github.com/focus-creative-games/luban （类型：硬约束）
- 4.x 及 fork 中常见的表头写法（如无 `##var` 前缀、`##column` 表示纵表）与 5.x 存在差异，做兼容设计时需留意。 — 来源: https://github.com/focus-creative-games/luban （类型：惯例）

---

## 1. Luban 官方配置表规范（硬事实核对）

### 1.1 什么 sheet 会被当成有效数据表

- 「A1（或标题区）用 `##` / `##var` / `##type` 等标记表头；其后是数据行。**A1 不以 `##` 开头的 sheet 会被忽略**。」 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 「xlsx 会读入**所有** sheet，但 A1 不以 `##` 开头的 sheet 会被忽略（可放策划说明等非数据 sheet）。」 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 「表要先登记：程序在 `__tables__`（或 XML）里登记后，你的 Excel 才会被导出。只在自己电脑新建 xlsx **不会**自动进包。」 — 来源: https://www.datable.cn/docs/designer/concepts （类型：硬约束）
- 「Schema 是契约：先有（或同时维护）表声明，再填数据。不要指望工具根据 Excel「猜完结构并覆盖定义」。」 — 来源: https://www.datable.cn/docs/guide/add-table （类型：硬约束）
- 支持的源文件：`xls` / `xlsx` / `xlsm` / `csv` 等；也可用 `sheet名@文件.xlsx` 只读某一个 sheet。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）

### 1.2 多行表头的组织（字段名 / 类型 / 分组 / 注释各占一行）

Luban 官方最小完整示例（`Item` 表，字段 `id/name/price/on_sale`）：

```
##var    id   name  price  on_sale  #备注
##type   int  string int    bool
##group  c,s  c     c      c
##       道具ID 名称  价格   是否上架  策划备注列
1001     金币  0     是     基础货币
1002     药水  50    true
##       1003  草稿  1      否        本行是注释行，不导出
```

- 行/列作用表（官方原文）：
  - `##var`（或首格 `##`）= 字段名行；
  - `##type` = 类型行；
  - `##group` = 导出分组：`c` 客户端、`s` 服务器、空=各端都要；
  - `##` / `##comment` = 注释行，也可作字段中文说明；
  - 字段名以 `#` 开头或为空 = **注释列**，不导出；
  - 数据行首列以 `##` 开头 = **注释行**，整行不导出。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 「`##xxx` 行顺序可调；`##group`、注释行可选。字段名推荐 `xx_yy_zz`，生成时按语言转成 Pascal/camel 等。」 — 来源: https://www.datable.cn/docs/excel/basics （类型：惯例）
- 「不要改 `##type` 里的类型名（例如把 `int` 改成「整数」）。」 — 来源: https://www.datable.cn/docs/designer/concepts （类型：硬约束）
- 表头行"能不能改"官方对照：`##`/`##var` 字段名行一般由程序定；`##type` 不要改成中文或"看起来像"的字；`##group` 按项目规范填 `c`/`s`；`##`/`##comment` 注释行可写中文说明、整行不导出；数据行是策划主战场。 — 来源: https://www.datable.cn/docs/designer/headers （类型：硬约束）

### 1.3 注释列 vs 注释行（易错点）

- 「注释列：字段名为空，或以 `#` 开头（如 `#备注`）——这列填了也不进游戏。」 — 来源: https://www.datable.cn/docs/designer/headers （类型：硬约束）
- 「注释行：该行**第一格**以 `##` 开头——整行忽略。」 — 来源: https://www.datable.cn/docs/designer/headers （类型：硬约束）
- 常见错误对照：「填了备注却进游戏 → 字段名没加 `#`，被当成正式列 → 备注列名改成 `#xxx` 或空」；「某行怎么改都不生效 → 该行第一格是 `##` 注释行 → 去掉行首 `##`」。 — 来源: https://www.datable.cn/docs/designer/headers （类型：硬约束）
- tag 机制补充：「`##` 永久注释，任何导出都不包含」「永久废弃行用首列 `##`，不要只靠『删掉数字假装没有』」。 — 来源: https://www.datable.cn/docs/quality/tags （类型：硬约束）

### 1.4 行/列语义与纵表

- 默认横表：「大多数表都是横表，即一行一个记录。」（见 README excel 格式概览目录） — 来源: https://github.com/Peoley199/luban （类型：惯例）
- 纵表模式（单例表更适合）：fork/历史 README 记载「A1 为 `##column` 表示使用纵表模式，一行一个字段」。5.x 官方 `excel/basics` 页面未展开纵表细节，纵表精确标记符**未找到 5.x 官方可靠公开来源**核对；技能内若涉及纵表，建议注明版本差异。 — 来源: https://github.com/Peoley199/luban （类型：惯例）
- 表模式对照：`map`（默认，普通 key-value 表，有主键）、`list`（无主键列表，支持联合主键 `a+b` 与独立多索引 `a,b`）、`one`/`singleton`（单例表，通常一行）。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 主键规则：「未写 index 且 mode 为 map 时，常默认取 value bean 的第一个字段。」 — 来源: https://www.datable.cn/docs/schema/excel-schema （类型：硬约束）
- 联合主键校验：「无论是否生成代码，导出数据时都会按联合索引校验主键合法性。」 — 来源: https://www.datable.cn/docs/schema/excel-schema （类型：硬约束）

### 1.5 对合并单元格的态度

- **合并单元格在 Luban 中是"一个字段占多列"的合法表达，不是被全面禁止**：官方原文「Excel 里一个字段占多列时，用**合并单元格**标出范围（不是把字段名在每一列各写一遍）。」 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
- 合并单元格 = 一个小结构：「一个字段（如「消耗」）占多列时，程序会把这几列**合并**，表示同属一个字段。请按从左到右的子字段填，**不要拆开合并区域**，也不要在中间插入无关列。」 — 来源: https://www.datable.cn/docs/designer/complex （类型：硬约束）
- 多级表头（列限定）的动机：「复合结构若纯流式按列顺序填，**空白单元格会被自动跳过**，字段多时容易错位；流式也不支持『留空 = 默认值』。因此在 `##var` 下再写一行 `##var` 为子字段命名，可精确限定每列归属，提高可读性。」 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
- 常见坑（官方）：
  - 「合并单元格列数与 bean / 容器实际占用列数不一致。」 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
  - 「文档或表头里把字段名在每一列重复填写，和 Excel 合并语义不一致，也容易让策划误解。」 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
  - 「`list` 中间留空被忽略，导致元素错位（需要占位时改用紧凑格式或明确分隔）。」 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
- 检查清单：「合并单元格区域没有被拆开或列错位」「列表分隔符与样表一致」「多行列表的续行主键留空方式与样表一致」。 — 来源: https://www.datable.cn/docs/designer/checklist （类型：硬约束）
- CSV 等不支持合并单元格的格式：官方给出替代写法「在**起始列**写 `[{字段名}`，在**结束列**写 `{字段名}]`，中间列留空，语义等价于 Excel 合并」。 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
- **关键结论（供技能规范采信）**：Luban 并不"禁止合并单元格"；它禁止的是**随意拆/并表头**、**数据列与合并语义不一致**、**list 中间留空**。排版诊断时应区分"程序预设的结构性合并（保留）"与"策划手滑合并数据行（报警）"。 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）

### 1.6 对空行、空单元格的态度

- 「CSV 无法合并单元格…」同节指出「**空白格常被忽略**」（list/array/set 分列填时）。 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
- 「`string` 空单元格 = 空串；流式格式里若需空串，须用 `""`。」 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 「`datetime` 一般**不要留空**；缺省时分秒按 0 处理」；常见坑含「datetime 留空导致解析失败」。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 「除容器外可用 `T?`。都可用 `null` 表示空。」`int?` 可留空或填 `null`；可空列的"没有"按约定留空或 `null`。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 「若枚举有值为 `0` 的项，可留空取该项；否则留空会报错。」 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 完全空行的处理未在 Luban 5.x 文档中找到"截断"级明文规定；tabtoy v3 有明文「Empty Row Termination: Processing stops at first completely empty row」（见 §2.2）。Luban 侧**未找到可靠公开来源**给出同样明确的空行截断语义。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）

### 1.7 sheet 命名与文件命名

- sheet 选择语法：`sheet名@文件.xlsx` 只读某一个 sheet；示例 `Bag@item.xlsx`。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 文件组织 input 写法：`item.xlsx`（读全部有效 sheet）、`Bag@item.xlsx`（只读名为 Bag 的 sheet）、`a.xlsx,b.xlsx`（多文件合并成一张逻辑表）、`xlsx_dir`（读目录下文件）。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 表必须在 Schema 中声明（`<table name="TbItem" value="Item" index="id" input="item.xlsx"/>`）；`full_name` 表全名可带模块前缀（如 `item.TbEquip`）。 — 来源: https://www.datable.cn/docs/schema/excel-schema （类型：硬约束）
- 「Sheet 标题区以 `##` 开头（A1 常见为 `##` / `##var`）」「表已在配置工程中登记（不是只有自己本地 xlsx）」。 — 来源: https://www.datable.cn/docs/designer/checklist （类型：硬约束）
- Luban 官方 5.x 文档未强制规定业务数据文件的命名模板（如"某字母-表名-分组.xlsx"）；此类命名约定见于生态项目 GameFrameX 的 `tableImporter.name=gameframex`（`[any letter]-[table name]-[group]-[comment].xlsx`），属项目级约定而非 Luban 核心强制。 — 来源: https://github.com/GameFrameX/luban （类型：惯例）

### 1.8 数据校验与排版的关系（Luban 内建）

- 校验在**生成期**执行；发布流水线建议加 `--strict`（校验失败则生成失败）。 — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
- 校验写在**字段类型字符串**上（XML `type="..."` 或 Excel `##type`），即校验规则直接落在表头行，是"表头即 schema"的排版基础。 — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
- 校验器一览（官方原文摘录）：
  - 非默认：`int!`、`int?!` 不能为类型默认值 / null — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
  - 引用：`int#ref=item.TbItem` 必须是目标表合法主键；`int#ref=item.TbItem?` 0 或 `""` 时跳过 — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
  - 路径：`string#path=unity` 需 `-x pathValidator.rootDir=...` — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
  - 范围：`int#range=[1,100]` 开闭区间；`[1,]` / `[,100]` 半边无穷 — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
  - 容器大小：`(list#size=4),int` size 加在**容器**上 — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
  - 允许值集合：`int#set=1;2;3` 推荐用 `;` 分隔 — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
  - 正则：`string#regex=^[a-z]+$` — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
  - list 建索引：`(list#index=id),Foo` 元素某字段唯一 — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
- 「Excel 表头等价」示例：`##type  int  int#ref=item.TbItem  (list#sep=|),(int#ref=item.TbItem)`，若 `9999` 不在 `item.TbItem` 中生成期报错。 — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
- tag 过滤（行级）：数据行**第一列**填 tag；`##` 永久不导出；`test` 配 `--excludeTag test` 正式包去掉；`unchecked` 校验器跳过此记录（慎用）。 — 来源: https://www.datable.cn/docs/quality/tags （类型：硬约束）
- `--includeTag` 与 `--excludeTag` 不能同时使用。 — 来源: https://www.datable.cn/docs/quality/tags （类型：硬约束）

---

## 2. 其他配置表工具链规范对照

### 2.1 tabtoy（davyxu/tabtoy）v2 官方 Manual

- 「数据表单必须拥有4条信息行，从上到下分别是：字段名行、字段类型行、字段特性行、字段描述行。」 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：硬约束）
- 「首行首列单元格非空的表单，被识别为数据表单；表单(Sheet)名字前带有 `#` 时，表单内容不会被导出。」 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：硬约束）
- 字段名行：「以_或英文开头的标示符，不能包含中文」；字段类型行支持 `int32/int64/uint32/uint64/string/bool/float` 及枚举/结构体，数组加 `repeated`。 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：硬约束）
- 字段特性行（pbt 文本）：`RepeatCheck: true`（重复性检查，用于 ID 不重复）、`ListSpliter: "分隔符"`、`Default: "..."`、`MakeIndex: true`、`Alias: "字段中文名"`、`MustFill: true`。 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：硬约束）
- 分隔符反模式明文警告：「整形数值类在电子表格中的分隔符推荐使用分号`;` 切忌使用逗号`,` 因逗号为电子表格默认的大数分割符。」 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：硬约束）
- 字段描述行：「此行不解析，但请保留，并以中文编写注释，方便查看。」 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：惯例）
- 类型表单（`@Types`）每文件仅 1 个，含"文件特性行 + 类型字段描述行"；枚举「首值必须为0」「枚举值不能重复」；结构体字段不能再次包含结构体。 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：硬约束）
- 多文件合并：输入文件名用 `+` 连接（`Info.xlsx+Info2.xlsx`）；纵表在 `@Types` 的 1,1 单元格写 `Vertical: "true"`。 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：硬约束）

### 2.2 tabtoy v3（三表系统，DeepWiki 基于官方源码）

- 三表系统：Index（清单） / Type（类型） / Data（数据）分离，便于校验与多人协作。 — 来源: https://deepwiki.com/davyxu/tabtoy/3.1-input-format-specification （类型：硬约束）
- Index 表列：模式（`类型表`/`数据表`）、表类型、表文件名、标记（client/server 条件导出）。 — 来源: https://deepwiki.com/davyxu/tabtoy/3.1-input-format-specification （类型：硬约束）
- Type 表列：种类（`表头`/`枚举`）、对象类型、标识名、字段名、字段类型、数组切割、值、索引、标记。 — 来源: https://deepwiki.com/davyxu/tabtoy/3.1-input-format-specification （类型：硬约束）
- 校验规则：索引字段重复 `DuplicateValueInMakingIndex`、字段未定义 `HeaderFieldNotDefined`、重复表头 `DuplicateHeaderField`、类型不兼容。 — 来源: https://deepwiki.com/davyxu/tabtoy/3.1-input-format-specification （类型：硬约束）
- 注释与空行：「Row Comments: Prefix first column with `#` to exclude entire row」「Column Comments: Prefix header with `#` to exclude entire column」「**Empty Row Termination: Processing stops at first completely empty row**」。 — 来源: https://deepwiki.com/davyxu/tabtoy/3.1-input-format-specification （类型：硬约束）
- 多列数组：同名字的多列在导出内容中合并，空单元格填类型默认值。 — 来源: https://deepwiki.com/davyxu/tabtoy/3.1-input-format-specification （类型：硬约束）

### 2.3 Excel-to-JSON / 导出工具类（xlsx-exporter）

- 工作表首行定义字段名（必须是合法变量名，唯一，除非是集合类型），`#` 开头的列被忽略。 — 来源: https://github.com/yatyricky/xlsx-exporter （类型：硬约束）
- 第二行定义字段类型；第三行定义字段规则（`Unique` / `Index` / `Default:xxx`，多规则逗号分隔）；第四行留空，**数据从第五行开始**。 — 来源: https://github.com/yatyricky/xlsx-exporter （类型：硬约束）
- 枚举须定义在名为 `@Enum` 的工作表；首三列（Enum Name / Value / …）为枚举定义区。 — 来源: https://github.com/yatyricky/xlsx-exporter （类型：硬约束）
- 「同一个字段名多列会被合并进导出内容」，数组用 `[]`、map 用 `map<K,V>`。 — 来源: https://github.com/yatyricky/xlsx-exporter （类型：硬约束）

### 2.4 Unity ScriptableObject 导出链路

- XlsToJson（Unity 编辑器扩展）：把 Excel/Google Sheets 转成 Json / ScriptableObject / 静态 C# 值表类，并生成带 `FindRowByXxx()` 索引器的单例访问类。 — 来源: https://github.com/catsnipe/XlsToJson （类型：硬约束）
- XlsToJson 命名约束：「Sheet (tab) names must be alphanumeric. Rename the default Japanese tab name such as "シート1".」 — 来源: https://github.com/catsnipe/XlsToJson （类型：硬约束）
- 双向工作流：编辑过的数据可导出回 Excel；Google Spreadsheet 同步是单向的（spreadsheet 是 source of truth），分享 URL 不进仓库。 — 来源: https://github.com/catsnipe/XlsToJson （类型：惯例）
- Excel-to-Unity 示例：Excel 导出 Json → 构建 `[Serializable]` 数据类 → `ScriptableObject` 静态数据库（如 `DataCollectionBasic : ScriptableObject` 含多个 `List<>`）→ Unity 端 Reload。 — 来源: https://github.com/nbhung100914/excel-to-unity-example （类型：惯例）
- Luban 自身也支持导出 Unity ScriptableObject，并支持 Unity/Unreal/Cocos2x/Godot 等引擎，证明"Excel → 代码/数据 → 引擎资产"是通用链路。 — 来源: https://github.com/focus-creative-games/luban （类型：硬约束）

### 2.5 各工具链的共同约束（跨工具提炼）

- **多行表头是共识**：Luban 3~4 行标记行、tabtoy v2 固定 4 信息行、xlsx-exporter 3 规则行 + 数据从第 5 行起。差异只在具体行数与标记语法。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- **字段名用 ASCII 标识符、不用中文**：Luban 推荐 `xx_yy_zz`；tabtoy 「以_或英文开头，不能包含中文」；xlsx-exporter「必须是合法变量名」。 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：硬约束）
- **类型独立成行**：三者都把类型写在专门行/列，解析器据此做类型转换与校验。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- **主键/唯一性是一等公民**：Luban `index=` + 联合/独立索引校验；tabtoy `RepeatCheck` + `MakeIndex`；xlsx-exporter `Unique`/`Index` 规则。 — 来源: https://www.datable.cn/docs/schema/excel-schema （类型：硬约束）
- **枚举有专门定义区且约束严格**：Luban `__enums__`/枚举列；tabtoy 枚举首值必须为 0 且不可重复；xlsx-exporter `@Enum` 表。 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：硬约束）
- **分端导出（group/tag）普遍存在**：Luban `##group` c/s/tag；tabtoy `标记` 列 client/server；GameFrameX 文件名 group 段。 — 来源: https://www.datable.cn/docs/designer/groups （类型：硬约束）
- **注释行/列的 `#` 前缀约定跨工具一致**：Luban `#`/`##`；tabtoy `#` 前缀跳行/列；xlsx-exporter `#` 开头列忽略。 — 来源: https://www.datable.cn/docs/designer/headers （类型：硬约束）

---

## 3. 游戏策划配置表「可维护性」的排版共识

> 说明：本节多为"惯例/观点"，因游戏厂商内部表格规范很少公开成文；凡无可靠来源处已标注。

### 3.1 列顺序（ID 在前？）

- **ID/主键列放在最左**是硬性倾向而非纯习惯：Luban「未写 index 且 mode 为 map 时，常默认取 value bean 的第一个字段」——首列即默认主键。 — 来源: https://www.datable.cn/docs/schema/excel-schema （类型：硬约束）
- tabtoy 示例数据表首列即 `ID`，且重复性检查/索引通常加在 ID 列。 — 来源: https://github.com/davyxu/tabtoy/blob/6eaaa7c7/README.md （类型：惯例）
- xlsx-exporter 示例中 `UTID`（主键）为首列。 — 来源: https://github.com/yatyricky/xlsx-exporter （类型：惯例）
- 分组切列：Luban 复杂结构用合并单元格把同属一个字段的子列聚在一起，「请按从左到右的子字段填，不要在中间插入无关列」。 — 来源: https://www.datable.cn/docs/designer/complex （类型：硬约束）
- **未找到可靠公开来源**给出"ID 在前、分组列切分"的跨公司明文规范；以上为从工具默认行为推导的惯例。 — 来源: 本调研（类型：惯例）

### 3.2 宽表 vs 窄表的取舍

- 横表（一行一记录）是默认；单例/全局配置更适合纵表（一行一字段）。 — 来源: https://github.com/Peoley199/luban （类型：惯例）
- 复合结构"一行一数"会读不过来、拆表对策划和程序都不友好，Luban 因此支持多行字段 `*name`（同一主键下多行表示列表元素）。 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
- 列限定（多级表头）的取舍理由官方明确：流式按列顺序填"空白格会被自动跳过，字段多时容易错位"，故用额外 `##var` 子字段行精确限定归属。 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
- **未找到可靠公开来源**以"宽表/窄表"术语系统论述游戏配置表取舍；上述为从 Luban 文档推导的取舍依据。 — 来源: 本调研（类型：惯例）

### 3.3 注释列 / 备注列的位置

- Luban 推荐把注释列字段名写成 `#备注` 或留空，且示例中 `#备注` 置于**数据列之后（最右）**。 — 来源: https://www.datable.cn/docs/designer/headers （类型：惯例）
- 注释行用 `##`/`##comment` 置于表头区（字段中文说明）或用行首 `##` 置于数据区（草稿行）。 — 来源: https://www.datable.cn/docs/designer/headers （类型：硬约束）
- tabtoy 的"字段描述行"固定为第 4 信息行、以中文编写并保留。 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：惯例）
- **结论**：把"给人看的注释列放右侧、给机器看的类型/分组放上部"是跨工具的稳定模式。 — 来源: https://www.datable.cn/docs/designer/headers （类型：惯例）

### 3.4 版本与封版标记

- Luban 行级 tag 机制可承担"版本/封版"语义：`test`/`dev` 测试行统一打标，CI 正式生成加 `-e test`；`##` 标记永久废弃行。 — 来源: https://www.datable.cn/docs/quality/tags （类型：硬约束）
- 白名单式发布：`--includeTag ship` 只导出指定标记行，与 `--excludeTag` 互斥。 — 来源: https://www.datable.cn/docs/quality/tags （类型：硬约束）
- **未找到可靠公开来源**说明游戏行业在 Excel 表内用"版本号/封版日期"单元格做显式版本标记的标准做法；tag 机制是 Luban 的近似替代。 — 来源: 本调研（类型：惯例）

### 3.5 按模块分文件 vs 单文件多 sheet

- Luban 支持两种且都可成立：`sheet名@文件.xlsx` 单 sheet 读取；`a.xlsx,b.xlsx` 多文件合并为一张逻辑表；`xlsx_dir` 读目录下文件。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 生态项目 GameFrameX 用"目录即命名空间"，按模块分文件夹自动派生 generated code namespace。 — 来源: https://github.com/GameFrameX/luban （类型：惯例）
- 无数据的说明 sheet 可放在同一文件里（A1 不以 `##` 开头即被忽略）。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- tabtoy 用 Index 表集中登记多文件、多 sheet，本质也是"按模块分文件 + 清单汇总"。 — 来源: https://deepwiki.com/davyxu/tabtoy/3.1-input-format-specification （类型：硬约束）

### 3.6 行业分享中的观点（GDC）

- GDC 2024/2025 的 Spreadsheets Microtalks 明确："Spreadsheets! They're the most versatile tool in a game designer's palette, offering unmatched possibilities."，讲者来自 Double Fine、EA Maxis、Hyperkinetic Studios 等。 — 来源: https://gdcvault.com/play/1035550/Tools-Summit-A-Series-of （类型：观点）
- Epic Tavern 案例：「built directly from the google sheets into the game's data…The spreadsheets were set up to organize the data, but we needed to devise a way to work together on the story…in a way that worked for the data but didn't make thinking about the story impossible.」——说明"表格结构要服务数据，也要不阻碍人的思考"。 — 来源: https://gdcvault.com/play/1035719/Spreadsheets （类型：观点）
- Merchant Guilds 案例：团队用 Apps Scripts 把表格内容直接部署，「making it a trusted source for live game content」——支撑"表格即单一数据源"的维护理念。 — 来源: https://gdcvault.com/play/1035550/Tools-Summit-A-Series-of （类型：观点）
- 本地化案例（Cheryl Platz）：把 Figma 文件转成 Google Sheets 驱动的多语言，说明表格作为跨职能协作界面的价值。 — 来源: https://gdcvault.com/play/1035719/Spreadsheets （类型：观点）
- 数值可视化观点：「special emphasis on creating data-driven spreadsheets that allow for easy visualization and iteration of the data.」 — 来源: https://gdcvault.com/play/1016268/Fundamental-Multiplayer-RPG （类型：观点）
- **谨慎说明**：GDC 演讲多谈"表格作为设计/原型/经济模拟工具"，直接讲"配置表排版规范（表头行数、列顺序、颜色图例）"的公开演讲**未找到可靠公开来源**。 — 来源: 本调研（类型：观点）

---

## 4. 配置表「可校验性」与排版的关系

### 4.1 数据验证（下拉列表、范围限制）

- 微软官方：数据验证可"限制数据类型或用户输入单元格的值，例如下拉列表"；允许类型包括整数、小数、列表、日期、时间、文本长度、自定义。 — 来源: https://support.microsoft.com/kb/211485 （类型：硬约束）
- 数据验证可"将输入限制为预定义列表项""限制指定区间外的数字""限制特定时间框架外的日期""限制文本字符数""基于公式或其他单元格值验证"。 — 来源: https://support.microsoft.com/zh-cn/office/more-on-data-validation （类型：硬约束）
- 数据验证有"输入消息"与"错误警报"两类提示；错误样式含 Stop / Warning 等。 — 来源: https://support.microsoft.com/kb/211485 （类型：硬约束）
- 映射到配置表：枚举列用"列表"验证对齐 Luban `#set=`/枚举 alias；数值列用"整数/小数 + 范围"对齐 Luban `#range=[1,100]`；日期列用"日期"验证对齐 `datetime`。 — 来源: https://support.microsoft.com/kb/211485 （类型：惯例）
- **注意边界**：Excel 数据验证是"录入期软拦截"，Luban `#range`/`#ref` 是"生成期硬校验"；二者应叠加，不能互相替代。 — 来源: https://www.datable.cn/docs/quality/validators （类型：惯例）

### 4.2 条件格式标错

- 微软官方：可用"突出显示单元格规则 → 重复值"给重复数据上色，"对重复数据进行颜色编码可以帮助您找到并在必要时删除该数据"。 — 来源: https://support.microsoft.com/zh-cn/excel/filter-for-or-remove-duplicate-values （类型：硬约束）
- 高级规则：使用公式 `=COUNTIF($A$2:$A$400,A2)>1` 标重复；"唯一/重复值"格式规则会将 `*` 和 `?` 视为通配符。 — 来源: https://support.microsoft.com/zh-cn/topic/ef68c97a-1b5e-47eb-9b3f-a548f941df4f （类型：硬约束）
- DBCS 语言环境下"重复值"规则会视全角/半角字符相同；需区分时用 COUNTIF 公式规则。 — 来源: https://support.microsoft.com/zh-hk/topic/34402f91-c7e7-4060-944c-65d913033d18 （类型：硬约束）
- **映射到配置表**：ID 列用"重复值"条件格式标红（对齐 Luban map 主键唯一/tabtoy RepeatCheck）；必填列用"空值"规则标黄（对齐 MustFill/非空约束）；数值越界用公式规则标橙（对齐 `#range`）。 — 来源: https://support.microsoft.com/zh-cn/excel/filter-for-or-remove-duplicate-values （类型：惯例）
- "空值标黄 / 越界标橙"的具体色值行业无统一标准，**未找到可靠公开来源**规定；此处为可定制的排版约定。 — 来源: 本调研（类型：惯例）

### 4.3 冻结策略

- **未找到可靠公开来源**（微软/Luban/tabtoy 官方文档均未给出配置表专用冻结行列数）。
- 从表结构推导的惯例：冻结表头标记行（Luban 3~4 行 `##var/##type/##group/##comment`）+ 首列主键列，便于横向滚动时保持字段名与 ID 可见。 — 来源: https://www.datable.cn/docs/excel/basics （类型：惯例）

### 4.4 让"程序改过的字段"一眼可见

- Luban 的 group 机制要求"改 group 后要重新生成，旧客户端数据不会自动变"，即字段归属变化需走重新生成流程。 — 来源: https://www.datable.cn/docs/designer/groups （类型：硬约束）
- 行级 tag（`##` 永久注释、`test`/`dev`）提供了"哪些行是草稿/正式"的可视区分手段。 — 来源: https://www.datable.cn/docs/quality/tags （类型：硬约束）
- "人工填写区 vs 程序生成区"用颜色区分、以及颜色图例：Luban 官方用 `##group` 标记"给谁的字段"，但未规定单元格填色方案；**未找到可靠公开来源**规定配置表颜色图例标准。 — 来源: 本调研（类型：惯例）

---

## 5. 策划表 vs 程序表 vs 运营表（同一数据的排版差异）

- Luban 将读者明确分工："程序：定义 schema、写生成命令、运行时加载；策划：按约定在 Excel 填数据。" — 来源: https://www.datable.cn/docs/intro （类型：硬约束）
- 策划关注"表头有规矩、注释列、主战场在数据行"；程序关注 `##type`/`##group`/主键/引用校验；二者看同一 sheet 的不同部分。 — 来源: https://www.datable.cn/docs/designer/concepts （类型：硬约束）
- `##group` 直接造成"客户端/服务器看到不同列"——同一份数据在不同端导出结果不同：如 `icon` 仅 c、`drop_weight` 仅 s。 — 来源: https://www.datable.cn/docs/designer/groups （类型：硬约束）
- 表级分组可让"整张表只属于客户端或服务器"，另一端的导出里根本不出现该表。 — 来源: https://www.datable.cn/docs/designer/groups （类型：硬约束）
- 行级 tag 可让同一文件同时承载"测试行/正式行"，运营/测试与发布读不同子集。 — 来源: https://www.datable.cn/docs/quality/tags （类型：硬约束）
- 独立说明 sheet（A1 非 `##`）可放"策划说明/字段字典"，供人阅读而不导出，是面向策划/运营的文档层。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- **未找到可靠公开来源**以"策划表/程序表/运营表"三分法系统论述排版策略；以上为从 Luban 的 group/tag/schema 分工推导的对应关系。 — 来源: 本调研（类型：惯例）

---

## 6. 反模式清单（配置表最常见排版错误）

### 6.1 有官方明文支撑的反模式

- Sheet A1 不是 `##` 开头 → 整表被跳过。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- 只建了 xlsx 忘了在 `__tables__` 注册 → 数据文件不会被收集。 — 来源: https://www.datable.cn/docs/guide/add-table （类型：硬约束）
- 把 `##type` 类型名改成中文（如 `int` 改成"整数"）→ 类型报错。 — 来源: https://www.datable.cn/docs/designer/concepts （类型：硬约束）
- 备注列没加 `#` → 被当成正式列填了值却进游戏。 — 来源: https://www.datable.cn/docs/designer/headers （类型：硬约束）
- 某行怎么改都不生效 → 该行第一格是 `##` 注释行。 — 来源: https://www.datable.cn/docs/designer/headers （类型：硬约束）
- 合并单元格列数与 bean/容器实际占用列数不一致；把字段名在每一列重复填写与 Excel 合并语义不一致。 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
- `list` 中间留空被忽略导致元素错位；map 只写 key 没写 value。 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
- datetime 留空导致解析失败。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- "主键不重复（map 表）""引用到的 id 在目标表真实存在"是检查清单硬项。 — 来源: https://www.datable.cn/docs/designer/checklist （类型：硬约束）
- tabtoy：字段名含中文；枚举首值非 0 或重复；数值列用逗号做分隔符（逗号是电子表格默认大数分隔符）。 — 来源: https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md （类型：硬约束）
- tabtoy v3：重复表头 `DuplicateHeaderField`、字段未定义 `HeaderFieldNotDefined`、索引重复 `DuplicateValueInMakingIndex`。 — 来源: https://deepwiki.com/davyxu/tabtoy/3.1-input-format-specification （类型：硬约束）
- xlsx-exporter：字段名非合法变量名、非唯一（集合类型除外）。 — 来源: https://github.com/yatyricky/xlsx-exporter （类型：硬约束）
- XlsToJson：sheet 名非字母数字（如默认日文"シート1"）。 — 来源: https://github.com/catsnipe/XlsToJson （类型：硬约束）

### 6.2 用户点名但无可靠公开来源的反模式

以下为用户要求覆盖的反模式，但**未找到可靠公开来源**将其明确列为"配置表排版错误"的权威条目；本报告基于工具约束给出可验证的近似判据：

- 列宽不统一：无可靠公开源；仅属视觉规范，不影响 Luban 导出。 — 来源: 本调研（类型：惯例）
- 混用全角符号：微软文档指出 DBCS 环境下"重复值"规则会把全角/半角视同，可能造成误判；可作为"混用全角半角有害"的间接证据。 — 来源: https://support.microsoft.com/zh-hk/topic/34402f91-c7e7-4060-944c-65d913033d18 （类型：惯例）
- 日期存成文本：Luban `datetime` 接受 Excel 日期或 `yyyy-mm-dd ...` 字符串，但"随便留空"会解析失败；存成任意文本是否报错**未找到可靠公开来源**明文。 — 来源: https://www.datable.cn/docs/excel/basics （类型：惯例）
- 数字存成文本：Luban `int` 填文字会类型报错（"文字进了 int"），可间接支撑。 — 来源: https://www.datable.cn/docs/designer/headers （类型：硬约束）
- 隐藏列藏着关键字段：Luban 按列位置读取，隐藏列仍会被读取（无明文禁止），但"隐藏导致人漏看"属 UX 判断，**未找到可靠公开来源**。 — 来源: 本调研（类型：惯例）
- 颜色无图例：Luban 官方未规定配色/图例，属自定义规范空白。 — 来源: 本调研（类型：惯例）

---

## 7. 给技能规范的提炼（供 UX 设计师技能采信）

> 本节是把调研结论转成"配置表排版诊断规则"的建议草案，均标明来源类型。

- **表头区硬规则集**：A1 以 `##`/`##var` 开头；保留 `##type`/`##group` 行；类型名不得汉化；注释列用 `#`。这是与 Luban 兼容的最低要求。 — 来源: https://www.datable.cn/docs/excel/basics （类型：硬约束）
- **结构性合并 vs 破坏性合并**：诊断时先识别合并单元格是否为"程序预设的子结构"（有下级 `##var` 子字段行）；是则保护，否则报警。 — 来源: https://www.datable.cn/docs/excel/nested-and-collections （类型：硬约束）
- **校验下沉到表头**：把 `#range`/`#ref`/`#set` 写进 `##type` 行，使"排版即 schema"；Excel 侧再叠加数据验证与条件格式做录入期提示。 — 来源: https://www.datable.cn/docs/quality/validators （类型：硬约束）
- **分端可视化**：在 `##group` 行用颜色区分 c/s/空列，并配图例；这是从 Luban group 语义派生的 UX 约定（图例本身无官方标准）。 — 来源: https://www.datable.cn/docs/designer/groups （类型：惯例）
- **草稿/封版用 tag 而非删数据**：行首 `##` 永久废弃，`test`/`dev` 配 CI `--excludeTag`。 — 来源: https://www.datable.cn/docs/quality/tags （类型：硬约束）
- **校验三件套对照表**：主键唯一（Excel 重复值条件格式 ↔ Luban map index）、必填非空（空值条件格式 ↔ MustFill/`!`）、范围/枚举（数据验证下拉/范围 ↔ `#range`/`#set`）。 — 来源: https://support.microsoft.com/zh-cn/excel/filter-for-or-remove-duplicate-values （类型：惯例）
- **冻结策略建议**：冻结表头标记行 + 主键首列（无官方来源，属推导惯例）。 — 来源: 本调研（类型：惯例）

---

## 8. 来源索引（按可靠度）

### 8.1 硬事实来源（官方）

1. Luban GitHub：https://github.com/focus-creative-games/luban
2. Luban 文档 · Excel 基础：https://www.datable.cn/docs/excel/basics
3. Luban 文档 · 嵌套与容器：https://www.datable.cn/docs/excel/nested-and-collections
4. Luban 文档 · 表头含义：https://www.datable.cn/docs/designer/headers
5. Luban 文档 · 最小概念：https://www.datable.cn/docs/designer/concepts
6. Luban 文档 · 复杂结构：https://www.datable.cn/docs/designer/complex
7. Luban 文档 · 分组：https://www.datable.cn/docs/designer/groups
8. Luban 文档 · 检查清单：https://www.datable.cn/docs/designer/checklist
9. Luban 文档 · 校验器：https://www.datable.cn/docs/quality/validators
10. Luban 文档 · tag 过滤：https://www.datable.cn/docs/quality/tags
11. Luban 文档 · Excel Schema：https://www.datable.cn/docs/schema/excel-schema
12. Luban 文档 · 加一张表：https://www.datable.cn/docs/guide/add-table
13. Luban 文档 · 能力清单：https://www.datable.cn/docs/reference/features
14. tabtoy v2 Manual：https://github.com/bbajm/tabtoy/blob/master/doc/Manual_V2.md
15. tabtoy v3（DeepWiki，基于官方源码）：https://deepwiki.com/davyxu/tabtoy/3.1-input-format-specification
16. xlsx-exporter：https://github.com/yatyricky/xlsx-exporter
17. XlsToJson：https://github.com/catsnipe/XlsToJson
18. Excel-to-Unity 示例：https://github.com/nbhung100914/excel-to-unity-example
19. Excel 数据验证（微软）：https://support.microsoft.com/kb/211485
20. Excel 重复值条件格式（微软）：https://support.microsoft.com/zh-cn/excel/filter-for-or-remove-duplicate-values
21. Excel 条件格式公式（微软）：https://support.microsoft.com/zh-cn/topic/ef68c97a-1b5e-47eb-9b3f-a548f941df4f

### 8.2 观点/生态来源

22. GDC Tools Summit Spreadsheets Microtalks：https://gdcvault.com/play/1035550/Tools-Summit-A-Series-of
23. GDC Spreadsheets Microtalks：https://gdcvault.com/play/1035719/Spreadsheets
24. GDC Fundamental Multiplayer RPG Math：https://gdcvault.com/play/1016268/Fundamental-Multiplayer-RPG
25. GameFrameX/luban（生态约定）：https://github.com/GameFrameX/luban
26. Luban 历史/fork 写法参考（非规范）：https://github.com/Peoley199/luban

### 8.3 明确未找到可靠公开来源的条目

- Luban 对"完全空行"的明确截断语义（tabtoy v3 有，Luban 5.x 文档未明确）。
- 游戏行业"列顺序 / 宽窄表 / 版本封版标记 / 颜色图例 / 按模块分文件"的跨公司明文规范。
- 以"策划表/程序表/运营表"三分法系统论述排版的公开文章或演讲。
- 配置表专用冻结行列数的官方建议。
- "日期/数字存成文本""隐藏列藏字段""列宽不统一"的权威反模式条目。
