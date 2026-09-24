# -*- coding: utf-8 -*-
"""
生成「唐代行军制度」一文的三张图。

输出目录：content/assets/xingjun/

  xingjun_concept.svg    两种「道」的辨析，以及行军的四级编制
  xingjun_examples.svg   六支著名行军一览
  direnjie_titles.svg    《神探狄仁杰》剧中头衔与史书职务对照

图内文字字号 ≥12px、标题 16px，配色沿用 Okabe-Ito 色盲友好方案。
"""
import os

from svgkit import (C_INK, C_AXIS, C_GRID, C_REF, C_UP, C_DOWN, C_MID, C_OK, C_BASE,
                    FS_TITLE, FS_NOTE, txt, write_svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "xingjun")
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
        yy = y + h / 2 + (i - (n - 1) / 2) * 20 + size * 0.36
        el.append(txt(x + w / 2, yy, content, size, C_INK, "middle", "bold" if bold else None))
    return el


def arrow_h(x1, x2, y, color=C_AXIS, sw=1.8):
    return (f'<path d="M {x1:.1f} {y} L {x2 - 6:.1f} {y}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}"/>'
            f'<path d="M {x2 - 11} {y - 4.5} L {x2 - 5} {y} L {x2 - 11} {y + 4.5}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


# ============================================================
# 图一：两种「道」与四级编制
# ============================================================
def gen_concept():
    W, H = 720, 430
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "「行军」的「道」是出兵方向，不是行政区", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "唐代有两个「道」，同名而异义，读史时必须按上下文分辨",
                 FS_NOTE, C_AXIS, "middle"))

    left = [("行政的道", 13, True),
            ("河南道、河北道、江南道……", 12.0, False),
            ("有明确辖境，本质是监察区", 12.0, False),
            ("长官：采访处置使、节度使", 12.0, False)]
    right = [("行军的道", 13, True),
             ("葱山道、伊丽道、交河道……", 12.0, False),
             ("只表示这一路兵往哪个方向去", 12.0, False),
             ("长官：行军大总管", 12.0, False)]
    p.extend(box(24, 70, 324, 150, left, C_UP, op=0.14))
    p.extend(box(372, 70, 324, 150, right, C_DOWN, op=0.14))

    p.append(txt(24, 248, "「葱山」是葱岭，「伊丽」是伊犁河，「交河」是吐鲁番的城——都不是行政区。",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, 272, "所以「葱山道行军大总管」的意思是一次战役的前线统帅，打完即撤。",
                 FS_NOTE, C_AXIS))

    p.append(txt(24, 306, "行军的编制（据《通典》所引《李靖兵法》）", 12.5, C_INK, "start", "bold"))
    chain = [("大总管", "全军统帅"), ("总管", "分领一军"), ("子总管", "领一营"), ("队", "五十人为一队")]
    for i, (name, note) in enumerate(chain):
        x = 21 + i * 176
        p.extend(box(x, 318, 150, 56, [(name, 13, True), (note, 12.0, False)], C_OK, op=0.16))
        if i < 3:
            p.append(arrow_h(x + 152, x + 176, 346))

    p.append("</svg>")
    write_svg(os.path.join(OUT, "xingjun_concept.svg"), "\n".join(p))


