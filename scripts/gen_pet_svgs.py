# -*- coding: utf-8 -*-
"""生成 PET 笔记配图：LOR 几何、TOF 定位。
输出到 content/assets/pet/"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "content", "assets", "pet")
os.makedirs(OUT, exist_ok=True)


def gen_lor():
    """探测器环 + 湮灭点 + 反向光子 + LOR。"""
    W, H = 560, 420
    cx, cy, R = 280, 200, 150
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="24" text-anchor="middle" font-size="15" font-weight="bold" '
         f'fill="#333">符合探测：一次湮灭确定一条响应线（LOR）</text>']
    # 探测器环：分段色块
    n = 36
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = a0 + 2 * math.pi / n * 0.82
        x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
        x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        p.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
                 f'stroke="#4c86c6" stroke-width="9" stroke-linecap="round"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R-9}" fill="none" stroke="#d8e4f0" stroke-width="1"/>')
    # 湮灭点（偏离中心）
    px, py = cx + 40, cy - 30
    # LOR：过 P 点、给定方向的两端探测器
    ang = math.radians(205)
    dx, dy = math.cos(ang), math.sin(ang)
    t = 400  # 足够长，与环相交
    ax, ay = px - dx * t, py - dy * t
    bx, by = px + dx * t, py + dy * t
    # 与环求交（解析）：|P+td|=R
    b = 2 * (dx * (px - cx) + dy * (py - cy))
    c = (px - cx) ** 2 + (py - cy) ** 2 - R ** 2
    disc = math.sqrt(b * b - 4 * c)
    t1, t2 = (-b - disc) / 2, (-b + disc) / 2
    xA, yA = px + dx * t1, py + dy * t1
    xB, yB = px + dx * t2, py + dy * t2
    # LOR 虚线
    p.append(f'<line x1="{xA:.1f}" y1="{yA:.1f}" x2="{xB:.1f}" y2="{yB:.1f}" '
             f'stroke="#d62728" stroke-width="1.6" stroke-dasharray="7,5"/>')
    # 两个光子箭头
    for (ex, ey, s) in ((xA, yA, 1), (xB, yB, -1)):
        ux, uy = (ex - px) * s / 1, (ey - py) * s / 1
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        sx, sy = px + ux * 26, py + uy * 26
        mx, my = px + ux * (L - 30) * 0.92, py + uy * (L - 30) * 0.92
        p.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{mx:.1f}" y2="{my:.1f}" '
                 f'stroke="#f5b942" stroke-width="2.6"/>')
        # 箭头头部
        ha = math.atan2(uy, ux)
        for da in (math.radians(150), -math.radians(150)):
            p.append(f'<line x1="{mx:.1f}" y1="{my:.1f}" '
                     f'x2="{mx + 11 * math.cos(ha + da):.1f}" '
                     f'y2="{my + 11 * math.sin(ha + da):.1f}" '
                     f'stroke="#f5b942" stroke-width="2.6"/>')
    # 击中探测器高亮
    for (hx, hy) in ((xA, yA), (xB, yB)):
        p.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="9" fill="none" '
                 f'stroke="#d62728" stroke-width="2.2"/>')
    # 湮灭点星形标记
    p.append(f'<circle cx="{px}" cy="{py}" r="6" fill="#d62728"/>')
    p.append(f'<text x="{px + 10}" y="{py - 10}" font-size="13" fill="#d62728" '
             f'font-weight="bold">湮灭点 P（未知）</text>')
    p.append(f'<text x="{(xA+xB)/2:.1f}" y="{(yA+yB)/2 + (18 if dx*dy>0 else -12):.1f}" '
             f'text-anchor="middle" font-size="13" fill="#d62728" font-weight="bold">LOR</text>')
    p.append(f'<text x="{W/2}" y="{H-32}" text-anchor="middle" font-size="12.5" fill="#555">'
             f'两个 511 keV 光子近似反向飞行，分别击中环上两个探测器（红圈）</text>')
    p.append(f'<text x="{W/2}" y="{H-14}" text-anchor="middle" font-size="12.5" fill="#555">'
             f'系统只知道：湮灭一定在这条红虚线上——但线上具体哪个点，无法确定</text>')
    p.append("</svg>")
    with open(os.path.join(OUT, "pet_lor.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("written: pet_lor.svg")


def gen_tof():
    """无 TOF（整线等概率） vs 有 TOF（概率集中成峰）。"""
    W, H = 640, 300
    x0, x1 = 90, 550   # LOR 两端
    yA, yB = 90, 220
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="24" text-anchor="middle" font-size="15" font-weight="bold" '
         f'fill="#333">TOF 的作用：把"整条线"剪成"一小段"（x = c·Δt / 2）</text>']
    # --- 上半：无 TOF ---
    p.append(f'<text x="30" y="{yA+4}" font-size="12.5" fill="#555">无 TOF</text>')
    p.append(f'<circle cx="{x0}" cy="{yA}" r="6" fill="#4c86c6"/>')
    p.append(f'<circle cx="{x1}" cy="{yA}" r="6" fill="#4c86c6"/>')
    p.append(f'<text x="{x0-12}" y="{yA+4}" text-anchor="end" font-size="12" fill="#4c86c6">A</text>')
    p.append(f'<text x="{x1+12}" y="{yA+4}" font-size="12" fill="#4c86c6">B</text>')
    p.append(f'<line x1="{x0}" y1="{yA}" x2="{x1}" y2="{yA}" stroke="#999" stroke-width="1.4"/>')
    # 整线均匀概率带
    p.append(f'<rect x="{x0}" y="{yA-16}" width="{x1-x0}" height="10" fill="#d62728" '
             f'fill-opacity="0.25" stroke="none"/>')
    p.append(f'<text x="{(x0+x1)/2}" y="{yA-24}" text-anchor="middle" font-size="11.5" '
             f'fill="#d62728">线上每个位置等概率——约束只有一条线</text>')
    # --- 下半：有 TOF ---
    p.append(f'<text x="30" y="{yB+4}" font-size="12.5" fill="#555">有 TOF</text>')
    p.append(f'<circle cx="{x0}" cy="{yB}" r="6" fill="#4c86c6"/>')
    p.append(f'<circle cx="{x1}" cy="{yB}" r="6" fill="#4c86c6"/>')
    p.append(f'<text x="{x0-12}" y="{yB+4}" text-anchor="end" font-size="12" fill="#4c86c6">A</text>')
    p.append(f'<text x="{x1+12}" y="{yB+4}" font-size="12" fill="#4c86c6">B</text>')
    p.append(f'<line x1="{x0}" y1="{yB}" x2="{x1}" y2="{yB}" stroke="#999" stroke-width="1.4"/>')
    # 高斯峰（中心偏右）
    mu, sigma = x0 + (x1 - x0) * 0.62, 34
    pts = []
    steps = 120
    for i in range(steps + 1):
        xx = x0 + (x1 - x0) * i / steps
        g = math.exp(-((xx - mu) ** 2) / (2 * sigma ** 2))
        pts.append(f"{xx:.1f},{yB - 14 - 44 * g:.1f}")
    p.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#d62728" stroke-width="2.2"/>')
    p.append(f'<line x1="{mu:.1f}" y1="{yB-8}" x2="{mu:.1f}" y2="{yB-64}" '
             f'stroke="#d62728" stroke-width="1" stroke-dasharray="3,3"/>')
    p.append(f'<text x="{mu:.1f}" y="{yB-72}" text-anchor="middle" font-size="11.5" '
             f'fill="#d62728" font-weight="bold">概率最高的位置（Δt 决定）</text>')
    p.append(f'<text x="{W/2}" y="{H-14}" text-anchor="middle" font-size="12.5" fill="#555">'
             f'TOF 没有给出精确坐标，而是给出沿线的一个概率分布——重建算法因此大幅去噪</text>')
    p.append("</svg>")
    with open(os.path.join(OUT, "pet_tof.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("written: pet_tof.svg")


gen_lor()
gen_tof()
