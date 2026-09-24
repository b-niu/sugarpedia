# -*- coding: utf-8 -*-
"""
生成《改名狂魔武则天》一文的两张统计图。

输出目录：content/assets/rename/

  nianhao_compare.svg  年号数量的横向对比：从"一生一个"到"一年多一个"
  zunhao_length.svg    尊号字数的膨胀：从 2 字到 16 字

计数口径（图中已注明）：
  年号按史书所载实际使用的年号个数计；
  尊号按尊号全文计字（含末尾"皇帝"二字）。若不计"皇帝"，玄宗那个为十四字，
  史书常引作"十四字"，两种算法都对，文中会一并说明。

图内文字字号 ≥12px、标题 16px，配色沿用 Okabe-Ito 色盲友好方案，
满足 docs/design.md「排版与渲染规范」的要求。
"""
import os

from svgkit import (C_INK, C_AXIS, C_GRID, C_REF, C_UP, C_DOWN,
                    FS_TITLE, FS_NOTE, txt, write_svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "rename")
os.makedirs(OUT, exist_ok=True)


# ============================================================
# 图一：年号数量对比
# ============================================================
def gen_nianhao():
    # (人物, 在位年数, 年号个数, 是否高亮)
    rows = [
        ("唐高祖", 9, 1, False),
        ("唐太宗", 23, 1, False),
        ("唐玄宗", 44, 3, False),
        ("唐高宗", 34, 14, True),
        ("武则天", 21, 17, True),
    ]
    W = 720
    TOP, RH = 92, 36
    H = TOP + RH * len(rows) + 62
    LABEL_X, BAR_X0 = 16, 186
    PX_PER = 20.0          # 每个年号占 20px
    MAXN = 18

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif">'
         f'<rect width="{W}" height="{H}" fill="white"/>']
    p.append(txt(W / 2, 28, "年号数量对比：从一生一个，到一年多一个", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "横轴为年号个数；括号内为在位年数", FS_NOTE, C_AXIS, "middle"))

    # 刻度
    for n in (0, 5, 10, 15):
        gx = BAR_X0 + n * PX_PER
        p.append(f'<path d="M {gx} {TOP - 16} L {gx} {TOP + RH * len(rows) - 8}" fill="none" '
                 f'stroke="{C_GRID}" stroke-width="1"/>')
        p.append(txt(gx, TOP + RH * len(rows) + 12, str(n), FS_NOTE, C_AXIS, "middle"))

    for i, (name, years, cnt, hot) in enumerate(rows):
        y = TOP + i * RH
        color = C_UP if hot else C_DOWN
        p.append(txt(LABEL_X, y + 18, f"{name}（在位 {years} 年）", 12.5, C_INK, "start", "bold"))
        bw = max(cnt * PX_PER, 6)
        p.append(f'<rect x="{BAR_X0}" y="{y + 6}" width="{bw:.1f}" height="18" rx="9" '
                 f'fill="{color}" fill-opacity="0.30" stroke="{color}" stroke-width="1.4"/>')
        p.append(txt(BAR_X0 + bw + 12, y + 20, f"{cnt} 个", 12.5, color, "start", "bold"))

    p.append(txt(16, H - 34, "唐代（含武周）共 290 年、二十帝，年号合计 75 个；其中高宗的 14 个与", FS_NOTE, C_AXIS))
    p.append(txt(16, H - 14, "武则天的 17 个占了四成以上。武则天的 17 个含她临朝称制期间的四个年号。", FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "nianhao_compare.svg"), "\n".join(p))


# ============================================================
# 图二：尊号字数的膨胀
# ============================================================
def gen_zunhao():
    rows = [
        ("674", "唐高宗", "天皇"),
        ("688", "武则天", "圣母神皇"),
        ("690", "武则天", "圣神皇帝"),
        ("693", "武则天", "金轮圣神皇帝"),
        ("694", "武则天", "越古金轮圣神皇帝"),
        ("695", "武则天", "慈氏越古金轮圣神皇帝"),
        ("695", "武则天", "天册金轮大圣皇帝"),
        ("712", "唐玄宗", "开元神武皇帝"),
        ("739", "唐玄宗", "开元圣文神武皇帝"),
        ("753", "唐玄宗", "开元天地大宝圣文神武孝德证道皇帝"),
    ]
    W = 720
    TOP, RH = 92, 30
    H = TOP + RH * len(rows) + 64
    COL_YEAR, COL_WHO, COL_TEXT = 16, 62, 132
    BAR_X0 = 452
    PX_PER = 13.5          # 每个字 13.5px；16 字 → 216px

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif">'
         f'<rect width="{W}" height="{H}" fill="white"/>']
    p.append(txt(W / 2, 28, "尊号的字数膨胀：从 2 字到 16 字", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "右侧方块一格一字；尊号全文计字，含末尾「皇帝」二字", FS_NOTE, C_AXIS, "middle"))

    for n in range(0, 17, 4):
        gx = BAR_X0 + n * PX_PER
        p.append(f'<path d="M {gx} {TOP - 14} L {gx} {TOP + RH * len(rows) - 6}" fill="none" '
                 f'stroke="{C_GRID}" stroke-width="1"/>')
        p.append(txt(gx, TOP + RH * len(rows) + 14, f"{n} 字", FS_NOTE, C_AXIS, "middle"))

    for i, (yr, who, title) in enumerate(rows):
        y = TOP + i * RH
        n = len(title)
        hot = n >= 10
        color = C_UP if hot else C_DOWN
        p.append(txt(COL_YEAR, y + 17, yr, FS_NOTE, C_AXIS))
        p.append(txt(COL_WHO, y + 17, who, FS_NOTE, C_INK))
        p.append(txt(COL_TEXT, y + 17, title, 12.0, color, "start", "bold"))
        for k in range(n):
            fill = color
            p.append(f'<rect x="{BAR_X0 + k * PX_PER + 1:.1f}" y="{y + 5}" width="11.5" height="14" '
                     f'rx="2" fill="{fill}" fill-opacity="0.32" stroke="{fill}" stroke-width="1"/>')

    p.append(txt(16, H - 34, "695 年还发生过一次减字：武则天去掉「慈氏越古」，改为「天册金轮大圣皇帝」。", FS_NOTE, C_AXIS))
    p.append(txt(16, H - 14, "若不计末尾「皇帝」二字，玄宗那个为 14 字，史书常引作「十四字」。", FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "zunhao_length.svg"), "\n".join(p))


gen_nianhao()
gen_zunhao()
