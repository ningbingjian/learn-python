# Course Structure v3.0

本文定义 `learn-python-course` 的逻辑层级、物理目录、正文与源码对应关系、Python 工程边界以及课程状态语义。

## 1. 逻辑层级

课程统一使用：

```text
Stage
└── Module
    └── Unit
```

- **Stage**：较大的能力成长阶段。
- **Module**：相对完整的知识域。
- **Unit**：一个核心问题、机制或能力闭环。

Unit 不能仅因为“这个 API 还没单独讲”而成立。一个好的 Unit 应回答：为什么现在需要它、它改变了什么能力、用什么证据证明学会。

## 2. 逻辑层级与物理目录分开

如果 Stage 下直接放 Module 最清楚：

```text
01-python-language-foundations/
├── README.md
├── 01-first-useful-python-program/
├── 02-collections-and-mutable-state/
└── ...
```

如果 Module 下的核心目录全部是 Unit，可以直接：

```text
01-first-useful-python-program/
├── README.md
├── 01-handle-first-task/
├── 02-assignment-and-binding/
└── 03-trust-user-input/
```

不额外套 `modules/`、`units/`。判断标准：

> 删除这一层后，学习者是否仍然能准确理解归属？如果可以，优先删除。

只有真实承担分类职责的目录才保留，例如 Unit 内的 `examples/`、`exercises/`、`fixtures/`、`benchmarks/`。

## 3. Book-first，而不是目录优先

Unit README 像一本技术书的章节导言或完整正文，负责：

```text
核心问题
→ 已有直觉或代码
→ 概念与模型
→ 机制或设计因果
→ 证据
→ 边界与代价
→ 迁移能力
```

Unit README 不应退化为大量文件点击导航。正文没有产生新源码状态时，不为每个小标题创建目录。

## 4. 文档与源码一一对应

凡是需要源码支撑的正式教学状态，必须满足：

```text
NN-topic/
├── README.md
├── src/ 或明确的可执行脚本
└── tests/（当行为适合自动验证时）
```

若当前状态本身是真实 Package / Application 或需要独立依赖，再增加：

```text
pyproject.toml
uv.lock（独立项目时）
```

核心约束：

> **当前 README 讲的就是当前目录源码；当前目录源码就是正文结束后的完整状态。**

禁止：

- README 讲 A，源码已经是后续 D。
- 必须 checkout 历史 commit 才能得到对应代码。
- 只有 diff，没有演进后的完整状态。
- 只有最终项目，需要学习者反推中间过程。
- README 提到不存在的文件或命令。

Git 历史只用于维护、Review 和高级 diff，不是正常学习入口。

## 5. 推荐的 Unit 结构

一个存在连续源码演进的 Unit 可以是：

```text
03-shared-mutable-state/
├── README.md
├── 01-aliasing-bug/
│   ├── README.md
│   ├── src/
│   └── tests/
├── 02-explicit-copy-boundary/
│   ├── README.md
│   ├── src/
│   └── tests/
└── exercises/
```

`01` 和 `02` 是书籍正文中的教学章节，同时保存对应章节结束后的完整状态。它们不额外包 `steps/`、`checkpoints/`、`snapshots/`，除非这些词本身就是当前技术领域的概念。

如果 Unit 只有一个完整状态，则直接让 Unit 根目录的 README 与源码对应，不强行再套一层。

## 6. 什么变化值得保存新的完整源码状态

不是每一个术语、语法或方法调用都需要复制源码。以下变化通常值得保留：

- 数据模型或对象关系明显改变。
- 责任边界改变。
- 新机制进入主要运行路径。
- 对外行为发生可观察变化。
- 测试策略明显改变。
- 错误状态本身值得与修复版本并排比较。
- 当前版本会成为下一章节的明确基线。

以下通常不值得单独建状态：

- 增加一个普通 API 调用。
- 只改输出文案。
- 只为解释一个术语复制整套项目。
- 同一结论可以在当前正文中的小例子直接证明。

纯理论没有新源码状态时，可以只有 README。

## 7. 源码演进关系

如果当前章节基于上一状态继续：

```text
上一完整状态
↓
正文指出新需求或缺陷
↓
解释为什么现有设计不足
↓
按真实修改顺序演进
↓
当前目录保存新完整状态
```

下一章节必须明确：

```text
基于哪个目录？
上一版本有什么？
为什么不够？
修改了哪些职责、文件和行为？
测试怎样变化？
当前完整结果是什么？
```

上一状态继续保留。不要用 Git commit 代替正式教学状态。

## 8. 完整教学状态不等于独立 pyproject

这是 Python 课程必须明确区分的两个维度：

```text
教学维度
→ 每个有意义状态必须完整可见、可运行、可验证

工程维度
→ 是否需要独立 Package、环境、依赖与锁文件
```

因此禁止默认执行：

```text
每个 Unit 一个 pyproject.toml
每个小 API 一个虚拟环境
每个状态复制相同的 pytest / Ruff 配置
```

### 8.1 共享 Module 项目

当多个状态使用相同 Python 基线、依赖和测试工具，而且不是独立发布包时，可以在 Module 根目录统一维护：

```text
01-first-useful-python-program/
├── README.md
├── pyproject.toml
├── uv.lock
├── 01-handle-first-task/
├── 02-assignment-and-binding/
└── 03-trust-user-input/
```

子目录仍保存各自完整源码状态，根项目只负责公共工程配置和统一验证。

### 8.2 uv workspace

