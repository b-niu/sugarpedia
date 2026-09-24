# -*- coding: utf-8 -*-
"""
生成「唐代卫府制」一文的两张图。

输出目录：content/assets/weifu/

  weifu_structure.svg    卫府制的层级：皇帝—兵部／十六卫／东宫十率／北衙禁军—折冲府—团旅队火
  fubing_timeline.svg    府兵制与卫府制的时间线：西魏成型到天宝八载停鱼书

图内文字字号 ≥12px、标题 16px，配色沿用 Okabe-Ito 色盲友好方案，
满足 docs/design.md「排版与渲染规范」的要求。
"""
import os

from svgkit import (C_INK, C_AXIS, C_GRID, C_REF, C_UP, C_DOWN, C_MID, C_OK,
                    FS_TITLE, FS_NOTE, txt, write_svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "weifu")
os.makedirs(OUT, exist_ok=True)


def svg_open(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif">'
            f'<rect width="{w}" height="{h}" fill="white"/>')


def box(x, y, w, h, lines, color, fs=12.5, op=0.18, rx=8):
    el = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
          f'fill="{color}" fill-opacity="{op}" stroke="{color}" stroke-width="1.5"/>']
    n = len(lines)
    for i, (content, size, bold) in enumerate(lines):
        yy = y + h / 2 + (i - (n - 1) / 2) * 17 + size * 0.36
        el.append(txt(x + w / 2, yy, content, size, C_INK, "middle", "bold" if bold else None))
    return el


def vconn(x, y1, y2, color=C_REF):
    return (f'<path d="M {x:.1f} {y1:.1f} L {x:.1f} {y2:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="1.6"/>')


# ============================================================
# 图一：卫府制的层级
# ============================================================
def gen_structure():
    W, H = 720, 520
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "卫府制的层级：卫统府，府统团旅队火", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "十二卫遥领全国折冲府，十六卫中余下四卫专掌门户与贴身宿卫",
                 FS_NOTE, C_AXIS, "middle"))

    CX = W / 2
    # 皇帝
    p.extend(box(CX - 70, 78, 140, 42, [("皇　帝", 13.5, True)], C_UP, op=0.26))
    p.append(vconn(CX, 120, 146, C_UP))

    # 第二层：四路
    row2 = [
        (24, 152, "兵　部", ["掌军籍、番第", "与调发"]),
        (200, 136, "十六卫（南衙）", ["十二卫统折冲府", "四卫掌门户宿卫"]),
        (352, 136, "东宫十率", ["太子系统的", "军事机构"]),
        (504, 192, "北衙禁军", ["羽林、龙武、", "神武、神策", "直属皇帝"]),
    ]
    for x, w, title, subs in row2:
        lines = [(title, 12.5, True)] + [(s, FS_NOTE, False) for s in subs]
        p.extend(box(x, 152, w, 62, lines, C_DOWN, op=0.16))
        p.append(vconn(x + w / 2, 146, 152, C_REF))

    # 汇到折冲府
    p.append(vconn(CX, 214, 250, C_REF))
    p.extend(box(CX - 210, 250, 420, 62,
                 [("折冲府（全国约 634 府）", 13, True),
                  ("上府 1200 人　中府 1000 人　下府 800 人", FS_NOTE, False)],
                 C_MID, op=0.22))
    p.append(vconn(CX, 312, 350, C_REF))

    # 编制层级
    tiers = [("团", "200 人", "校尉"), ("旅", "100 人", "旅帅"),
             ("队", "50 人", "队正"), ("火", "10 人", "火长")]
    bw, gap = 140, 22
    x0 = (W - (bw * 4 + gap * 3)) / 2
    for i, (name, num, chief) in enumerate(tiers):
        x = x0 + i * (bw + gap)
        p.extend(box(x, 350, bw, 68,
                     [(f"{name}　{num}", 13, True), (f"统将：{chief}", FS_NOTE, False)],
                     C_OK, op=0.18))
        if i < 3:
            ax = x + bw
            p.append(f'<path d="M {ax + 2} {384} L {ax + gap - 4} {384}" fill="none" '
                     f'stroke="{C_OK}" stroke-width="2"/>')
            p.append(f'<path d="M {ax + gap - 10} 379 L {ax + gap - 3} 384 '
                     f'L {ax + gap - 10} 389" fill="none" stroke="{C_OK}" stroke-width="2" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>')

    p.append(txt(24, H - 62, "每府置折冲都尉一人、左右果毅都尉各一人，下辖四至六团；", FS_NOTE, C_AXIS))
    p.append(txt(24, H - 42, "府兵平时在家务农，按番次轮流上番宿卫，每次一个月；远处可纳资代番。",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, H - 20, "全国折冲府并非都要进京：东北、江南等地的府兵主要承担地方任务。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "weifu_structure.svg"), "\n".join(p))


# ============================================================
# 图二：时间线
# ============================================================
def gen_timeline():
    events = [
        ("550 · 西魏", ["大统十六年", "八柱国十二大将军"]),
        ("隋·炀帝", ["置十二卫", "与四府"]),
        ("唐初", ["改骠骑府、车骑府", "为折冲府"]),
        ("贞观年间", ["置军府 634 个", "关中约占四成"]),
        ("722 · 开元十年", ["募兵十三万", "充任宿卫"]),
        ("723—725 年", ["长从宿卫改称", "彍骑"]),
        ("749 · 天宝八载", ["停折冲府", "上下鱼书"]),
    ]
    W, H = 720, 372
    AXIS_Y = 196
    BOX_W, BOX_H = 142, 76
    X0, STEP = 88, 93
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "府兵制与卫府制：从成型到终结", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "横轴按事件先后排列，刻度不按年代比例", FS_NOTE, C_AXIS, "middle"))
    p.append(f'<path d="M 36 {AXIS_Y} L 684 {AXIS_Y}" fill="none" stroke="{C_AXIS}" '
             f'stroke-width="2" stroke-linecap="round"/>')

    for i, (head, lines) in enumerate(events):
        x = X0 + i * STEP
        above = (i % 2 == 0)
        hot = (i >= 4)
        color = C_UP if hot else C_DOWN
        if above:
            by = AXIS_Y - 44 - BOX_H
            link = (f'<path d="M {x} {by + BOX_H} L {x} {AXIS_Y - 7}" fill="none" '
                    f'stroke="{color}" stroke-width="1.4"/>')
        else:
            by = AXIS_Y + 44
            link = (f'<path d="M {x} {AXIS_Y + 7} L {x} {by}" fill="none" '
                    f'stroke="{color}" stroke-width="1.4"/>')
        p.append(f'<path d="M {x} {AXIS_Y - 7} L {x} {AXIS_Y + 7}" fill="none" '
                 f'stroke="{C_AXIS}" stroke-width="2"/>')
        p.append(link)
        p.append(f'<rect x="{x - BOX_W / 2}" y="{by}" width="{BOX_W}" height="{BOX_H}" rx="8" '
                 f'fill="white" stroke="{color}" stroke-width="1.4"/>')
        p.append(txt(x, by + 22, head, 12.0, color, "middle", "bold"))
        for k, ln in enumerate(lines):
            p.append(txt(x, by + 42 + k * 17, ln, 12.0, C_INK, "middle"))

    p.append(txt(24, H - 16, "蓝色为成型与定型阶段，朱红为向募兵制转变并终结的阶段。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "fubing_timeline.svg"), "\n".join(p))


gen_structure()
gen_timeline()
