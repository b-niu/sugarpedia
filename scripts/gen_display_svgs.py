# -*- coding: utf-8 -*-
"""
生成点运算（Point Operations）传递函数的 SVG 矢量图。

输出目录：content/assets/display/
被两篇笔记共用：
  · 显示设备亮度、对比度与Alpha通道调控的物理机制与数学建模
  · 扫描仪三参数：亮度、对比度与伽马的点运算

符号约定（与笔记正文保持一致）：
  g  对比度增益（gain）—— 线性式 y = g·x + b 的首项系数，即 OpenCV convertScaleAbs 的 alpha 参数
  b  亮度偏置（bias）  —— 同一线性式的截距，即 OpenCV 的 beta 参数
  γ  伽马指数          —— 幂律变换 y = x^γ，源自 CRT 与 sRGB / BT.1886 标准
  α  专用于 Alpha 通道覆盖率，不用于对比度增益，以免同一份图谱里一符两义

视觉规范：曲线线宽 3px、轴线 1.6px，图内所有文字字号 ≥12px、标题 16px，
配色采用 Okabe-Ito 色盲友好方案，图例自动挑选不相交的角落。所有文本经 XML 转义，
写出前用 ElementTree 自检，保证产物是合法 SVG。以上均满足 docs/design.md
「排版与渲染规范」的要求。
"""
import os
import xml.etree.ElementTree as ET

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "display")
os.makedirs(OUT, exist_ok=True)

# ---------------- 画布与版心 ----------------
W, H = 720, 430
M_L, M_R, M_T, M_B = 76, 26, 54, 96
PW, PH = W - M_L - M_R, H - M_T - M_B
AXIS_TITLE_Y = H - 54          # x 轴标题基线
FOOT_BOTTOM = H - 14           # 脚注末行基线
FOOT_LEAD = 18                 # 脚注行距

# ---------------- 视觉规范 ----------------
FONT = "Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif"
C_INK = "#2B2B2B"      # 主文字
C_AXIS = "#5A5A5A"     # 轴线与刻度
C_GRID = "#EDEDED"     # 网格
C_REF = "#AFAFAF"      # 辅助虚线
C_BASE = "#4A4A4A"     # 基准曲线
C_UP = "#D55E00"       # 增强 / 过量（朱红）
C_DOWN = "#0072B2"     # 减弱 / 不足（蓝）
C_OK = "#009E73"       # 正确 / 保留（绿）
LW_CURVE = 3.0
LW_AXIS = 1.6
FS_TITLE = 16
FS_BODY = 12.5
FS_TICK = 12
FS_NOTE = 12


def esc(t):
    """XML 文本转义；SVG 里的 < > & 必须转义，否则不是合法 XML"""
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def clamp01(v):
    return 0.0 if v < 0.0 else (1.0 if v > 1.0 else v)


def to_px(x, y):
    """归一化坐标 [0,1]² -> 画布像素坐标"""
    return (M_L + x * PW, M_T + (1.0 - y) * PH)


def path_from_fn(fn, n=180):
    """返回 (采样点列表, path 的 d 属性)"""
    pts = []
    for i in range(n + 1):
        px, py = to_px(i / n, clamp01(fn(i / n)))
        pts.append((px, py))
    d = "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in pts)
    return pts, d


def txt(x, y, content, fs=FS_BODY, fill=C_INK, anchor="start", weight=None, transform=None):
    """统一的 <text> 输出口，负责转义与属性拼装"""
    attrs = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-size="{fs}"', f'fill="{fill}"']
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if transform:
        attrs.append(f'transform="{transform}"')
    return f'<text {" ".join(attrs)}>{esc(content)}</text>'


def tick_label(t):
    return f"{t:g}"


def _text_width(t_content, fs):
    """粗略估算文本宽度：中日韩字符按 1.35em，其余按 0.62em"""
    return sum(1.35 if ord(ch) > 0x2E80 else 0.62 for ch in t_content) * fs


def _render_marks(p, marks):
    x_left, y_bottom = to_px(0, 0)
    _, y_top = to_px(0, 1)
    for m in marks:
        kind = m["type"]
        if kind == "vline":
            gx, _ = to_px(m["x"], 0)
            color = m.get("color", C_AXIS)
            p.append(f'<line x1="{gx:.1f}" y1="{y_bottom:.1f}" x2="{gx:.1f}" y2="{y_top:.1f}" '
                     f'stroke="{color}" stroke-width="1.7" stroke-dasharray="5,4"/>')
            if m.get("label"):
                p.append(txt(gx - 7, y_top + 19, m["label"], FS_TICK, color,
                             anchor="end", weight="bold"))
        elif kind == "pivot":
            gx, gy = to_px(m["x"], m["y"])
            p.append(f'<line x1="{gx:.1f}" y1="{gy:.1f}" x2="{gx:.1f}" y2="{y_bottom:.1f}" '
                     f'stroke="{C_REF}" stroke-width="1.5" stroke-dasharray="4,4"/>')
            p.append(f'<line x1="{gx:.1f}" y1="{gy:.1f}" x2="{x_left:.1f}" y2="{gy:.1f}" '
                     f'stroke="{C_REF}" stroke-width="1.5" stroke-dasharray="4,4"/>')
            p.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="5" fill="#FFFFFF" '
                     f'stroke="{C_INK}" stroke-width="2.2"/>')
            p.append(txt(gx - 12, gy + 22, m["label"], FS_TICK, C_INK, anchor="end"))


