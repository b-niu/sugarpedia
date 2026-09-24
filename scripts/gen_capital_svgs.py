# -*- coding: utf-8 -*-
"""
生成「长安与洛阳的棋盘格」一文的三张平面示意图。

输出目录：content/assets/capital/

  changan_plan.svg   唐长安城：三重城垣、朱雀大街、东西两市与坊的棋盘
  luoyang_plan.svg   隋唐洛阳城：洛水横贯、宫城在西北、三市
  heian_plan.svg     平安京：左京「洛阳」、右京「长安」，以及它与长安的差异

三张图均为**示意图**：按文献与考古的布局关系绘制，坊的数目作了简化，
未逐坊标名，也不代表精确比例；数据说明放在图内脚注。

图内文字字号 ≥12px、标题 16px，配色沿用 Okabe-Ito 色盲友好方案，
满足 docs/design.md「排版与渲染规范」的要求。
"""
import os

from svgkit import (C_INK, C_AXIS, C_GRID, C_REF, C_UP, C_DOWN, C_MID, C_BASE,
                    FS_TITLE, FS_NOTE, txt, write_svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "capital")
os.makedirs(OUT, exist_ok=True)

FS_L = 12.0          # 图内标注


def svg_open(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif">'
            f'<rect width="{w}" height="{h}" fill="white"/>')


