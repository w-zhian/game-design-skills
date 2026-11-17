# Agent 2 调研：Excel 工作簿的工程规范与成熟审美惯例

> 调研目标：为「Excel 表格排版 UX 设计师」技能提供「行业内已形成共识的表长什么样」的可验证依据。
> 调研日期：2026-11-17
> 方法：WebSearch / WebFetch 实检索；所有色值均来自官方设计系统文档；WCAG 对比度为本人按 W3C 公式实测计算（见 §4.4）。
> 排除来源：知乎、微信公众号、百度百科/知道、CSDN 洗稿——本次检索未采用上述来源。

## 0. 可信度分级（本文统一口径）

| 标记 | 含义 |
|---|---|
| 一手官方文档 | Microsoft Learn / Microsoft Support、W3C、各设计系统官方文档 |
| 专业机构标准 | Wall Street Prep、CFI、FMI/FAST、IBM Carbon、Ant Design、Material 3、Tailwind 官方 |
| 行业培训/媒体 | 投行培训机构、行业博客、专业社区文章（可佐证，但需交叉验证） |
| 实测计算 | 本文按公开公式自行计算（如 WCAG 对比度），非来源原文直接给出 |
| 未验证，需实测 | 无法从来源确认，明确标注，禁止凭记忆填值 |

---

## 1. 财务建模 / 投行 Excel 的「颜色语义」惯例

这是 Excel 视觉规范中最成熟、最接近「行业标准」的体系。核心目的：让审阅者在 30 秒内判断「这是什么类型的单元格」，从而决定能否修改、是否需要追溯来源。**注意：各机构存在细微差异，本文保留冲突，不强行统一。**

### 1.1 Wall Street Prep（WSP）标准

WSP 在 3-Statement Model 教程中给出五档颜色，比多数机构多一档「数据供应商链接」：

| 类型 | 颜色 | 原文 |
|---|---|---|
| Hard-coded numbers (inputs) | Blue（蓝字） | 硬编码输入 |
| Formulas (calculations) | Black（黑字） | 公式/计算 |
| Links to other worksheets | Green（绿字） | 链接到其他工作表 |
| Links to other files | Red（红字） | 链接到其他文件 |
| Links to data providers (CIQ, FactSet) | Dark Red（深红字） | 链接到外部数据商 |

— 来源: https://wallstreetprep.com/knowledge/build-integrated-3-statement-financial-model （可信度：专业机构标准）

WSP 另外明确：历史数据「直接输入且不应改动」用蓝字，公式（如 PPE Closing）用黑字；预测值若来自同一工作簿其他 tab 的链接，用黑字而非蓝字。— 来源: https://wallstreetprep.com/knowledge/profit-loss （可信度：专业机构标准）

WSP 的月度现金流教程里有一句关键补充：若 "Expected" 列的值是从明细模型链接进来的，应为**黑字**而非蓝字（因为它是工作簿内链接），只有真正硬编码才用蓝字。— 来源: https://wallstreetprep.com/knowledge/monthly-cash-flow-forecast-model （可信度：专业机构标准）

> **诊断要点**：WSP 口径下「绿字」并非所有跨表链接，而是「链接到其他工作表」；WSP 对「链接到其他文件」用红、「数据商」用深红。不要与 CFI 口径混用。

### 1.2 Corporate Finance Institute（CFI / FMVA）标准

CFI 的四档口径：

| 类型 | 颜色 |
|---|---|
| Hard-coded numbers / inputs | Blue（蓝字） |
| Formulas referring to other cells（同表公式引用） | Black（黑字） |
| References to other worksheets（跨工作表引用） | Green（绿字），CFI 明确说 green 正变得越来越常见 |
| References to external sources（外部来源引用） | Red（红字） |

— 来源: https://corporatefinanceinstitute.com/resources/excel/cool-excel-spreadsheets/ （可信度：专业机构标准）

CFI 在《Financial Modeling Best Practices》PDF 中的表述略有收窄：只强调「blue font for hard-codes and inputs，formulas can stay black」，并说「green is becoming more common for links to another worksheet，而 workbook links、hyperlinks、external data 没有清晰的颜色惯例」。— 来源: https://corporatefinanceinstitute.com/assets/CFI-Financial-Modeling-Best-Practices-2018-Case-Championships.pdf （可信度：专业机构标准）

CFI 的 Excel Test 把「蓝字=硬编码、黑字=公式」作为可考核的正确选项。— 来源: https://corporatefinanceinstitute.com/resources/knowledge/tests/excel-test （可信度：专业机构标准）

CFI 的模型审计文章把「格式不当或不一致」列为常见模型错误，并明确推荐蓝字硬编码、黑字公式，因为这样审计更快。— 来源: https://corporatefinanceinstitute.com/learn/resources/financial-modeling/model-audit/ （可信度：专业机构标准）

### 1.3 Financial Modeling Institute（FMI）与 FAST Standard

FMI 在 Advanced Financial Modeler (AFM) Body of Knowledge 中：蓝字=输入、黑字=同表公式或链接，并允许第三种深色用于「链接到 assumptions tab 或其他由建模者定义的用途」。— 来源: https://claritylab.one/using-colour-to-encode-meaning-in-financial-models （可信度：行业培训/媒体，转述 FMI 官方 Body of Knowledge）

