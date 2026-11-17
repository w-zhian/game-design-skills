# Agent 1 调研：数据表格设计与信息可视化理论

> 用途：为「Excel 表格排版 UX 设计师」技能提供**最基础的一层原理**——不讲 Excel 操作，只讲「什么样的表格才是好表格」。
> 调研方式：全部结论均通过 WebSearch / WebFetch 实地抓取，不凭记忆。
> 调研日期：2026-11-17。

---

## 0. 阅读约定（可信度分级 / 排除源 / 冲突处理 / 事实与推断）

### 0.1 可信度标注
- **一手**：作者本人著作/官网/官方规范/政府机构/大学研究原文。如 Tufte 本人站点、Few 本人 PDF、W3C WCAG、NCBI/PubMed、Microsoft Learn 字体文档、NN/g 官方文章、Okabe & Ito 作者页。
- **二手**：权威机构指南、专业数据可视化博客、书籍摘要站、转引原话的媒体。如 Royal Statistical Society 指南、Datawrapper Blog、Towards Data Science、datawrapper/gt book 等。
- **推断**：本次调研未找到直接出处，由已验证事实推导出的组合建议或常识性判断。已明确标注。

### 0.2 严格排除的源
按要求排除：知乎、微信公众号、百度百科/知道、CSDN 洗稿文。本次调研**未引用上述任何来源**。个别中文站点（maoken.com、idctop.com）仅作低权重实践观察，均已标「二手」并附更权威的一手源交叉印证；关键数字类结论不依赖它们。

### 0.3 冲突处理
遇到「竖线要不要画」「斑马纹要不要用」等各家分歧，**保留冲突并在第 8 章集中列出**，注明各自理由，不和稀泥。

### 0.4 事实 vs 推断
每条结论后格式为 `— 来源: <URL>（可信度：X）`。凡未找到直接出处的组合建议，一律标「推断」。

---

## 1. Edward Tufte：数据墨水比与表格主张

### 1.1 数据墨水比（data-ink ratio）
- 数据墨水比 = data-ink / total ink，目标是「在合理范围内最大化」，趋近 1.0。Few 转述 Tufte 1983 年原话「Above all else show the data」，并给出公式化简：`data-ink ratio = 1.0 − 可在不损失信息前提下去掉的墨比例`。— 来源: https://perceptualedge.com/articles/ie/elegance.pdf（可信度：一手，Few 引用 Tufte 一手定义）
- 定义：data-ink 是「图形中不可擦除的核心，为响应数字变化而排列的非冗余墨」；非数据墨（non-data ink）是边框、网格、装饰阴影等。— 来源: https://perceptualedge.com/articles/ie/elegance.pdf（可信度：一手）
- 操作化四步：①移除不必要的非数据墨；②弱化并规整剩余非数据墨；③移除不必要的数据墨；④强调最重要的数据墨。判断标准：「去掉这个组件会不会损失数据或信息？」答「否」就删。— 来源: https://perceptualedge.com/articles/ie/elegance.pdf（可信度：一手）
- Few 明确指出图中「图例边框、绘图区边框、网格线」都是不必要的非数据墨；并引用 Saint-Exupery：「完美不是无可增添，而是无可删减。」— 来源: https://perceptualedge.com/articles/ie/elegance.pdf（可信度：一手）

### 1.2 他反对的 chartjunk / 冗余网格 / 3D
- Chartjunk 定义：图形中「不承载信息的装饰性内部装饰，以及无谓的三维或透视效果」。— 来源: https://en.wikipedia.org/wiki/Information_visualization（可信度：二手，转述 Tufte）
- Tufte 的「1+1=3」效应：两个元素近距离放置会产生可见的交互作用，可造成 moiré 振动（摩尔纹）、光学抖动，甚至显示「并不存在的信息」。在主流科学出版物中 moiré 振动占 2%–20%，统计与计算机出版物中 chartjunk 占 12%–68%。— 来源: https://chnm.gmu.edu/digitalhistory/links/cached/chapter4/4_13b_tufte.htm（可信度：二手，GMU 历史中心整理 Tufte 原则）
- 具体去 chartjunk 手法：避免重网格（heavy grids）、用断点线替代箱形盒、用 x/y 网格替代封闭边框、用空白代替柱状图中的网格线、用刻度（不带线）标示数据位置、去掉坐标轴上的线、从数据值起轴（range frame）、用直接标注替代图例。— 来源: https://chnm.gmu.edu/digitalhistory/links/cached/chapter4/4_13b_tufte.htm（可信度：二手）
- ⚠️ **未验证（已剔除来源，不作为规则依据）**：「dreaded grid（可怕网格）」被列为四大 chartjunk 之一、另三种是 moiré / duck / decoration。
  这些术语在 Tufte 体系中确实存在（源于《The Visual Display of Quantitative Information》），但初版所引来源是一个
  **AI 生成的 skill 文件**（GitHub `compabob` 仓库内的 `chart-tufte/SKILL.md`），属循环引用，不可作为事实依据。
  **2026-11-17 复核时已剔除该来源；本条降级为「术语线索，待用 VDQI 原书页码核实」**。
  已在 §1.2 前两条中由 chnm.gmu.edu 整理的 Tufte 原则替代覆盖（重网格/边框/网格线属非数据墨），结论不受影响。
- ⚠️ **未验证（同上）**：Tufte 称超出数据维度的编码（1D 数据画 3D 饼图）为「结构上不诚实」。
  该主张方向可信（与 VDQI 的 lie factor 一致），但初版来源同为上述 AI 生成文件，**已剔除，未采信为规则依据**。
- 直接标注（direct labeling）优于独立图例：图例迫使读者视线在图形与图例间来回跳动。— 来源: https://chnm.gmu.edu/digitalhistory/links/cached/chapter4/4_13b_tufte.htm（可信度：二手）

### 1.3 Small multiples（小型多图）
- 定义：同一页面上缩略图尺寸的成组图形，表现同一现象的不同方面；必须**使用相同的度量与尺度**。— 来源: https://chnm.gmu.edu/digitalhistory/links/cached/chapter4/4_13b_tufte.htm（可信度：二手）
- 作用：促成比较、增强维度感、展示备选范围；在计算机上尤其有用，因为可叠加图像、快速循环切换。— 来源: https://chnm.gmu.edu/digitalhistory/links/cached/chapter4/4_13b_tufte.htm（可信度：二手）
- ⚠️ **未验证（已剔除来源）**：多面板时「比较重要处用相同 y 轴尺度；只关心局部形状时才用不同尺度」——
  方向与 Tufte 的 small multiples 原则一致（定义见上条，已由 chnm.gmu.edu 来源支撑），
  但这句具体表述的初版来源是 AI 生成文件，**不作为独立依据采信**。
