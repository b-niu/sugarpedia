# -*- coding: utf-8 -*-
"""
生成「汉代武官体系」一文的三张图。

输出目录：content/assets/han/

  mil_systems.svg      汉代军事官职的六条线（校尉、中郎将、将军各归哪一支）
  general_ranks.svg    将军的层级：重号四层与杂号
  sili_xiaowei.svg     司隶校尉：品秩不高而权势极重

图内文字字号 ≥12px、标题 16px，配色沿用 Okabe-Ito 色盲友好方案。
"""
import os

from svgkit import (C_INK, C_AXIS, C_GRID, C_REF, C_UP, C_DOWN, C_MID, C_OK, C_BASE,
                    FS_TITLE, FS_NOTE, txt, write_svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "han")
os.makedirs(OUT, exist_ok=True)


def svg_open(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif">'
            f'<rect width="{w}" height="{h}" fill="white"/>')


def box(x, y, w, h, lines, color, op=0.18, rx=8, sw=1.5):
    el = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
          f'fill="{color}" fill-opacity="{op}" stroke="{color}" stroke-width="{sw}"/>']
    n = len(lines)
    for i, (content, size, bold) in enumerate(lines):
        yy = y + h / 2 + (i - (n - 1) / 2) * 18 + size * 0.36
        el.append(txt(x + w / 2, yy, content, size, C_INK, "middle", "bold" if bold else None))
    return el


# ============================================================
# 图一：六条线
# ============================================================
def gen_systems():
    W, H = 720, 436
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "汉代的军事官职分属六条线", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "「校尉」「中郎将」「将军」都只是名号，自己的职权要看挂在哪一条线上",
                 FS_NOTE, C_AXIS, "middle"))

    cells = [
        ("宫官系统", "光禄勋 → 郎官", "中郎将为其统领，宿卫宫门", C_DOWN),
        ("南　军", "卫尉掌宫城卫士", "负责皇宫内部的宿卫", C_MID),
        ("北　军", "中尉（执金吾）→ 八校尉", "京师屯兵，战时抽调出征", C_UP),
        ("城　门", "城门校尉", "掌京师十二座城门", C_REF),
        ("出　征", "将军 → 部曲 → 校尉", "因战事临时组建，事罢即撤", C_OK),
        ("监　察", "司隶校尉察京师七郡", "刺史（后之州牧）察一州", C_BASE),
    ]
    cw, ch = 222, 126
    for i, (title, l1, l2, color) in enumerate(cells):
        cx = 17 + (i % 3) * 231
        cy = 72 + (i // 3) * 150
        p.extend(box(cx, cy, cw, 34, [(title, 13, True)], color, op=0.22, rx=7))
        p.extend(box(cx, cy + 42, cw, 84, [(l1, 12.0, False), (l2, 12.0, False)],
                     color, op=0.10, rx=7, sw=1.2))

    p.append(txt(24, H - 42, "汉代以「石」计秩：中二千石、二千石、比二千石、千石、六百石依次而降。",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, H - 20, "同一个名号可以出现在不同线上，所以「校尉」的含金量差别极大。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "mil_systems.svg"), "\n".join(p))


# ============================================================
# 图二：将军的层级
# ============================================================
def gen_ranks():
    W, H = 720, 424
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "将军：重号四层与杂号", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "重号将军名号固定、位次明确；杂号将军因事而设，名号无定",
                 FS_NOTE, C_AXIS, "middle"))

    tiers = [
        ("大将军", "位在三公之上", C_DOWN, 0.26, 360),
        ("骠骑将军 · 车骑将军 · 卫将军", "位比公，在三公之下", C_UP, 0.22, 330),
        ("前将军 · 后将军 · 左将军 · 右将军", "位次上卿，不常置", C_MID, 0.20, 300),
        ("杂　号　将　军", "因战事或职能临时设立", C_REF, 0.18, 270),
    ]
    for i, (name, note, color, op, bw) in enumerate(tiers):
        y = 78 + i * 74
        p.extend(box(24, y, bw, 58, [(name, 13, True), (note, 12.0, False)], color, op=op))

    p.extend(box(408, 78, 288, 258, [], C_OK, op=0.08))
    p.append(txt(420, 104, "杂号的命名有章可循", 12.5, C_OK, "start", "bold"))
    for i, s in enumerate(["按兵种：轻车、材官、楼船、强弩",
                           "按对象：伏波、破羌、度辽、横海",
                           "按职能：护军、骁骑、骑都尉",
                           "",
                           "汉代杂号已名目繁多，到南北朝",
                           "更增至三百六十一种——「将军」",
                           "二字由此严重贬值。"]):
        p.append(txt(420, 134 + i * 26, s, 12.0, C_INK))

    p.append(txt(24, H - 42, "重号将军均开府：长史、司马各一人，从事中郎二人，掾属二十九人等。",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, H - 20, "将军以本号领军的，其下各有部曲与校尉；东汉重号将军多不常置。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "general_ranks.svg"), "\n".join(p))


# ============================================================
# 图三：司隶校尉
# ============================================================
def gen_sili():
    W, H = 720, 430
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "司隶校尉：品级不高，权势极重", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "左为秩禄对比（条越长秩越高），右为它真正掌握的东西",
                 FS_NOTE, C_AXIS, "middle"))

    p.append(txt(36, 84, "秩禄对比", 12.5, C_INK, "start", "bold"))
    bars = [
        ("刺史", "六百石", 132, C_MID),
        ("司隶校尉", "比二千石", 250, C_DOWN),
        ("州牧", "二千石", 272, C_UP),
    ]
    for i, (name, rank, bw, color) in enumerate(bars):
        y = 104 + i * 62
        p.extend(box(36, y, bw, 44, [(name, 12.5, True)], color, op=0.20, rx=6))
        p.append(txt(36 + bw + 12, y + 29, rank, 12.0, C_INK))

    p.extend(box(370, 70, 326, 268, [], C_OK, op=0.08))
    p.append(txt(386, 96, "它实际掌握的", 12.5, C_OK, "start", "bold"))
    items = [
        ("三独坐", ["朝会专席，与御史中丞、", "尚书令并列，为皇帝所优宠"]),
        ("察京师", ["辖京兆、冯翊、扶风、弘农、", "河内、河东、河南共七郡"]),
        ("号卧虎", ["旧有此称，百僚畏之"]),
        ("属　官", ["从事史十二人，都官从事", "掌察举百官犯法"]),
        ("位　次", ["魏晋时坐于端门外，", "位在诸卿之上"]),
    ]
    yy = 124
    for k, lines in items:
        p.append(txt(386, yy, k, 12.0, C_INK, "start", "bold"))
        for j, s in enumerate(lines):
            p.append(txt(446, yy + j * 20, s, 12.0, C_INK))
        yy += 20 * len(lines) + 14
    p.append(txt(24, H - 42, "沿革：汉武帝征和四年（前89）置；成帝元延四年省，哀帝复置称司隶；东汉复称司隶校尉。",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, H - 20, "汉百官朝会一般接席而坐，唯此三官独坐一席，是皇帝给的优宠。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "sili_xiaowei.svg"), "\n".join(p))


gen_systems()
gen_ranks()
gen_sili()