FAST Standard（Flexible/Appropriate/Structured/Transparent）：**红字=exports（导出）、蓝字=imports（导入）**；用灰色底纹表示 sheet 内逆向计算流（counter-flow）；用黄色底纹+显式方括号标签标记临时代码。FAST 明确说「具体颜色选择没那么重要，重要的是保持一套可被团队一致解读的建模语言」。— 来源: https://claritylab.one/using-colour-to-encode-meaning-in-financial-models （可信度：行业培训/媒体，转述 FAST 标准）

> **冲突保留**：FAST 的「红=导出」与投行主流「红=外部文件链接/错误警示」语义不同；若技能要输出「红字」诊断，必须区分「FAST 语境」与「投行语境」。

### 1.4 其他投行/行业口径（佐证与差异）

| 来源 | 蓝 | 黑 | 绿 | 红 | 其他 |
|---|---|---|---|---|---|
| Wall Street Prep | 硬编码输入 | 公式 | 跨工作表链接 | 跨文件链接 | 深红=数据商链接 |
| CFI | 硬编码输入 | 同表公式/引用 | 跨工作表引用 | 外部来源引用 | — |
| FMI (AFM) | 输入 | 同表公式/链接 | 第三种深色（可选） | — | 允许建模者自定义第三色 |
| FAST | imports 导入 | — | — | exports 导出 | 灰底=逆向流；黄底=临时代码 |
| IIM SKILLS（Wall Street 通用语言） | 输入/硬编码/历史值/假设/驱动 | 公式、同表引用 | 公式、sheet 引用（部分模型省略） | 必须修正的错误 | 紫=链接其他 Excel 文件（部分模型省略） |
| dealacademy.co.uk | 硬编码输入与假设 | 公式/计算 | 跨 sheet 链接 | 外部文件链接（少用） | — |
| ibinterviewquestions.com | 硬编码输入 | 同表公式 | 跨 sheet 链接 | 需注意/错误/占位符（红字或红底） | 部分银行加紫字=外部文件链接 |

— 来源: https://iimskills.com/financial-modeling-best-practices/ （可信度：行业培训/媒体）
— 来源: https://dealacademy.co.uk/blog/financial-modelling-best-practices （可信度：行业培训/媒体）
— 来源: http://ibinterviewquestions.com/guides/valuation-investment-banking/formatting-standards-color-conventions-ib-models （可信度：行业培训/媒体）
— 来源: https://www.financial-modeling.com/clean-financial-model-architecture-excel-investment-banking/ （可信度：行业培训/媒体）

### 1.5 黄色底纹的语义（重要：各源不一致）

- CFI aligned FMVA：黄色填充是输入单元格上「常见的额外标记」，但**字体颜色才是 FMVA 教学的识别符**；不要把黄底当作替代方案（黑白打印、Show Formulas 检查时黄底会丢失）。— 来源: https://open-exam-prep.com/study-guides/fmva/modeling-guidelines/color-conventions-and-formatting （可信度：行业培训/媒体，转述 CFI FMVA 课程）
- FAST：黄色底纹=临时代码，并要求配显式方括号标签。— 来源: https://claritylab.one/using-colour-to-encode-meaning-in-financial-models （可信度：行业培训/媒体，转述 FAST 标准）
- ibinterviewquestions：红字或红底=需注意、含错误、最终版前必须更新的占位符。— 来源: http://ibinterviewquestions.com/guides/valuation-investment-banking/formatting-standards-color-conventions-ib-models （可信度：行业培训/媒体）
- 建模一手建议：浅蓝底用于输入、灰底用于计算，与字体颜色叠加形成双通道提示。— 来源: https://tiltanalytics.com/good-vs-bad-financial-model/ （可信度：行业培训/媒体）

> **冲突保留**：黄色底在 CFI 语境=输入增强标记，在 FAST 语境=临时代码。技能诊断黄底时必须结合上下文，不要单一判定为「待复核」。

### 1.6 关于「精确 RGB 值」的警告

FMVA 对齐指南明确：CFI **不要求记忆某个未公开的 RGB 值**， firms vary RGB values，不应声称存在「CFI 秘密色号」。— 来源: https://open-exam-prep.com/study-guides/fmva/modeling-guidelines/color-conventions-and-formatting （可信度：行业培训/媒体）

Daloopa 同样指出：虽然黑/蓝/绿/红是行业标准，但具体每个颜色对应什么由各金融机构自行确认。— 来源: https://daloopa.com/?p=2667 （可信度：行业培训/媒体）

> **结论**：本文只规定语义映射，不编造「投行标准蓝 = #XXXXXX」。若要给脚本落地色值，用 §4 的设计系统 HEX，并注明「这是 UX 配色，不是投行语义标准色」。

---

## 2. 工作簿结构的经典规范

### 2.1 I-C-O 原则（Inputs / Calculations / Outputs 物理分离）

