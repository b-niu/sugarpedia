# -*- coding: utf-8 -*-
"""生成"表"字语义树配图。输出到 content/assets/philology/"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "content", "assets", "philology")
os.makedirs(OUT, exist_ok=True)

# 节点：(id, x, y, w, text, fill, stroke, text_color)
ROOT = dict(x=30, y=190, w=110, text="外衣（本义）", fill="#d9a441", stroke="#8a6d1f")
NODES = [
    dict(x=200, y=70, w=110, text="外面、表面", fill="#eef3f8", stroke="#4c86c6"),
    dict(x=200, y=200, w=110, text="标记、标识", fill="#eef3f8", stroke="#4c86c6"),
    dict(x=390, y=30, w=90, text="表亲", fill="#f4ecdd", stroke="#b08a3e"),
    dict(x=390, y=90, w=90, text="华表", fill="#f4ecdd", stroke="#b08a3e"),
    dict(x=390, y=150, w=90, text="圭表", fill="#f4ecdd", stroke="#b08a3e"),
    dict(x=390, y=210, w=90, text="年表", fill="#f4ecdd", stroke="#b08a3e"),
    dict(x=390, y=270, w=90, text="表文", fill="#f4ecdd", stroke="#b08a3e"),
    dict(x=560, y=150, w=130, text="钟表（计时）", fill="#dfeee9", stroke="#3d8b7d"),
    dict(x=560, y=210, w=130, text="现代表格", fill="#dfeee9", stroke="#3d8b7d"),
    dict(x=560, y=270, w=130, text="贺表（公文）", fill="#dfeee9", stroke="#3d8b7d"),
]
# 连线：(from 右侧中点, to 左侧中点, dashed)
EDGES = [
    ((140, 220), (200, 100), False),   # 根 → 外面
    ((140, 220), (200, 230), False),   # 根 → 标记
    ((310, 100), (390, 60), False),    # 外面 → 表亲
    ((310, 230), (390, 120), False),   # 标记 → 华表
    ((310, 230), (390, 180), False),   # 标记 → 圭表
    ((310, 230), (390, 240), False),   # 标记 → 年表
    ((310, 230), (390, 300), False),   # 标记 → 表文
    ((480, 180), (560, 180), False),   # 圭表 → 钟表
    ((480, 240), (560, 240), False),   # 年表 → 现代表格
    ((480, 300), (560, 300), False),   # 表文 → 贺表
]
NODE_H = 36


def gen_tree():
    W, H = 720, 340
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="24" text-anchor="middle" font-size="15" font-weight="bold" '
         f'fill="#333">"表"的语义树：从一个词根长出的四条支线</text>']
    # 连线（贝塞尔）
    for ((x1, y1), (x2, y2), _) in EDGES:
        mid = (x1 + x2) / 2
        p.append(f'<path d="M {x1} {y1} C {mid} {y1}, {mid} {y2}, {x2} {y2}" '
                 f'fill="none" stroke="#b9c2cc" stroke-width="1.6"/>')
    # 节点
    def draw(n):
        return (f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{NODE_H}" rx="7" '
                f'fill="{n["fill"]}" stroke="{n["stroke"]}" stroke-width="1.6"/>'
                f'<text x="{n["x"] + n["w"]/2}" y="{n["y"] + NODE_H/2 + 5}" text-anchor="middle" '
                f'font-size="13.5" font-weight="bold" fill="#333">{n["text"]}</text>')
    p.append(draw(ROOT))
    for n in NODES:
        p.append(draw(n))
    # 时代标注（右侧竖排式小字）
    era = [("近代", 165), ("明清", 288), ("汉魏六朝", 42)]
    for text, y in era:
        p.append(f'<text x="{W-10}" y="{y}" text-anchor="end" font-size="11" fill="#98a2ad">{text}</text>')
    p.append(f'<text x="{W/2}" y="{H-8}" text-anchor="middle" font-size="12.5" fill="#555">'
             f'金色＝本义 · 蓝边＝一次引申 · 米色＝具体义项 · 绿色＝仍在使用的现代义项</text>')
    p.append("</svg>")
    with open(os.path.join(OUT, "biao_semantic_tree.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("written: biao_semantic_tree.svg")


gen_tree()
