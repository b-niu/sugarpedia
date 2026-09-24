# -*- coding: utf-8 -*-
"""生成天文笔记配图：行星自转轴倾角对比、天王星极昼极夜成因。
输出到 content/assets/astronomy/"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "content", "assets", "astronomy")
os.makedirs(OUT, exist_ok=True)


def axis_endpoints(cx, cy, tilt_deg, half_len):
    """自转轴两端点：tilt 为偏离竖直方向的角度（顺时针）。"""
    a = math.radians(tilt_deg)
    dx = math.sin(a) * half_len
    dy = math.cos(a) * half_len
    return (cx - dx, cy - dy), (cx + dx, cy + dy)


def tilt_panel(p, cx, cy, tilt, name, sub, color):
    """画一个行星：圆盘 + 自转轴 + 轨道面横线 + 倾角标注。"""
    r = 34
    # 轨道面（横虚线）
    p.append(f'<line x1="{cx-70}" y1="{cy}" x2="{cx+70}" y2="{cy}" '
             f'stroke="#888" stroke-width="1.2" stroke-dasharray="5,4"/>')
    p.append(f'<text x="{cx+70}" y="{cy-6}" text-anchor="end" font-size="10" fill="#888">轨道面</text>')
    # 行星圆盘
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" fill-opacity="0.18" '
             f'stroke="{color}" stroke-width="1.8"/>')
    # 自转轴
    (x1, y1), (x2, y2) = axis_endpoints(cx, cy, tilt, r + 26)
    p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#333" stroke-width="2.2"/>')
    for (x, y) in ((x1, y1), (x2, y2)):
        p.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#333"/>')
    # 倾角弧线（竖直参考线与自转轴之间）
    p.append(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r - 26}" '
             f'stroke="#aaa" stroke-width="1" stroke-dasharray="2,3"/>')
    if tilt != 0:
        p.append(f'<path d="M {cx} {cy - r + 12} A {r - 12} {r - 12} 0 0 1 '
                 f'{cx + (r - 12) * math.sin(math.radians(tilt)):.1f} '
                 f'{cy - (r - 12) * math.cos(math.radians(tilt)):.1f}" '
                 f'fill="none" stroke="#d62728" stroke-width="1.4"/>')
        p.append(f'<text x="{cx + 14}" y="{cy - 22}" font-size="12" fill="#d62728" '
                 f'font-weight="bold">{tilt}°</text>')
    else:
        p.append(f'<text x="{cx + 14}" y="{cy - 22}" font-size="12" fill="#d62728" '
                 f'font-weight="bold">0°</text>')
    # 名称与说明
    p.append(f'<text x="{cx}" y="{cy + r + 34}" text-anchor="middle" font-size="14" '
             f'font-weight="bold" fill="#333">{name}</text>')
    p.append(f'<text x="{cx}" y="{cy + r + 52}" text-anchor="middle" font-size="11" fill="#666">{sub}</text>')


def gen_tilt_comparison():
    """四行星自转轴倾角对比。"""
    W, H = 920, 260
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="24" text-anchor="middle" font-size="15" font-weight="bold" '
         f'fill="#333">四颗行星的自转轴倾角（相对轨道面）</text>']
    panels = [
        ("水星", "0°：端正直立", "#8d99ae", 0),
        ("地球", "23.4°：四季之源", "#4c86c6", 23.4),
        ("天王星", "97.8°：整体躺倒", "#6fc2b4", 97.8),
        ("金星", "177.4°：近乎倒转（逆行）", "#d9a441", 177.4),
    ]
    slot = W / 4
    for i, (name, sub, color, tilt) in enumerate(panels):
        tilt_panel(p, slot * i + slot / 2, 140, tilt, name, sub, color)
    p.append("</svg>")
    with open(os.path.join(OUT, "tilt_comparison.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("written: tilt_comparison.svg")


def gen_uranus_seasons():
    """天王星公转中两极轮流朝阳：四个轨道位置。"""
    W, H = 920, 300
    cx, cy = W / 2, 160
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="24" text-anchor="middle" font-size="15" font-weight="bold" '
         f'fill="#333">天王星的极昼与极夜：自转轴指向固定，公转带来轮流朝阳</text>']
    # 太阳
    p.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="#f5b942"/>')
    p.append(f'<text x="{cx}" y="{cy + 34}" text-anchor="middle" font-size="12" fill="#b8860b">太阳</text>')
    # 轨道
    p.append(f'<circle cx="{cx}" cy="{cy}" r="105" fill="none" stroke="#bbb" '
             f'stroke-width="1.2" stroke-dasharray="6,5"/>')
    # 天王星自转轴固定指向（躺倒，与竖直成 97.8°，这里取指向右上）
    tilt = 97.8
    positions = [
        (-105, 0, "北极朝阳\n约 42 年极昼（北极）"),
        (0, -105, "阳光直射赤道"),
        (105, 0, "南极朝阳\n约 42 年极昼（南极）"),
        (0, 105, "阳光直射赤道"),
    ]
    for i, (dx, dy, label) in enumerate(positions):
        px, py = cx + dx, cy + dy
        # 太阳光线
        p.append(f'<line x1="{cx + dx * 0.14}" y1="{cy + dy * 0.14}" x2="{px - dx * 0.09}" '
                 f'y2="{py - dy * 0.09}" stroke="#f5b942" stroke-width="1.4" stroke-dasharray="3,4"/>')
        # 天王星
        r = 22
        p.append(f'<circle cx="{px}" cy="{py}" r="{r}" fill="#6fc2b4" fill-opacity="0.3" '
                 f'stroke="#3d8b7d" stroke-width="1.6"/>')
        (x1, y1), (x2, y2) = axis_endpoints(px, py, tilt, r + 14)
        p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#333" stroke-width="2"/>')
        p.append(f'<text x="{x2 + 4}" y="{y2}" font-size="10" fill="#333">N</text>')
        p.append(f'<text x="{x1 - 12}" y="{y1}" font-size="10" fill="#333">S</text>')
        # 位置标签
        lx = px
        ly = py + r + 30 if dy >= 0 else py - r - 26
        if dx != 0:
            ly = py - r - 26 if dx < 0 else py + r + 30
        lines = label.split("\n")
        for j, ln in enumerate(lines):
            p.append(f'<text x="{lx}" y="{ly + j * 14}" text-anchor="middle" '
                     f'font-size="11" fill="#555">{ln}</text>')
    p.append(f'<text x="{W/2}" y="{H-10}" text-anchor="middle" font-size="12" fill="#666">'
             f'自转轴在恒星背景中几乎固定（指向武仙座方向）；天王星每 84 年公转一周，'
             f'两极各自迎来约 42 年极昼。</text>')
    p.append("</svg>")
    with open(os.path.join(OUT, "uranus_seasons.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("written: uranus_seasons.svg")


gen_tilt_comparison()
gen_uranus_seasons()
