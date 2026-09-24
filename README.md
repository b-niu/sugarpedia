# SugarPedia

> 个人知识沙盒与多维认知网络。持续生长的网状知识库：从量子物理到计算机底层逻辑，从医学影像原理到历史人物传记，乃至古典训诂学。
>
> 原则：**知识无边界，弱目录结构，强节点链接。**

计划基于 [Quartz 4](https://quartz.jzhao.xyz/) 构建静态站点并发布于 GitHub Pages（尚未初始化，见 [TODO](./TODO.md)）。当前仓库先以纯 Markdown 形式生长内容。

## 一、📖 导航

| 文档 | 内容 |
|---|---|
| [设计文档](./docs/design.md) | 项目定位、目录结构、命名与 Tag 规范、写作模板、Quartz 配置要点 |
| [content/](./content/) | 知识库正文（Quartz 渲染源） |
| [scripts/](./scripts/) | 配图生成等工具脚本 |
| [TODO](./TODO.md) | 待办清单 |

## 二、🔗 克隆与子模块

```bash
# 首次克隆：连子模块一起拉
git clone --recurse-submodules https://github.com/b-niu/sugarpedia.git

# 已有本地仓库：补拉/初始化子模块
git submodule update --init --recursive
```

同步子模块远端的更新（子模块自己的 `main`）：

```bash
git submodule update --remote --merge sugarvault
```

> **排查提示**：若 `git status` 出现 `modified: sugarvault (modified content)`，说明是子模块**工作区**有未提交改动，不是网络或权限问题。此时 `git submodule update` 无法恢复被删除的文件——HEAD 没变，Git 只会回一句 `Already on 'main'`。正确做法是进子模块执行 `git restore -- .`，再回主仓库确认 `git status` 干净。

## 三、🗂️ 知识分区

```text
content/
├── 01_nature/         🌌 自然科学
├── 02_culture/        🏛️ 人文社科
├── 03_engineering/    ⚙️ 工程技术
├── 04_questions/      ❓ 悬赏与探究
├── 05_workbench/      🛠️ 折腾记录
└── 06_sources/        📖 溯源库
```

## 四、📚 文章索引

| 分区 | 文章 | 状态 |
|---|---|---|
| 🌌 物理 | [电子与正电子：一枚粒子和它的镜像](./content/01_nature/physics/电子与正电子：一枚粒子和它的镜像.md) | growing |
| 🌌 医学影像 | [一颗正电子的旅程：PET 如何听见身体里的光](./content/01_nature/biology/一颗正电子的旅程：PET如何听见身体里的光.md) | growing |
| 🌌 天文 | [行星的奇妙"转向"：南北极、不变平面与那些"躺倒"的行星](./content/01_nature/astronomy/行星的奇妙转向：南北极、不变平面与躺倒的行星.md) | growing |
| 🏛️ 训诂 | [Normal 的四重含义：正常、法向量、正态分布与师范](./content/02_culture/philology/Normal的四重含义：正常、法向量、正态分布与师范.md) | growing |
| 🏛️ 训诂 | [fast 的三个身份：牢固、快捷与斋戒](./content/02_culture/philology/fast的三个身份：牢固、快捷与斋戒.md) | growing |
| 🏛️ 训诂 | [naïve 头上的两个点：分音符、法语与"天真"的来历](./content/02_culture/philology/naive头上的两个点：分音符、法语与天真的来历.md) | growing |
| 🏛️ 训诂 | ["表"字的语义演变时间线](./content/02_culture/philology/表字的语义演变时间线.md) | growing |
| ⚙️ 计算机科学 | [显示设备亮度、对比度与 Alpha 通道调控的物理机制与数学建模](./content/03_engineering/computer_science/显示设备亮度、对比度与Alpha通道调控的物理机制与数学建模.md) | growing |
| ⚙️ 计算机科学 | [扫描仪三参数：亮度、对比度与伽马的点运算](./content/03_engineering/computer_science/扫描仪三参数：亮度、对比度与伽马的点运算.md) | growing |

> 配图均为 SVG 矢量图，由 [scripts/](./scripts/) 中的 Python 脚本参数化生成，可复现、可调整。

## 五、🔒 内容声明

本仓库仅收录客观知识与脱敏后的技术分析，不包含任何个人身份信息、网络配置、硬件资产清单或密钥凭证。详见[设计文档](./docs/design.md)的"🔒 内容安全纪律"一节。