- I-C-O 三原则：Inputs 存放所有硬编码假设，必须集中在专门的 Assumptions 工作表；Calculations 只含引用输入或前置计算的公式；Outputs 是呈现层，只含指向计算区的链接。目标是「VP 改一个输入数字，变更可预测地传导，无需改计算公式」。— 来源: https://www.financial-modeling.com/clean-financial-model-architecture-excel-investment-banking/ （可信度：行业培训/媒体）
- 推荐的 tab 顺序：README/Index → Assumptions → Historicals/Data → Projections(IS/BS/CFS) → 支持性 schedule（Debt/CAPEX/WCR）→ Valuation → Summary/Dashboard → Checks。其中 Assumptions 是「唯一应该出现蓝字的地方」，Checks 是专门的错误标记页。— 来源: https://www.financial-modeling.com/clean-financial-model-architecture-excel-investment-banking/ （可信度：行业培训/媒体）
- 三表模型的结构规则：用 roll-forward schedule 预测资产负债表项目；把输入聚合到一个 worksheet 或一个 section，与计算和输出分离；避免文件间链接。— 来源: https://wallstreetprep.com/knowledge/build-integrated-3-statement-financial-model （可信度：专业机构标准）
- CFI：把不同类型数据放在不同表格和工作表中；财务模型的输入（不同情景下的假设）通常与建模过程其他部分分开存放；工作簿开头加封面页，让受众第一眼知道文件是什么、谁准备的。— 来源: https://corporatefinanceinstitute.com/resources/excel/cool-excel-spreadsheets/ （可信度：专业机构标准）
- CFI 模型结构建议：也可把整个模型建在一张 worksheet 上，用分组（grouping）划分 section，便于展开/收缩和移动；自上而下顺序为 假设与驱动 → 利润表 → 资产负债表 → 现金流量表 → 支持性 schedule → 估值 → 敏感性分析 → 图表。— 来源: https://corporatefinanceinstitute.com/assets/CFI-Financial-Modeling-Best-Practices-2018-Case-Championships.pdf （可信度：专业机构标准）

> **冲突保留**：CFI 同时给出「一张表 + 分组」与「多个 worksheet 分离」两种方案；投行实践更偏向后者。对游戏数值策划的上万行配置表，「一个 sheet 一个职责」更可执行。

### 2.2 禁止 magic number（公式里硬编码数字）

- 「One Formula, One Row」：某一行第一个单元格的公式应可原样复制到该行所有期间，不得在公式里直接写死增长率等输入。— 来源: https://iimskills.com/financial-modeling-best-practices/ （可信度：行业培训/媒体）
- 「公式中不得含硬编码数字」：硬编码数字难以被审阅者发现，应把所有输入集中到同一 tab，公式去引用它。— 来源: https://iimskills.com/financial-modeling-best-practices/ （可信度：行业培训/媒体）
- ibinterviewquestions：每个输入都应从 assumptions tab 流入；公式单元格中硬编码数字是最常见也最危险的建模错误之一。— 来源: http://ibinterviewquestions.com/guides/valuation-investment-banking/formatting-standards-color-conventions-ib-models （可信度：行业培训/媒体）
- 结构常数（如一年 12 个月、365 天）在 CFI 风格中也倾向放入带标签的输入单元格，因为 360/365 天惯例可能变化。— 来源: https://open-exam-prep.com/study-guides/fmva/modeling-guidelines/color-conventions-and-formatting （可信度：行业培训/媒体）

### 2.3 时间轴横向排布惯例

- 「Time flows left to right：历史年在左、预测年在右，永不反向。」— 来源: https://dealacademy.co.uk/blog/financial-modelling-best-practices （可信度：行业培训/媒体）
- CFI：用不同颜色区分历史期与预测期（历史行底色高亮、历史硬编码蓝字、预测公式黑字），使事实与预测的边界可视。— 来源: https://corporatefinanceinstitute.com/resources/excel/cool-excel-spreadsheets/ （可信度：行业培训/媒体）
- WSP：以最短期间（年/季/月/周）决定模型周期性，年度用于 DCF/LBO，季度用于股权研究/信用/FP&A/并表，月度用于重组与项目融资，周用于破产 13 周现金流。— 来源: https://wallstreetprep.com/knowledge/build-integrated-3-statement-financial-model （可信度：专业机构标准）

### 2.4 命名 sheet、导航与 index 页

- CFI：始终给 worksheet、chart、table 起标题；标题要有意义且精确，让用户一眼抓住要点。— 来源: https://corporatefinanceinstitute.com/resources/excel/documenting-excel-models-best-practices/ （可信度：专业机构标准）
- CFI：用超链接快速访问工作簿其他 section，常用于目录页（table of contents）链接到不同 worksheet/section，也可指向上下文信息或重要公式。— 来源: https://corporatefinanceinstitute.com/resources/excel/documenting-excel-models-best-practices/ （可信度：专业机构标准）
- CFI：Grouping 功能可折叠所有 section，使模型呈现「目录」外观。— 来源: https://corporatefinanceinstitute.com/resources/excel/documenting-excel-models-best-practices/ （可信度：专业机构标准）
- 封面/Index 页应包含模型标识、版本历史、日期、联系人。— 来源: https://www.financial-modeling.com/clean-financial-model-architecture-excel-investment-banking/ （可信度：行业培训/媒体）
- WSP：一个 sheet 一个职责的结构使审核路径线性化——每个输出追溯到计算 tab，计算 tab 追溯到假设 tab。— 来源: http://ibinterviewquestions.com/guides/valuation-investment-banking/financial-model-architecture-layout-flow （可信度：行业培训/媒体）

---

## 3. 微软官方对表格（Excel Table / ListObject）与格式的建议

### 3.1 何时应该转成正式 Table 对象

微软官方列出的 Table 优势：

