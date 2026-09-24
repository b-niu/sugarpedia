# -*- coding: utf-8 -*-
"""生成粒子物理笔记配图：安德森云室判向逻辑、湮灭与对产生的双向门。
输出到 content/assets/particle/"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "content", "assets", "particle")
os.makedirs(OUT, exist_ok=True)


def gen_cloud_chamber():
    """安德森云室：铅板 + 两条可能方向的轨迹 + 磁场，演示如何判断粒子来向。"""
    W, H = 640, 360
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="24" text-anchor="middle" font-size="15" font-weight="bold" '
         f'fill="#333">安德森的判断：铅板减速 + 磁场偏转，暴露粒子的来向与电荷</text>']
    # 云室边框
    p.append(f'<rect x="60" y="40" width="520" height="280" fill="#f7fafc" '
             f'stroke="#888" stroke-width="1.5" rx="6"/>')
    # 铅板（中央横条）
    p.append(f'<rect x="80" y="170" width="480" height="20" fill="#9aa5b1"/>')
    p.append(f'<text x="560" y="184" font-size="12" fill="#555" text-anchor="end">铅板（穿越即减速）</text>')
    # 磁场符号（垂直纸面向里 ⊗）
    for bx in range(100, 560, 80):
        for by in (70, 130, 230, 290):
            p.append(f'<circle cx="{bx}" cy="{by}" r="7" fill="none" stroke="#b0b8c1" stroke-width="1.2"/>')
            p.append(f'<line x1="{bx-4.5}" y1="{by-4.5}" x2="{bx+4.5}" y2="{by+4.5}" '
                     f'stroke="#b0b8c1" stroke-width="1.2"/>')
            p.append(f'<line x1="{bx-4.5}" y1="{by+4.5}" x2="{bx+4.5}" y2="{by-4.5}" '
                     f'stroke="#b0b8c1" stroke-width="1.2"/>')
    p.append(f'<text x="70" y="56" font-size="11.5" fill="#889">磁场方向：垂直纸面向里</text>')
    # 上方轨迹：大弯（慢），下方：小弯（快）。曲线为圆弧。
    # 上：粒子若从上往下，刚进云室能量高→下方弯小。实际照片：下弯大。
    # 画两组：实线（真解：自下而上，下方弯曲大=慢）与虚线（误判：自上而下）。
    # 实线轨迹：从下(慢,大曲率)穿板到上(快,小曲率)
    path_real = "M 300 300 Q 300 215 380 150 Q 440 105 520 92"
    path_fake = "M 520 92 Q 440 105 380 150 Q 300 215 300 300"
    p.append(f'<path d="{path_real}" fill="none" stroke="#d62728" stroke-width="2.6"/>')
    p.append(f'<path d="{path_fake}" fill="none" stroke="#4c86c6" stroke-width="2" '
             f'stroke-dasharray="6,5"/>')
    p.append(f'<text x="252" y="316" font-size="12.5" fill="#d62728" font-weight="bold">'
             f'下方弯得急 = 速度慢</text>')
    p.append(f'<text x="470" y="80" font-size="12.5" fill="#d62728" font-weight="bold">'
             f'上方弯得缓 = 速度快</text>')
    p.append(f'<text x="{W/2}" y="344" text-anchor="middle" font-size="12.5" fill="#555">'
             f'结论：粒子自下而上飞行，偏转方向显示电荷为正——这就是正电子（蓝虚线为"自上而下"的误判方向）</text>')
    p.append("</svg>")
    with open(os.path.join(OUT, "cloud_chamber.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("written: cloud_chamber.svg")


def gen_two_way():
    """湮灭与对产生：双向门。左：e+e- → 2γ；右：γ → e+e-（核旁）。"""
    W, H = 680, 300
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="24" text-anchor="middle" font-size="15" font-weight="bold" '
         f'fill="#333">物质与能量的双向门（阈值：2mₑc² ≈ 1.022 MeV）</text>']
    cy = 150
    # —— 左半：湮灭 ——
    lx = 170
    p.append(f'<text x="{lx}" y="70" text-anchor="middle" font-size="13.5" '
             f'font-weight="bold" fill="#333">湮灭（湮没质能 → 光子）</text>')
    # 电子/正电子两点
    for (dx, label, color) in ((-55, "e⁺", "#d9a441"), (55, "e⁻", "#4c86c6")):
        ex = lx + dx
        p.append(f'<circle cx="{ex}" cy="{cy+55}" r="9" fill="{color}"/>')
        p.append(f'<text x="{ex}" y="{cy+85}" text-anchor="middle" font-size="12.5" fill="#333">{label}</text>')
        # 指向中心的箭头
        mx, my = lx + dx * 0.35, cy + 18
        p.append(f'<line x1="{lx + dx*0.75:.0f}" y1="{cy+48}" x2="{mx:.0f}" y2="{my}" '
                 f'stroke="{color}" stroke-width="2"/>')
        ha = math.atan2(my - (cy + 48), mx - (lx + dx * 0.75))
        for da in (math.radians(150), -math.radians(150)):
            p.append(f'<line x1="{mx:.0f}" y1="{my}" '
                     f'x2="{mx + 9 * math.cos(ha + da):.0f}" y2="{my + 9 * math.sin(ha + da):.0f}" '
                     f'stroke="{color}" stroke-width="2"/>')
    # 两个出射光子（波浪线简化为折线箭头）
    for s in (-1, 1):
        gx, gy = lx + s * 150, cy - 55
        p.append(f'<line x1="{lx + s*22}" y1="{cy-8}" x2="{gx - s*10}" y2="{gy+8}" '
                 f'stroke="#f5b942" stroke-width="2.2"/>')
        ha = math.atan2(gy + 8 - (cy - 8), (gx - s*10) - (lx + s*22))
        for da in (math.radians(150), -math.radians(150)):
            p.append(f'<line x1="{gx - s*10:.0f}" y1="{gy+8:.0f}" '
                     f'x2="{gx - s*10 + 9 * math.cos(ha + da):.0f}" '
                     f'y2="{gy + 8 + 9 * math.sin(ha + da):.0f}" stroke="#f5b942" stroke-width="2.2"/>')
        p.append(f'<text x="{gx + s*4:.0f}" y="{gy - 6:.0f}" text-anchor="middle" '
                 f'font-size="12.5" fill="#b8860b">γ 511 keV</text>')
    p.append(f'<text x="{lx}" y="{cy-38}" text-anchor="middle" font-size="12" fill="#666">'
             f'动量守恒要求两个光子背向飞行</text>')
    # 中间分隔与双向箭头
    p.append(f'<line x1="{W/2}" y1="50" x2="{W/2}" y2="250" stroke="#ccc" stroke-width="1" '
             f'stroke-dasharray="5,5"/>')
    p.append(f'<text x="{W/2}" y="{cy}" text-anchor="middle" font-size="20" fill="#999">⇄</text>')
    # —— 右半：对产生 ——
    rx = 510
    p.append(f'<text x="{rx}" y="70" text-anchor="middle" font-size="13.5" '
             f'font-weight="bold" fill="#333">对产生（光子 → 粒子对）</text>')
    p.append(f'<circle cx="{rx}" cy="{cy-30}" r="12" fill="none" stroke="#666" stroke-width="2"/>')
    p.append(f'<text x="{rx}" y="{cy-52}" text-anchor="middle" font-size="12" fill="#666">原子核（接走反冲）</text>')
    # 入射光子
    p.append(f'<line x1="{rx-190}" y1="{cy-30}" x2="{rx-18}" y2="{cy-30}" '
             f'stroke="#f5b942" stroke-width="2.2"/>')
    p.append(f'<text x="{rx-100}" y="{cy-42}" text-anchor="middle" font-size="12.5" '
             f'fill="#b8860b">γ ≥ 1.022 MeV</text>')
    for (dx, label, color) in ((-60, "e⁻", "#4c86c6"), (60, "e⁺", "#d9a441")):
        ex = rx + dx
        p.append(f'<line x1="{rx + dx*0.25:.0f}" y1="{cy-24}" x2="{ex - dx*0.35:.0f}" '
                 f'y2="{cy+45}" stroke="{color}" stroke-width="2"/>')
        p.append(f'<circle cx="{ex}" cy="{cy+55}" r="9" fill="{color}"/>')
        p.append(f'<text x="{ex}" y="{cy+85}" text-anchor="middle" font-size="12.5" fill="#333">{label}</text>')
    p.append(f'<text x="{rx}" y="{cy-8}" text-anchor="middle" font-size="12" fill="#666">'
             f'必须在核旁发生，由核带走少量反冲动量</text>')
    p.append(f'<text x="{W/2}" y="{H-12}" text-anchor="middle" font-size="12.5" fill="#555">'
             f'同一组守恒律（能量、动量、电荷）统治两个方向——单向的时间箭头在这里是双向的</text>')
    p.append("</svg>")
    with open(os.path.join(OUT, "two_way.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("written: two_way.svg")


gen_cloud_chamber()
gen_two_way()
