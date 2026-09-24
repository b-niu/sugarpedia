# -*- coding: utf-8 -*-
"""
生成「扫描件暗纹与水印的提取」一文的曲线演示图。

输出目录：content/assets/scan/
三张图分工：
  pattern_clip.svg  反例：提高亮度或对比度会把暗纹与纸白一起推到 255 截断
  gamma_ladder.svg  正解：压暗型伽马端点固定，能放大高光反差，代价是压深暗部
  white_point.svg   收尾：白场重定标消除灰雾，以及白场点过头会重新截断

坐标一律使用八位代码值（0～255）的真实尺度，并放大到高光区间，便于看清几级灰阶的差别。
图内文字字号 ≥12px、标题 16px，曲线线宽 3px，配色为 Okabe-Ito 色盲友好方案，
满足 docs/design.md「排版与渲染规范」的要求。
"""
import os

from svgkit import (FONT, C_INK, C_AXIS, C_GRID, C_REF, C_BASE, C_UP, C_DOWN, C_MID, C_OK,
                    FS_TITLE, FS_BODY, FS_TICK, FS_NOTE,
                    clip255, text_width, txt, write_svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "scan")
os.makedirs(OUT, exist_ok=True)

# ---------------- 画布与版心 ----------------
W, H = 720, 460
M_L, M_R, M_T, M_B = 78, 34, 56, 112
PW, PH = W - M_L - M_R, H - M_T - M_B
AXIS_TITLE_Y = H - 62
FOOT_BOTTOM = H - 14
FOOT_LEAD = 18
LW_CURVE = 3.0
LW_AXIS = 1.6
LEG_LH = 20
LEG_PAD = 10


def make_axis(x_range, y_range):
    x0, x1 = x_range
    y0, y1 = y_range

    def X(v):
        return M_L + (v - x0) / (x1 - x0) * PW

    def Y(v):
        return M_T + (y1 - v) / (y1 - y0) * PH

    return X, Y


def curve_path(fn, x_range, y_range, X, Y, n=240):
    x0, x1 = x_range
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = min(max(clip255(fn(x)), y_range[0]), y_range[1])
        pts.append(f"{X(x):.2f},{Y(y):.2f}")
    return "M" + " L".join(pts)


def legend_box(labels, curves, x_range, y_range, X, Y):
    """四角择优选位：取与曲线相交采样点最少的一角，同分优先右下"""
    w = max(text_width(lb, FS_BODY) for lb in labels) + 58
    h = len(curves) * LEG_LH + LEG_PAD + 12
    cands = {
        "br": (M_L + PW - w - 14, M_T + PH - h - 14),
        "tr": (M_L + PW - w - 14, M_T + 14),
        "tl": (M_L + 14, M_T + 14),
        "bl": (M_L + 14, M_T + PH - h - 14),
    }
    samples = []
    for _label, fn, _c, _d in curves:
        x0, x1 = x_range
        pts = []
        for i in range(201):
            x = x0 + (x1 - x0) * i / 200
            y = min(max(clip255(fn(x)), y_range[0]), y_range[1])
            pts.append((X(x), Y(y)))
        samples.append(pts)
    best, best_hits = None, None
    for key in ("br", "tr", "tl", "bl"):
        bx, by = cands[key]
        hits = sum(1 for pts in samples for (px, py) in pts
                   if bx <= px <= bx + w and by <= py <= by + h)
        if best_hits is None or hits < best_hits:
            best, best_hits = (bx, by, w, h), hits
    return best, best_hits


