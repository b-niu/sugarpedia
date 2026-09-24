# -*- coding: utf-8 -*-
"""
生成「唐代官制」一文的两张时间线图。

输出目录：content/assets/tang/

  xiangming_timeline.svg  宰相名号与机构改名的事件线（618—767）
  poets_timeline.svg      常见诗人与文学家的在世年代与最高官职（659—852）

两张图的横轴均按事件／年代排列：
  - 图一为事件序（年代跨度前密后疏，按比例会挤成一团），刻度不按比例；
  - 图二为公元纪年，按比例映射。

图内文字字号 ≥12px、标题 16px，配色沿用 Okabe-Ito 色盲友好方案，
满足 docs/design.md「排版与渲染规范」的要求。
"""
import os

from svgkit import (C_INK, C_AXIS, C_GRID, C_REF, C_UP, C_DOWN, C_MID,
                    FS_TITLE, FS_NOTE, txt, write_svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "tang")
os.makedirs(OUT, exist_ok=True)

FS_BOX = 12.0


# ============================================================
# 图一：宰相名号与机构改名
# ============================================================
def gen_xiangming():
    W, H = 720, 360
    events = [
        ("618 · 唐初", ["三省长官", "即是宰相"], False),
        ("643 · 贞观十七", ["同中书门下", "三品始见"], False),
        ("662 · 龙朔二年", ["改称东台西台", "侍中称左相"], False),
        ("670 · 咸亨元年", ["恢复旧名"], False),
        ("682 · 永淳元年", ["同中书门下", "平章事始授"], False),
        ("684 · 光宅元年", ["中书省改凤阁", "门下省改鸾台"], True),
        ("705 · 神龙元年", ["恢复旧名"], False),
        ("757 · 至德二载", ["同三品最后", "一次授任"], False),
        ("767 · 大历二年", ["侍中与中书令", "升为正二品"], False),
    ]
    AXIS_Y = 200
    BOX_W, BOX_H = 136, 76
    X0, STEP = 78, 70.0
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif">'
         f'<rect width="{W}" height="{H}" fill="white"/>']
    p.append(txt(W / 2, 28, "宰相名号与机构改名：618—767", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "同一批职位，名号改了三轮；玄宗以后，宰相头衔渐渐固定在「同平章事」上",
                 FS_NOTE, C_AXIS, "middle"))

    p.append(f'<path d="M 40 {AXIS_Y} L 680 {AXIS_Y}" fill="none" stroke="{C_AXIS}" '
             f'stroke-width="2" stroke-linecap="round"/>')

    for i, (head, lines, hot) in enumerate(events):
        x = X0 + i * STEP
        above = (i % 2 == 0)
        color = C_UP if hot else C_DOWN
        if above:
            by = AXIS_Y - 48 - BOX_H
            link = f'<path d="M {x} {by + BOX_H} L {x} {AXIS_Y - 7}" fill="none" stroke="{color}" stroke-width="1.4"/>'
        else:
            by = AXIS_Y + 48
            link = f'<path d="M {x} {AXIS_Y + 7} L {x} {by}" fill="none" stroke="{color}" stroke-width="1.4"/>'
        p.append(f'<path d="M {x} {AXIS_Y - 7} L {x} {AXIS_Y + 7}" fill="none" stroke="{C_AXIS}" '
                 f'stroke-width="2"/>')
        if hot:
            p.append(f'<circle cx="{x}" cy="{AXIS_Y}" r="4.5" fill="{C_UP}"/>')
        p.append(link)
        p.append(f'<rect x="{x - BOX_W / 2}" y="{by}" width="{BOX_W}" height="{BOX_H}" rx="8" '
                 f'fill="white" stroke="{color}" stroke-width="1.4"/>')
        p.append(txt(x, by + 22, head, FS_BOX, color, "middle", "bold"))
        for k, ln in enumerate(lines):
            p.append(txt(x, by + 42 + k * 18, ln, FS_BOX, C_INK, "middle"))

    p.append(txt(24, H - 10, "横轴按事件先后排列，刻度不按年代比例；红框为机构改名事件。",
                 FS_NOTE, C_AXIS))
    p.append("</svg>")
    write_svg(os.path.join(OUT, "xiangming_timeline.svg"), "\n".join(p))


def C_BASE_OR_DOWN(hot):
    """普通事件用蓝色，改名等关键事件用朱红（在 gen_xiangming 内使用）"""
    return C_UP if hot else C_DOWN


