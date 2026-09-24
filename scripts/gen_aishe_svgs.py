# -*- coding: utf-8 -*-
"""
生成「矮与射：一次并不存在的互换」一文的构形示意图。

输出目录：content/assets/philology/

三张图分工：
  she_evolution.svg      射：从甲骨文到楷书，看「弓」如何走样成「身」
  ai_composition.svg     矮：从矢委声的形声结构，以及同从「矢」的义类字族
  two_char_timeline.svg  两字的出现时间对照：矮最早只到小篆，与射相差上千年

字形说明：甲骨文、金文、小篆各形为按构形理据绘制的**示意图**，用折线近似，
不摹写古文字原形，因此不涉及任何拓本、字形库或字体的图像版权；
楷书字形直接以文字呈现。图示只表达「哪个构件发生了变化」，不承担拓本功能。

图内文字字号 ≥12px、标题 16px，配色沿用 Okabe-Ito 色盲友好方案，
满足 docs/design.md「排版与渲染规范」的要求。
"""
import os

from svgkit import (C_INK, C_AXIS, C_REF, C_LINE, C_BASE, C_UP, C_DOWN, C_OK, C_MID,
                    FS_TITLE, FS_BODY, FS_NOTE,
                    txt, write_svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "philology")
os.makedirs(OUT, exist_ok=True)

LW_STROKE = 2.0          # 构件线宽；刻意避开 1.6，示意图形不参与坐标区判定
LW_CELL = 1.4

# ---------------- 构件示意图：坐标为 0..100 方框内的折线 ----------------
# 每个构件是若干条折线，用折线近似弧线，画出来是示意图而非拓本摹写
GLYPHS = {
    # 弓：右凸的弓背 + 左侧的弦
    "弓": [[(16, 6), (32, 14), (43, 32), (46, 50), (43, 68), (32, 86), (16, 94)],
           [(16, 6), (16, 94)]],
    # 矢：上为镞、中为杆、下为羽
    "矢": [[(50, 12), (50, 88)],
           [(34, 32), (50, 10), (66, 32)],
           [(37, 76), (50, 88), (63, 76)]],
    # 又：自上而右下的手臂 + 两根手指
    "又": [[(74, 8), (56, 40), (26, 84)],
           [(56, 40), (80, 34)],
           [(50, 52), (74, 46)]],
    # 身：躯干轮廓 + 腹线
    "身": [[(30, 10), (62, 10), (66, 32), (66, 56), (56, 78), (50, 94)],
           [(30, 10), (30, 94)],
           [(30, 42), (66, 42)]],
    # 寸：手形 + 右下的一点（短横）
    "寸": [[(68, 14), (48, 50), (24, 84)],
           [(48, 50), (72, 42)],
           [(54, 70), (78, 70)]],
    # 禾：直杆 + 下垂的穗 + 两片叶
    "禾": [[(50, 4), (50, 94)],
           [(50, 12), (36, 22), (32, 34)],
           [(50, 12), (64, 22), (68, 34)],
           [(50, 46), (28, 60)],
           [(50, 46), (72, 60)]],
    # 女：头身一竖 + 交臂 + 交腿
    "女": [[(50, 8), (50, 36)],
           [(24, 46), (50, 30), (76, 46)],
           [(50, 36), (28, 92)],
           [(50, 36), (72, 92)]],
}


def glyph(name, cx, cy, size, color, lw=LW_STROKE):
    """把一个构件居中画在 (cx, cy)，size 为其外接方框边长（0..100 映射到 size）"""
    s = size / 100.0
    out = []
    for line in GLYPHS[name]:
        pts = [(cx + (x - 50) * s, cy + (y - 50) * s) for x, y in line]
        d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}" + "".join(f" L {x:.1f} {y:.1f}" for x, y in pts[1:])
        out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{lw}" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
    return out


