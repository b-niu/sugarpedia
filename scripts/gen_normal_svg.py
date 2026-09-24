# -*- coding: utf-8 -*-
"""生成 Normal 笔记配图：正态分布钟形曲线与 μ±1.96σ 基准区间。
输出到 content/assets/statistics/"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "content", "assets", "statistics")
os.makedirs(OUT, exist_ok=True)


def gen_normal_dist():
    W, H = 680, 340
    ox, oy, pw, ph = 90, 260, 500, 190  # 坐标原点与绘图区
    mu = ox + pw / 2
    sigma = pw / 6.2  # ±3σ 铺满绘图区

    def y_of(x_val):
        """x_val 为以 σ 为单位的偏离量，返回屏幕 y。"""
        g = math.exp(-x_val ** 2 / 2)
        return oy - ph * g

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="24" text-anchor="middle" font-size="15" font-weight="bold" '
         f'fill="#333">正态分布：以 μ 为位置基准、σ 为尺度基准的钟形曲线</text>']
    # 坐标轴
    p.append(f'<line x1="{ox-10}" y1="{oy}" x2="{ox+pw+10}" y2="{oy}" stroke="#888" stroke-width="1.4"/>')
    # μ±1.96σ 着色区间（95% 置信）
    z = 1.96
    xL, xR = mu - z * sigma, mu + z * sigma
    steps = 160
    poly = [f"{xL:.1f},{oy}"]
    for i in range(steps + 1):
        xx = xL + (xR - xL) * i / steps
        poly.append(f"{xx:.1f},{y_of((xx - mu) / sigma):.1f}")
    poly.append(f"{xR:.1f},{oy}")
    p.append(f'<polygon points="{" ".join(poly)}" fill="#6fc2b4" fill-opacity="0.35"/>')
    # 曲线（±3.2σ）
    pts = []
    for i in range(200):
        x_val = -3.2 + 6.4 * i / 199
        pts.append(f"{mu + x_val * sigma:.1f},{y_of(x_val):.1f}")
    p.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#4c86c6" stroke-width="2.4"/>')
    # 均值竖线
    p.append(f'<line x1="{mu}" y1="{oy}" x2="{mu}" y2="{y_of(0)}" '
             f'stroke="#d62728" stroke-width="1.6" stroke-dasharray="5,4"/>')
    p.append(f'<text x="{mu}" y="{y_of(0) - 10}" text-anchor="middle" font-size="12.5" '
             f'font-weight="bold" fill="#d62728">μ：位置基准</text>')
    # 刻度标注
    for (x_val, label) in ((-3, "μ−3σ"), (-1.96, "μ−1.96σ"), (-1, "μ−σ"), (0, "μ"),
                           (1, "μ+σ"), (1.96, "μ+1.96σ"), (3, "μ+3σ")):
        tx = mu + x_val * sigma
        p.append(f'<line x1="{tx:.1f}" y1="{oy}" x2="{tx:.1f}" y2="{oy + 5}" stroke="#888" stroke-width="1.2"/>')
        anchor = "middle"
        p.append(f'<text x="{tx:.1f}" y="{oy + 20}" text-anchor="{anchor}" font-size="11.5" fill="#555">{label}</text>')
    # 置信区间标注
    p.append(f'<text x="{(xL+xR)/2:.0f}" y="{oy - 24}" text-anchor="middle" font-size="12" '
             f'fill="#2e7d6e" font-weight="bold">μ ± 1.96σ（95% 置信区间：日常语境的"正常范围"）</text>')
    # 尾部标注
    p.append(f'<text x="{mu - 2.7 * sigma:.0f}" y="{y_of(3) - 8:.0f}" text-anchor="middle" '
             f'font-size="11.5" fill="#888">远离基准 = 罕见</text>')
    p.append(f'<text x="{W/2}" y="{H-10}" text-anchor="middle" font-size="12.5" fill="#555">'
             f'同一张图回答三个问题：什么算正常（第一节）、偏离哪个方向（第二节·正交与基准）、误差如何分布（第三节）</text>')
    p.append("</svg>")
    with open(os.path.join(OUT, "normal_dist.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("written: normal_dist.svg")


gen_normal_dist()
