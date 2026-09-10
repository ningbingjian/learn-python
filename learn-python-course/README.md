# Learn Python Course v3.0

> 目标：从第一次运行 Python 程序开始，逐步形成语言理解、工程实现、运行时分析、Web 与数据系统、生产诊断、分布式架构和 AI 平台能力，最终达到高级 / 资深 Python 工程师与 Python 架构师水平。

## 1. 课程产品定义

这不是：

```text
Python API 大全
框架快速入门合集
面试八股清单
几百个互不相干的小 Demo
一个知识点一个 pyproject.toml
README 数量与字数竞赛
```

而是一套能力训练系统：

```text
理解问题
→ 写出可运行实现
→ 用实验验证模型
→ 通过测试固定行为
→ 用证据调试和诊断
→ 建立性能基线
→ 比较设计方案
→ 随约束变化演进系统
→ 形成架构与治理能力
```

最终能力包括：

```text
Python 语言与 Pythonic 编程
Typing、Data Model 与元编程
测试、调试、Packaging 与工程质量
线程、进程、asyncio 与 CPython Runtime
HTTP、ASGI、数据库与 Web 框架
缓存、消息、搜索与分布式系统
安全、可观测、SRE 与云原生交付
数据分析、数据工程与模型服务
LLM、RAG、Agent、MCP 与 AI Platform
生产系统设计、演进和技术治理
```

## 2. v3.0 的核心变化

v3.0 的路线、进度和教学规范适用于本目录。仓库中的 [learn-python-examples](../learn-python-examples/README.md) 按 phase 组织独立学习路径，与本课程并存；两套材料分别记录进度，不互相替代。

v3.0 使用四条核心原则：

1. **问题闭环驱动**：Unit 对应一个核心问题或能力闭环，不对应一个孤立 API。
2. **Book-first**：正文首先像正常技术书，主要篇幅用于理论、机制、代码因果、边界和工程判断。
3. **Evolutionary Source**：源码按真实需求和责任变化自然演进，只保留有教学意义的完整状态。
4. **Evidence-based**：测试、日志、Profile、Metric、Trace、Benchmark 和故障证据用于证明结论。

## 3. 课程层级

统一逻辑层级：

```text
Stage
└── Module
    └── Unit
```

- **Stage**：一段较大的能力成长阶段。
- **Module**：相对完整的知识域。
- **Unit**：一个核心问题、机制或能力闭环。

逻辑层级不要求物理目录机械增加 `modules/`、`units/`。删除一层纯包装目录后仍能看清归属，就优先删除。

例如：

```text
01-python-language-foundations/
├── README.md
├── 01-first-useful-python-program/
├── 02-collections-and-mutable-state/
├── 03-control-flow/
├── 04-functions-and-contracts/
├── 05-modules-and-packages/
├── 06-classes-and-object-collaboration/
└── 07-integration-and-stage-project/
```

Unit 内正文按书籍章节组织，不默认把 Step、Checkpoint、Snapshot 当作阅读层级。

## 4. 教学形态由目标决定

| 类型 | 主要问题 | 典型证据 | 是否必须有代码 |
|---|---|---|---|
| `THEORY` | 模型为什么成立 | 推导、图、反例 | 否 |
| `CONCEPT` | 心智模型怎样建立 | 对比、例子、关系图 | 不一定 |
| `BUILD` | 怎样正确实现 | 完整源码、运行与测试 | 是 |
| `MECHANISM` | 内部机制怎样工作 | 控制变量实验 | 通常是 |
| `FAILURE` | 怎样从症状定位根因 | 日志、异常、dump、trace | 不一定 |
| `SOURCE` | 框架或运行时怎样落地 | 调用链、断点、固定版本源码 | 是 |
| `PERFORMANCE` | 瓶颈在哪里，优化是否有效 | workload、baseline、profile、复测 | 通常是 |
| `DESIGN` | 多种方案怎样选择 | 约束、Trade-off、ADR | 不一定 |
| `CASE` | 真实系统为什么成功或失败 | Case Study、Postmortem | 否 |
| `OPS` | 怎样部署、观察、恢复 | CLI、配置、监控、回滚 | 不一定 Python |
| `PROJECT` | 能否组合能力交付 | 需求、里程碑、测试、验收 | 通常是 |

一个 Unit 可以组合多种类型，不把每个知识点机械拆成一个独立项目。

## 5. 正文与源码关系

需要源码支撑的正式教学状态使用：

```text
NN-topic/
├── README.md
├── src/ 或可执行脚本
└── tests/
```

若它本身是真实 Package / Application 边界，再增加 `pyproject.toml`。核心规则是：

