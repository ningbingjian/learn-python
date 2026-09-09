# Learn Python Course Teaching Guide v3.0

> 适用范围：`learn-python-course` 下所有 Stage、Module、Unit、教学章节、Example、Focused Lab、Exercise、Case 与 Project。
>
> 核心原则：**大纲体系化，正文书籍化，问题形成因果链，源码按能力变化自然演进，结论由证据支撑。**

## 1. 课程设计的最高目标

课程首先训练能力，而不是生产目录、README、代码文件和测试数量。

编写任何内容前先回答：

```text
学习者完成后必须真正理解什么？
学习者必须能够做什么？
他现在为什么需要这个知识？
最容易建立什么错误模型？
什么代码、实验、数据或故障证据能够证明理解？
怎样验证他能迁移，而不是只会照抄？
```

设计顺序：

```text
能力目标
→ 核心问题
→ 前置与学习障碍
→ 因果链和讲解顺序
→ 正文 / 源码 / 实验 / 案例
→ 练习与验收
→ 质量审查
```

禁止先决定“建几个项目、写几个类、凑几个测试”，再反推教学内容。

## 2. Unit 必须是问题闭环

Unit 不是一个孤立语法、API 或术语的容器。

不推荐：

```text
Unit: int
Unit: bool
Unit: append
Unit: @decorator syntax
```

推荐：

```text
怎样把文本输入转换成可信业务数据？
为什么共享可变对象会制造跨函数 Bug？
什么时候选择 list、tuple、dict 或 set？
为什么同步请求不应该直接承担长任务？
```

一个 Unit 可以在同一问题链中讲多个必要知识。知识点是否完整，不由目录数量证明。

## 3. Book-first：正文首先像一本正常技术书

正文主要负责：

```text
提出真实问题
→ 展示已有直觉、代码或系统
→ 说明它为什么不足
→ 建立概念和模型
→ 用代码 / 实验 / 数据证明
→ 解释边界、代价和替代方案
→ 形成可迁移结论
```

而不是反复出现：

```text
先点击这个目录
现在只记住一句话
暂时什么都不要理解
完成后再进入下一关
每一小节都重新创建项目
```

必要导航可以有，但正文篇幅必须主要用于技术内容。

标题优先表达技术问题或结论，不默认使用：

```text
Step 0
Step 1
Checkpoint 1
Snapshot 2
```

BUILD、OPS 等确实需要按顺序操作时可以使用步骤，但步骤只是表达方式，不是课程层级。

## 4. 先形成能力，再逐步深化模型

Python 入门不能采用：

```text
先完整理解 CPython Runtime
→ 再理解对象模型所有术语
→ 最后才允许写真实程序
```

更合理的是：

```text
先运行和修改程序
→ 处理输入与数据
→ 遇到共享引用、默认参数等真实问题
→ 建立准确语言模型
→ 在后续 Stage 进入运行时和源码
```

例如第一段 Python 程序只需要理解源码、解释器、入口和可观察行为。Bytecode、Frame、Evaluation Loop 和 PyObject 放到 CPython Runtime Stage；不能因为这些知识重要，就在 Hello World 后一次性倒灌。

“晚讲”不等于“不讲”，“建立入口”也不等于提前展开全部细节。

## 5. 因果链优先于知识清单

课程应让上一状态的问题成为下一知识存在的理由。

例如 Language Foundations：

```text
单文件保存少量数据
→ 数据增多，需要容器
→ 规则增多，需要控制流
→ 重复增多，需要函数
→ 单文件过长，需要 Module / Package
→ dict 与外部函数难以表达稳定对象，需要 class
```

例如 FastAPI：

```text
手写 ASGI 证明协议
→ 路由、校验、依赖和文档重复
→ FastAPI 提供更高层抽象
→ 框架便利带来隐式控制流
→ 通过 Starlette / ASGI / asyncio 解释边界
```

如果一个新概念不能回答“为什么现在出现”，通常说明顺序、范围或载体需要调整。

## 6. 教学类型

一个 Unit 可以组合以下类型。

### 6.1 THEORY

```text
问题
→ 直觉
→ 模型
→ 推导
→ 定义
→ 反例
→ 边界
→ 工程联系
```

适合一致性、复杂度、对象协议、事务隔离等内容。理论课不需要为了目录完整伪造源码。

### 6.2 CONCEPT

至少回答：

```text
是什么？
为什么出现？
不是什么？
和相邻概念有什么区别？
正例与反例是什么？
对工程设计有什么影响？
```

例如 coroutine、Task、Future 不能只给定义，必须建立关系和运行模型。

### 6.3 BUILD

```text
已有基线或首次创建项目
→ 新需求 / 缺陷
→ 必要理论
→ 按真实顺序修改
→ 运行与测试
→ 解释结果
→ 保存完整新状态
```