def panel(x, y, w, h, fill="#FAFBFC", stroke="#DCE3EA"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{LW_CELL}"/>')


def svg_open(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" '
            f'font-family="Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif">'
            f'<rect width="{w}" height="{h}" fill="white"/>')


# ============================================================
# 图一：射 —— 弓如何走样成身
# ============================================================
def gen_she_evolution():
    W, H = 720, 596
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "「射」的构件走形：弓→身，又→寸", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "同一个字，两侧构件各自走样，全程与「矮」无关", FS_NOTE, C_AXIS, "middle"))

    # 行：(时代, [(构件名, 颜色)], 说明, 是否楷书文字行, 楷书字)
    rows = [
        ("甲骨文·商", [("弓", C_DOWN), ("矢", C_UP)],
         "张弓搭箭之形：左侧是弓，右侧是箭", False, None),
        ("金文·西周", [("弓", C_DOWN), ("矢", C_UP), ("又", C_OK)],
         "再添一只手（又），表示引弓而发", False, None),
        ("小篆·秦（一系）", [("身", C_UP), ("矢", C_UP)],
         "弓背的轮廓走样成了「身」，字作「䠶」", False, None),
        ("小篆·秦（二系）", [("身", C_UP), ("寸", C_OK)],
         "承接金文的那只手「又」走样成了「寸」", False, None),
        ("楷书·今", [], "两系合流，规范字形定为「射」", True, "射"),
    ]

    cell_x, cell_w, cell_h = 148, 152, 82
    top0, dy = 74, 100
    for i, (era, comps, desc, is_kai, kai) in enumerate(rows):
        y0 = top0 + i * dy
        cy = y0 + cell_h / 2
        p.append(txt(24, cy + 5, era, FS_BODY, C_INK, "start", "bold"))
        p.append(panel(cell_x, y0, cell_w, cell_h))
        if is_kai:
            p.append(txt(cell_x + cell_w / 2, cy + 16, kai, 40, C_BASE, "middle", "bold"))
        else:
            n = len(comps)
            if n == 2:
                xs, gsize = [cell_x + 46, cell_x + 106], 58
            else:
                xs, gsize = [cell_x + 29, cell_x + 76, cell_x + 123], 44
            for (name, color), gx in zip(comps, xs):
                p.extend(glyph(name, gx, cy - 8, gsize, color))
                p.append(txt(gx, y0 + cell_h - 6, name, FS_NOTE, color, "middle", "bold"))
        p.append(txt(316, cy + 5, desc, FS_BODY, C_INK))

    p.append(txt(24, H - 40, "同一颜色＝同一个构件：弓（蓝）在后世走样为身（红），又（绿）走样为寸（绿）。",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, H - 20, "字形为按构形理据绘制的示意图，用折线近似，不摹写古文字原形。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "she_evolution.svg"), "\n".join(p))


# ============================================================
# 图二：矮 —— 义符与声符各司其职
# ============================================================
def gen_ai_composition():
    W, H = 720, 452
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "「矮」的构形：义符管长度，声符只管读音", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "拆开看结构，才能判断「曲解成射」错在哪一步", FS_NOTE, C_AXIS, "middle"))

    # --- 区块一：矮 = 矢 + 委 ---
    p.append(panel(24, 66, 672, 168))
    def node(x, y, w, h, s, color):
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="white" '
                 f'stroke="{color}" stroke-width="{LW_CELL}"/>')
        p.append(txt(x + w / 2, y + h / 2 + 9, s, 26, color, "middle", "bold"))
    node(52, 92, 64, 50, "矮", C_BASE)
    p.append(txt(132, 126, "＝", 20, C_AXIS, "middle", "bold"))
    node(158, 92, 64, 50, "矢", C_DOWN)
    p.append(txt(238, 126, "＋", 20, C_AXIS, "middle", "bold"))
    node(264, 92, 64, 50, "委", C_OK)
    # 构件属性
    p.append(txt(190, 166, "义符", FS_NOTE, C_DOWN, "middle", "bold"))
    p.append(txt(296, 166, "声符", FS_NOTE, C_OK, "middle", "bold"))
    p.append(txt(52, 200, "「矢」提示义类：古人以矢为准量长短。「委」只提供读音（wěi），不参与表义。",
                 FS_BODY, C_INK))
    p.append(txt(52, 220, "把「委」读成「抛弃」再合成「把箭抛出去」，是把声符当成了义符。",
                 FS_BODY, C_INK))

    # --- 区块二：同从矢的义类字族 ---
    p.append(panel(24, 252, 672, 150))
    p.append(txt(52, 282, "同一条义类还留在这几个字里：", FS_BODY, C_INK, "start", "bold"))
    for i, (ch, gl) in enumerate([("短", "长度不足"), ("矬", "个子矮"), ("矫", "取直")]):
        x = 72 + i * 120
        p.append(f'<rect x="{x}" y="298" width="62" height="48" rx="8" fill="white" '
                 f'stroke="{C_DOWN}" stroke-width="{LW_CELL}"/>')
        p.append(txt(x + 31, 333, ch, 24, C_DOWN, "middle", "bold"))
        p.append(txt(x + 31, 364, gl, FS_NOTE, C_AXIS, "middle"))
    p.append(txt(452, 300, "《说文》释「短」：", FS_BODY, C_INK))
    p.append(txt(452, 320, "「有所长短，以矢为正。」", FS_BODY, C_INK))
    p.append(txt(452, 348, "箭杆有定长，故可作标尺；", FS_NOTE, C_AXIS))
    p.append(txt(452, 366, "「矫」「矩」等取直之字亦从矢。", FS_NOTE, C_AXIS))

    p.append(txt(24, H - 18, "「矮」最早形体为小篆，甲骨文、金文中均不见此字。", FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "ai_composition.svg"), "\n".join(p))