> **当前 README 讲解当前目录的源码；当前目录保存这篇正文结束后的完整结果。**

源码组织不采用两个极端：

```text
永远只维护一个最终版本
一个 API 就复制一套独立工程
```

而根据关系选择：

```text
存在真实继承关系
→ 基于上一完整状态演进，并保留前后状态

没有真实继承关系
→ 独立 Example / Project

需要隔离机制、故障、源码或性能变量
→ Focused Lab

只有理论推导
→ README 即可
```

完整教学状态与独立 Python 工程不是同一个概念。同一 Module 内的相关状态可以共享项目配置；只有真实 Package、依赖边界或隔离需求存在时，才增加独立 `pyproject.toml` 或 uv workspace member。

详见：

- [`COURSE_STRUCTURE.md`](COURSE_STRUCTURE.md)
- [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md)
- [`QUALITY_GATE.md`](QUALITY_GATE.md)

## 6. 深度分层

每个 Unit 可以包含：

```text
Must
→ 主学习路径和必要能力

Should
→ 工程边界、常见故障和设计选择

Expert
→ 运行时、源码、性能与复杂权衡
```

深度标签不能破坏正文连续阅读，也不能为了“显得深入”把后续阶段内容提前倒灌。

## 7. 实践体系

```text
Micro Exercise
      ↓
Focused Lab
      ↓
Module Project
      ↓
Stage Project
      ↓
Architecture Spine / Graduation Project
```

- **Micro Exercise**：验证单个概念的迁移能力。
- **Focused Lab**：严格隔离机制、故障、源码或性能变量。
- **Module Project**：组合一个 Module 的核心能力。
- **Stage Project**：证明整个 Stage 的能力已经形成。
- **Architecture Spine**：在真正适合时让长期系统继续演进，不强迫所有知识塞进同一个项目。

贯穿项目负责连续性，完整源码状态负责可追溯性，Focused Lab 负责隔离性，三者不能互相替代。

## 8. 学习路线

完整课程见 [`CURRICULUM.md`](CURRICULUM.md)。路线分为五段：

```text
00～07  Python 基础与工程能力
08～12  系统、并发、运行时与设计能力
13～17  Web 与数据库服务能力
18～24  分布式生产平台与云原生能力
25～28  数据、AI 与毕业级架构能力
```

不同目标可以选不同路径：

- **Python 工程主线**：00～12。
- **Web 后端主线**：00～17，再按需进入 18～24。
- **数据 / AI 主线**：00～11、25～27，并补齐 22～24 的生产能力。
- **架构师主线**：完成核心路径后进入 18～24 与 28，不要求把所有框架当作同等深度主线。

## 9. 当前建设状态

```text
课程治理与总路线：                  BUILT
Stage 00 Developer Bootstrap：      DESIGNED
Stage 01 Language Foundations：     BUILT
Stage 02～28：                      PLANNED
正式 BUILT Unit：                   21
正式 VALIDATED Unit：               0
```

入口：

- [`stages/README.md`](stages/README.md)：Stage 状态索引。
- [`stages/00-developer-bootstrap/`](stages/00-developer-bootstrap/)：Stage 00 设计。
- [`stages/01-python-language-foundations/`](stages/01-python-language-foundations/)：Stage 01 完整课程：7 个 Module、21 个 Unit 与七个源码里程碑。

Stage 01 的七个 Module、21 个 Unit 及必要源码、实验和练习已建设并通过作者检查，整体为 `BUILT`；真实学习者验证仍为 0，不标记 `VALIDATED`。验证范围见 [Stage 01 VERIFY.md](stages/01-python-language-foundations/VERIFY.md)。

## 10. 状态语义

- `PLANNED`：只有路线中的位置和能力方向。
- `DESIGNED`：教学边界、Unit 设计、前置、源码策略和验收已经明确。
- `BUILT`：该 Unit 必要材料已经完成，并通过 Technical Gate 与 Teaching Gate。
- `VALIDATED`：真实学习者跟做、迁移、解释、诊断或性能分析验证通过。

不是所有 Unit 都必须机械拥有源码、Lab、Exercise 和 Project 全套目录。是否需要由能力目标决定。

## 11. 最终判断标准

不再问：

```text
一共写了多少课？
README 有多少行？
有多少 pyproject.toml？
目录看起来是否足够庞大？
```

而问：

```text
为什么现在学这个是否清楚？
理论是否能解释真实代码和现象？
正文与源码是否严格对应？
源码为什么演进是否清楚？
学习者能否独立实现和迁移？
能否根据证据调试、诊断和优化？
能否根据约束比较方案？
能否在规模和条件变化时调整架构？
```
