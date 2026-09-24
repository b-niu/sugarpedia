# -*- coding: utf-8 -*-
"""
SVG 排版审计：用几何计算检查矢量图的排版缺陷，取代肉眼看图。

检查项（对应 docs/design.md「排版与渲染规范」）：
  1. 图内文字字号不得小于 12px
  2. 文字不得越出画布（横向 / 纵向）
  3. 文字之间不得重叠
  4. 曲线不得越出绘图区、不得穿进图例底板
  5. 矩形图元不得越出画布

用法：
    python scripts/audit_svgs.py                       # 审计 content/assets 下全部 SVG
    python scripts/audit_svgs.py content/assets/scan    # 只审计指定目录
    python scripts/audit_svgs.py a.svg b.svg            # 审计指定文件

退出码：0 表示全部通过，1 表示存在缺陷。可直接接入 CI 或提交前钩子。
"""
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
DEFAULT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "assets")
MIN_FONT = 12.0

TOKEN = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]|-?(?:\d+\.?\d*|\.\d+)")
# 每种命令每段参数的个数，以及终点在参数列表中的偏移
SEG = {"M": (2, 0), "L": (2, 0), "T": (2, 0), "H": (1, 0), "V": (1, 0),
       "C": (6, 4), "S": (4, 2), "Q": (4, 2), "A": (7, 5), "Z": (0, 0)}


def text_width(content, fs):
    """与 svgkit.text_width 同源的宽度估算：中日韩字符 1.35em，其余 0.62em"""
    return sum(1.35 if ord(ch) > 0x2E80 else 0.62 for ch in content) * fs


def bbox(x, y, content, fs, anchor):
    w = text_width(content, fs)
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    return (x0, y - fs * 0.80, x0 + w, y + fs * 0.26)


def overlap(a, b):
    ox = min(a[2], b[2]) - max(a[0], b[0])
    oy = min(a[3], b[3]) - max(a[1], b[1])
    return (ox, oy) if ox > 0 and oy > 0 else None


def path_points(d):
    """解析 path 的 d，返回各段终点。曲线段按弦近似，足够做越界判定。"""
    pts = []
    cx = cy = 0.0
    cmd, args = None, []

    def flush(cmd, args):
        nonlocal cx, cy
        base = cmd.upper()
        if base not in SEG:
            return
        step, off = SEG[base]
        if step == 0:
            return
        rel = cmd.islower()
        n = len(args)
        for k in range(0, n - step + 1, step):
            if base == "H":
                x = cx + args[k] if rel else args[k]
                y = cy
            elif base == "V":
                x = cx
                y = cy + args[k] if rel else args[k]
            else:
                x, y = args[k + off], args[k + off + 1]
                if rel:
                    x += cx
                    y += cy
            cx, cy = x, y
            pts.append((cx, cy))

    for tok in TOKEN.findall(d):
        if tok.isalpha():
            if cmd:
                flush(cmd, args)
            cmd, args = tok, []
        else:
            args.append(float(tok))
    if cmd:
        flush(cmd, args)
    return pts


