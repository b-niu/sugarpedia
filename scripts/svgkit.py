# -*- coding: utf-8 -*-
"""
SVG 绘图的共用基元：文本转义、统一 text 输出、宽度估算、写出与 XML 自检、
Okabe-Ito 色盲友好配色、单调三次插值。

供 scripts/ 下的各绘图脚本 import 使用（脚本所在目录会自动加入 sys.path）。
"""
import xml.etree.ElementTree as ET

# ---------------- 字体与配色 ----------------
FONT = "Segoe UI, Microsoft YaHei, Helvetica, Arial, sans-serif"
C_INK = "#2B2B2B"      # 主文字
C_AXIS = "#5A5A5A"     # 轴线与刻度
C_GRID = "#EDEDED"     # 网格
C_REF = "#AFAFAF"      # 辅助虚线
C_LINE = "#8A8A8A"     # 参考轮廓线
C_BASE = "#4A4A4A"     # 基准曲线
C_UP = "#D55E00"       # 增强 / 过量（朱红）
C_DOWN = "#0072B2"     # 减弱 / 不足（蓝）
C_MID = "#56B4E9"      # 中间态（天蓝）
C_OK = "#009E73"       # 正确 / 保留（绿）
FS_TITLE = 16
FS_BODY = 12.5
FS_TICK = 12
FS_NOTE = 12


def esc(text):
    """XML 文本转义；SVG 里的 < > & 必须转义，否则不是合法 XML"""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def clamp01(v):
    return 0.0 if v < 0.0 else (1.0 if v > 1.0 else v)


def clip255(v):
    return 0.0 if v < 0.0 else (255.0 if v > 255.0 else v)


def text_width(content, fs):
    """粗略估算文本宽度：中日韩字符按 1.35em，其余按 0.62em"""
    return sum(1.35 if ord(ch) > 0x2E80 else 0.62 for ch in content) * fs


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


def write_svg(fp, content):
    """写出前先用 ElementTree 自检，保证产物是合法 SVG"""
    ET.fromstring(content)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"written: {fp}")


def monotone(xs, ys):
    """Fritsch–Carlson 单调三次插值，返回可调用函数 f(x)。

    用于把若干控制点连成光滑且不过冲的曲线，形态接近图像软件里的曲线工具。
    """
    n = len(xs)
    d = [(ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]) for i in range(n - 1)]
    m = [0.0] * n
    m[0], m[-1] = d[0], d[-1]
    for i in range(1, n - 1):
        m[i] = (d[i - 1] + d[i]) / 2.0
    for i in range(n - 1):
        if d[i] == 0.0:
            m[i] = m[i + 1] = 0.0
        else:
            a, b = m[i] / d[i], m[i + 1] / d[i]
            s = a * a + b * b
            if s > 9.0:
                t = 3.0 / (s ** 0.5)
                m[i], m[i + 1] = t * a * d[i], t * b * d[i]

    def f(x):
        if x <= xs[0]:
            return ys[0]
        if x >= xs[-1]:
            return ys[-1]
        for i in range(n - 1):
            if xs[i] <= x <= xs[i + 1]:
                h = xs[i + 1] - xs[i]
                t = (x - xs[i]) / h
                h00 = 2 * t ** 3 - 3 * t ** 2 + 1
                h10 = t ** 3 - 2 * t ** 2 + t
                h01 = -2 * t ** 3 + 3 * t ** 2
                h11 = t ** 3 - t ** 2
                return (h00 * ys[i] + h10 * h * m[i]
                        + h01 * ys[i + 1] + h11 * h * m[i + 1])
        return ys[-1]

    return f