- 结构化引用（structured references）：在表中输入公式时，Excel 自动用列名代替单元格地址，使公式更易理解；表外也可使用「表名+列名」的组合引用。— 来源: https://corporatefinanceinstitute.com/resources/excel/documenting-excel-models-best-practices/ （可信度：专业机构标准，转述微软功能）
- 自动扩展/收缩：结构化引用随表格大小增减自动扩展或收缩；内嵌在表中的公式也随数据扩展收缩；相比整列引用和动态范围，性能劣势更小。— 来源: https://learn.microsoft.com/zh-hk/office/vba/excel/concepts/excel-performance/excel-tips-for-optimizing-performance-obstructions （可信度：一手官方文档）
- 带状行（Banded Rows）：奇数行与偶数行交替底纹「for ease of reading」；新增或删除行时自动带状继续生效。— 来源: https://support.microsoft.com/en-us/excel/format-an-excel-table （可信度：一手官方文档）
- 筛选按钮（AutoFilter）、标题行、合计行（SUBTOTAL，可含/忽略隐藏行）、首列/末列强调。— 来源: https://support.microsoft.com/en-us/excel/format-an-excel-table （可信度：一手官方文档）
- 套用表样式时，Excel 会自动把数据区域转换为表格；不想用表格功能时可「转换为范围」但保留样式。— 来源: https://int.support.office.com/f1/article/6789619F-C889-495C-99C2-2F971C0E2370 （可信度：一手官方文档）
- 微软数据工厂文档给出的选择指南：需要筛选下拉、结构化引用公式、一张表放多个数据块、用 StartCell 精确控制位置、套用 TableStyleMedium1 等样式时用 Table。— 来源: https://learn.microsoft.com/zh-hk/fabric/data-factory/dataflow-gen2-data-destinations-excel-advanced （可信度：一手官方文档）

### 3.2 什么时候不该用 Table（微软官方语境）

- 只需要简单单一数据块、从 A1 开始、**不需要 Excel 表格功能（筛选器、结构化引用）**时，用 SheetData 而非 Table。— 来源: https://learn.microsoft.com/zh-hk/fabric/data-factory/dataflow-gen2-data-destinations-excel-advanced （可信度：一手官方文档）
- 想要没有表格格式的原始数据、要省略表头、数据将被需要纯范围的其他系统使用时，用 Range。— 来源: https://learn.microsoft.com/zh-hk/fabric/data-factory/dataflow-gen2-data-destinations-excel-advanced （可信度：一手官方文档）
- 若只要表格样式而不要表格功能，可把表格转换为一般数据范围；但**转换后向范围新增数据时不会自动带状**。— 来源: https://support.microsoft.com/zh-tw/office/將底紋套用至工作表中的替代列或欄-a443b0f5-2025-42f6-9099-5de09c05e880 （可信度：一手官方文档）
- 结构化引用区分大小写；不能引用表外单元格；表重命名后需更新公式。— 来源: https://learn.microsoft.com/en-us/answers/questions/5232908/problem-with-excel-workbook-links-on-onedrive （可信度：一手官方文档，Microsoft Learn 社区答复）
- 对财务模型：CFI 的约定是「模型内尽量少跨文件链接」，Table 更适合原始数据层而非呈现层。— 来源: https://corporatefinanceinstitute.com/resources/excel/documenting-excel-models-best-practices/ （可信度：专业机构标准）

> **诊断规则建议**：数据明细/原始数据区 → 用 Table；财务模型计算区与汇报表头 → 保持普通 Range（避免结构化引用污染 audit 路径）。

### 3.3 条件格式最佳实践

- CFI：条件格式可对满足条件的 cell 应用基于颜色的格式，如色阶（高分绿、低分红）；规则可自定义；图表建议只用 2-3 色并保持同主题。— 来源: https://corporatefinanceinstitute.com/resources/excel/cool-excel-spreadsheets/ （可信度：专业机构标准）
- CFI 现金流模型风险高亮：Balance Sheet Check 用绿字无填充表示 Okay；用浅红填充+深红字表示 Error；现金余额低于阈值时浅红填充+深红字。把模型变成「自动预警系统」。— 来源: https://corporatefinanceinstitute.com/resources/excel/conditional-formatting-cash-flow-models/ （可信度：专业机构标准）
- CFI：净利为负时条件格式设红底、否则绿底。— 来源: https://corporatefinanceinstitute.com/resources/excel/documenting-excel-models-best-practices/ （可信度：专业机构标准）
- Power BI 官方文档（同类原则）：高/中/低三档阈值分别绿/黄/红；百分比规则用小数（0.25 表示 25%），并确保规则覆盖负值区间。— 来源: https://learn.microsoft.com/zh-hk/power-bi/create-reports/desktop-conditional-table-formatting （可信度：一手官方文档）
- 微软 Q&A 示例：Yes→绿填充、No→红填充，用「使用公式确定要设置格式的单元格」+EXACT 实现。— 来源: https://learn.microsoft.com/en-us/answers/a/11506047 （可信度：一手官方文档，社区答复）

### 3.4 数据验证最佳实践

