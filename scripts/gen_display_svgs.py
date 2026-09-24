# -*- coding: utf-8 -*-
"""生成显示传递函数的 SVG 矢量图，输出到 content/assets/display/"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "content", "assets", "display")
os.makedirs(OUT, exist_ok=True)

W, H = 320, 300          # 每张图尺寸
M_L, M_B, M_T, M_R = 44, 40, 16, 14
PW, PH = W - M_L - M_R, H - M_B - M_T

def to_px(x, y):
    """x,y in [0,1] -> svg coords"""
    return (M_L + x * PW, M_T + (1 - y) * PH)

def clamp01(v):
    return max(0.0, min(1.0, v))

def path_from_fn(fn, n=128):
    pts = []
    for i in range(n + 1):
        x = i / n
        y = clamp01(fn(x))
        px, py = to_px(x, y)
        pts.append(f"{px:.1f},{py:.1f}")
    return "M" + " L".join(pts)

def make_svg(fname, title, curves, y_label="输出亮度 V_out"):
    """curves: list of (label, fn, color, dash)"""
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
                 f'width="{W}" height="{H}" font-family="sans-serif" font-size="11">')
    parts.append(f'<rect width="{W}" height="{H}" fill="white"/>')
    # title
    parts.append(f'<text x="{W/2}" y="{M_T+2}" text-anchor="middle" '
                 f'font-size="12" font-weight="bold" fill="#333">{title}</text>')
    # axes
    x0, y0 = to_px(0, 0)
    x1, y1 = to_px(1, 1)
    parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#888" stroke-width="1"/>')
    parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#888" stroke-width="1"/>')
    # ticks + grid (quarter lines)
    for t in (0.25, 0.5, 0.75, 1.0):
        gx, gy = to_px(t, t)
        parts.append(f'<line x1="{gx}" y1="{y0}" x2="{gx}" y2="{y0-4}" stroke="#888"/>')
        parts.append(f'<line x1="{x0}" y1="{gy}" x2="{x0-4}" y2="{gy}" stroke="#888"/>')
        parts.append(f'<line x1="{gx}" y1="{y0}" x2="{gx}" y2="{to_px(0,0)[1]}" '
                     f'stroke="#eee" stroke-width="0.5"/>')
        parts.append(f'<line x1="{x0}" y1="{gy}" x2="{to_px(1,0)[0]}" y2="{gy}" '
                     f'stroke="#eee" stroke-width="0.5"/>')
    parts.append(f'<text x="{(x0+x1)/2}" y="{H-24}" text-anchor="middle" fill="#666">输入信号 x</text>')
    parts.append(f'<text x="13" y="{(y0+y1)/2}" text-anchor="middle" fill="#666" '
                 f'transform="rotate(-90 13 {(y0+y1)/2})">{y_label}</text>')
    parts.append(f'<text x="{x1}" y="{y0+12}" text-anchor="middle" fill="#666">1</text>')
    parts.append(f'<text x="{x0}" y="{y0+12}" text-anchor="middle" fill="#666">0</text>')
    # curves
    for label, fn, color, dash in curves:
        d = path_from_fn(fn)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2"{dash_attr}/>')
    # legend
    lx = M_L + 8
    ly = M_T + 16
    for label, fn, color, dash in curves:
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        parts.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+22}" y2="{ly}" '
                     f'stroke="{color}" stroke-width="2"{dash_attr}/>')
        parts.append(f'<text x="{lx+27}" y="{ly+4}" fill="#333">{label}</text>')
        ly += 16
    parts.append("</svg>")
    fp = os.path.join(OUT, fname)
    with open(fp, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print("written:", fp)

# 8bit offset b 换算到 [0,1]: b_norm = b/255
B30 = 30 / 255

# 1) 偏置（亮度）
make_svg("bias.svg", "亮度 = 黑电平偏置 b（增益 g=1）", [
    ("b=0（基准）",   lambda x: x,                        "#555", ""),
    ("b=+30（过高）", lambda x: clamp01(x + B30),         "#d62728", "6,3"),
    ("b=-30（过低）", lambda x: clamp01(x - B30),         "#1f77b4", "6,3"),
])

# 2) 增益（对比度，枢轴 0.5）
def gain(g):
    return lambda x: clamp01(g * (x - 0.5) + 0.5)

make_svg("gain.svg", "对比度 = 增益 g（枢轴 128 灰）", [
    ("g=1.0（基准）", lambda x: x,          "#555", ""),
    ("g=1.4（过大）", gain(1.4),            "#d62728", "6,3"),
    ("g=0.6（不足）", gain(0.6),            "#1f77b4", "6,3"),
])

# 3) 伽马 EOTF
make_svg("gamma.svg", "伽马曲线 EOTF：L = x^γ", [
    ("γ=2.2（标准）", lambda x: x ** 2.2,   "#555", ""),
    ("γ=1.8（过低）", lambda x: x ** 1.8,   "#1f77b4", "6,3"),
    ("γ=2.6（过高）", lambda x: x ** 2.6,   "#d62728", "6,3"),
])

# 4) Alpha 混合：白前景盖黑背景，随 alpha 变化的出射亮度
N = 128
nonlinear = [(i / N, (i / N) * 1.0) for i in range(N + 1)]           # 编码值 0.5α? 直接 alpha*1
lin_pts = []
nl_pts = []
for i in range(N + 1):
    a = i / N
    lin_pts.append((a, a ** 2.2))              # 线性混合再编码: (a*1^2.2)^... -> 编码值 a? 
    nl_pts.append((a, a ** 2.2))               # placeholder

# 精确计算：
# 线性正确：L = a*1^2.2 + (1-a)*0 = a，编码值 C = a^(1/2.2)
# 非线性错误：C_naive = a，出射 L = a^2.2
make_svg("alpha.svg", "白α前景盖黑底：出射亮度对比", [
    ("线性空间混合（正确）", lambda a: a,                     "#2ca02c", ""),
    ("非线性空间混合（错误）", lambda a: a ** 2.2,            "#d62728", "6,3"),
], y_label="物理出射亮度 L")