首次创建和演进已有项目的讲解职责不同，不能每次机械重讲 uv 入门。

### 6.4 MECHANISM

```text
先预测
→ 隔离主要变量
→ 运行实验
→ 观察证据
→ 推导规则
→ 建立机制模型
→ 测试边界
```

适合引用共享、descriptor lookup、event loop、connection pool、GC、cache、MVCC 等。

### 6.5 FAILURE

```text
症状
→ 建立多个假设
→ 收集证据
→ 排除错误假设
→ Root Cause
→ 修复
→ 回归
→ 防复发
```

不能看到异常名后直接公布答案。日志、traceback、metric、trace、dump、数据库状态等证据必须真正参与推理。

### 6.6 SOURCE

```text
已知现象
→ 固定 Python / Framework 版本
→ 最小触发入口
→ 断点、调用栈和关键状态
→ 核心源码路径
→ 回到外部行为
```

禁止从源码文件第一行开始翻译。源码课的目标是解释稳定现象、扩展点和边界，不是证明阅读行数。

### 6.7 PERFORMANCE

```text
目标与指标
→ workload / dataset / environment
→ baseline
→ profile / metric / trace
→ bottleneck hypothesis
→ 改变一个主要变量
→ re-measure
→ 对比收益和副作用
→ 容量、成本与边界
```

一次 benchmark、一次本机毫秒值或没有 warm-up / 数据集说明的结果不能支持性能结论。

### 6.8 DESIGN

```text
问题与约束
→ 方案 A / B / C
→ Trade-off
→ Failure Mode
→ 决策
→ ADR
→ 重新评估条件
```

避免“最佳实践”脱离场景。设计结论必须说明在什么条件下会改变。

### 6.9 CASE

真实案例重点解释：当时约束、候选方案、决策、结果、失误、修复和可迁移原则。不能把事后知道的答案伪装成当时显而易见。

### 6.10 OPS

重点是可执行操作、状态观察、风险、权限、备份、回滚和恢复验证。命令能执行不等于操作安全。

### 6.11 PROJECT

Project 必须有：

```text
背景与用户价值
约束与禁止项
里程碑
关键设计
运行与测试
验收标准
变化任务
复盘
```

Project 不是把前面示例复制到一个大目录，也不以组件数量证明“生产级”。

## 7. 文档与源码一一对应

需要源码支撑的章节必须满足：

> 当前 README 讲解当前目录源码；当前目录保存正文结束后的完整结果。

如果基于上一状态演进，章节开头应自然交代：

```text
本节基于哪个目录？
上一版本具备什么？
新需求或故障是什么？
为什么现有设计不足？
```

正文按真实修改顺序解释：

```text
原代码与职责
→ 为什么改
→ 改哪些文件和行为
→ 哪些部分不改及原因
→ 测试如何变化
→ 运行结果
→ 当前完整状态
```

可以使用 Before / After 和 diff 辅助，但不能用 diff 代替完整源码。

## 8. 什么内容进入主线，什么内容使用 Focused Lab

判断规则：

```text
新知识能自然解决主线当前问题
→ 在演进项目中讲

需要隔离一个语言 / 运行时 / 故障 / 性能变量
→ Focused Lab

只需要理论或设计推导
→ README / Case / ADR

需要组合能力
→ Module / Stage Project
```

典型 Focused Lab：

```text
float precision
mutable default argument
closure late binding
shared mutable state
asyncio cancellation
backpressure
GC cycle
GIL vs free-threaded
connection pool exhaustion
SQLAlchemy identity map
cache stampede
```

不要为了连续性把独立实验硬塞入业务项目，也不要为了独立性复制几十套相同脚手架。

## 9. Python 特有的纵向关系

课程后期必须把框架能力连接到语言、运行时、操作系统、网络和数据库。

### FastAPI

```text
FastAPI
↓
Pydantic + Starlette
↓
ASGI
↓
asyncio / threadpool boundary
↓
Socket / OS IO
```

### Pydantic

```text
Pydantic Model
↓
Annotation / Typing
↓
Class creation / schema generation
↓
Validation / serialization contract
```

不要把 Pydantic 简化成“Python 版 Java Bean”。

### SQLAlchemy

```text
ORM
↓
Session / Identity Map / Unit of Work
↓
Engine / Connection Pool
↓
DB-API / Driver
↓
TCP
↓
Database Transaction / MVCC / Lock
```

### Python 并发

```text
Thread / Process / Coroutine
↓
GIL / free-threaded / serialization / event loop
↓
CPython Runtime
↓
OS Scheduler / IO Multiplexing
```

### Packaging

```text
importable source
↓
project metadata
↓
build backend
↓
sdist / wheel
↓
resolver / environment / index
↓
reproducible delivery and supply chain
```