- ⚠️ **未验证（已剔除来源，且非 Tufte 原话）**：「数据点 ≤20 个时用表格而非图形」——
  这是社区流传的经验阈值，初版来源为 AI 生成文件。**没有找到 Tufte 或 Few 的原文支撑这个数字。**
  `report-dashboard-rules.md` 中引用该数字时已标注「社区派生经验值」，
  使用时应把它当启发式而非规则，不要对用户说成「Few/Tufte 的标准」。

### 1.4 Tufte 对「表格（table）本身」的具体主张（本次调研的重点）
> 多数人只知 Tufte 讲图，他在《Beautiful Evidence》与本人站点上其实对表格有非常具体的论断。

- **表格密度天花板**：「Tables of numbers attain maximum densities of only 300 characters per square inch or 50 characters per square centimeter.」而图形显示分辨率高得多——制图学指出人眼可分辨 0.1 mm，相当于每平方英寸 60,000 个区分点。— 来源: https://www.edwardtufte.com/notebook/page/4（可信度：一手，Tufte 本人站点）
- **精度哲学**：「This financial table reports 24 numbers accurate to 5 significant digits; the accompanying sparklines show about 14,000 numbers readable from 1 to 2 significant digits. The idea is to be approximately right rather than exactly wrong.」——表格负责少量高精度值，图形负责大量低精度值；「宁可大致正确，不要精确错误」。— 来源: https://www.edwardtufte.com/notebook/page/4（可信度：一手；「approximately right rather than exactly wrong」引自 Tukey 1965）
- **表格会强化近因偏差**：「Tables sometimes reinforce recency bias by showing only current levels or recent changes; sparklines improve the attention span of tables.」——表格只显示当前水平/近期变化，会放大近因偏差；在表中嵌入 sparkline 可延长表格的「注意力跨度」。— 来源: https://www.edwardtufte.com/notebook/page/4（可信度：一手）
- **字体与白空间的具体观察**：重设计表格时「Gill Sans does quite well compared to the Helvetica in the original Times table. Smaller than the Helvetica, the Gill Sans appears sturdier and more readable, **in part because of the increased white space that results from its smaller x-height and reduced size**.」——小 x-height + 更小字号带来更多白空间，反而更结实易读。— 来源: https://www.edwardtufte.com/notebook/page/4（可信度：一手）
- **数据区面积效率**：重设计后的 sparkline 表格数据区（不含列标签）只比原表大 21%，却多呈现约 5,000 个数字。— 来源: https://www.edwardtufte.com/notebook/page/4（可信度：一手）
- **报纸表格密度实例**：8 行/英寸的表格中，每列可加约 160 条 sparkline，一个 5 栏财经版可额外呈现 400,000 个每日价格及其变化。— 来源: https://www.edwardtufte.com/notebook/page/4（可信度：一手）
- **表格 = 名词 + 数字矩阵**：Tufte 描述典型数据分析表是「一列名词（如共同基金）+  accompanying numbers（资产、变化）」，分析者扫视数据矩阵后做决策。— 来源: https://www.edwardtufte.com/notebook/page/4（可信度：一手）
- **色彩在表格中的角色**：用颜色把 sparkline 与数字关联（红=序列最旧/最新值，蓝=年度高低点）；「颜色应作为主要识别手段且保持低调」。— 来源: https://www.edwardtufte.com/notebook/page/4 与 https://chnm.gmu.edu/digitalhistory/links/cached/chapter4/4_13b_tufte.htm（可信度：一手 + 二手）
- **统计图形七条优秀标准**（包含 tabulation 目的）：展示数据、引导思考实质而非方法、不歪曲数据、小空间呈现多数字、大数据集连贯、鼓励比较、多细节层次、有清晰目的（描述/探索/制表/装饰）、与文字描述紧密结合。— 来源: https://en.wikipedia.org/wiki/Information_visualization（可信度：二手，转述 Tufte 1983 原文）

---

## 2. Stephen Few：表格设计原则

> 一手来源为其本人站点 perceptualedge.com 的 PDF；其书《Show Me the Numbers》《Information Dashboard Design》的具体表格规则亦有权威转述，均标明可信度。

### 2.1 何时用表格、何时用图形
- Few 的判断标准：读者需要**查单个值或比较精确数字**时用表格；信息在**形状/趋势/比较**中时用图形。— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手，归纳 Few《Show Me the Numbers》）
- Datawrapper 补充：表格适合查具体信息、精确数字、排名、双向比较；图形适合看整体模式与异常值。多数人不会读完超过 3 行的表格，只找自己关心的那行。— 来源: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables（可信度：二手）
- 常见失败：「把表格当图形用」——20 行数字，论点其实只是「先升后平」，读者被迫做本该分析者做的视觉工作。— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手）