只有当多个状态或组件本身就是不同 Package / Application，且需要统一依赖解析和锁文件时，才考虑 uv workspace：

```text
module/
├── pyproject.toml
├── uv.lock
├── packages/
│   ├── app-a/pyproject.toml
│   └── library-b/pyproject.toml
└── ...
```

workspace 不是为了让目录看起来高级。它适合多个真实包共同开发，不适合依赖约束冲突、需要独立虚拟环境或必须严格证明依赖隔离的实验。

Python 环境本身不能保证某个 workspace member 只导入自己声明的依赖，因此课程测试必须主动检查依赖边界，不能把共享环境中的“碰巧可导入”当作配置正确。

### 8.3 独立项目

出现以下情况时可以独立 `pyproject.toml` 与锁文件：

- Python 版本或依赖约束冲突。
- 需要完全独立虚拟环境。
- 构建、发布或运行方式本身就是教学重点。
- 性能、故障或源码实验需要隔离。
- 当前内容与主线没有真实继承关系。

README 必须解释为什么独立，而不是默认复制脚手架。

## 9. 依赖不能破坏教学差异

共享根项目或 workspace 不能让早期源码状态提前获得后续依赖。

例如：

```text
前三个状态只使用标准库
第四个状态首次引入 FastAPI
```

不能因为根项目方便，就让前三个状态默认依赖 FastAPI。依赖出现本身若是课程演进的重要变化，就必须由对应状态明确声明，并通过测试防止边界泄漏。

## 10. 首次创建项目的教学职责

首次出现新的工程时，正文必须说明创建过程，但深度取决于前置知识。

早期阶段尚未系统学习 Packaging 时，只说明当前必须知道的：

```text
项目为什么存在
Python 基线
源码和测试目录
如何用 uv 同步与运行
当前依赖为什么需要
```

Stage 07 已学 Packaging 后，再完整解释：

```text
pyproject 标准与工具配置
build backend
src layout
dependency groups
lock 与 resolution
sdist / wheel
发布与私有索引
```

高级阶段不要机械重复 uv 入门，而应说明当前 Package、workspace member、依赖边界、运行入口和部署关系。

## 11. Focused Lab 归属于 Unit

需要控制变量时使用 Focused Lab，例如：

- 浮点精度。
- 共享可变对象。
- mutable default argument。
- closure late binding。
- asyncio cancellation 与 backpressure。
- GC 循环引用。
- GIL / free-threaded 对照。
- SQLAlchemy Session / connection pool 行为。

Lab 默认放在真正讲解它的 Unit 内。能在正常演进项目中清楚证明的机制，不额外创建 Lab。

## 12. Project 归属

Module Project 由负责综合验收的 Unit 承接，不要求 Module 顶层固定存在 `project/`。

Stage Project 可以作为 Stage 的一个明确 Module 或 Unit。Project 必须有背景、约束、里程碑、测试、验收和变化任务，不能只是把前面代码复制到一起。

长期 Architecture Spine 只在需求自然出现时演进，不强迫浮点、GC、Descriptor、网络抓包等内容全部塞入同一个业务系统。

## 13. THEORY / DESIGN / CASE / OPS

不需要源码时可以只有 README 和必要资产：

```text
THEORY → 推导、图、反例
DESIGN → 约束、方案、Trade-off、ADR
CASE   → 背景、决策、结果、复盘
OPS    → 命令、状态、风险、回滚
```

不要为了“看起来实践”伪造 Python Package。

## 14. Exercises

练习必须明确基于哪一个正式源码状态，优先采用：

```text
已有完整状态
→ 新需求
→ 约束
→ 验收标准
→ Hint
→ Solution
```

只有确实需要预置缺失代码或失败测试时，才维护独立 `starter/`。

## 15. CI 与验证

所有正式保留的可运行状态都应被验证，而不是只验证最终版本。

根据工程结构至少检查：

```text
uv 能恢复环境
脚本 / Package 能运行
pytest 能通过
Ruff / type check 按当前阶段要求通过
Module 根项目或 workspace 整体可验证
关键子项目能按文档独立运行
```

如果是性能结论，还必须保存 workload、环境、baseline、profile 或 metric，以及修改后的复测结果。

## 16. 命名规则

- 目录使用 `NN-kebab-case`。
- 名称表达业务问题、技术机制或源码状态，不表达内部生成术语。
- Python package 使用合法且稳定的 snake_case 名称。
- 不把章节编号强行写入所有 package 和 class 名称。
- `main.py` 只有在它确实是入口时使用，不让所有示例都退化成无语义的 `main.py`。

## 17. 路径与链接

- 所有相对链接必须指向真实路径。
- 移动或删除目录后必须清理旧引用、CI working-directory 和运行命令。
- README 中“基于某状态”的链接必须真实存在。
- 不在正式导航中引用旧版课程树。

## 18. 状态语义

统一：

```text
PLANNED → DESIGNED → BUILT → VALIDATED
```

- `PLANNED`：只有路线位置和能力方向。
- `DESIGNED`：核心问题、边界、因果链、材料形态、源码策略和验收设计完成。
- `BUILT`：必要材料完成，并通过 Technical Gate 与 Teaching Gate。
- `VALIDATED`：真实学习验证通过。

目录存在、README 生成、测试通过都不能单独代表完成。只有 `VALIDATED` 才表示课程经过真实学习者验证。

## 19. Git 的定位

Git 保存历史、支持 Review、显示 diff 和追踪决策。正式课程目录只保留当前正确体系；旧版本不创建 `_old/`、`legacy/`、`backup/` 污染学习入口。