### AI 应用

```text
Model API / inference
↓
streaming / structured output / tool call
↓
retrieval / state / workflow
↓
evaluation / tracing / security
↓
model gateway / tenant / cost / reliability
```

纵向关系用于解释真实边界，不要求每节课都强行进入底层。

## 10. 跨语言比较

与 Java、JavaScript、Go 等语言比较可以帮助迁移已有知识，但必须遵守：

- 比较用于澄清，不替代 Python 自身模型。
- 不假设所有学习者都有同一种语言背景。
- 不把 Python 概念强行翻译成另一个生态的同名对象。
- 比较后必须回到 Python 的真实代码、协议和运行行为。

例如 `__init__` 可以与 constructor 对比，但必须说明对象创建与初始化不是完全相同的抽象。

## 11. 代码讲解要求

任何关键代码或修改至少说明：

```text
为什么需要它？
它承担什么职责？
输入、输出和副作用是什么？
运行时发生什么？
失败时会怎样？
测试证明什么，不能证明什么？
```

不要求逐行解释显而易见语法，也不能只给最终代码不解释因果。

示例名称应表达领域或机制。不要让所有文件、函数和类都叫：

```text
main.py
Demo
Example
Manager
Utils
Helper
```

## 12. 错误、边界和反例

核心概念至少包含一个有价值的错误理解、失败行为或边界条件。但不能每课机械复制同一份“常见误区”。

好的反例应满足：

- 它代表真实高概率误用。
- 它能暴露当前模型的必要性。
- 学习者可以运行、观察或推导。
- 修复后能解释为什么有效。

## 13. 测试与证据

自动化测试用于固定行为，不是装饰。

根据阶段选择：

```text
assert / doctest
pytest unit test
integration / contract / E2E
property-based test
benchmark / profile
fault injection
```

测试文件可以在前置未覆盖时由课程提供，但正文必须说明它当前只是验收工具；不能一边说“不需要理解测试”，一边让测试结构占据每个入门 Lesson 的主要注意力。

## 14. Progressive Depth

Unit 内可以标记 Must / Should / Expert：

```text
Must
→ 没有它无法形成当前主能力

Should
→ 工程中高频边界、故障和设计判断

Expert
→ 源码、性能、扩展机制和复杂权衡
```

Expert 内容必须服务当前问题。若完整机制在后续 Stage 有更自然的位置，应明确后置，不在入门阶段提前展开。

## 15. 学习者模型与前置知识

每个 Unit 必须写清实际依赖的能力，而不是泛泛写“有 Python 基础”。

前置已经系统学习过的工具不机械重讲；当前项目中首次出现的新边界必须介绍。

默认学习者第一次接触当前问题，但不意味着每一章都要重新解释 Terminal、uv、pytest 和目录创建。

## 16. Exercises 与 Learning Transfer

练习优先验证迁移能力：

```text
基于哪个完整状态
→ 新需求或新故障
→ 约束
→ 验收标准
→ 必要 Hint
→ Solution / Review Guide
```

避免只让学习者改一个常量、照抄正文或回答可以直接搜索标题的问题。

## 17. 版本、平台与可重复性

涉及版本差异的内容必须：

- 指明 Python / Framework / Database 的基线。
- 区分稳定契约和版本实现细节。
- 说明 macOS、Linux、Windows 差异是否影响结果。
- 命令、输出和测试应可重复。
- 源码分析与性能课程必须固定版本和环境。

## 18. 控制废话和模板污染

以下情况需要重写：

- 大量重复“现在打开文件”“只记住这一句”。
- 每个知识点都有相同的 20 节目录模板。
- README 很长，但删除导航后技术内容很薄。
- 每课固定复制“Challenge / Mastery Check / 下一课”，却没有真正迁移任务。
- 不同主题残留上一章类名、业务和编号。
- 一个 API 一个项目，没有状态演进价值。

结构应服务内容，不让模板替内容做决定。

## 19. AI / Generator 的使用边界

AI 可以辅助：

```text
目录与链接检查
代码格式与静态检查
测试生成初稿
多版本命令验证
重复内容检测
术语一致性检查
```

必须由人工判断：

```text
教学因果是否成立
Why 是否真实
理论模型是否准确
源码演进是否自然
性能结论是否有证据
故障根因是否经过排除
设计选择是否考虑约束
练习是否真正验证迁移
```

生成速度不能成为降低课程质量的理由。

## 20. 发布一个 Unit 前的自问

作者必须能用清楚、非模板化的话回答：

> 学习者为什么现在需要这个 Unit？它解决上一状态的什么问题？正文与源码如何互相证明？为什么这些源码状态值得保留？完成后学习者能独立做什么？什么证据表明他不只是照抄？
