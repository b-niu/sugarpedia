# -*- coding: utf-8 -*-
"""生成"超"字语义时间线配图。输出到 content/assets/philology/"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "content", "assets", "philology")
os.makedirs(OUT, exist_ok=True)


def gen_timeline():
    W, H = 760, 420
    ax = 120  # 时间轴 x
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="26" text-anchor="middle" font-size="15" font-weight="bold" '
         f'fill="#333">"超"的语义时间线：一个词根，五个时期，四条支线</text>']
    # 主时间轴（自上而下 = 时间推进）
    p.append(f'<line x1="{ax}" y1="55" x2="{ax}" y2="385" stroke="#8a6d1f" stroke-width="2.4"/>')
    p.append(f'<polygon points="{ax-6},385 {ax+6},385 {ax},396" fill="#8a6d1f"/>')
    # 时期节点：(y, 时代, 节点文本, 节点色)
    rows = [
        (75, "先秦", "本义：跳、跃上（《左传》超乘 ·《孟子》超北海）", "#d9a441"),
        (140, "两汉", "越过 → 超出、超迁（越级提拔，见于汉代公文）", "#c9b06a"),
        (300, "20世纪", "前缀化 → 超级、超声、超导（日语译词与本土引申合流）", "#3d8b7d"),
        (350, "20世纪", "入名高峰 → 超字殿后，粤语区尤为常见", "#d62728"),
    ]
    node_h = 34
    for (y, era, text, color) in rows:
        p.append(f'<circle cx="{ax}" cy="{y}" r="5" fill="{color}"/>')
        p.append(f'<text x="{ax-14}" y="{y+5}" text-anchor="end" font-size="13" '
                 f'font-weight="bold" fill="#333">{era}</text>')
        p.append(f'<rect x="{ax+18}" y="{y-node_h//2}" width="560" height="{node_h}" rx="7" '
                 f'fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-width="1.4"/>')
        p.append(f'<text x="{ax+32}" y="{y+5}" font-size="13" fill="#333">{text}</text>')
    # 汉末—唐：同期两条支线，双框并排共享一个时代标签
    ymid = 205
    p.append(f'<circle cx="{ax}" cy="{ymid}" r="5" fill="#4c86c6"/>')
    p.append(f'<text x="{ax-14}" y="{ymid+5}" text-anchor="end" font-size="13" '
             f'font-weight="bold" fill="#333">汉末—唐</text>')
    for (x, w, text, color) in [
        (ax+18, 262, "本土：超群、超凡（人名义来源）", "#4c86c6"),
        (ax+296, 282, "译经：超脱、超度（新义，与本土并行）", "#7fb069"),
    ]:
        p.append(f'<rect x="{x}" y="{ymid-node_h//2}" width="{w}" height="{node_h}" rx="7" '
                 f'fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-width="1.4"/>')
        p.append(f'<text x="{x+12}" y="{ymid+5}" font-size="12.5" fill="#333">{text}</text>')
    p.append(f'<text x="{W/2}" y="{H-6}" text-anchor="middle" font-size="12.5" fill="#555">'
             f'人名用"超"取的是汉末已成的"高出同列"义，其盛行期在 20 世纪、以粤语区最集中</text>')
    p.append("</svg>")
    with open(os.path.join(OUT, "chao_semantic_timeline.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("written: chao_semantic_timeline.svg")


gen_timeline()