### 2.2 对齐（Alignment）
- **数字右对齐**：「Numbers that represent quantitative values, as opposed to those that are merely identifiers, should always be aligned to the right.」——以便个位对个位、量级沿列可见。— 来源: https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/（可信度：二手，Few 原书规则转述）
- **日期左对齐**：「Dates are best aligned to the left, using a format that keeps the number of characters in each portion of the date.」— 来源: 同上（可信度：二手）
- **文本左对齐**：「Text that expresses neither numbers nor dates works best when aligned to the left.」— 来源: 同上（可信度：二手）
- **表头与数据同对齐**：列头应与其下列数据同对齐（数字列表头也右对齐）。— 来源: https://www.gointrepid.com/blog/posts/data-visualization-secrets-creating-tables（可信度：二手，转引 Few）
- **不要居中对齐**：「Do not use center alignment (even if it's tempting and your tool does it by default).」居中造成锯齿状边缘，难以纵向扫描。— 来源: 同上（可信度：二手）
- Few 原话（关于文本对齐的本质）：「The most effective alignment of text is primarily a matter of convention rather than the mechanics of visual perception」——对齐主要是惯例而非视觉机制，但惯例力量强大，忽视会导致困惑。— 来源: https://www.gointrepid.com/blog/posts/data-visualization-secrets-creating-tables（可信度：二手，Few 原话直引）
- **小数位对齐**：同一列使用相同小数位数，小数点与末位同时右对齐；混合小数位（1.2 / 0.85 / 12.417）迫使眼睛逐个解析。— 来源: https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/ 与 https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手）

### 2.3 有效数字与舍入
- 「Show only the precision the decision needs.」例：1.0837 的 relative 暗示四位有效数字精度，而底层数据可能只有 300 条理赔——过度精确是一种「悄悄的可信度声明」。— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手，归纳 Few）
- 经验值：relative 三位、纯保费取整元、百分比一位小数。— 来源: 同上（可信度：二手）
- 与 Tufte「approximately right rather than exactly wrong」一致。— 来源: https://www.edwardtufte.com/notebook/page/4（可信度：一手）

### 2.4 网格线用法（horizontal rules only）
- 「Heavy gridlines, borders and fill compete with the data; Few's guidance is to reduce non-data ink and let white space do the grouping.」— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手，归纳 Few）
- **去掉全部竖向网格线，用留白分隔列**；最多在表头下、合计行上各放一条浅横线。— 来源: 同上（可信度：二手）
- 对图形：网格线「should always be visually subdued」，只用于增强查找/比较或局部模式感知。— 来源: https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/（可信度：二手）
- 斑马纹：「Avoid fill colour and shading in every other row unless the table is very wide.」— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手）
- **一个高亮原则**：「Use one highlight — bold, or a single colour — and use it only on what the reader should notice.」几乎全部强调 = 没有强调。— 来源: 同上（可信度：二手）

### 2.5 单位与排序
- **单位放表头不放单元格**：「Repeat units in the header (Pure premium ($)) rather than on every cell.」— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手）
- 货币符号只在汇总处使用，不附每个数字。— 来源: https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/（可信度：二手）
- **排序（sequencing）**：数字和日期有自然顺序；无内在顺序的数据用字母序。字母序是默认但「几乎从不是最有用的」——应按量级、自然序列（年龄段、车龄、保单年度）排序，相关表格间保持一致顺序。— 来源: https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/ 与 https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手）
- Datawrapper 建议：可考虑按「隐形列」排序（如按人口数排城市但不显示人口列）；长表/分页表尤其要花心思排序；不确定时开放自定义排序。— 来源: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables（可信度：二手）

### 2.6 分组与留白（Few 原书规则转述）
- 组间用竖向白空间，但「only enough to make the break noticeable」。— 来源: https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/（可信度：二手）
- 每组开头重复列头；组与组之间不要改变表格结构；多分类分组时组头放同一行；读者需隔离查看某组时，每组另起一页。— 来源: 同上（可信度：二手）
- Few 原话：「White space is used to group data objects that belong together by separating them from others.」— 来源: https://towardsdatascience.com/five-rules-for-designing-tables-a953a16e50f3/（可信度：二手，Few《Show Me the Numbers》原话直引）
- Few 建议**行高 = 字号的 2 倍**（10pt 字 → 20pt 行高）。— 来源: https://towardsdatascience.com/five-rules-for-designing-tables-a953a16e50f3/（可信度：二手，转引 Few）
- 字体：同一字体贯穿全表、选用简洁易读字体、字号尽量大。— 来源: https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/（可信度：二手）

### 2.7 Dashboard 上的表格该多简（Few 本人一手）
- 好的 dashboard 特征：「The amount of information that it displays is not overwhelming.」「Only what is necessary appears on the dashboard. It is not cluttered or distractingly decorated.」— 来源: https://www.perceptualedge.com/articles/Whitepapers/Dashboard_Design.pdf（可信度：一手，Few 本人）
- 「Because color is used so sparingly, it is easy to spot those items that require attention by scanning for red.」——颜色极度克制，红色只留给需要注意的项。— 来源: 同上（可信度：一手）
- 「The most important items have been placed in the prominent position of the screen—the upper left.」— 来源: 同上（可信度：一手）
- 「Effective dashboards lack eye candy. They are not designed to wow people upon first sight, but to inform people with precisely what they need in the way that they need it day in and day out.」— 来源: 同上（可信度：一手）
- Few 的 dashboard 十三宗罪（含「超出单屏」「上下文不足」「过度细节/精度」「间接表达度量」「无意义的变化」「编码不准确」「排列不当」「无效高亮」「无用装饰堆砌」「误用/滥用颜色」）。— 来源: https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf（经 https://skillsmp.com/creators/caarlos0/dotfiles/skills-dashboard 索引）（可信度：二手，Few 原清单转述）
- **Few 对 Excel 作为 dashboard 平台的罕见肯定**：「it is actually possible to achieve the layout flexibility that I'm advocating with Microsoft Excel... if you happen to know some of the tricks that lie under the covers」，并推荐 Charley Kyd《Dashboard Reporting with Excel》与 MicroCharts 插件的 sparklines/bullet graphs。— 来源: https://perceptualedge.com/articles/visual_business_intelligence/pervasive_hurdles_to_dd.pdf（可信度：一手，Few 本人）

### 2.8 他明确反对什么（清单）
- 反对：3D 效果（「Always avoid 3-d」）；反对用除线长、2D 位置以外的视觉属性编码定量值（仅这两种可靠）；反对柱状图不从零起；反对图例放在数据区内；反对重/亮网格线；反对居中对齐；反对无意义精度；反对 dashboard 上的 eye candy 与过度颜色。— 来源: https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/ 与 https://www.perceptualedge.com/articles/Whitepapers/Dashboard_Design.pdf（可信度：二手 + 一手）

---

## 3. 格式塔原理在表格上的应用

> 一手来源为 Nielsen Norman Group（NN/g）官方文章，作者 Aurora Harley / Lillian Yang 等。

### 3.1 Proximity（邻近性）
- 定义：「Items close together are likely to be perceived as part of the same group — sharing similar functionality or traits.」邻近性是「最重要的分组原则之一，可压过颜色/形状相似等竞争线索」。— 来源: https://www.nngroup.com/articles/gestalt-proximity（可信度：一手，NN/g）
- 用**不同量的留白**来联合或分离元素，是传达有意义分组的关键。— 来源: 同上（可信度：一手）
- 落地到文本：段落靠白空间成组；标题与对应段落距离 < 与上一段落距离，从而指示归属。— 来源: 同上（可信度：一手）
- 落地到表格：行间距/列间距的大小直接决定读者按行还是按列扫描（见第 5 章）。— 来源: https://unotes.net/documents/e84e14fc-4add-4a97-ac58-18ef2f9f82b8/designing-effective-tables-optimizing-communication（可信度：二手，Few 原书转述）
- 反向警告：把无关元素放太近（如把「Add」按钮和「Next/Cancel」放一起）会让它们被误认为一组而被忽略。— 来源: https://www.nngroup.com/articles/gestalt-proximity（可信度：一手）

### 3.2 Similarity（相似性）
- 定义：「Items which share a visual characteristic are perceived as more related than items that are dissimilar.」共享特征可以是颜色、形状、大小。— 来源: https://www.nngroup.com/articles/gestalt-similarity/（可信度：一手，NN/g，2020-09-06）
- 特性：相似性可「跨分散位置联合元素」，是最有韧性（most resilient）的分组原则，但通常被邻近性或共同区域压过。颜色是最强的相似特征，能联合不同类型的元素。— 来源: 同上（可信度：一手）
- 落地到表格：同类数据用同色（如状态列「已达标」统一用一种色）；「链接色应只保留给可交互文本，不能用于关键词/不可点标题」，否则用户会误判同类。— 来源: 同上（可信度：一手）
- 警告：形状过于相似会让用户忽略标签细节、误判为同类；颜色相同的按钮会被认为同等重要，主次按钮必须用不同颜色区分。— 来源: 同上（可信度：一手）

### 3.3 Enclosure / Common region（包围 / 共同区域）
- 定义：「The principle of common region says that items within a boundary are perceived as a group and assumed to share some common characteristic or functionality.」— 来源: https://www.nngroup.com/articles/common-region/（可信度：一手，NN/g，2020-07-12；学术依据 Palmer, S.E. 1992, Cognitive Psychology 24(3):436-447）
- 边界可由边框或背景色构成；共同区域是「强视觉线索，可压过邻近性与相似性」。— 来源: 同上（可信度：一手）
- **直接点名表格**：「in a comparison table it's important to distinguish both the column and the row... 'Zebra' stripes, where alternating rows have a colored background, are a common method of uniting horizontal elements while whitespace or another border distinguishes each column.」— 来源: 同上（可信度：一手）
- **过度使用警告**：「When possible, using whitespace alone to create clear groupings reduces the visual complexity of a design. Borders are often added in an abundance of caution... this approach can result in busy, cluttered designs.」— 来源: 同上（可信度：一手）
- **Enclosure 的反面（Few）**：强网格会「excessively fragment the data and introduce clutter... promoting a strong perception of individual cells through the Gestalt principle of enclosure rather than a seamless flow of information.」——即全网格把表格变成一个个「笼子」，破坏连续扫描。— 来源: https://unotes.net/documents/e84e14fc-4add-4a97-ac58-18ef2f9f82b8/designing-effective-tables-optimizing-communication（可信度：二手，Few《Show Me the Numbers》原书转述）

### 3.4 Continuity（连续性）
- 定义：「Elements arranged in visual paths and sequences are perceived as part of the same whole.」— 来源: https://nngroup.com/articles/psychology-study-guide/（可信度：一手，NN/g 官方心理学学习指南）
- 落地：对齐的数字列形成一条隐形垂直通道，读者视线沿它下移；被打断（居中对齐、混合小数位）就破坏连续性。— 来源: 推断（基于 Few 对齐规则与 NN/g 连续性定义）
- 表格方向性：让列间距 > 行间距则引导纵向扫描；反之引导横向扫描。— 来源: https://unotes.net/documents/e84e14fc-4add-4a97-ac58-18ef2f9f82b8/designing-effective-tables-optimizing-communication（可信度：二手，Few 原书转述）

### 3.5 落地结论：表头与数据如何区分
- 表头应「distinct but not overwhelming... exist to orient the reader, not to compete with the data for attention.」常见错误是把表头做得又大又粗又彩色，反客为主。— 来源: https://rich-iannone.github.io/gt-effective-display-tables/01-introduction.html（可信度：二手，R `gt` 包官方有效表格指南）
- 首选靠**对齐 + 留白 + 一条细横线**区分表头与数据，而非靠填满底色。— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits 与 https://prototypr.io/news/web-typography-designing-tables-to-be-read-not-looked-at（可信度：二手，后者转引 Jan Tschichold《Asymmetric Typography》）
- Tufte/GMU 原则：「Concentrate on the data and NOT the data containers.」— 来源: https://chnm.gmu.edu/digitalhistory/links/cached/chapter4/4_13b_tufte.htm（可信度：二手）

### 3.6 落地结论：分组行如何使用
- 组间用竖向白空间（刚好能看出断句即可），每组开头**重复列头**，组间表格结构保持一致。— 来源: https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/（可信度：二手，Few 原书规则）
- 需要隔离查看某组时，每组另起一页；多分类分组时把组头放同一行。— 来源: 同上（可信度：二手）
- 使用**强/淡交替的分组横线**而非给每个单元格画框：每 3–5 条一条细线；宽表每 3 行一条。— 来源: https://reliefweb.int/attachments/ec6e53ca-15c4-369d-83ba-95c4f43363b6/t-121007-tb-table-design.pdf（可信度：二手， ReliefWeb 技术简报《Technical Brief on Effective Table Design》）
- 眼动实验表明：**突出小计/总计的方式比用网格线更重要**，且用背景色突出小计/总计最受欢迎。— 来源: https://www.researchgate.net/publication/295507835_Using_Eye_Tracking_Technology_to_Improve_Information_Perception_of_Tabular_Managerial_Information（可信度：二手，学术研究）

---

## 4. 数字排版细节

### 4.1 Tabular figures（等宽数字）为何至关重要
- 定义：「Numerals drawn to identical widths so digits stack into columns, and so a changing number does not shift the text around it.」— 来源: https://vocab.design/tabular-figures（可信度：二手，字体排印专业站）
- 问题机理：多数正文字体把 `1` 画得比 `0` 窄（proportional figures），放进列里「hundreds place of one row sits over the tens place of the next, and the column stops being readable as a column」。— 来源: 同上（可信度：二手）
- 解决方案：tabular figures 给每个数字相同的 advance width（通常取最宽者），无需任何对齐操作即逐位对齐，小数点落在预期位置。— 来源: 同上（可信度：二手）
- 附加价值：原位更新的数字（时钟、倒计时、实时票数）宽度恒定，旁边内容不会「抽搐」。— 来源: 同上（可信度：二手）
- CSS/OpenType 映射：`font-variant-numeric: tabular-nums` 对应 OpenType `tnum`；`proportional-nums` 对应 `pnum`；字体若不含该 feature 会忽略请求而非伪造，需先确认字体支持。— 来源: 同上（可信度：二手）
- Datawrapper：「For most of your data visualizations, use tabular figures.」并推荐 multiplexed/uni-width 字体（各字重等宽），便于用粗体高亮表格数字而不破坏对齐。— 来源: https://www.datawrapper.de/blog/fonts-for-data-visualization（可信度：二手）
- **比例字体 + tabular-nums 是多数数据表的最佳选择**：纯等宽字体用于代码好，但混合文字数字表会让文字间距不自然。— 来源: https://wpdatatables.com/best-fonts-for-tables/（可信度：二手）
- 数据：据 2024 Web Almanac，仅 16% 的网络字体支持 tabular/proportional 数字变体——多数网页字体并非为表格设计。— 来源: https://wpdatatables.com/best-fonts-for-tables/（可信度：二手，转引 HTTP Archive Web Almanac）
- **Lining vs Oldstyle**：Lining figures 与大写字母等高，适合表格与标题；Oldstyle 有升降部，适合正文段落。两条轴独立，存在 tabular oldstyle figures。— 来源: https://www.datawrapper.de/blog/fonts-for-data-visualization 与 https://vocab.design/tabular-figures（可信度：二手）
- **使用范围要 scope**：不要把全文设成 tabular-nums（会让正文像电子表格）；只在表格、指标、计时器上启用。— 来源: https://vocab.design/tabular-figures（可信度：二手）
- 负号：真正的减号 `−`（U+2212）比连字符 `-` 视觉长度更合适；仅靠颜色编码负值不足。— 来源: https://unmorning.com/the-fine-art-of-number-typesetting-choosing-type-for-tables-and-data/（可信度：二手）

### 4.2 右对齐与小数点对齐
- 数字右对齐、文本左对齐（Few，见 2.2）。— 来源: https://www.gointrepid.com/blog/posts/data-visualization-secrets-creating-tables（可信度：二手，转引 Few）
- Royal Statistical Society：「Numbers should be right-aligned to allow for easy identification of large and small numbers. In this way, large numbers literally stick out.」— 来源: https://royal-statistical-society.github.io/datavisguide/docs/principles.html（可信度：二手，英国皇家统计学会指南）
- 同一列位数一致，小数点与末位右对齐（Few，见 2.2）。— 来源: https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/（可信度：二手）

### 4.3 有效数字与舍入策略
- RSS 指南：「The number of digits should be consistent within a table row or column (i.e., the same variable) but can differ across variables. Unnecessary precision should be avoided.」— 来源: https://royal-statistical-society.github.io/datavisguide/docs/principles.html（可信度：二手，权威机构）
- Ehrenberg「Rudiments of Numeracy」经典做法：数值舍入到**两位有效数字**，按组内大小重排行，每组底部放清晰标注的汇总行——让模式立即显现。— 来源: https://rich-iannone.github.io/gt-effective-display-tables/01-introduction.html（可信度：二手）
- Datawrapper 建议短格式：`1.3m` 代替 `1.300.000`，`0.1` 代替 `0.1129302`，以缩窄列宽。— 来源: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables（可信度：二手）
- 冲突提示：Tufte/Ehrenberg 主张激进舍入看模式，Few 主张按决策需要保留必要精度——取舍取决于「读者是查精确值还是看模式」，详见第 8 章。— 来源: https://www.edwardtufte.com/notebook/page/4 与 https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：一手 + 二手）

### 4.4 单位放在表头还是单元格
- Few：单位放表头（`Pure premium ($)`）而非每格；货币符号只在汇总处。— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits 与 https://principus.si/2021/03/22/stephen-few-show-me-the-numbers-designing-tables-and-graphs-to-enlighten/（可信度：二手）
- 数字与单位之间用**不换行空格（non-breaking space）**粘住，避免换行时 `12` 与 `kg` 分离。— 来源: https://unmorning.com/the-fine-art-of-number-typesetting-choosing-type-for-tables-and-data/（可信度：二手）

### 4.5 千分位分隔符的争议
- 不同locale 约定冲突：美式 `1,000,000`；德式 `1.000.000`；法式 `1 000 000`（细空格）；瑞士 `9'034'102`。同一份表跨国阅读时，`,`/`.` 含义相反会直接误读。— 来源: https://rich-iannone.github.io/gt-effective-display-tables/01-introduction.html（可信度：二手）
- Datawrapper 倾向用短格式 `1.3m` 规避长串分隔符。— 来源: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables（可信度：二手）
- **推断**：对中文游戏数值表，优先「单位进表头 + 适度舍入 + 必要时用「万/亿」作单位」而非 6 位以上逗号串；是否显示千分位应由「同表内是否跨 locale 使用」决定。— 来源: 推断（基于上述 Locale 事实与 Few/Datawrapper 建议）

---

## 5. 表格密度的经典结论

### 5.1 什么时候该密、什么时候该疏
- **数据行数决定布局**：「If you show only a few rows, a wide layout is more pleasant to the eye. If your table has a lot of rows, consider a compact layout that shows more data in the same available space.」——行多则密、行少则疏。— 来源: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables（可信度：二手）
- 行多的好处：跨行比较更容易，整表更可能落在一屏/一页内。— 来源: 同上（可信度：二手）
- Few 的原始机理：通过操纵白空间引导扫描方向——列间距 > 行间距则纵向扫描，行间距 > 列间距则横向扫描；但行间距/文字高度超过 1:1 后就浪费空间、密度降到不可接受。— 来源: https://unotes.net/documents/e84e14fc-4add-4a97-ac58-18ef2f9f82b8/designing-effective-tables-optimizing-communication（可信度：二手，Few 原书转述）
- 载体决定密度：幻灯片上的表格要比近距离阅读的表格「fewer rows, larger text, and higher contrast」。— 来源: https://rich-iannone.github.io/gt-effective-display-tables/01-introduction.html（可信度：二手）
- 密度天花板：Tufte 给出表格约 300 字符/平方英寸的物理上限。— 来源: https://www.edwardtufte.com/notebook/page/4（可信度：一手）

### 5.2 一个单元格塞几个信息的取舍
- RSS 指南：「If table cells contain more than a single value (e.g., means and confidence intervals), it should be considered if there is a better way to display the data... Options include splitting the numbers into multiple table cells, rows, or columns, or reducing the font size for the less relevant numbers.」— 来源: https://royal-statistical-society.github.io/datavisguide/docs/principles.html（可信度：二手，权威机构）
- 推断：游戏数值表里「数值+单位」「当前值/上下限」「数值+评级图标」塞一格，应先问能否拆列/拆行；不能拆时再考虑缩小次要信息字号/灰度，但需保证对比度（见第 6 章）。— 来源: 推断（基于 RSS 指南）
- Datawrapper：能显示条形/迷你图就别堆文字，但条形列会比普通数字列宽，建议只对最重要的一两列用。— 来源: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables（可信度：二手）

### 5.3 行高与留白
- Few：行高 = 2 倍字号（10pt 字 → 20pt 行高）。— 来源: https://towardsdatascience.com/five-rules-for-designing-tables-a953a16e50f3/（可信度：二手，转引 Few）
- Datawrapper：列越少越易读，优先收窄列（图标、缩写、把重复词提到表头、短格式、舍入）；可考虑行列转置，因为人更擅长纵向浏览。— 来源: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables（可信度：二手）
- 斑马纹条件：长表/多列时用浅灰隔行防串行；「zebra shading is likely unnecessary or even confusing when your table shows data in only a few columns」。— 来源: 同上（可信度：二手）
- 眼动实验：不带背景色的「无网格线」错误率 0%，但「水平网格线」任务耗时最短（6.83 秒），是最优效率方案；「竖向彩色背景」最差（12.04 秒）。— 来源: https://www.researchgate.net/publication/295507835_Using_Eye_Tracking_Technology_to_Improve_Information_Perception_of_Tabular_Managerial_Information（可信度：二手，学术研究）
- 长表分页：表格应短于桌面屏高，否则读者意识不到下面还有内容。— 来源: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables（可信度：二手）

---

## 6. 可访问性与配色

### 6.1 WCAG 2.x 对比度精确阈值（一手规范）
- SC 1.4.3 Contrast (Minimum)（Level AA）：普通文本至少 **4.5:1**；大号文本至少 **3:1**。— 来源: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html（可信度：一手，W3C 官方）
- 大号文本定义：「at least 18 point if not bold and at least 14 point if bold」，中文/日文/韩文字体需等效尺寸；按页面换算 `1pt = 1.333px`，约等于 24px 与 18.66px（原文约 18.5px）。— 来源: 同上（可信度：一手）
- **阈值不可四舍五入**：「4.499:1 would not meet the 4.5:1 threshold」「2.999:1 不满足 3:1」。— 来源: 同上（可信度：一手）
- 例外：incidental 文本（非活动 UI、纯装饰、不可见、含其他重要视觉内容的图片一部分）与 logotypes 无对比度要求；但企业品牌色导致的低对比度不豁免。— 来源: 同上（可信度：一手）
- 适用范围：也适用于文字图像、placeholder、hover/focus 时出现的文字。— 来源: 同上（可信度：一手）
- 非文本（UI 组件、图形对象）另有 SC 1.4.11 的 3:1 要求（推断补充：边框/图标也应≥3:1）。— 来源: 推断（基于 WCAG 体系；本次未抓取 1.4.11 原文）

### 6.2 色盲比例与类型
- NCBI Bookshelf《The Perception of Color》Table 1 先天性色觉缺陷患病率：男性约 **8%**，女性约 **0.5%**；其中 Protanomaly 男 1%，Deutanomaly 男 5%，Protanopia 男 1%，Deuteranopia 男 1.5%，Tritanopia 罕见。— 来源: https://www.ncbi.nlm.nih.gov/books/NBK11538/table/ch28kallcolor.T1/（可信度：一手，NCBI/权威著作）
- PubMed：红绿色盲「present in about 8% of males and 0.44% of females」；其中 **3/4 是 deuteranopes/deuteranomalous，1/4 是 protanopes/protanomalous**。— 来源: https://pubmed.ncbi.nlm.nih.gov/7637311（可信度：一手，PubMed 摘要）
- 全球综述：北欧裔男性约 8%、女性约 0.5%；中国男性 4.0–6.9%、日本约 4.0%。— 来源: https://pmc.ncbi.nlm.nih.gov/articles/PMC12385717/（可信度：一手，PMC 综述）
- Okabe & Ito（作者本人）：白人男性 1/12（8%）红绿色盲，亚洲 1/20（5%），非洲 1/25（4%）；250 人房间里预计有 10 名以上色盲。— 来源: https://jfly.uni-koeln.de/color/（可信度：一手，作者本人页面）

### 6.3 为什么不能只用颜色传递信息
- WCAG SC 1.4.1 Use of Color（Level A）：「Color is not used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element.」— 来源: https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html（可信度：一手，W3C）
- 官方允许的额外视觉区分：若颜色差异还伴随**明度差异**且相对亮度对比≥3:1（如浅绿 vs 深红），则视为额外视觉区分；但若依赖「准确识别某颜色」（如绿框=有效/红框=无效），则无论对比度多少都需额外指示器。— 来源: 同上（可信度：一手）
- 失败案例：F81（仅用颜色标识必填/错误字段）、F13（图表仅用颜色编码且说明只提颜色）。— 来源: 同上（可信度：一手）
- 正确做法：颜色 + 文字/图标/形状双编码（如红字必填字段旁加图标）。— 来源: 同上（可信度：一手）
- Okabe & Ito 三原则：①选所有色觉类型都易辨的配色；②不仅用颜色，还结合形状、位置、线型、填充图案；③需要口头沟通颜色名时明确说出颜色名。并强调「Do not convey information in color only. Show difference BOTH in color and shape (solid and dotted lines, different symbols, various hatching).」— 来源: https://jfly.uni-koeln.de/color/（可信度：一手）
- 红绿问题：红绿色盲难以区分相近亮度的红与绿；protanopes 觉得红色很暗（深红近乎黑）。建议用**洋红（magenta）代替红**，用**朱红 vermilion #D55E00**代替纯红 `#FF0000`。— 来源: 同上（可信度：一手）
- 小物件/细线用粗体 sans-serif（Arial/Helvetica）色标，比细体 Times 更易辨。— 来源: 同上（可信度：一手）
- 直接标注优于分离图例：「label elements of the graph on the graph itself rather than making a separate color-coded key, since matching same colors in distant places is extremely difficult.」— 来源: 同上（可信度：一手）

### 6.4 色盲安全调色板（Okabe-Ito）
- 8 色十六进制值（多源一致）：`#000000`、`#E69F00`、`#56B4E9`、`#009E73`、`#F0E442`、`#0072B2`、`#D55E00`、`#CC79A7`。— 来源: https://conceptviz.app/blog/okabe-ito-palette-hex-codes-complete-reference 与 https://labcanvas.com/tools/palettes（可信度：二手，多源交叉验证；作者页 Fig 16 为图片故以文本源为准）
- 该配色在模拟 protanopia/deuteranopia 下任意两色最小色差 ΔE*ab ≈ 17，高于「≥10 即色盲友好」阈值。— 来源: https://labcanvas.com/tools/palettes（可信度：二手）
- 使用建议：暖冷色交替；同温色之间拉开明度/饱和度差；避免低饱和/低亮度组合。— 来源: https://jfly.uni-koeln.de/color/（可信度：一手）
- 对 Excel 落地（推断）：状态色「达标/预警/异常」不应仅用红/绿，应搭配文字或符号（✓ / ! / ✕）；conditional formatting 的状态色改用上述色盲安全色，且保留 WCAG 4.5:1 文字对比。— 来源: 推断（基于 WCAG 1.4.1 + Okabe-Ito）

---

## 7. 中文字体与排版特殊性

### 7.1 字体回退（font fallback）导致的中英文混乱
- Microsoft 官方问答：Arial/Calibri 本身不含常用中文字符，输入中文时 Excel 自动回退到宋体/等线显示；「单元格整体仍显示 Arial，但进入编辑状态后中文会显示为其他字体」。— 来源: https://learn.microsoft.com/zh-cn/answers/questions/5993224/excel-arial（可信度：一手，Microsoft Learn 官方问答）
- 解决方案：把 Excel 默认字体改为「等线」或「微软雅黑」（包含中文字符的字体），重启 Excel；已有文件需手动改。— 来源: 同上（可信度：一手）
- Microsoft Q&A：等线是完整中文字体、包含西文字符，设默认字体后「所有内容（包括中英文）将统一使用等线字体」，但英文字体会变为等线风格；若要保留 Calibri 英文风格需用 VBA 按字符切换。— 来源: https://answers.microsoft.com/zh-hans/msoffice/forum/all/excel常规字体设/7601640b-9d6f-4bbc-923f-f78316b4b96f（可信度：一手，Microsoft 社区官方问答）
- **字体不统一的代价**：字体/字号不一致会让行高跳动、打印时列宽对不上、导出 PDF 后每页表格位置不一致。— 来源: https://www.maoken.com/article-list/excel-unify-font（可信度：二手，实践观察）
- **数字与中文混排基线**：中文用一套字、数字另一套字会「视觉上基线对不齐」；表格里数字列多时建议整表用同一款字，靠右对齐和等宽数字解决对齐，而不是频繁换字体。— 来源: 同上（可信度：二手，与 4.1 的 tabular-nums 原则一致）

### 7.2 全角字符与列宽跳动
- 中文字体全角字符宽度通常约为数字/半角英文字母的两倍；Excel 列宽以「字符数」计量，混排时按最长内容自动调整会导致列宽跳动。— 来源: 推断（基于 Microsoft 字体回退事实与 Excel 列宽机制的常识性判断；未找到本次调研中的直接权威出处）
- 后果：同一列中「中文说明」与「数字」混排、或单元格内剪贴板带入不可见空格/换行符，会让自动列宽异常宽。— 来源: https://idctop.com/article/473116.html（可信度：二手，低权重实践观察）
- 实践建议（推断）：数值列与文字列分开设字体/对齐；数值列用固定列宽或自动列宽后锁定，避免后续输入中文把列撑宽。— 来源: 推断

### 7.3 推荐字体栈与依据
- **中文主体：微软雅黑 / 等线（DengXian）**。依据：Microsoft 官方推荐这两款作为 Excel 默认字体以解决中英文回退不一致。— 来源: https://learn.microsoft.com/zh-cn/answers/questions/5993224/excel-arial（可信度：一手）
- **数字：Consolas**。Microsoft 官方字体文档：Consolas「aimed for use in programming environments... All characters have the same width」，Fixed pitch = True，且含 lining numerals、斜线/点/正常零、OpenType 特性；随 Windows/Office 分发。— 来源: https://learn.microsoft.com/zh-cn/typography/font-list/consolas（可信度：一手，Microsoft Typography）
- **跨平台开源中文：Source Han Sans / Noto Sans CJK**。Datawrapper 将 Noto Sans 列为「good options and free to use」且自带 tabular、lining figures。— 来源: https://www.datawrapper.de/blog/fonts-for-data-visualization（可信度：二手）；Source Han Sans 与 Noto Sans CJK 同源为 Adobe/Google 开源 CJK 无衬线体为常识性背景，**本次未抓到一手出处，标推断**。— 来源: 推断
- **组合建议（推断）**：微软雅黑/等线作全表基础字体保证中文一致；数字列改用 Consolas（固定宽度+lining figures）实现逐位对齐；若需强调某数值用粗体而非换字体，避免破坏宽度对齐。— 来源: 推断（基于 7.1–7.3 已验证事实的组合）
- 注意：Consolas 等纯等宽字体用于长段中文会不自然；仅在数字列局部使用（呼应 4.1「scope」原则）。— 来源: 推断

---

## 8. 冲突清单（保留分歧，不和稀泥）

### 冲突 1：表格要不要竖向网格线
- **反对方（主流）**：Few 体系主张「drop vertical gridlines entirely；用留白分隔列」。— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手）
- **反对方（排版学）**：Tschichold「Tables should not be set to look like nets with every number enclosed. Try to do without rules altogether.」但留了例外——「Vertical rules are needed only when the space between columns is so narrow that mistakes will occur」。— 来源: https://prototypr.io/news/web-typography-designing-tables-to-be-read-not-looked-at（可信度：二手，转引 Jan Tschichold《Asymmetric Typography》）
- **反对方（实证）**：眼动实验「Do not use vertical segregation」——竖线错误率 10.7%（无网格线 0%），显著最差。— 来源: https://www.researchgate.net/publication/295507835_Using_Eye_Tracking_Technology_to_Improve_Information_Perception_of_Tabular_Managerial_Information（可信度：二手，学术研究）
- **条件保留方**：ReliefWeb 技术简报「avoid vertical column lines or keep them subdued」——极窄列时可用但要压淡。— 来源: https://reliefweb.int/attachments/ec6e53ca-15c4-369d-83ba-95c4f43363b6/t-121007-tb-table-design.pdf（可信度：二手）
- **结论**：默认不画竖线；唯一共识例外是列间距过窄导致串行时，用极淡竖线。这不是完全对立，而是「默认禁用 + 窄列例外」。

### 冲突 2：数据区内部到底要不要横线、要多密
- ** Few/精算体系**：最多表头下、合计行上各一条浅横线，数据区内不画。— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手）
- **ReliefWeb**：每 3–5 条一条细线；宽表每 3 行一条。— 来源: https://reliefweb.int/attachments/ec6e53ca-15c4-369d-83ba-95c4f43363b6/t-121007-tb-table-design.pdf（可信度：二手）
- **眼动实验**：效率最优是水平网格线（6.83 秒），但错误率最优是无网格线（0%），最终推荐「无网格线 + 突出小计/总计」。— 来源: https://www.researchgate.net/publication/295507835_Using_Eye_Tracking_Technology_to_Improve_Information_Perception_of_Tabular_Managerial_Information（可信度：二手）
- **结论**：保留冲突。横向分隔的密度取决于表宽、行数与是否有小计/总计，三家给出不同密度，不能和稀泥成一条规则。

### 冲突 3：斑马纹（隔行底色）
- **支持（有条件）**：Datawrapper——长表多列时用浅灰隔行防串行；少列时不必要甚至困惑。— 来源: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables（可信度：二手）
- **反对（Few）**：除非表很宽，否则避免隔行填充。— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手）
- **强反对（Web 排版实践，**不是** Tschichold）**：「Avoid zebra striping, tints and fills, and any other backgrounds... They serve to distort the meaning of the data by highlighting every other row to the detriment of neighbouring rows.」— 来源: https://prototypr.io/news/web-typography-designing-tables-to-be-read-not-looked-at（可信度：二手）
- **Tschichold 本人的主张——仅针对分隔线（rules），不涉及斑马纹**：「Tables should not be set to look like nets with every number enclosed. Try to do without rules altogether... Vertical rules are needed only when the space between columns is so narrow that mistakes will occur in reading without rules.」— 来源: 同上文章转引《Asymmetric Typography》（可信度：二手转引）
- **中立（NN/g）**：斑马纹是有效 common region 手段，但边框/背景过度使用会造成杂乱，优先用留白。— 来源: https://www.nngroup.com/articles/common-region/（可信度：一手）
- **结论**：保留冲突。多列长表 vs 少列表 vs 排版学纯主义，结论不同。

> ⚠️ **2026-11-17 归属更正（重要）**：初版把「Avoid zebra striping, tints and fills...」整条归给 Jan Tschichold，
> 并附了一个不可验证的短链（cur.at）。复核 prototypr.io 原文后确认：**该句出自 Richard Rutter（《Web Typography》作者）**；
> 他用 Tschichold 的另一句原话来总结「分隔线」问题。两句话讲的是两件事（斑马纹 vs 表格边框），
> 初版合并成一条并错误归属。已拆分更正。
> 教训：**二手引文不能因为「读起来像那一派的观点」就归给那个人，必须回溯原始出处。**

### 冲突 4：数字宽度实现方式
- 一致点：表格数字要逐位对齐，用 tabular-nums（tnum）。— 来源: https://vocab.design/tabular-figures（可信度：二手）
- 分歧点：是否用**纯等宽字体**（如 Consolas）。一方认为表格/仪表盘 tabular figures「non-negotiable」；另一方认为「proportional with tabular nums is the right call for most data tables」，纯等宽对混合文字数字表不自然。— 来源: https://unmorning.com/the-fine-art-of-number-typesetting-choosing-type-for-tables-and-data/ 与 https://wpdatatables.com/best-fonts-for-tables/（可信度：二手）
- **结论**：方法一致、实现路径分歧；推荐按列局部使用等宽字体（见 7.3 推断）。

### 冲突 5：舍入力度与千分位
- **激进舍入派**：Tufte「approximately right rather than exactly wrong」；Ehrenberg 舍入到 2 位有效数字。— 来源: https://www.edwardtufte.com/notebook/page/4 与 https://rich-iannone.github.io/gt-effective-display-tables/01-introduction.html（可信度：一手 + 二手）
- **按需精度派**：Few「show only the precision the decision needs」——某些决策确需 1.0837 这种精度。— 来源: https://open-exam-prep.com/study-guides/cas-pcpa/ch08-tables-charts/designing-tables-exhibits（可信度：二手）
- **一致性派**：RSS——同一变量内位数一致，不同变量可不同。— 来源: https://royal-statistical-society.github.io/datavisguide/docs/principles.html（可信度：二手）
- **千分位 Locale 冲突**：`,` 在美式是千分位、在德式是小数点，字面相同含义相反。— 来源: https://rich-iannone.github.io/gt-effective-display-tables/01-introduction.html（可信度：二手）
- **结论**：保留冲突。精度取舍取决于使用场景（查值 vs 看模式）；千分位须按读者 locale 决定或改用「万/亿」单位规避。

---

## 9. 事实与推断对照表

| 结论 | 性质 | 主来源 |
|---|---|---|
| 数据墨水比定义与四步法 | 事实（一手） | Few 转 Tufte |
| 表格密度上限 300 字符/平方英寸 | 事实（一手） | Tufte 本人站点 |
| 「宁可大致正确，不要精确错误」 | 事实（一手） | Tufte 本人站点（引 Tukey） |
| 小 x-height → 更多白空间 → 更可读 | 事实（一手） | Tufte 本人站点 |
| 数字右对齐、文本/日期左对齐、表头同对齐、禁居中 | 事实（二手转述 Few） | principus.si / gointrepid |
| 行高 = 2×字号 | 事实（二手转引 Few） | Towards Data Science |
| dashboard 信息量不压倒、颜色极克制、重要项左上 | 事实（一手） | Few 白皮书 |
| 邻近性可压过相似性；共同区域可压过邻近性 | 事实（一手） | NN/g |
| 斑马纹在宽表防串行、少表反困惑 | 事实（二手，冲突） | Datawrapper / Few / Tschichold |
| Tabular figures 逐位对齐、text 用 proportional | 事实（二手） | vocab.design / Datawrapper |
| Consolas 固定宽度、含 lining figures | 事实（一手） | Microsoft Typography |
| WCAG 4.5:1 / 3:1；18pt/14pt bold；阈值不四舍五入 | 事实（一手） | W3C WCAG 2.1 |
| 色盲男约 8%、女约 0.5%；3/4 为绿色盲类 | 事实（一手） | NCBI / PubMed |
| 不能仅用颜色传递信息；须文字/形状双编码 | 事实（一手） | W3C SC 1.4.1 / Okabe & Ito |
| Okabe-Ito 8 色 HEX | 事实（二手交叉验证） | conceptviz / labcanvas |
| 中文回退致中英文字体不一致 | 事实（一手） | Microsoft Learn |
| 微软雅黑/等线为中文主体、Consolas 为数字 | 事实（一手依据）+ 推断（组合） | Microsoft Typography |
| 微软雅黑/等线 + Consolas 的组合字体栈 | 推断 | 基于以上事实推导 |
| 千分位在中文表改用「万/亿」单位 | 推断 | 基于 Locale 冲突事实 |
| 单元格多值优先拆列/拆行 | 事实（二手）+ 推断（落地） | RSS 指南 |

---

## 10. 给「Excel 表格排版 UX 设计师」技能的高价值落地点（源自以上调研）

1. **先判表格 vs 图形**：读者要查精确值/排名 → 表格；要看趋势/异常 → 图形（Few + Datawrapper）。≤20 个数字优先表格（社区派生，标低权重）。
2. **对齐铁律**：数字右对齐 + 相同小数位 + 小数点对齐；文本/日期左对齐；表头同对齐；绝不居中（Few）。
3. **去非数据墨**：删竖向网格线、删整表外框；表头下/合计行上最多一条细横线；靠留白分组（Few + Tufte + Tschichold）。
4. **数字字体**：数字列用 Consolas 或开启 tabular-nums 的字体，逐位对齐；中文主体用微软雅黑/等线，避免字体回退导致列宽跳动（Microsoft）。
5. **颜色克制且双编码**：状态色用 Okabe-Ito 色盲安全色，且必须搭配文字/符号；正文对比≥4.5:1、大字号≥3:1，且不能四舍五入（WCAG + Okabe & Ito）。

---

*（文件结束。全文结论均附来源 URL 与可信度；第 8 章集中保留了 5 组来源冲突，未做折中。）*