# ============================================================
# 图三：两字的出现时间对照
# ============================================================
def gen_two_char_timeline():
    W, H = 720, 344
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "两个字没有可互换的时间窗口", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "射自甲骨文起一直在用；「矮」迟至小篆才出现", FS_NOTE, C_AXIS, "middle"))

    axis_y = 178
    x0, x1 = 96, 664
    eras = [(122, "商·甲骨文"), (258, "西周·金文"), (402, "秦·小篆"), (532, "汉·隶书"), (646, "今·楷书")]
    # 时间轴
    p.append(f'<path d="M {x0} {axis_y} L {x1} {axis_y}" fill="none" stroke="{C_AXIS}" '
             f'stroke-width="{LW_STROKE}"/>')
    for x, label in eras:
        p.append(f'<path d="M {x} {axis_y - 7} L {x} {axis_y + 7}" fill="none" stroke="{C_AXIS}" '
                 f'stroke-width="{LW_STROKE}"/>')
        p.append(txt(x, axis_y + 26, label, FS_NOTE, C_AXIS, "middle"))

    # 射：全程实线
    p.append(f'<rect x="{x0}" y="132" width="{x1 - x0}" height="18" rx="9" fill="{C_OK}" '
             f'fill-opacity="0.18" stroke="{C_OK}" stroke-width="{LW_CELL}"/>')
    p.append(txt(380, 125, "射：甲骨文已见，本义始终是射箭", FS_NOTE, C_OK, "middle", "bold"))

    # 矮：前段缺位，自小篆起有
    p.append(f'<rect x="{x0}" y="212" width="{402 - x0}" height="18" rx="9" fill="none" '
             f'stroke="{C_REF}" stroke-width="{LW_CELL}" stroke-dasharray="6,5"/>')
    p.append(f'<rect x="402" y="212" width="{x1 - 402}" height="18" rx="9" fill="{C_DOWN}" '
             f'fill-opacity="0.18" stroke="{C_DOWN}" stroke-width="{LW_CELL}"/>')
    p.append(txt(268, 250, "甲骨文、金文中均不见「矮」", FS_NOTE, C_REF, "middle", "bold"))
    p.append(txt(534, 250, "最早见于小篆", FS_NOTE, C_DOWN, "middle", "bold"))

    # 分界标记
    p.append(f'<path d="M 402 100 L 402 288" fill="none" stroke="{C_UP}" stroke-width="1.4" '
             f'stroke-dasharray="4,4"/>')
    p.append(txt(402, 92, "矮字登场", FS_NOTE, C_UP, "middle", "bold"))

    p.append(txt(24, H - 16, "时间刻度未按比例；「矮」的最早形体依据字书与出土文字材料。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "two_char_timeline.svg"), "\n".join(p))


gen_she_evolution()
gen_ai_composition()
gen_two_char_timeline()