def _legend_box(curves, pts_list, pad=14):
    """在四个角落中挑选与曲线相交采样点最少的那个；同分时优先右下角"""
    lh = 23
    bw = max(_text_width(c[0], FS_BODY) for c in curves) + 58
    bh = len(curves) * lh + 14
    x_left, y_bottom = to_px(0, 0)
    x_right, y_top = to_px(1, 1)
    cands = {
        "br": (x_right - bw - pad, y_bottom - bh - pad),
        "tr": (x_right - bw - pad, y_top + pad),
        "tl": (x_left + pad, y_top + pad),
        "bl": (x_left + pad, y_bottom - bh - pad),
    }
    best, best_hits = None, None
    for key in ("br", "tr", "tl", "bl"):
        bx, by = cands[key]
        hits = sum(1 for pts in pts_list for (px, py) in pts
                   if bx <= px <= bx + bw and by <= py <= by + bh)
        if best_hits is None or hits < best_hits:
            best, best_hits = (bx, by, bw, bh, lh), hits
    return best, best_hits


def _render_legend(p, curves, box):
    bx, by, bw, bh, lh = box
    p.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="8" '
             f'fill="#FFFFFF" fill-opacity="0.96" stroke="#DCDCDC" stroke-width="1"/>')
    ly = by + 21
    for label, _fn, color, dash in curves:
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        p.append(f'<line x1="{bx + 13:.1f}" y1="{ly:.1f}" x2="{bx + 41:.1f}" y2="{ly:.1f}" '
                 f'stroke="{color}" stroke-width="{LW_CURVE}" stroke-linecap="round"{dash_attr}/>')
        p.append(txt(bx + 49, ly + 4.5, label))
        ly += lh


def _render_footnote(p, lines, x, width_hint):
    """脚注支持多行；每行过宽时抛错，避免生成溢出画布的图"""
    y = FOOT_BOTTOM - FOOT_LEAD * (len(lines) - 1)
    for i, ln in enumerate(lines):
        if _text_width(ln, FS_NOTE) > width_hint:
            raise ValueError(f"脚注过宽（{_text_width(ln, FS_NOTE):.0f} > {width_hint}）: {ln}")
        p.append(txt(x, y + i * FOOT_LEAD, ln, FS_NOTE, C_AXIS))