# ============================================================
# 图二：六支著名行军
# ============================================================
def gen_examples():
    W, H = 720, 412
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "几支著名的行军", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "同一场战争可以换一个「道」再打一次——因为道只是路线，不是编制",
                 FS_NOTE, C_AXIS, "middle"))

    cols = [24, 178, 332, 486]
    widths = [146, 146, 146, 210]
    heads = ["行军道", "统帅", "时间", "目标"]
    p.append(txt(cols[0] + 8, 88, heads[0], 12.5, C_INK, "start", "bold"))
    for i, hd in enumerate(heads[1:], 1):
        p.append(txt(cols[i] + 8, 88, hd, 12.5, C_INK, "start", "bold"))
    p.append(f'<path d="M 24 98 L 696 98" stroke="{C_GRID}" stroke-width="1.4"/>')

    rows = [
        ("代州道", "李　靖", "贞观三年（629）", "东突厥颉利可汗", C_UP),
        ("交河道", "侯君集", "贞观十三年（639）", "高　昌", C_UP),
        ("辽东道", "李　勣", "贞观十九年（645）", "高　丽", C_UP),
        ("葱山道", "程知节", "永徽六年（655）", "西突厥阿史那贺鲁", C_DOWN),
        ("伊丽道", "苏定方", "显庆二年（657）", "西突厥阿史那贺鲁", C_DOWN),
        ("河北道", "李显（狄仁杰副）", "圣历元年（698）", "后突厥默啜", C_MID),
    ]
    for r, (dao, shuai, year, aim, color) in enumerate(rows):
        y = 106 + r * 46
        if r % 2 == 0:
            p.append(f'<rect x="20" y="{y}" width="680" height="42" rx="6" fill="{color}" '
                     f'fill-opacity="0.07"/>')
        p.append(txt(cols[0] + 8, y + 27, dao, 12.5, C_INK, "start", "bold"))
        p.append(txt(cols[1] + 8, y + 27, shuai, 12.0, C_INK))
        p.append(txt(cols[2] + 8, y + 27, year, 12.0, C_INK))
        p.append(txt(cols[3] + 8, y + 27, aim, 12.0, C_INK))

    p.append(txt(24, 400, "655 年程知节的葱山道行军，前军总管就是苏定方；两年后苏定方自领伊丽道，擒获贺鲁。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "xingjun_examples.svg"), "\n".join(p))


# ============================================================
# 图三：剧中与史书
# ============================================================
def gen_direnjie():
    W, H = 720, 434
    p = [svg_open(W, H)]
    p.append(txt(W / 2, 28, "狄仁杰的头衔：剧中与史书", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "左为《神探狄仁杰》剧中的叠加头衔，右为史书所记的职务",
                 FS_NOTE, C_AXIS, "middle"))

    p.extend(box(24, 68, 324, 32, [("《神探狄仁杰》剧中", 12.5, True)], C_DOWN, op=0.22, rx=6))
    play = ["同凤阁鸾台平章事（宰相）", "内　史（即中书令）", "户部侍郎",
            "幽州大都督", "洛州牧", "河北道行军大总管",
            "葱山道行军大总管", "流沙道行军大总管", "两道黜置大使、黜陟使"]
    for i, s in enumerate(play):
        p.append(txt(36, 122 + i * 24, s, 12.0, C_INK))

    p.extend(box(372, 68, 324, 32, [("史书所记", 12.5, True)], C_UP, op=0.22, rx=6))
    real = [("神功元年（697）幽州都督", "备御契丹"),
            ("圣历元年（698）", "河北道行军副元帅"),
            ("　（太子李显为元帅，狄仁杰代行）", ""),
            ("同凤阁鸾台平章事、内史", "武则天时确任此职"),
            ("黜陟使", "武则天时确有此类差遣")]
    yy = 122
    for k, v in real:
        p.append(txt(384, yy, k, 12.0, C_INK))
        if v:
            p.append(txt(384, yy + 18, v, 12.0, C_AXIS))
            yy += 42
        else:
            yy += 24

    p.append(f'<path d="M 360 68 L 360 {H - 76}" fill="none" stroke="{C_GRID}" stroke-width="1.4" '
             f'stroke-dasharray="5,5"/>')
    p.append(txt(24, H - 54, "剧中诏书原话：「加葱山道行军大总管、流沙道行军大总管，并两道黜置大使，",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, H - 32, "统领安西、北庭、崑陵、濛池四都护府……遇不决之事，不必请奏。」",
                 FS_NOTE, C_AXIS))
    p.append(txt(24, H - 12, "「某某道行军大总管」正是唐代真实的名号格式。", FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "direnjie_titles.svg"), "\n".join(p))


gen_concept()
gen_examples()
gen_direnjie()