- 微软官方 DataValidation 对象五属性：rule（规则）、errorAlert（错误警报，样式含 information/warning/stop）、prompt（悬停提示）、ignoreBlanks（默认 true）、type（只读）。— 来源: https://learn.microsoft.com/zh-cn/office/dev/add-ins/excel/excel-add-ins-data-validation?view=excel-js-preview （可信度：一手官方文档）
- 重要限制：数据验证仅在用户直接输入或从工作簿其他地方复制并选择「数值」粘贴时触发；若复制纯文本粘贴到带验证区域，**不会触发验证**。— 来源: https://learn.microsoft.com/zh-cn/office/dev/add-ins/excel/excel-add-ins-data-validation?view=excel-js-preview （可信度：一手官方文档）
- CFI：数据验证用于限制单元格可输入的数据类型；最高效的下拉列表做法是自建列表并命名（如 ProductType），在 Source 框输入 =ProductType；用 Table 做列表源可自动更新；还可加输入提示和错误警报。— 来源: https://corporatefinanceinstitute.com/resources/excel/documenting-excel-models-best-practices/ （可信度：专业机构标准）
- 与颜色编码配合：用浅蓝标识输入单元格，用条件格式把超出可接受范围的值标红，形成「视觉提示+验证拦截」双层防护。— 来源: https://daloopa.com/?p=2667 （可信度：行业培训/媒体）

---

## 4. 配色方案的具体数值（可直接用的 HEX）

### 4.1 IBM Carbon 中性灰阶（官方 HEX）

| Token | 名称 | HEX | 官方用途 |
|---|---|---|---|
| — | White | `#ffffff` | 全局背景（White 主题） |
| — | Gray 10 | `#f4f4f4` | 全局背景（Gray 10 主题）、layer-01 |
| — | Gray 20 | `#e0e0e0` | layer-accent、selected layer |
| — | Gray 30 | `#c6c6c6` | active layer |
| — | Gray 50 | `#8d8d8d` | hover 半透明基色、disabled |
| — | Gray 60 | `#6f6f6f` | 浅色主题文字/图标下界 |
| — | Gray 70 | `#525252` | 浅色主题次要文字 |
| — | Gray 80 | `#393939` | background-inverse |
| — | Gray 90 | `#262626` | 全局背景（Gray 90 深色主题） |
| — | Gray 100 | `#161616` | 全局背景（Gray 100 主题）、primary text |

— 来源: https://carbondesignsystem.com/elements/color/overview/ 和 https://carbondesignsystem.com/elements/color/tokens/ （可信度：专业机构标准，官方设计系统）

Carbon 关键规则：浅色主题分层在 White 与 Gray 10 之间交替，文本/图标用 Gray 100–Gray 60；**避免中间调（Avoid use of midtones）**。— 来源: https://carbondesignsystem.com/elements/color/overview/ （可信度：专业机构标准）

Carbon 状态色官方 HEX：Red 60 `#da1e28`（danger/error）、Orange 40 `#ff832b`（serious warning）、Yellow 30 `#f1c21b`（regular warning）、Green 50 `#24A148`（normal/success）、Blue 70 `#0043ce`（passive notification）、Purple 60 `#8a3ffc`（outlier）。— 来源: https://carbondesignsystem.com/building-blocks/core/patterns/status-indicators （可信度：专业机构标准）

### 4.2 Ant Design 中性灰阶与语义色（官方 HEX）

| 名称 | HEX |
|---|---|
| gray-0 | `#ffffff` |
| gray-1 | `#fafafa` |
| gray-2 | `#f5f5f5` |
| gray-3 | `#f0f0f0` |
| gray-4 | `#d9d9d9` |
| gray-5 | `#bfbfbf` |
| gray-6 | `#8c8c8c` |
| gray-7 | `#595959` |
| gray-8 | `#434343` |
| gray-9 | `#262626` |

— 来源: https://ant.design/docs/spec/colors （可信度：专业机构标准，官方设计系统）

Ant Design 产品级中性色（含透明度，官方）：Heading Text `#000000E0`、Text `#000000E0`、Secondary Text `#000000A6`、Disabled Text `#00000040`、Default Border `#D9D9D9`、Separator `#0505050F`、Layout Background `#F5F5F5`。— 来源: https://ant.design/docs/spec/colors （可信度：专业机构标准）

Ant Design 语义色（官方）：品牌蓝 `#1677ff`；Dust Red 系 red-4 `#ff4d4f`、red-5 `#f5222d`；Volcano orange-5 `#fa541c`；Gold gold-5 `#faad14`；Polar Green green-5 `#52c41a`；Daybreak Blue blue-5 `#1677ff`。— 来源: https://ant.design/docs/spec/colors （可信度：专业机构标准）

Ant Design 明确说中性色定义「incorporating the WCAG 2.0 standard」。— 来源: https://ant.design/docs/spec/colors （可信度：专业机构标准）

### 4.3 Tailwind 灰阶（官方 HEX，v1/v2 经典色阶）

Tailwind v2 升级指南给出的 gray 色阶（HEX）：100 `#f7fafc`、200 `#edf2f7`、300 `#e2e8f0`、400 `#cbd5e0`、500 `#a0aec0`、600 `#718096`、700 `#4a5568`、800 `#2d3748`、900 `#1a202c`。— 来源: https://tailwindcss.com/docs/upgrading-to-v2 （可信度：专业机构标准，官方设计系统）

> 注意：Tailwind v4 默认色阶已改为 OKLCH（如 `--color-gray-50: oklch(0.984 0.003 247.858)`），不再是 HEX。若脚本要落地 HEX，用上面的 v2 色阶或 Carbon/Ant。— 来源: https://tailwindcss.com/docs/colors （可信度：一手官方文档）

### 4.4 实测 WCAG 对比度（本文按 W3C 公式计算）