def make_svg(title, curves, y_label="输出灰度 y（归一化）",
             x_label="输入灰度 x（归一化）", marks=None, footnote=None):
    """curves: [(图例文字, 函数, 颜色, 虚线样式)]"""
    x_left, y_bottom = to_px(0, 0)
    x_right, y_top = to_px(1, 1)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="{FONT}">',
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
         txt(W / 2, M_T - 24, title, FS_TITLE, C_INK, anchor="middle", weight="bold")]

    # 网格与刻度（0 / 0.25 / 0.5 / 0.75 / 1）
    for t in (0.0, 0.25, 0.5, 0.75, 1.0):
        gx, gy = to_px(t, t)
        if 0.0 < t < 1.0:
            p.append(f'<line x1="{gx:.1f}" y1="{y_bottom:.1f}" x2="{gx:.1f}" y2="{y_top:.1f}" '
                     f'stroke="{C_GRID}" stroke-width="1"/>')
            p.append(f'<line x1="{x_left:.1f}" y1="{gy:.1f}" x2="{x_right:.1f}" y2="{gy:.1f}" '
                     f'stroke="{C_GRID}" stroke-width="1"/>')
        p.append(f'<line x1="{gx:.1f}" y1="{y_bottom:.1f}" x2="{gx:.1f}" y2="{y_bottom + 6:.1f}" '
                 f'stroke="{C_AXIS}" stroke-width="1.3"/>')
        p.append(f'<line x1="{x_left:.1f}" y1="{gy:.1f}" x2="{x_left - 6:.1f}" y2="{gy:.1f}" '
                 f'stroke="{C_AXIS}" stroke-width="1.3"/>')
        p.append(txt(gx, y_bottom + 22, tick_label(t), FS_TICK, C_AXIS, anchor="middle"))
        p.append(txt(x_left - 11, gy + 4.3, tick_label(t), FS_TICK, C_AXIS, anchor="end"))

    # 轴线
    p.append(f'<line x1="{x_left:.1f}" y1="{y_bottom:.1f}" x2="{x_right:.1f}" y2="{y_bottom:.1f}" '
             f'stroke="{C_AXIS}" stroke-width="{LW_AXIS}"/>')
    p.append(f'<line x1="{x_left:.1f}" y1="{y_bottom:.1f}" x2="{x_left:.1f}" y2="{y_top:.1f}" '
             f'stroke="{C_AXIS}" stroke-width="{LW_AXIS}"/>')

    # 轴标题
    p.append(txt((x_left + x_right) / 2, AXIS_TITLE_Y, x_label, FS_BODY, C_AXIS, anchor="middle"))
    cy = (y_bottom + y_top) / 2
    p.append(txt(26, cy, y_label, FS_BODY, C_AXIS, anchor="middle",
                 transform=f"rotate(-90 26 {cy:.1f})"))

    _render_marks(p, marks or [])

    paths = [path_from_fn(fn) for _label, fn, _c, _d in curves]
    for (_pts, d), (_label, _fn, color, dash) in zip(paths, curves):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        p.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{LW_CURVE}" '
                 f'stroke-linecap="round" stroke-linejoin="round"{dash_attr}/>')

    box, hits = _legend_box(curves, [pts for pts, _d in paths])
    if hits:
        print(f"  [warn] {title}: 图例与曲线相交 {hits} 个采样点")
    _render_legend(p, curves, box)

    if footnote:
        lines = list(footnote) if isinstance(footnote, (list, tuple)) else [footnote]
        _render_footnote(p, lines, M_L, W - M_L - 10)

    p.append("</svg>")
    return "\n".join(p)


def write_svg(fname, content):
    fp = os.path.join(OUT, fname)
    ET.fromstring(content)          # XML 自检，语法错误直接抛异常
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"written: {fname}")


# =============== 1. 亮度 = 直流偏置 β ===============
BIAS_CODE = 30 / 255     # 以八位代码级表示的偏置量，换算到归一化域
write_svg("bias.svg", make_svg(
    "亮度：直流偏置 b（g = 1，γ = 1）",
    [
        ("b = 0", lambda x: x, C_BASE, ""),
        ("b = +30", lambda x: clamp01(x + BIAS_CODE), C_UP, "8,4"),
        ("b = −30", lambda x: clamp01(x - BIAS_CODE), C_DOWN, "8,4"),
    ],
    marks=[{"type": "vline", "x": 1 - BIAS_CODE, "label": "1 − b", "color": C_UP}],
    footnote=[
        "b 为亮度偏置，斜率恒为 1；b > 0 调亮，b < 0 调暗。",
        "x > 1 − b 的像素被截断为 1.0，层次差异不可逆地丢失。",
    ],
))

# =============== 2. 对比度 = 增益 α（枢轴 0.5）===============
def gain(a):
    return lambda x: clamp01(a * (x - 0.5) + 0.5)


write_svg("gain.svg", make_svg(
    "对比度：绕中性灰的增益 g（b = 0，γ = 1）",
    [
        ("g = 1.0", lambda x: x, C_BASE, ""),
        ("g = 1.4", gain(1.4), C_UP, "8,4"),
        ("g = 0.6", gain(0.6), C_DOWN, "8,4"),
    ],
    marks=[{"type": "pivot", "x": 0.5, "y": 0.5, "label": "枢轴 (0.5, 0.5)"}],
    footnote=[
        "g 为对比度增益，曲线绕枢轴 (0.5, 0.5) 旋转：g > 1 反差变强，g < 1 反差变弱。",
        "x ≥ 0.5 + 0.5/g 的高光被截断为纯白。",
    ],
))

# =============== 3. 伽马 = 幂律变换 ===============
write_svg("gamma.svg", make_svg(
    "伽马：幂律变换 y = x^γ",
    [
        ("γ = 2.2", lambda x: x ** 2.2, C_BASE, ""),
        ("γ = 1.8", lambda x: x ** 1.8, C_DOWN, "8,4"),
        ("γ = 2.6", lambda x: x ** 2.6, C_UP, "8,4"),
    ],
    footnote=[
        "γ 为幂律指数，两端端点恒为 0 与 1，不产生高光截断；",
        "γ > 1 时曲线下凹，高光侧的局部斜率大于 1。",
    ],
))