def make_figure(fname, title, curves, x_range, y_range, x_ticks, y_ticks,
                vlines, x_pattern, x_paper, footnote, x_dark=None):
    X, Y = make_axis(x_range, y_range)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="{FONT}">',
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
         txt(W / 2, M_T - 24, title, FS_TITLE, C_INK, anchor="middle", weight="bold")]

    # 网格与刻度
    for t in x_ticks:
        gx = X(t)
        p.append(f'<line x1="{gx:.1f}" y1="{M_T:.1f}" x2="{gx:.1f}" y2="{M_T + PH:.1f}" '
                 f'stroke="{C_GRID}" stroke-width="1"/>')
        p.append(txt(gx, M_T + PH + 22, t, FS_TICK, C_AXIS, anchor="middle"))
    for t in y_ticks:
        gy = Y(t)
        p.append(f'<line x1="{M_L:.1f}" y1="{gy:.1f}" x2="{M_L + PW:.1f}" y2="{gy:.1f}" '
                 f'stroke="{C_GRID}" stroke-width="1"/>')
        p.append(txt(M_L - 11, gy + 4.3, t, FS_TICK, C_AXIS, anchor="end"))

    # 边框：用 4 条边线而非 rect，让 scripts/audit_svgs.py 能据粗线识别出绘图区
    for (ax, ay, bx, by) in ((M_L, M_T, M_L + PW, M_T),
                             (M_L, M_T + PH, M_L + PW, M_T + PH),
                             (M_L, M_T, M_L, M_T + PH),
                             (M_L + PW, M_T, M_L + PW, M_T + PH)):
        p.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" '
                 f'stroke="{C_AXIS}" stroke-width="{LW_AXIS}"/>')

    # 轴标题
    p.append(txt(M_L + PW / 2, AXIS_TITLE_Y, "输入代码值", FS_BODY, C_AXIS, anchor="middle"))
    cy = M_T + PH / 2
    p.append(txt(28, cy, "输出代码值", FS_BODY, C_AXIS, anchor="middle",
                 transform=f"rotate(-90 28 {cy:.1f})"))

    # 样本输入竖线（暗纹 / 纸白）
    for vx, vlabel, side in vlines:
        gx = X(vx)
        p.append(f'<line x1="{gx:.1f}" y1="{M_T:.1f}" x2="{gx:.1f}" y2="{M_T + PH:.1f}" '
                 f'stroke="{C_REF}" stroke-width="1.3" stroke-dasharray="5,4"/>')
        tx = gx - 6 if side == "end" else gx + 6
        p.append(txt(tx, M_T + 19, vlabel, FS_TICK, C_AXIS, anchor=side))

    # 曲线 + 两个样本点
    for _label, fn, color, dash in curves:
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        p.append(f'<path d="{curve_path(fn, x_range, y_range, X, Y)}" fill="none" '
                 f'stroke="{color}" stroke-width="{LW_CURVE}" stroke-linecap="round" '
                 f'stroke-linejoin="round"{dash_attr}/>')
        for vx in (x_pattern, x_paper):
            vy = min(max(clip255(fn(vx)), y_range[0]), y_range[1])
            p.append(f'<circle cx="{X(vx):.1f}" cy="{Y(vy):.1f}" r="4.2" fill="#FFFFFF" '
                     f'stroke="{color}" stroke-width="2.4"/>')

    # 图例（Δ 与暗部代价均由函数实算，保证图与文一致）
    labels = []
    for label, fn, _c, _d in curves:
        dp = round(fn(x_paper)) - round(fn(x_pattern))
        extra = f"　暗部 {x_dark}→{round(fn(x_dark))}" if x_dark else ""
        labels.append(f"{label}　Δ={dp}{extra}")
    (bx, by, bw, bh), hits = legend_box(labels, curves, x_range, y_range, X, Y)
    if hits:
        print(f"  [warn] {fname}: 图例与曲线相交 {hits} 个采样点")
    p.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="8" '
             f'fill="#FFFFFF" fill-opacity="0.97" stroke="#DCDCDC" stroke-width="1"/>')
    ly = by + 19
    for ((label, _fn, color, dash), full) in zip(curves, labels):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        p.append(f'<line x1="{bx + 13:.1f}" y1="{ly:.1f}" x2="{bx + 41:.1f}" y2="{ly:.1f}" '
                 f'stroke="{color}" stroke-width="{LW_CURVE}" stroke-linecap="round"{dash_attr}/>')
        p.append(txt(bx + 49, ly + 4.5, full))
        ly += LEG_LH

    # 脚注
    y = FOOT_BOTTOM - FOOT_LEAD * (len(footnote) - 1)
    for i, ln in enumerate(footnote):
        if text_width(ln, FS_NOTE) > W - M_L - 14:
            raise ValueError(f"脚注过宽（{text_width(ln, FS_NOTE):.0f}）: {ln}")
        p.append(txt(M_L, y + i * FOOT_LEAD, ln, FS_NOTE, C_AXIS))

    p.append("</svg>")
    write_svg(os.path.join(OUT, fname), "\n".join(p))


# ================= 图 1：反例，往亮调会让暗纹消失 =================
def clip_add(b):
    return lambda x: clip255(x + b)


def gain(g, b=0.0):
    return lambda x: clip255(g * (x - 128) + 128 + b)