标准：普通文本 ≥ 4.5:1，大号文本（≥18pt 或 ≥14pt 粗体）≥ 3:1（AA 级）。— 来源: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum （可信度：一手官方文档）
增强级 AAA：普通文本 ≥ 7:1，大号文本 ≥ 4.5:1。— 来源: https://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-contrast.html （可信度：一手官方文档）
计算口径：相对亮度 L = 0.2126R + 0.7152G + 0.0722B（各通道先线性化），对比度 = (L亮+0.05)/(L暗+0.05)。阈值不可四舍五入（4.499:1 不达标）。— 来源: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum （可信度：一手官方文档）

| 应用 | 前景 | 背景 | 对比度（实测） | 判定 |
|---|---|---|---|---|
| 正文文字 | `#161616` Carbon Gray100 | `#ffffff` | **18.10:1** | AAA 通过 |
| 深色表头上的白字 | `#ffffff` | `#393939` Carbon Gray80 | **11.55:1** | AAA 通过 |
| 次要文字 | `#525252` Carbon Gray70 | `#ffffff` | **7.81:1** | AAA 通过 |
| 弱化文字 | `#6f6f6f` Carbon Gray60 | `#ffffff` | **5.02:1** | AA 通过 |
| 占位符/禁用文字 | `#8d8d8d` Carbon Gray50 | `#ffffff` | **3.32:1** | 仅大号文本/非文本 UI 通过 |
| 边框线 | `#e0e0e0` Carbon Gray20 | `#ffffff` | **1.32:1** | 非文本，靠形状而非对比度识别 |
| 斑马纹上的正文 | `#161616` | `#f4f4f4` Carbon Gray10 | **16.45:1** | AAA 通过 |
| 斑马纹上的正文（Ant） | `#262626` Ant gray-9 | `#f0f0f0` Ant gray-3 | **13.28:1** | AAA 通过 |
| 强调色（白底蓝字） | `#0f62fe` Carbon Blue60 | `#ffffff` | **5.00:1** | AA 通过 |
| 强调色深阶 | `#0043ce` Carbon Blue70 | `#ffffff` | **7.79:1** | AAA 通过 |
| 白字配强调底 | `#ffffff` | `#0f62fe` Carbon Blue60 | **5.00:1** | AA 通过 |
| 警示色 | `#da1e28` Carbon Red60 | `#ffffff` | **5.00:1** | AA 通过 |
| 警示色（Ant） | `#f5222d` Ant red-5 | `#ffffff` | **4.08:1** | AA 通过（接近下限） |

（以上对比度为本文实测计算 — 可信度：实测计算）

### 4.5 给技能直接落地的一套配色（组合建议）

| 角色 | HEX | 来源 | 说明 |
|---|---|---|---|
| 表头底色（深色方案） | `#393939` | Carbon Gray80 | 配白字 11.55:1 |
| 表头底色（浅色方案） | `#f0f0f0` | Ant gray-3 | 配 `#262626` 字 13.28:1 |
| 斑马纹 | `#f4f4f4` | Carbon Gray10 | 极浅，不与白底争夺注意力 |
| 分隔线/边框 | `#d9d9d9` | Ant Design Default Border | 中性灰，比纯黑线柔和 |
| 次级分隔线 | `#e0e0e0` | Carbon Gray20 | 更弱的分区 |
| 正文 | `#161616` | Carbon Gray100 | 18.10:1 |
| 次要文字 | `#525252` | Carbon Gray70 | 7.81:1 |
| 强调色 | `#0f62fe` | Carbon Blue60 | 5.00:1 |
| 链接/输入强调深阶 | `#0043ce` | Carbon Blue70 | 7.79:1，适合小字号蓝字 |
| 警示/错误 | `#da1e28` | Carbon Red60 | 5.00:1 |
| 成功/正常 | `#24A148` | Carbon Green50 | 状态色官方值 |
| 警告 | `#f1c21b` | Carbon Yellow30 | 状态色官方值 |

> **注意**：Carbon Blue60 `#0f62fe` 与投行「蓝字=输入」语义无官方绑定关系；这套是 UX 配色，语义映射见 §1。若要做「输入蓝字」且要过 AA，用 `#0043ce`（7.79:1）比 `#0f62fe`（5.00:1）更稳。
> **未验证，需实测**：Material Design 3 与 Microsoft Fluent 2 的中性灰阶精确 HEX 未能从本次检索的一手文档页中逐档确认（M3 以 tone 0–100 与 token 形式给出，示例值如 `md.ref.palette.secondary90 = #E8DEF8`；Fluent 2 检索无结果）。落地前需查官方 token 表实测。— 来源: https://m3.material.io/foundations/design-tokens/overview （可信度：一手官方文档）

---

## 5. 字体与字号规范