def audit(fp):
    """返回 (问题列表, (宽, 高))；空列表代表通过"""
    root = ET.parse(fp).getroot()
    view = [float(v) for v in root.get("viewBox").split()]
    W, H = view[2], view[3]
    issues = []

    # --- 文字 ---
    texts = []
    for el in root.iter(NS + "text"):
        content = (el.text or "").strip()
        if not content:
            continue
        fs = float(el.get("font-size", 12))
        if fs < MIN_FONT:
            issues.append(f"字号 {fs}px 小于 {MIN_FONT:g}px：[{content[:22]}]")
        if el.get("transform"):
            continue                      # 旋转的轴标签不参与重叠判定
        bb = bbox(float(el.get("x")), float(el.get("y")), content, fs,
                  el.get("text-anchor", "start"))
        texts.append((content, bb))
        if bb[0] < -0.5 or bb[2] > W + 0.5:
            issues.append(f"文字横向越界：[{content[:22]}] "
                          f"{bb[0]:.0f}..{bb[2]:.0f}（画布 0..{W:.0f}）")
        if bb[1] < -0.5 or bb[3] > H + 0.5:
            issues.append(f"文字纵向越界：[{content[:22]}] "
                          f"{bb[1]:.0f}..{bb[3]:.0f}（画布 0..{H:.0f}）")

    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            ov = overlap(texts[i][1], texts[j][1])
            if ov and ov[0] > 3 and ov[1] > 3:
                issues.append(f"文字重叠：[{texts[i][0][:16]}] × [{texts[j][0][:16]}] "
                              f"{ov[0]:.0f}×{ov[1]:.0f}px")

    # --- 绘图区：仓库里坐标图的坐标框约定为「实线 + stroke-width 恰好 1.6」---
    # 只认这个约定，示意图（流程图、天体示意等）不带它，于是自动跳过绘图区与图例判定，
    # 避免把示意图里的长线误当成坐标轴、把圆角框误当成图例而误报。
    horiz, vert = None, None
    for e in root.iter(NS + "line"):
        if e.get("stroke-width") != "1.6" or e.get("stroke-dasharray"):
            continue
        x1, y1 = float(e.get("x1")), float(e.get("y1"))
        x2, y2 = float(e.get("x2")), float(e.get("y2"))
        if abs(x2 - x1) >= abs(y2 - y1):
            if horiz is None or abs(x2 - x1) > horiz[0]:
                horiz = (abs(x2 - x1), min(x1, x2), max(x1, x2))
        elif vert is None or abs(y2 - y1) > vert[0]:
            vert = (abs(y2 - y1), min(y1, y2), max(y1, y2))
    plot = (horiz[1], vert[1], horiz[2], vert[2]) if (horiz and vert) else None

    # --- 图例底板（rx=8 的圆角矩形）；只在坐标图里判定，示意图的圆角框不算图例 ---
    legend = None
    if plot:
        for el in root.iter(NS + "rect"):
            if el.get("rx") == "8":
                lx, ly = float(el.get("x")), float(el.get("y"))
                legend = (lx, ly, lx + float(el.get("width")), ly + float(el.get("height")))
        if legend and (legend[2] > W + 0.5 or legend[3] > H + 0.5):
            issues.append(f"图例底板越界：{legend}")

    # --- 曲线 ---
    for el in root.iter(NS + "path"):
        pts = path_points(el.get("d", ""))
        if not pts:
            continue
        lw = float(el.get("stroke-width", 1))
        if plot:
            out = sum(1 for (px, py) in pts
                      if px < plot[0] - lw or px > plot[2] + lw
                      or py < plot[1] - lw or py > plot[3] + lw)
            if out:
                issues.append(f"路径超出绘图区（{out}/{len(pts)} 个顶点）")
        if legend:
            inside = sum(1 for (px, py) in pts
                         if legend[0] <= px <= legend[2] and legend[1] <= py <= legend[3])
            if inside:
                issues.append(f"路径穿入图例底板（{inside} 个顶点）")

    # --- 矩形 ---
    for el in root.iter(NS + "rect"):
        rx, ry = float(el.get("x", 0)), float(el.get("y", 0))
        rw, rh = float(el.get("width", 0)), float(el.get("height", 0))
        if rx < -0.5 or ry < -0.5 or rx + rw > W + 0.5 or ry + rh > H + 0.5:
            issues.append(f"矩形越界：x={rx:.0f} y={ry:.0f} w={rw:.0f} h={rh:.0f}")

    return issues, (W, H)


def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += glob.glob(os.path.join(p, "**", "*.svg"), recursive=True)
        elif p.lower().endswith(".svg"):
            files.append(p)
        else:
            files += glob.glob(p)
    return sorted(set(os.path.normpath(f) for f in files))


def main(argv):
    targets = argv[1:] or [DEFAULT_ROOT]
    files = collect(targets)
    if not files:
        print("没有找到任何 SVG 文件，请检查路径。")
        return 1

    bad = 0
    print(f"待审计 {len(files)} 个 SVG\n")
    for fp in files:
        try:
            issues, (W, H) = audit(fp)
        except ET.ParseError as exc:
            print(f"=== {os.path.basename(fp)} ===\n  ! XML 非法：{exc}")
            bad += 1
            continue
        print(f"=== {os.path.basename(fp)}  ({W:.0f}×{H:.0f}) ===")
        if issues:
            bad += 1
            for it in dict.fromkeys(issues):
                print("  ! " + it)
        else:
            print("  OK 无排版问题")

    print(f"\n合计 {len(files)} 个文件，{len(files) - bad} 个通过，{bad} 个有问题。")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