def rect(x, y, w, h, fill="white", stroke=C_REF, sw=1.2, rx=0, op=1.0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')


def line(x1, y1, x2, y2, stroke=C_REF, sw=1.0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" fill="none" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


def legend(x, y, items, gap=150):
    """图例：每组 (颜色, 说明)"""
    out = []
    cx = x
    for color, label in items:
        out.append(rect(cx, y - 11, 20, 12, fill=color, stroke=color, sw=1.0, rx=2, op=0.35))
        out.append(txt(cx + 26, y, label, FS_NOTE, C_AXIS))
        cx += gap
    return out


# ============================================================
# 图一：唐长安城
# ============================================================
def gen_changan():
    W, H = 720, 596
    GX0, GY0, GX1, GY1 = 74, 84, 646, 508     # 郭城
    HX0, HX1 = 292, 428                        # 宫城 / 皇城 横向范围
    GONG_Y1, HUANG_Y1 = 152, 204               # 宫城底、皇城底
    AX0, AX1 = 352, 368                        # 朱雀大街
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "唐长安城：三重城垣与坊的棋盘", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "面积约 84 平方公里，外郭城内有 108 坊，另加东西两市", FS_NOTE, C_AXIS, "middle"))

    # 郭城
    p.append(rect(GX0, GY0, GX1 - GX0, GY1 - GY0, "white", C_AXIS, 2.0))

    # 坊：南部（皇城以南）与两侧（宫城皇城东西）
    CW, CH = 39.4, 38.0
    for r in range(8):
        for c in range(7):
            for side, bx in ((0, GX0), (1, AX1)):
                p.append(rect(bx + c * CW, HUANG_Y1 + r * CH, CW, CH, "white", C_GRID, 1.0))
    for r in range(2):
        for c in range(5):
            p.append(rect(GX0 + c * 42.0, GY0 + r * 34.0, 42.0, 34.0, "white", C_GRID, 1.0))
            p.append(rect(HX1 + c * 42.0, GY0 + r * 34.0, 42.0, 34.0, "white", C_GRID, 1.0))

    # 宫城、皇城
    p.append(rect(HX0, GY0, HX1 - HX0, GONG_Y1 - GY0, C_UP, C_UP, 1.4, op=0.22))
    p.append(rect(HX0, GONG_Y1, HX1 - HX0, HUANG_Y1 - GONG_Y1, C_DOWN, C_DOWN, 1.4, op=0.22))
    p.append(txt((HX0 + HX1) / 2, GY0 + 42, "宫城", FS_L + 0.5, C_UP, "middle", "bold"))
    p.append(txt((HX0 + HX1) / 2, GONG_Y1 + 34, "皇城", FS_L + 0.5, C_DOWN, "middle", "bold"))

    # 朱雀大街（中轴）
    p.append(rect(AX0, HUANG_Y1, AX1 - AX0, GY1 - HUANG_Y1, C_BASE, C_BASE, 1.0, op=0.30))
    p.append(txt(AX1 + 8, GY1 - 18, "朱雀大街（天街）", FS_L, C_INK, "start", "bold"))

    # 东西两市（各占两坊）
    p.append(rect(GX0 + 5 * CW, HUANG_Y1 + 5 * CH, CW * 2, CH * 2, C_MID, C_MID, 1.4, op=0.32))
    p.append(rect(AX1 + 2 * CW, HUANG_Y1 + 5 * CH, CW * 2, CH * 2, C_MID, C_MID, 1.4, op=0.32))
    p.append(txt(GX0 + 6 * CW, HUANG_Y1 + 6 * CH + 4, "西市", FS_L, C_INK, "middle", "bold"))
    p.append(txt(AX1 + 3 * CW, HUANG_Y1 + 6 * CH + 4, "东市", FS_L, C_INK, "middle", "bold"))

    # 门
    p.append(txt((HX0 + HX1) / 2, GY0 - 8, "承天门（宫城正门）", FS_L, C_AXIS, "middle"))
    p.append(txt(AX0 - 6, HUANG_Y1 - 6, "朱雀门", FS_L, C_AXIS, "end"))
    p.append(txt((AX0 + AX1) / 2, GY1 + 18, "明德门（外郭城正南门）", FS_L, C_AXIS, "middle"))

    p.extend(legend(74, H - 46, [
        (C_UP, "宫城"), (C_DOWN, "皇城"), (C_MID, "东市、西市"), (C_GRID, "坊（示意，未逐坊标名）"),
    ], gap=142))
    p.append(txt(74, H - 18, "外郭城东西约 9721 米、南北约 8650 米；朱雀大街文献记「广百步」，折合今约 150 米。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "changan_plan.svg"), "\n".join(p))


# ============================================================
# 图二：隋唐洛阳城
# ============================================================
def gen_luoyang():
    W, H = 720, 560
    GX0, GY0, GX1, GY1 = 84, 84, 616, 468
    HX0, HX1 = 84, 250                       # 宫城在西北
    GONG_Y1, HUANG_Y1 = 176, 232
    RIVER_Y0, RIVER_Y1 = 232, 262            # 洛水横贯
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "隋唐洛阳城：洛水横贯，宫城在西北", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "面积约 47 平方公里，郭城内分坊，商肆集中在北、南、西三市", FS_NOTE, C_AXIS, "middle"))

    p.append(rect(GX0, GY0, GX1 - GX0, GY1 - GY0, "white", C_AXIS, 2.0))

    # 坊：洛北（宫城以东）与洛南
    for r in range(2):
        for c in range(9):
            p.append(rect(HX1 + 8 + c * 40.0, GY0 + 6 + r * 38.0, 40.0, 38.0, "white", C_GRID, 1.0))
    for r in range(5):
        for c in range(13):
            p.append(rect(GX0 + 6 + c * 41.0, RIVER_Y1 + 8 + r * 34.0, 41.0, 34.0, "white", C_GRID, 1.0))

    # 宫城 / 皇城（西北）
    p.append(rect(HX0, GY0, HX1 - HX0, GONG_Y1 - GY0, C_UP, C_UP, 1.4, op=0.22))
    p.append(rect(HX0, GONG_Y1, HX1 - HX0, HUANG_Y1 - GONG_Y1, C_DOWN, C_DOWN, 1.4, op=0.22))
    p.append(txt((HX0 + HX1) / 2, GY0 + 46, "宫城", FS_L + 0.5, C_UP, "middle", "bold"))
    p.append(txt((HX0 + HX1) / 2, GY0 + 66, "（紫微城）", FS_NOTE, C_UP, "middle"))
    p.append(txt((HX0 + HX1) / 2, GONG_Y1 + 34, "皇城·太微城", FS_NOTE, C_DOWN, "middle"))

    # 洛水
    p.append(rect(GX0, RIVER_Y0, GX1 - GX0, RIVER_Y1 - RIVER_Y0, C_MID, C_MID, 1.0, op=0.30))
    p.append(txt(GX1 - 10, RIVER_Y0 + 20, "洛水", FS_L + 0.5, C_INK, "end", "bold"))

    # 三市
    p.append(rect(HX1 + 8 + 4 * 40.0, GY0 + 6, 40.0, 38.0, C_MID, C_MID, 1.4, op=0.32))
    p.append(txt(HX1 + 8 + 4 * 40.0 + 20, GY0 + 30, "北市", FS_NOTE, C_INK, "middle", "bold"))
    p.append(rect(GX0 + 6 + 6 * 41.0, RIVER_Y1 + 8 + 2 * 34.0, 82.0, 34.0, C_MID, C_MID, 1.4, op=0.32))
    p.append(txt(GX0 + 6 + 7 * 41.0, RIVER_Y1 + 8 + 2 * 34.0 + 23, "南市", FS_NOTE, C_INK, "middle", "bold"))
    p.append(rect(GX0 + 6 + 1 * 41.0, RIVER_Y1 + 8 + 3 * 34.0, 41.0, 34.0, C_MID, C_MID, 1.4, op=0.32))
    p.append(txt(GX0 + 6 + 1 * 41.0 + 20, RIVER_Y1 + 8 + 3 * 34.0 + 23, "西市", FS_NOTE, C_INK, "middle", "bold"))

    # 中轴：定鼎门 → 天街 → 应天门
    p.append(line(240, GY1, 240, RIVER_Y0, C_BASE, 2.0, "6,4"))
    p.append(txt(240, GY1 + 18, "定鼎门（外郭城正南门）", FS_L, C_AXIS, "middle"))
    p.append(txt(258, GY1 - 40, "定鼎门大街", FS_L, C_INK, "start", "bold"))
    p.append(txt(258, GY1 - 22, "（天街）", FS_NOTE, C_AXIS, "start"))
    p.append(txt(HX0 + 20, HUANG_Y1 + 16, "应天门", FS_L, C_UP, "start", "bold"))
    p.append(txt(GX0 + 10, GY0 + 22, "玄武门·西苑", FS_NOTE, C_AXIS))

    p.extend(legend(84, H - 46, [
        (C_UP, "宫城"), (C_DOWN, "皇城"), (C_MID, "洛水与三市"), (C_GRID, "坊（示意）"),
    ], gap=158))
    p.append(txt(84, H - 18, "宫城占全城约六分之一；城垣以夯土筑成，图未按比例，坊数亦作简化。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "luoyang_plan.svg"), "\n".join(p))


# ============================================================
# 图三：平安京
# ============================================================
def gen_heian():
    W, H = 720, 560
    GX0, GY0, GX1, GY1 = 120, 84, 600, 456
    AX0, AX1 = 356, 364                       # 朱雀大路
    KY0, KY1 = GY0, 148                       # 平安宫
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "平安京：左京称「洛阳」，右京称「长安」", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "794 年迁都，仿唐长安与洛阳的条坊制，规模约为长安的四分之一",
                 FS_NOTE, C_AXIS, "middle"))

    p.append(rect(GX0, GY0, GX1 - GX0, GY1 - GY0, "white", C_AXIS, 2.0))
    # 左右京底色
    p.append(rect(GX0, GY0, AX0 - GX0, GY1 - GY0, C_UP, C_UP, 1.0, op=0.10))
    p.append(rect(AX1, GY0, GX1 - AX1, GY1 - GY0, C_DOWN, C_DOWN, 1.0, op=0.10))

    # 条坊格
    CW, CH = 39.2, 32.0
    for r in range(9):
        for c in range(6):
            p.append(rect(GX0 + c * CW, KY1 + r * CH, CW, CH, "white", C_GRID, 1.0))
            p.append(rect(AX1 + c * CW, KY1 + r * CH, CW, CH, "white", C_GRID, 1.0))

    # 平安宫
    p.append(rect(236, KY0, 248, KY1 - KY0, C_UP, C_UP, 1.6, op=0.28))
    p.append(txt(360, KY0 + 38, "平安宫", FS_L + 1, C_UP, "middle", "bold"))

    # 朱雀大路
    p.append(rect(AX0, KY1, AX1 - AX0, GY1 - KY1, C_BASE, C_BASE, 1.0, op=0.35))
    p.append(txt(AX0 - 10, GY1 - 96, "左京", FS_L + 4, C_UP, "end", "bold"))
    p.append(txt(AX0 - 10, GY1 - 74, "洛阳", FS_L + 1, C_UP, "end"))
    p.append(txt(AX1 + 10, GY1 - 96, "右京", FS_L + 4, C_DOWN, "start", "bold"))
    p.append(txt(AX1 + 10, GY1 - 74, "长安", FS_L + 1, C_DOWN, "start"))

    # 东市、西市、东寺、西寺
    p.append(rect(GX0 + 2 * CW, KY1 + 2 * CH, CW * 2, CH * 2, C_MID, C_MID, 1.4, op=0.32))
    p.append(rect(AX1 + 2 * CW, KY1 + 2 * CH, CW * 2, CH * 2, C_MID, C_MID, 1.4, op=0.32))
    p.append(txt(GX0 + 3 * CW, KY1 + 3 * CH + 4, "西市", FS_NOTE, C_INK, "middle", "bold"))
    p.append(txt(AX1 + 3 * CW, KY1 + 3 * CH + 4, "东市", FS_NOTE, C_INK, "middle", "bold"))
    p.append(rect(GX0 + 2 * CW, GY1 - 2 * CH - 8, CW * 2, CH * 2, C_REF, C_REF, 1.4, op=0.30))
    p.append(rect(AX1 + 2 * CW, GY1 - 2 * CH - 8, CW * 2, CH * 2, C_REF, C_REF, 1.4, op=0.30))
    p.append(txt(GX0 + 3 * CW, GY1 - CH - 4, "西寺", FS_NOTE, C_AXIS, "middle", "bold"))
    p.append(txt(AX1 + 3 * CW, GY1 - CH - 4, "东寺", FS_NOTE, C_AXIS, "middle", "bold"))

    p.append(txt(360, GY1 + 20, "罗城门（朱雀大路南端）", FS_L, C_AXIS, "middle"))
    p.append(txt(636, GY1 - 8, "右京地势低湿，", FS_NOTE, C_DOWN, "end"))
    p.append(txt(636, GY1 + 8, "半个世纪即荒废", FS_NOTE, C_DOWN, "end"))

    p.extend(legend(120, H - 46, [
        (C_UP, "平安宫与左京"), (C_DOWN, "右京"), (C_MID, "东市、西市"), (C_REF, "东寺、西寺"),
    ], gap=150))
    p.append(txt(120, H - 18, "平安京没有构筑高大的城墙，这是它与长安、洛阳最明显的不同。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "heian_plan.svg"), "\n".join(p))


gen_changan()
gen_luoyang()
gen_heian()