- 微软官方默认：在 worksheet 中输入数据时，Excel 自动使用 **Calibri 11pt**。— 来源: https://support.microsoft.com/en-us/topic/b3f1792b-9980-4b92-9aa5-5dd6e940b195 （可信度：一手官方文档）
- 微软官方行列尺寸：普通视图下**行高以磅（point）显示、列宽以字符数（默认字体可容纳的字符数）显示**；列宽最小 0（隐藏）、最大 255、**默认 8.43**；行高最小 0（隐藏）、最大 409、**默认 15.00**。— 来源: https://support.microsoft.com/zh-cn/excel/change-the-column-width-and-row-height （可信度：一手官方文档）
- CFI 列宽方法：拖拽、列宽对话框（精确数值）、AutoFit（双击列边界，按最长条目自动调整）、Alt+H+O+I（AutoFit）、Alt+H+O+W（自定义宽度）；长文本用 Wrap Text 并增加行高。— 来源: https://corporatefinanceinstitute.com/resources/excel/adjust-column-width-in-excel （可信度：专业机构标准）
- CFI 强调「用统一列宽保持一致性」，AutoFit 快速但「may not always provide the visual consistency you need」。— 来源: https://corporatefinanceinstitute.com/resources/excel/adjust-column-width-in-excel （可信度：专业机构标准）
- 专业 UX 建议（博客，供参考）：正文 10–11pt、标题 12–14pt，只用一到两种字体（如 Calibri/Segoe UI 作正文）；左对齐文本、右对齐数字、短表头居中。— 来源: https://dashboardsexcel.com/blogs/blog/excel-tutorial-how-to-make-excel-spreadsheet-look-professional （可信度：博客转述，谨慎采用）
- 大表场景的列宽手感：Excel4Business 建议对积累多年的月度数据「隐藏历史数据、按年度汇总分组、冻结左侧上下文列」。— 来源: https://www.excel4business.com/guides/how-can-i-make-excel-look-more-professional-and-feel-more-like-a-website-or-phone-app （可信度：行业培训/媒体）
- CFI：跨多列居中标题优先用 **Center Across Selection** 而非 Merge & Center，因为合并单元格会破坏公式引用（引用指向左上角），跨选区居中保持单元格独立与引用完整。— 来源: https://corporatefinanceinstitute.com/resources/excel/center-across-selection-excel-365 （可信度：专业机构标准）

> **未验证，需实测**：「数字区 10pt、注释 9pt、表头 11pt 加粗」这类精确分档没有从一手文档中找到统一标准；建议技能按「默认 11pt → 数据区可降到 10pt → 表头 11pt 加粗」起步，行高 15–20pt 区间，并在体检报告中作为「风格一致性」而非「硬性标准」提示。

---

## 6. 打印与呈现规范

- 重复标题行（Print Titles）：若 worksheet 跨多个打印页，可添加每页都出现的行列标题；页面布局 → 打印标题 → 「顶端标题行」输入 `$1:$1`；「左端标题列」输入包含行标签的列。— 来源: https://support.microsoft.com/en-gb/excel/repeat-specific-rows-or-columns-on-every-printed-page （可信度：一手官方文档）
- 微软官方注意：处于单元格编辑模式、选中图表或未安装打印机时，「打印标题」命令变灰；选中多个工作表时该选项不可用。— 来源: https://support.microsoft.com/zh-cn/office/在每个打印页上重复特定的行或列-0d6dac43-7ee7-4f34-8b08-ffcc8b022409 （可信度：一手官方文档）
- 常见错误反面：表格跨页断开且无表头——微软专门有「Print Excel table headers on every page」文章解决此问题。— 来源: https://learn.microsoft.com/zh-cn/archive/blogs/hub/print-excel-table-headers-on-every-page （可信度：一手官方文档）
- 页面方向与尺寸：CFI 仪表板指南说方向可横可纵，最常见是 8.5×11 英寸（便于打印或转 PDF）；决策要素包括「邮件还是打印、给高管还是外行、内部还是外部、以图为主还是数字文字为主」。— 来源: https://corporatefinanceinstitute.com/resources/knowledge/analytics/dashboard （可信度：专业机构标准）
- 打印区域与分页：设置打印区域控制打印/PDF 范围；用分页预览确认视觉落在预期页面；调整边距与缩放，「Fit Sheet on One Page 要慎用，宽仪表板优先横向」。— 来源: https://dashboardsexcel.com/blogs/blog/excel-tutorial-how-to-make-excel-spreadsheet-look-professional （可信度：博客转述，谨慎采用）
- 页眉页脚应包含动态元素：文件名、工作表名、页码、最后刷新时间，以便追溯。— 来源: https://dashboardsexcel.com/blogs/blog/excel-tutorial-how-to-make-excel-spreadsheet-look-professional （可信度：博客转述，谨慎采用）
- 复杂报表应手动确定分页符，避免图表和表格被不自然地切断；关键汇总卡片应出现在第一页。— 来源: https://dashboardsexcel.com/blogs/blog/excel-tutorial-how-to-make-excel-spreadsheet-look-professional （可信度：博客转述，谨慎采用）

> **给技能的可执行检查项**：是否有 print_title_rows / print_title_cols；是否 A4 横向且 fitToWidth=1（宽表）；是否设置 print_area；是否手动 page break；页眉页脚是否含页码与文件名。

---

## 7. 大表的可读性工程（200 列不失控）

### 7.1 冻结窗格策略

- 微软官方：Freeze Panes 冻结「所选单元格上方和左侧」的行列；冻结前两列需选第三列再冻结；冻结行列需选「要保留行下方、列右侧」的单元格。— 来源: https://support.microsoft.com/en-us/office/freeze-panes-to-lock-rows-and-columns-dab2ffc9-020d-4026-8121-67dd25f2508f （可信度：一手官方文档）
- 大表实践：在逻辑表头处冻结窗格，使滚动时行列标题始终可见；对多年月度数据，冻结左侧提供上下文的列。— 来源: https://dashboardsexcel.com/blogs/blog/excel-tutorial-how-to-make-excel-spreadsheet-look-professional （可信度：博客转述，谨慎采用）
- Excel4Business：筛选常比逐行滚动更快；最宽的表往往是多年月度数据，应隐藏历史、按年度分组、或冻结左侧上下文列。— 来源: https://www.excel4business.com/guides/how-can-i-make-excel-look-more-professional-and-feel-more-like-a-website-or-phone-app （可信度：行业培训/媒体）

