# -*- coding: utf-8 -*-
"""
生成「唐代州县制度」一文的三张图。

输出目录：content/assets/zhou/

  zhou_county_ranks.svg   地方行政三层与州县分等（含户口标准与长官品级）
  shidao_split.svg        贞观十道到开元十五道：哪四个道被拆开
  zhonglangjiang.svg      汉代与唐代的「中郎将」并列对照

图内文字字号 ≥12px、标题 16px，配色沿用 Okabe-Ito 色盲友好方案，
满足 docs/design.md「排版与渲染规范」的要求。
"""
import os

from svgkit import (C_INK, C_AXIS, C_GRID, C_REF, C_UP, C_DOWN, C_MID, C_OK, C_BASE,
                    FS_TITLE, FS_NOTE, txt, write_svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "zhou")
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
        yy = y + h / 2 + (i - (n - 1) / 2) * 16.5 + size * 0.36
        el.append(txt(x + w / 2, yy, content, size, C_INK, "middle", "bold" if bold else None))
    return el


def arrow_h(x1, x2, y, color=C_AXIS, sw=2.0):
    return (f'<path d="M {x1:.1f} {y} L {x2 - 7:.1f} {y}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}"/>'
            f'<path d="M {x2 - 13} {y - 5} L {x2 - 6} {y} L {x2 - 13} {y + 5}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


# ============================================================
# 图一：地方三层与州县分等
# ============================================================
def gen_ranks():
    W, H = 720, 430
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "地方三层：道—府州—县，以及州县的分等", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "州按户口分等，长官的品级随之升降；县的分等更细", FS_NOTE, C_AXIS, "middle"))

    # 三层链条
    bw, by, bh = 168, 76, 56
    xs = [40, 276, 512]
    items = [
        ("道", ["监察区，开元十五道", "设采访处置使"]),
        ("府 · 州", ["州分辅雄望紧", "上中下七等"]),
        ("县", ["赤畿望紧上中", "中下下，等第最细"]),
    ]
    for (title, subs), x in zip(items, xs):
        lines = [(title, 15, True)] + [(s, FS_NOTE, False) for s in subs]
        p.extend(box(x, by, bw, bh, lines, C_UP if x < 200 else (C_DOWN if x < 440 else C_OK),
                     op=0.20))
    p.append(arrow_h(208, 276, by + bh / 2))
    p.append(arrow_h(444, 512, by + bh / 2))

    # 州的分等表
    p.extend(box(40, 168, 320, 168, [], C_DOWN, op=0.08))
    p.append(txt(56, 192, "州的三等（按户口）", 13, C_DOWN, "start", "bold"))
    rows = [
        ("上州", "户四万以上", "刺史 从三品"),
        ("中州", "户二万至四万", "刺史 正四品上"),
        ("下州", "户不足二万", "刺史 正四品下"),
    ]
    for i, (a, b, c) in enumerate(rows):
        y = 226 + i * 34
        p.append(txt(56, y, a, 12.5, C_INK, "start", "bold"))
        p.append(txt(120, y, b, FS_NOTE, C_AXIS))
        p.append(txt(244, y, c, FS_NOTE, C_INK))
    p.append(txt(56, 330, "另有辅、雄、望、紧四等，按政治地位而非户口，位于上州之前。",
                 FS_NOTE, C_AXIS))

    # 县的分等表
    p.extend(box(376, 168, 304, 168, [], C_OK, op=0.08))
    p.append(txt(392, 192, "县的两套等级", 13, C_OK, "start", "bold"))
    rows2 = [
        ("赤、畿", "京城与陪都所在及近郊"),
        ("望、紧", "按资地美恶，不限户数并为上县"),
        ("上县", "户六千以上（武德时为五千）"),
        ("中县", "户三千以上（武德时为二千）"),
    ]
    for i, (a, b) in enumerate(rows2):
        y = 224 + i * 30
        p.append(txt(392, y, a, 12.5, C_INK, "start", "bold"))
        p.append(txt(452, y, b, FS_NOTE, C_AXIS))

    p.append(txt(24, H - 64, "武德年间以三万户为上州，开元十八年（730）改以四万户为限；",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, H - 42, "缘边与岭南诸州的门槛酌情放宽。亲王出任中州、下州刺史时，",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, H - 20, "该州亦升为上州，王去任后仍旧。", FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "zhou_county_ranks.svg"), "\n".join(p))