make_figure(
    "pattern_clip.svg",
    "反例：提亮或提高对比度，暗纹与纸白一起撞上 255",
    [
        ("基线 g=1，b=0", lambda x: x, C_BASE, ""),
        ("提高亮度 b=+15", clip_add(15), C_DOWN, "9,4"),
        ("提高对比度 g=1.4", gain(1.4), C_UP, "9,4"),
    ],
    x_range=(190, 255), y_range=(180, 255),
    x_ticks=[190, 200, 210, 220, 230, 240, 250],
    y_ticks=[180, 200, 220, 240, 255],
    vlines=[(235, "暗纹 235", "end"), (245, "纸白 245", "start")],
    x_pattern=235, x_paper=245,
    footnote=[
        "提高亮度把纸白先顶上 255，差异由 10 掉到 5；",
        "提高对比度则以 128 为锚点把两个高光一起推过 255，输出并阶，差异归零。",
    ],
)


# ================= 图 2：正解，压暗型伽马 =================
def gamma_dark(gm):
    return lambda x: clip255(255.0 * (clip255(x) / 255.0) ** gm)


make_figure(
    "gamma_ladder.svg",
    "正解：压暗型伽马端点固定，以压深暗部为代价换取高光反差",
    [
        ("γ = 1.0（基线）", gamma_dark(1.0), C_BASE, ""),
        ("γ = 1.5", gamma_dark(1.5), C_OK, "9,4"),
        ("γ = 2.2", gamma_dark(2.2), C_DOWN, "9,4"),
        ("γ = 3.0", gamma_dark(3.0), C_UP, "9,4"),
    ],
    x_range=(190, 255), y_range=(60, 255),
    x_ticks=[190, 200, 210, 220, 230, 240, 250],
    y_ticks=[60, 100, 150, 200, 255],
    vlines=[(235, "暗纹 235", "end"), (245, "纸白 245", "start")],
    x_pattern=235, x_paper=245, x_dark=70,
    footnote=[
        "幂律两端端点固定，绝不截断：γ 越大，高光侧斜率越大，暗纹与纸白间距越开。",
        "代价在暗部：「暗部 70→」为墨绿大字输出，γ 越大压得越黑。",
    ],
)


# ================= 图 3：白场重定标 =================
def renorm(wp):
    return lambda x: clip255(255.0 * x / wp)


make_figure(
    "white_point.svg",
    "破除灰雾：白场重定标，把纸白映射回 255",
    [
        ("恒等（灰雾现状）", lambda x: x, C_BASE, ""),
        ("白场点 195（纸白处）", renorm(195), C_OK, "9,4"),
        ("白场点 188（点过头）", renorm(188), C_UP, "9,4"),
    ],
    x_range=(178, 215), y_range=(155, 255),
    x_ticks=[180, 185, 190, 195, 200, 205, 210],
    y_ticks=[160, 180, 200, 220, 240, 255],
    vlines=[(188, "暗纹 188", "end"), (195, "纸白 195", "start")],
    x_pattern=188, x_paper=195,
    footnote=[
        "输入为已压暗但发灰的结果：纸白 195、暗纹 188。重定标把差异放大 255/白场值 倍。",
        "同时纸白回到纯白；若白场点在纸白之下，纸白与暗纹一起截断，差异归零。",
    ],
)

# ========== 图 4：总纲——为什么默认扫成纯白，三参数如何把曲线拉出来 ==========
def gbg(g, b=0.0, gamma=None):
    """三参数联合：先做仿射变换 g(x−128)+128+b，再做（可选）幂律变换 γ"""
    def f(x):
        y = clip255(g * (x - 128) + 128 + b)
        return clip255(255.0 * (y / 255.0) ** gamma) if gamma else y
    return f


make_figure(
    "clipping_rescue.svg",
    "水印为什么扫成纯白：默认曲线截断，与三参数如何把它拉出来",
    [
        ("① 默认 g=1.4", gbg(1.4), C_UP, "9,4"),
        ("② 降对比度 g=1.0", gbg(1.0), C_MID, "9,4"),
        ("③ 再降亮度 b=−15", gbg(1.0, -15), C_DOWN, "9,4"),
        ("④ 再加伽马 γ=2.2", gbg(1.0, -15, 2.2), C_OK, ""),
    ],
    x_range=(215, 255), y_range=(140, 262),
    x_ticks=[220, 230, 240, 250],
    y_ticks=[140, 170, 200, 230, 255],
    vlines=[(235, "暗纹 235", "end"), (245, "纸白 245", "start")],
    x_pattern=235, x_paper=245,
    footnote=[
        "默认曲线在暗纹处就已到达 255，其后是一段水平平台。",
        "平台上的所有输入被压成同一个输出值，水印与纸白因此同值。",
    ],
)

print("done.")