### 7.2 列分组与折叠

- CFI：Grouping 可折叠/展开所有 section，形成「目录」外观。— 来源: https://corporatefinanceinstitute.com/resources/excel/documenting-excel-models-best-practices/ （可信度：专业机构标准）
- 大表实践：用 Data → Group 折叠辅助明细；配合缩进和组标签显示层级。— 来源: https://dashboardsexcel.com/blogs/blog/excel-tutorial-how-to-make-excel-spreadsheet-look-professional （可信度：博客转述，谨慎采用）
- 大型数据集：分组折叠适合层级/多级别数据；也可按类别/区域拆到多个 worksheet，再用汇总表整合。— 来源: https://www.exceldelta.com/tutorials/top-tips-for-organizing-large-datasets-in-excel （可信度：行业培训/媒体）

### 7.3 批注、数据验证提示与超链接目录

- CFI：单元格 Note（批注）会在右上角生成红色小三角，鼠标悬停显示说明框，适合放详细释义或计算解释。— 来源: https://corporatefinanceinstitute.com/resources/excel/documenting-excel-models-best-practices/ （可信度：专业机构标准）
- CFI：数据验证可加输入消息（input message）和错误警报（error alert）指出无效数据。— 来源: https://corporatefinanceinstitute.com/resources/excel/documenting-excel-models-best-practices/ （可信度：专业机构标准）
- 微软：prompt 属性在鼠标悬停于区域时显示提示消息；errorAlert 样式含 information / warning / stop。— 来源: https://learn.microsoft.com/zh-cn/office/dev/add-ins/excel/excel-add-ins-data-validation?view=excel-js-preview （可信度：一手官方文档）
- 超链接目录：20+ sheet 的文件常用内部链接从汇总表跳转到各 worksheet；甚至用文本框/形状做导航按钮并分配超链接。— 来源: https://www.excel4business.com/guides/how-can-i-make-excel-look-more-professional-and-feel-more-like-a-website-or-phone-app （可信度：行业培训/媒体）
- 内置导航：Excel 365/2021+ 的 Navigation 窗格（View → Navigation）可列出所有 sheet、table、chart、named range，支持搜索；右键底部导航箭头弹出 Activate 列表可一次看到所有 sheet。— 来源: https://howtogeek.com/microsoft-excel-hidden-navigation-hacks （可信度：行业培训/媒体）
- 名称框（Name Box）：下拉可见所有命名区域与表格，输入坐标（如 Z1000）可直接跳转。— 来源: https://howtogeek.com/microsoft-excel-hidden-navigation-hacks （可信度：行业培训/媒体）
- 首页仪表板：用 Ctrl+K 链接到「本文档中的位置」，每个子 sheet 都要有返回首页的链接形成闭环。— 来源: https://howtogeek.com/microsoft-excel-hidden-navigation-hacks （可信度：行业培训/媒体）
- 隐藏与保护：隐藏未用行列、保护含公式或配置的单元格、只留输入单元格解锁并明确标注样式。— 来源: https://dashboardsexcel.com/blogs/blog/excel-tutorial-how-to-make-excel-spreadsheet-look-professional （可信度：博客转述，谨慎采用）

### 7.4 游戏数值策划场景的落地映射

- 200 列配置表：冻结首行 + 首列（或前 N 个关键 ID 列）；对列按玩法模块分组（Data → Group）可折叠；首列放主键 ID 并冻结。
- 命名区域 + 一张 Index sheet：Index 页用 HYPERLINK 公式列出所有配置表与命名区域，配「最后更新时间」。
- 单元格批注写清「字段含义/取值范围/来源表」，与数据验证下拉复用同一份字典表。
- 避免在公式里写死数值：所有数值参数集中到 Assumptions/参数表 tab，命名后引用。
- 汇报表（给老板）与配置表（日常）分文件/分 sheet：汇报表用 Table + 冻结 + 打印标题；配置表保持纯 Range 便于脚本读写。

---

## 8. 本次调研的冲突与未验证项汇总

| 项目 | 冲突/缺口 | 处理 |
|---|---|---|
| 红字语义 | WSP=跨文件链接；FAST=exports；IIMSKILLS/ibinterviewquestions=错误/需注意 | 保留冲突，诊断时看上下文 |
| 黄底语义 | CFI=输入增强标记；FAST=临时代码 | 保留冲突 |
| 绿字语义 | CFI/WSP=跨工作表链接；CFI 另说「无清晰惯例」且「越来越常见」 | 标注为「常见但非强制」 |
| 紫字 | 部分机构=外部文件链接；部分模型省略 | 标为可选扩展 |
| Table vs Range | 微软鼓励 Table；CFI 模型实践常用单表+分组 | 按数据层/呈现层分别建议 |
| 精确投行 RGB | 各机构不同且 CFI 不要求记忆 | 不编造，引用设计系统 HEX |
| M3 / Fluent 2 灰阶 HEX | 未从一手文档逐档确认 | 明确写「未验证，需实测」 |
| 字号分档（数据/表头/注释） | 无一手统一标准 | 按默认 11pt 起步，作为风格一致性提示 |
| 页面设置细节（A4 横向、fitToWidth） | 仅博客级来源，无微软一手分档 | 标为博客转述，谨慎采用 |