# ============================================================
# 图二：十道到十五道
# ============================================================
def gen_shidao():
    W, H = 720, 402
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "从贞观十道到开元十五道：只有四个道被拆开", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "627 年分十道，733 年析为十五道；其余六道名号不变",
                 FS_NOTE, C_AXIS, "middle"))

    rows = [
        ("关内道", ["关内道", "京畿道"]),
        ("河南道", ["河南道", "都畿道"]),
        ("山南道", ["山南东道", "山南西道"]),
        ("江南道", ["江南东道", "江南西道", "黔中道"]),
    ]
    LX, RX = 40, 250
    for i, (parent, children) in enumerate(rows):
        y = 82 + i * 62
        p.extend(box(LX, y, 130, 44, [(parent, 13, True)], C_REF, op=0.14))
        ch = 128
        for j, c in enumerate(children):
            cx = RX + j * (ch + 14)
            p.extend(box(cx, y, ch, 44, [(c, 12.5, True)], C_UP, op=0.16))
            ax = LX + 132
            p.append(f'<path d="M {ax} {y + 22} L {cx - 4:.1f} {y + 22}" fill="none" '
                     f'stroke="{C_AXIS}" stroke-width="1.4"/>')
            p.append(f'<path d="M {cx - 11} {y + 17} L {cx - 4} {y + 22} L {cx - 11} {y + 27}" '
                     f'fill="none" stroke="{C_AXIS}" stroke-width="1.4" stroke-linecap="round" '
                     f'stroke-linejoin="round"/>')
    p.append(txt(40, 356, "名号不变的六道：河东、河北、陇右、淮南、剑南、岭南",
                 12.5, C_INK, "start", "bold"))
    p.append(txt(40, 378, "每道设采访处置使并给固定治所，「道」由此从监察区转为地方高层行政区。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "shidao_split.svg"), "\n".join(p))


# ============================================================
# 图三：汉唐中郎将对照
# ============================================================
def gen_zhonglangjiang():
    W, H = 720, 424
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "同名不同物：汉代与唐代的「中郎将」", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "左边是宫官系统的侍从武官，右边是十六卫系统的统兵官",
                 FS_NOTE, C_AXIS, "middle"))

    # 左：汉
    p.append(txt(178, 80, "汉代", 14, C_DOWN, "middle", "bold"))
    p.extend(box(48, 92, 260, 40, [("皇　帝", 12.5, True)], C_UP, op=0.18))
    p.extend(box(48, 146, 260, 40, [("光禄勋（九卿之一，掌宫殿门户）", 12, False)], C_DOWN, op=0.16))
    p.append(f'<path d="M 178 132 L 178 146" fill="none" stroke="{C_REF}" stroke-width="1.6"/>')
    p.append(txt(178, 200, "各置中郎将，分统郎官", FS_NOTE, C_AXIS, "middle"))
    for i, s in enumerate(["五官", "左", "右", "虎贲", "羽林"]):
        x = 34 + i * 56
        p.extend(box(x, 208, 50, 36, [(s, 12.0, True)], C_MID, op=0.16, rx=6, sw=1.2))
    p.append(txt(178, 264, "统郎官：三署郎、虎贲郎、羽林郎", FS_NOTE, C_AXIS, "middle"))
    p.append(txt(178, 284, "秩比二千石，低于诸将军", FS_NOTE, C_AXIS, "middle"))

    # 右：唐
    p.append(txt(542, 80, "唐代", 14, C_UP, "middle", "bold"))
    p.extend(box(412, 92, 260, 40, [("皇　帝", 12.5, True)], C_UP, op=0.18))
    p.extend(box(412, 146, 260, 40, [("十六卫（军事系统）与太子率府", 12, False)], C_DOWN, op=0.16))
    p.append(f'<path d="M 542 132 L 542 146" fill="none" stroke="{C_REF}" stroke-width="1.6"/>')
    p.append(txt(542, 200, "各置中郎将，统内府卫士", FS_NOTE, C_AXIS, "middle"))
    for i, s in enumerate(["亲府", "勋府", "翊府"]):
        x = 418 + i * 86
        p.extend(box(x, 208, 76, 36, [(s, 12.0, True)], C_OK, op=0.18, rx=6, sw=1.2))
    p.append(txt(542, 264, "统亲卫、勋卫、翊卫（内府卫士）", FS_NOTE, C_AXIS, "middle"))
    p.append(txt(542, 284, "正四品下；太子率府的为从四品上", FS_NOTE, C_AXIS, "middle"))

    p.append(f'<path d="M 360 76 L 360 {H - 70}" fill="none" stroke="{C_GRID}" stroke-width="1.4" '
             f'stroke-dasharray="5,5"/>')
    p.append(txt(24, H - 42, "汉代中郎将是「中郎」的统领，属光禄勋，性质是皇帝近侍与扈从；",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, H - 20, "唐代中郎将是武德七年由骠骑将军改称而来的统兵官，与「郎」已无关系。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "zhonglangjiang.svg"), "\n".join(p))


gen_ranks()
gen_shidao()
gen_zhonglangjiang()