# ============================================================
# 图二：诗人与文学家的在世年代与最高官职
# ============================================================
def gen_poets():
    # (姓名, 生年, 卒年, 最高官职, 等第标签)
    rows = [
        ("贺知章", 659, 744, "秘书监、太子宾客（正三品）", 2),
        ("陈子昂", 661, 702, "右拾遗（从八品上）", 4),
        ("张说", 667, 730, "中书令（宰相），封燕国公", 1),
        ("张九龄", 678, 740, "尚书右丞相（从二品）", 1),
        ("王维", 701, 761, "尚书右丞（正四品下）", 3),
        ("李白", 701, 762, "翰林供奉（无品秩）", 4),
        ("高适", 704, 765, "左散骑常侍（正三品）", 2),
        ("杜甫", 712, 770, "检校工部员外郎（从六品上）", 4),
        ("岑参", 715, 770, "嘉州刺史", 3),
        ("韩愈", 768, 824, "京兆尹（从三品）", 2),
        ("白居易", 772, 846, "太子少傅（正二品）", 1),
        ("刘禹锡", 772, 842, "太子宾客（正三品）", 2),
        ("李绅", 772, 846, "尚书右仆射（从二品）", 1),
        ("柳宗元", 773, 819, "柳州刺史", 3),
        ("元稹", 779, 831, "同中书门下平章事（宰相）", 1),
        ("杜牧", 803, 852, "中书舍人（正五品上）", 3),
    ]
    TIER_COLOR = {1: C_UP, 2: C_DOWN, 3: C_MID, 4: C_REF}
    TIER_NAME = {1: "二品以上或宰相", 2: "三品", 3: "四至六品", 4: "七品以下、无品秩或未仕"}

    W = 720
    TOP, RH = 84, 24
    H = TOP + RH * len(rows) + 46
    NAME_X, BAR_X0, BAR_X1, LABEL_X = 16, 112, 452, 462
    Y0, Y1 = 655, 870

    def px(year):
        return BAR_X0 + (year - Y0) * (BAR_X1 - BAR_X0) / (Y1 - Y0)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif">'
         f'<rect width="{W}" height="{H}" fill="white"/>']
    p.append(txt(W / 2, 28, "常见诗人与文学家的在世年代与最高官职", FS_TITLE, C_INK, "middle", "bold"))
    p.append(txt(W / 2, 50, "色块为生卒区间；右侧为史书所载最高官职，颜色按等第分组",
                 FS_NOTE, C_AXIS, "middle"))

    # 年代网格（画在色块之下）
    for yr in (660, 700, 740, 780, 820, 860):
        gx = px(yr)
        p.append(f'<path d="M {gx} {TOP - 20} L {gx} {TOP + RH * len(rows) + 4}" fill="none" '
                 f'stroke="{C_GRID}" stroke-width="1"/>')
        p.append(txt(gx, TOP + RH * len(rows) + 22, str(yr), FS_NOTE, C_AXIS, "middle"))

    for i, (name, by_, dy, office, tier) in enumerate(rows):
        yc = TOP + i * RH + RH / 2
        color = TIER_COLOR[tier]
        p.append(txt(NAME_X, yc + 4.5, name, 12.5, C_INK, "start", "bold"))
        xa, xb = px(by_), px(dy)
        p.append(f'<rect x="{xa:.1f}" y="{yc - 7:.1f}" width="{max(xb - xa, 6):.1f}" height="14" '
                 f'rx="7" fill="{color}" fill-opacity="0.30" stroke="{color}" stroke-width="1.4"/>')
        p.append(txt(LABEL_X, yc + 4.5, office, FS_NOTE, color))

    # 图例
    lx, ly = 16, H - 12
    for tier in (1, 2, 3, 4):
        p.append(f'<rect x="{lx}" y="{ly - 10}" width="22" height="11" rx="5.5" '
                 f'fill="{TIER_COLOR[tier]}" fill-opacity="0.30" stroke="{TIER_COLOR[tier]}" '
                 f'stroke-width="1.2"/>')
        p.append(txt(lx + 28, ly, TIER_NAME[tier], FS_NOTE, C_AXIS))
        lx += 28 + int(len(TIER_NAME[tier]) * 12.4) + 22
    p.append("</svg>")
    write_svg(os.path.join(OUT, "poets_timeline.svg"), "\n".join(p))


gen_xiangming()
gen_poets()
