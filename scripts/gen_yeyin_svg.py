# -*- coding: utf-8 -*-
"""
生成「叶音」一文的对照图：叶音的做法 vs 古音学的做法。

输出目录：content/assets/philology/

两者面对同一个现象（按今音读古诗不押韵），分岔点在第二步：
  - 叶音改的是「韵脚字的读音」，于是同一个字在不同诗篇得到不同读音，无从系统化；
  - 古音学改的是「古今音相同」这个假设，转而从韵例与谐声偏旁里求有规律的对应。

图内文字字号 ≥12px、标题 16px，配色沿用 Okabe-Ito 色盲友好方案，
满足 docs/design.md「排版与渲染规范」的要求。
"""
import os

from svgkit import (C_INK, C_AXIS, C_REF, C_UP, C_OK, C_DOWN,
                    FS_TITLE, FS_BODY, FS_NOTE,
                    txt, write_svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets", "philology")
os.makedirs(OUT, exist_ok=True)

W, H = 720, 404
PANEL_TOP, PANEL_H = 70, 300
BOX_H, BOX_GAP = 46, 16


def panel(x, w, title, color):
    el = [f'<rect x="{x}" y="{PANEL_TOP}" width="{w}" height="{PANEL_H}" rx="12" '
          f'fill="#FAFBFC" stroke="#DCE3EA" stroke-width="1.4"/>']
    el.append(txt(x + w / 2, PANEL_TOP + 20, title, FS_BODY + 1, color, "middle", "bold"))
    return el


def box(x, w, y, content, color):
    el = [f'<rect x="{x}" y="{y}" width="{w}" height="{BOX_H}" rx="8" '
          f'fill="white" stroke="{color}" stroke-width="1.4"/>']
    el.append(txt(x + w / 2, y + BOX_H / 2 + 4.5, content, FS_BODY, C_INK, "middle"))
    return el


def arrow(x, y_from, y_to, color):
    el = [f'<path d="M {x} {y_from} L {x} {y_to}" fill="none" stroke="{color}" '
          f'stroke-width="2" stroke-linecap="round"/>']
    el.append(f'<path d="M {x - 5} {y_to - 8} L {x} {y_to} L {x + 5} {y_to - 8}" '
              f'fill="none" stroke="{color}" stroke-width="2" '
              f'stroke-linecap="round" stroke-linejoin="round"/>')
    return el


def column(x, w, title, color, steps):
    el = panel(x, w, title, color)
    bx = x + 16
    bw = w - 32
    ys = [PANEL_TOP + 34 + i * (BOX_H + BOX_GAP) for i in range(len(steps))]
    for y, s in zip(ys, steps):
        el.extend(box(bx, bw, y, s, color))
    for i in range(len(ys) - 1):
        el.extend(arrow(x + w / 2, ys[i] + BOX_H + 3, ys[i + 1] - 3, color))
    return el


p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
     f'font-family="Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif">'
     f'<rect width="{W}" height="{H}" fill="white"/>']
p.append(txt(W / 2, 28, "同一起点，两种做法：叶音与古音学", FS_TITLE, C_INK, "middle", "bold"))
p.append(txt(W / 2, 50, "按今音读古诗不押韵，第一反应是改字音；古音学改的是假设", FS_NOTE, C_AXIS, "middle"))

p.extend(column(24, 320, "叶音的做法（已废弃）", C_UP, [
    "读到古诗不押韵",
    "临时改读韵脚字的读音",
    "同一个字在不同诗篇得到不同读音",
    "结果：读音各随其诗，无系统可循",
]))
p.extend(column(376, 320, "古音学的做法（今用）", C_OK, [
    "读到古诗不押韵",
    "假定古今读音本来就不同",
    "用韵例与谐声偏旁系统求证",
    "结果：得出有规律的音变对应，可检验",
]))

p.append(txt(24, H - 16, "两边的分岔点在第二步：叶音改的是字音，古音学改的是「古今音相同」这个假设。",
             FS_NOTE, C_AXIS))
p.append("</svg>")
write_svg(os.path.join(OUT, "yeyin_vs_guyinxue.svg"), "\n".join(p))
