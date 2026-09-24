# -*- coding: utf-8 -*-
"""
Markdown 文档规范审计，检查那些「源码看着对、渲染才露馅」的写法。

检查项：
  1. 加粗定界符失效——按 CommonMark 的翼侧（flanking）规则判定。
     中文场景最常见的坑是标点紧贴定界符，例如 `**……不可逆。**clip` 或 `的**"文、理"**划分`，
     定界符既不是左翼也不是右翼，`**` 会原样显示成两个星号。
  2. 行内公式 `$...$`——正文段落里不得出现（见 docs/design.md 排版规范第 2 条）。
  3. `$$` 公式块前后必须各留一个空行（同上第 1 条）。
  4. 图片相对路径必须能解析到真实文件。
  5. 同一张表格内各行的列数必须一致。

围栏代码块与行内代码会被整体跳过，因此规范文档里讲规则的示例不会误报。

用法：
    python scripts/audit_markdown.py            # 审计 content、docs 与 README
    python scripts/audit_markdown.py docs       # 只审计指定目录

退出码：0 表示全部通过，1 表示存在缺陷。
"""
import glob
import os
import re
import sys
import unicodedata

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DEFAULT_TARGETS = [os.path.join(ROOT, "content"), os.path.join(ROOT, "docs"),
                   os.path.join(ROOT, "README.md")]
EXTRA_PUNCT = set("。，、；：？！）】》」』“”‘’…—～·")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")


def is_punct(ch):
    if ch is None:
        return False
    if ch in EXTRA_PUNCT:
        return True
    return unicodedata.category(ch).startswith("P")


def flanking(s, i, j):
    """定界串 s[i:j] 的 (左翼, 右翼) 属性，直接照搬 CommonMark 定义"""
    before = s[i - 1] if i > 0 else None
    after = s[j] if j < len(s) else None
    left = (after is not None and not after.isspace()) and (
        not is_punct(after) or before is None or before.isspace() or is_punct(before))
    right = (before is not None and not before.isspace()) and (
        not is_punct(before) or after is None or after.isspace() or is_punct(after))
    return left, right


def mask_code(line):
    """把行内代码 `...` 的内容换成占位符，避免把代码里的符号算进来"""
    out = list(line)
    i = 0
    while True:
        a = line.find("`", i)
        if a < 0:
            break
        b = line.find("`", a + 1)
        if b < 0:
            break
        for k in range(a, b + 1):
            out[k] = "x"
        i = b + 1
    return "".join(out)


def check_emphasis(ln, s, issues):
    runs = [(m.start(), m.end()) for m in re.finditer(r"\*{2}", s)]
    if not runs:
        return
    if len(runs) % 2:
        issues.append((ln, "加粗定界符个数为奇数，无法配对", s.strip()[:76]))
        return
    for k in range(0, len(runs) - 1, 2):
        (a1, b1), (a2, b2) = runs[k], runs[k + 1]
        left_ok, _ = flanking(s, a1, b1)
        _, right_ok = flanking(s, a2, b2)
        why = []
        if not left_ok:
            why.append("开定界非左翼")
        if not right_ok:
            why.append("闭定界非右翼")
        if why:
            seg = s[max(0, a1 - 10):min(len(s), b2 + 10)]
            issues.append((ln, "加粗失效（" + "；".join(why) + "）", seg))


def audit(fp):
    issues = []
    lines = open(fp, encoding="utf-8").read().splitlines()

    # 标记围栏代码块
    in_code = [False] * len(lines)
    fence = False
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("```"):
            in_code[i] = True
            fence = not fence
            continue
        in_code[i] = fence

    masked = [None if in_code[i] else mask_code(ln) for i, ln in enumerate(lines)]

    dollar_parity = 0
    in_table = False
    table_cols = 0
    for i, raw in enumerate(lines, 1):
        if in_code[i - 1]:
            continue
        s = masked[i - 1]

        # 1. 加粗定界符
        check_emphasis(i, s, issues)

        # 2. 行内公式：含 $ 且不是独立的 $$ 块即为违规
        if "$" in s:
            t = s.strip()
            if t != "$$" and not (t.startswith("$$") and t.endswith("$$")):
                issues.append((i, "正文出现行内公式 $...$，应改用 Unicode 或独立成块", t[:76]))

        # 3. $$ 公式块前后的空行
        t = s.strip()
        if t == "$$":
            dollar_parity ^= 1
            if dollar_parity:                      # 这是开定界
                if i > 1 and lines[i - 2].strip():
                    issues.append((i, "$$ 公式块前缺空行", t))
            else:                                   # 这是闭定界
                if i < len(lines) and lines[i].strip():
                    issues.append((i, "$$ 公式块后缺空行", t))
        elif t.startswith("$$") and t.endswith("$$") and len(t) > 4:
            if i > 1 and lines[i - 2].strip():
                issues.append((i, "$$ 公式块前缺空行", t[:60]))
            if i < len(lines) and lines[i].strip():
                issues.append((i, "$$ 公式块后缺空行", t[:60]))

        # 4. 图片相对路径
        for m in IMG_RE.finditer(s):
            p = m.group(1)
            if p.startswith(("http://", "https://")):
                continue
            full = os.path.normpath(os.path.join(os.path.dirname(fp), p.split("#")[0]))
            if not os.path.exists(full):
                issues.append((i, "图片路径解析不到文件", p))

        # 5. 表格列数一致
        if raw.lstrip().startswith("|"):
            cols = raw.count("|")
            if not in_table:
                in_table, table_cols = True, cols
            elif cols != table_cols:
                issues.append((i, f"表格列数不一致（本行 {cols} 个竖线，表头 {table_cols} 个）",
                               raw.strip()[:60]))
        else:
            in_table = False

    return issues


def collect(targets):
    files = []
    for t in targets:
        if os.path.isdir(t):
            files += glob.glob(os.path.join(t, "**", "*.md"), recursive=True)
        elif t.lower().endswith(".md") and os.path.exists(t):
            files.append(t)
    return sorted(set(os.path.normpath(f) for f in files))


def main(argv):
    targets = argv[1:] or DEFAULT_TARGETS
    files = collect(targets)
    if not files:
        print("没有找到任何 Markdown 文件，请检查路径。")
        return 1
    bad = 0
    print(f"待审计 {len(files)} 个 Markdown 文件\n")
    for fp in files:
        issues = audit(fp)
        rel = os.path.relpath(fp, ROOT)
        if issues:
            bad += 1
            print(f"=== {rel}  命中 {len(issues)} 处 ===")
            for ln, why, seg in issues:
                print(f"  L{ln}  {why}\n      {seg}")
        else:
            print(f"=== {rel}  OK")
    print(f"\n合计 {len(files)} 个文件，{len(files) - bad} 个通过，{bad} 个有问题。")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
