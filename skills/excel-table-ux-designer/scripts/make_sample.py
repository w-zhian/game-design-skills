# -*- coding: utf-8 -*-
"""
生成「故意排版很烂」的回归测试样本。
诊断器应能报出全部问题；beautify.py 改造后应全部消失。

用法: python make_sample.py [输出路径]
"""
import sys
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


def build(path):
    wb = Workbook()

    # ── Sheet1: 典型的烂汇报表 ──────────────────────────────────────────
    ws = wb.active
    ws.title = "销售数据"

    headers = ["ID", "客户名称", "所属部门", "负责人", "销售额", "订单数", "转化率", "入职日期", "备注"]
    ws.append(headers)
    rows = [
        [1001, "上海晨光文具", "华东销售一部", "张三", "125000", 320, "0.12", "2026/1/5", ""],
        [1002, "北京中科云图科技", "华北销售部", "李四", "68000", 145, "0.08", "2026/2/11", ""],
        [1003, "广州南方数码", "华南销售部", "王五", "231500", 610, "0.19", "2026/3/1", ""],
        [1001, "深圳前海联易", "华南销售部", "赵六", "54000", 98, "0.05", "2026/3/18", "重复ID"],
        [1005, "杭州云栖网络", "", "孙七", "99000", 210, "0.11", "not-a-date", ""],
        [1006, "成都天府软件", "西南销售部", "周八", "176000", 405, "0.15", "2026/4/2", ""],
        [1007, "武汉光谷信息", "华中销售部", "吴九", "88000", 180, "0.09", "2026/4/20", ""],
        [1008, "南京紫金智造", "华东销售二部", "郑十", "142000", 355, "0.13", "2026/5/6", ""],
        [1009, "西安秦岭电子", "西北销售部", "钱一", "61000", 120, "0.07", "2026/5/22", ""],
        [1010, "苏州工业园微芯", "华东销售一部", "冯二", "203000", 520, "0.18", "2026/6/8", ""],
    ]
    for r in rows:
        ws.append(r)

    # 1) 不设列宽（全部默认 8.43）——长文本被截断
    # 2) 表头无样式
    # 3) 数值列全部居中（破坏小数位对齐）
    center = Alignment(horizontal="center", vertical="center")
    for r in range(1, len(rows) + 2):
        for c in range(1, len(headers) + 1):
            ws.cell(r, c).alignment = center

    # 4) 跨行合并：把「华东/华南」这类分组意图用了合并，制造读取陷阱
    ws.merge_cells("D1:D2")

    # 5) 自绘全表四边框（视觉像一张网）
    thin = Side(style="thin", color="FF999999")
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    for r in range(1, len(rows) + 2):
        for c in range(1, len(headers) + 1):
            ws.cell(r, c).border = box

    # 6) 底色种类过多（5 种），无图例
    palette = ["FFFFF2CC", "FFDDEBF7", "FFE2EFDA", "FFFCE4D6", "FFF2F2F2"]
    for i, r in enumerate(range(2, len(rows) + 2)):
        ws.cell(r, 1).fill = PatternFill("solid", start_color=palette[i % 5])

    # 7) 字体/字号混杂
    ws.cell(1, 1).font = Font(name="宋体", size=10, bold=False)
    ws.cell(1, 2).font = Font(name="黑体", size=12, bold=True)
    ws.cell(1, 3).font = Font(name="Calibri", size=14, bold=False)
    for r in range(2, len(rows) + 2):
        ws.cell(r, 5).font = Font(name="Consolas", size=9)
        ws.cell(r, 8).font = Font(name="微软雅黑", size=8)

    # 8) 销售额数字存成文本（已在 rows 里用字符串）
    # 9) 隐藏一列关键字段
    ws.column_dimensions["I"].hidden = True

    # 10) 无冻结、无打印设置、无条件格式、无数字格式

    # ── Sheet2: 疑似 Luban 配置表但表头写错 ─────────────────────────────
    ws2 = wb.create_sheet("ItemConfig")
    # 故意：首行字段名是 ASCII，但 A1 不是 ## 开头
    ws2.append(["id", "name", "quality", "price", "icon", "drop_weight"])
    ws2.append(["int", "string", "int", "int", "string", "float"])
    for i, (name, q, p) in enumerate(
            [("铁剑", 1, 100), ("钢剑", 2, 350), ("秘银剑", 3, 1200), ("龙牙剑", 4, 5000)], start=1):
        ws2.append([i, name, q, p, f"icon_{i}.png", 0.1 * q])
    for c in range(1, 7):
        ws2.column_dimensions[chr(64 + c)].width = 8.43

    # ── Sheet3: 空 sheet ────────────────────────────────────────────────
    wb.create_sheet("Sheet3")

    wb.save(path)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "ugly_sample.xlsx"
    print("已生成:", build(out))