# =============== 4. Alpha 混合（供显示设备一文使用）===============
write_svg("alpha.svg", make_svg(
    "白前景覆于黑底：线性与非线性空间混合的出射亮度",
    [
        ("线性空间", lambda a: a, C_OK, ""),
        ("非线性空间", lambda a: a ** 2.2, C_UP, "8,4"),
    ],
    y_label="物理出射亮度 L（归一化）",
    x_label="Alpha 覆盖率 α",
    footnote=[
        "线性空间混合为物理正确解；非线性空间混合是常见工程错误。",
        "α = 0.5 时前者出射 0.500，后者仅 0.214，光能损失 57.2%。",
    ],
))


# =============== 5. 截断与溢出对照图 ===============
def make_clipping_svg():
    N = 17                                    # 灰阶级数
    SW, SH, GAP = 56, 56, 5                   # 色块尺寸与间距
    MX = 30                                   # 左右留白
    LEFT = MX + 8                             # 色块起始 x
    TITLE_H = 64
    ROW_H = 128                               # 行高：行标题 + 色块 + 标注
    FOOT_H = 88
    Wc = LEFT + N * (SW + GAP) - GAP + MX
    Hc = TITLE_H + 3 * ROW_H + FOOT_H
    codes = [round(i * 255 / (N - 1)) for i in range(N)]

    rows = [
        ("① 理想呈现：全灰阶平滑过渡，暗部与高光都保留层次", lambda c: c, None, ""),
        ("② 暗部截断（压黑）：代码 ≤16 全部塌成纯黑，暗部层次归零",
         lambda c: 0 if c <= 16 else c, (0, 1), "≤16 → 0"),
        ("③ 高光截断（过曝）：代码 ≥235 全部顶成纯白，高光层次归零",
         lambda c: 255 if c >= 235 else c, (15, 16), "≥235 → 255"),
    ]

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wc} {Hc}" '
         f'width="{Wc}" height="{Hc}" font-family="{FONT}">',
         f'<rect width="{Wc}" height="{Hc}" fill="#FFFFFF"/>',
         txt(Wc / 2, 32, "截断与溢出：灰阶层次是如何丢失的", FS_TITLE, C_INK,
             anchor="middle", weight="bold")]

    for r, (label, fn, crush, crush_note) in enumerate(rows):
        ry = TITLE_H + r * ROW_H            # 色块顶边
        accent = C_OK if r == 0 else (C_DOWN if r == 1 else C_UP)

        # 左侧行标记
        p.append(f'<rect x="{MX - 8:.1f}" y="{ry:.1f}" width="4" height="{SH}" rx="2" '
                 f'fill="{accent}"/>')

        # 行标题置于色块上方，避免与下方标注争位
        p.append(txt(LEFT, ry - 10, label, FS_BODY, C_INK))

        for i, c in enumerate(codes):
            x = LEFT + i * (SW + GAP)
            v = fn(c)
            p.append(f'<rect x="{x:.1f}" y="{ry:.1f}" width="{SW}" height="{SH}" rx="3" '
                     f'fill="rgb({v},{v},{v})" stroke="#8A8A8A" stroke-width="1.3"/>')
            p.append(txt(x + SW / 2, ry + SH / 2 + 4.5, c, FS_TICK,
                         "#FFFFFF" if v < 140 else "#2B2B2B", anchor="middle"))

        # 被打平的区间：用强调色下划线 + 说明文字标出
        if crush:
            i_from, i_to = crush
            bx = LEFT + i_from * (SW + GAP)
            bw = (i_to - i_from + 1) * (SW + GAP) - GAP
            p.append(f'<line x1="{bx:.1f}" y1="{ry + SH + 10:.1f}" x2="{bx + bw:.1f}" '
                     f'y2="{ry + SH + 10:.1f}" stroke="{accent}" stroke-width="3.5" '
                     f'stroke-linecap="round"/>')
            p.append(txt(bx + bw / 2, ry + SH + 30, crush_note, FS_TICK, accent,
                         anchor="middle", weight="bold"))

    foot_lines = [
        "色块内数字为输入代码值（0 = 纯黑，255 = 纯白）。",
        "②③ 中被下划线标出的区间，多个输入代码被映射成同一个输出值，",
        "原始的层次差异在输出端彻底消失，无法恢复——截断是多对一映射，不存在反函数。",
    ]
    fy = Hc - 14 - 22 * (len(foot_lines) - 1)
    for i, ln in enumerate(foot_lines):
        if _text_width(ln, FS_NOTE) > Wc - 2 * MX:
            raise ValueError(f"说明文字过宽: {ln}")
        p.append(txt(MX, fy + i * 22, ln, FS_NOTE, C_AXIS))

    p.append("</svg>")
    return "\n".join(p)


write_svg("clipping.svg", make_clipping_svg())
print("done.")
