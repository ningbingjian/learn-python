# Stage 01 — Python Language Foundations

> 状态：`BUILT`<br>
> 设计角色：后续 Stage 的 Golden Reference 设计基线<br>
> Python 基线：3.14<br>
> 前置：完成 Stage 00，能够从终端运行 Python、使用 uv 恢复项目并执行基础测试<br>
> 当前进度：7 个 Module、21 个 Unit 与七个主线源码里程碑均为 `BUILT`；真实 Learning Gate 尚未执行<br>
> 阶段目标：从“能运行脚本”成长为“能独立实现、拆分、测试并解释一个结构清晰的命令行应用”。

## 1. Stage 总问题

> **一个简单 Python 脚本，怎样一步一步成长为结构清晰、可维护的 CLI 应用？**

本阶段不按语法清单组织，也不会在最后突然布置一个与前文无关的项目。`CLI Task Tracker` 从第一个 Unit 就出现，随后成为七个 Module 共享的同一条源码主线：

```text
处理第一条任务
→ 管理一组任务
→ 形成可交互业务流程
→ 用函数划分职责和契约
→ 用 Module / Package 拆分单文件
→ 用对象稳定表达数据与行为
→ 独立完成、测试并迁移完整应用
```

Stage 00 已经负责源码、解释器、进程、终端运行和最小工程工作流。Stage 01 假定这些能力已经形成，第一分钟就开始写有业务意义的 Python。

## 2. 为什么它是 Golden Reference

Stage 01 是后续 Stage 的课程设计参考样本，不是一个新的完成状态。它必须率先兑现以下教学契约：

1. **问题驱动**：新知识必须解决上一版本已经出现的问题。
2. **连续演进**：同一个 Task Tracker 持续成长，不为每个术语切换一次项目。
3. **代码先于术语大全**：先观察代码现象，再建立足够准确的语言模型。
4. **源码归属明确**：里程碑属于真正产生变化的 Unit，不另建一套平行项目树。
5. **少量关键状态**：整个 Stage 只预设七次有意义的完整源码变化。
6. **机制按需隔离**：只有控制变量确有价值时才使用 Focused Lab。
7. **边界清楚**：当前问题不需要的高级语言机制留到后续 Stage。
8. **迁移而非照抄**：最终 Learning Gate 要求学习者闭卷完成正文未出现的新需求。

`Golden Reference` 描述课程设计角色，不替代状态语义。现在七个 Module、21 个 Unit、七个独立可运行主线里程碑及必要实验、练习、参考解已建设，并完成作者技术与教学审查。状态为 `BUILT`；没有真实学习者跟做与闭卷迁移记录，因此不标记 `VALIDATED`。可重复证据见 [VERIFY.md](VERIFY.md)。

## 3. 七个 Module 的因果链

| Module | 核心问题 | 进入时的主要痛点 | 退出时的源码状态 |
|---|---|---|---|
| [01.01 First Useful Python Program](01-first-useful-python-program/) | 一个脚本怎样真正处理用户数据？ | 只能运行文件，还不能表达任务数据 | `01-interactive-script` |
| [01.02 Collections & Mutable State](02-collections-and-mutable-state/) | 一条任务怎样变成一组可管理的任务？ | 单个名字无法表达集合与关系 | `02-collection-model` |
| [01.03 Control Flow](03-control-flow/) | 程序怎样形成真正可用的业务流程？ | 数据存在，但没有规则、遍历和交互循环 | [`03-control-flow-cli`](03-control-flow/03-compose-interactive-cli/03-control-flow-cli/) |
| [01.04 Functions & Contracts](04-functions-and-contracts/) | 脚本变长后怎样划分职责？ | 重复、嵌套和隐式约定开始累积 | [`04-function-oriented`](04-functions-and-contracts/03-state-and-scope/04-function-oriented/) |
| [01.05 Modules & Packages](05-modules-and-packages/) | 单文件为什么开始不可维护？ | 函数增多，职责和导入边界不清 | [`05-package-structured`](05-modules-and-packages/03-break-circular-dependencies/05-package-structured/) |
| [01.06 Classes & Object Collaboration](06-classes-and-object-collaboration/) | `dict + 函数` 什么时候已经不够？ | 数据结构脆弱，行为散落在外部函数 | [`06-object-model`](06-classes-and-object-collaboration/03-compose-task-collaborators/06-object-model/) |
| [01.07 Integration & Stage Project](07-integration-and-stage-project/) | 能否独立组合、测试并迁移全部能力？ | 各部分已形成，但尚未经过完整交付验证 | [`07-complete-task-tracker`](07-integration-and-stage-project/02-complete-and-verify-task-tracker/07-complete-task-tracker/) |

知识结构与项目演进结构必须重合。某个知识如果不能说明“为什么在当前版本出现”，就需要重新判断它的顺序、深度或载体。

## 4. Module 与 Unit 边界

### Module 01.01 — First Useful Python Program

核心问题：怎样从一个能运行的 Python 文件，写出第一个能接收、处理和输出业务数据的小程序？

- **[Unit 01：怎样让程序处理第一条任务？](01-first-useful-python-program/01-handle-first-task/)** 从 `input()`、`print()`、字符串和 f-string 建立最小交互，不重复讲解释器与进程。
- **[Unit 02：赋值时到底发生了什么？](01-first-useful-python-program/02-assignment-and-binding/)** 从真实任务字段建立 name、binding、object、type、rebinding 与 identity 的必要模型；自然引入 `str`、`int`、`bool` 和 `None`。
- **[Unit 03：用户输入为什么不能直接相信？](01-first-useful-python-program/03-trust-user-input/)** 处理输入始终是字符串、显式转换、基础校验、`ValueError`、`None` 与 falsy 的边界，并形成可靠的第一版交互脚本。

浮点数不是 Task Tracker 的自然核心需求。需要解释精度时，在 Unit 03 内使用一个小型 `float-precision` Focused Lab，不给主线硬加虚假字段。

### Module 01.02 — Collections & Mutable State

核心问题：一条任务怎样变成一组能够新增、访问、修改和去重的任务？

- **[Unit 01：任务集合应该选择什么数据形状？](02-collections-and-mutable-state/01-choose-task-data-shape/)** 围绕顺序、唯一性、键值关系和稳定记录比较 `list`、`tuple`、`dict` 与 `set`，建立 `list[dict]` 的当前模型。
- **[Unit 02：嵌套数据怎样读取和修改？](02-collections-and-mutable-state/02-read-and-update-nested-data/)** 连接索引、切片、容器方法、嵌套结构与 mutation；只讲当前模型真实使用的操作。
- **[Unit 03：为什么修改一个名字会影响另一个名字？](02-collections-and-mutable-state/03-shared-mutable-state/)** 通过备份任务列表失败的 Bug 讲清 reference sharing、aliasing、mutable / immutable、浅复制与明确复制边界。

共享可变对象的控制变量实验归属于 Unit 03。它解释主线中的真实 Bug，不另起一个互不相关的小项目。

### Module 01.03 — Control Flow

核心问题：已经保存的数据怎样变成有规则、会重复执行并能正确结束的程序？

- **[Unit 01：怎样把业务规则写成可读分支？](03-control-flow/01-readable-business-branches/)** 使用 `if / elif / else`、比较、布尔运算、truthiness 和简单条件表达式，解释条件求值、规则重叠与修改边界。
- **[Unit 02：怎样处理一组任务并正确终止？](03-control-flow/02-traverse-and-terminate-loops/)** 使用 `for`、`while`、`range`、`break`、`continue` 和必要的 loop `else`，区分“遍历数据”和“维持交互”。
- **[Unit 03：怎样把命令、规则和循环组合成可用 CLI？](03-control-flow/03-compose-interactive-cli/)** 用字面量 `match` 路由稳定命令，完成新增、查看、完成和退出流程；在集合变换自然出现时引入 comprehension，并说明何时普通循环更可读。

退出本 Module 时，Task Tracker 第一次成为真正可用的交互程序，但仍允许它是一个开始变长的单文件脚本。

### Module 01.04 — Functions & Contracts

核心问题：重复和嵌套开始妨碍修改后，怎样用函数建立职责与可测试契约？

- **[Unit 01：什么时候应该把代码抽成函数？](04-functions-and-contracts/01-extract-responsibilities/)** 从重复逻辑、命名困难和分支嵌套推导函数边界，而不是先背函数语法。
- **[Unit 02：参数和返回值怎样形成稳定契约？](04-functions-and-contracts/02-parameters-and-return-contracts/)** 覆盖 positional / keyword / default 参数、返回值、多值解包，以及 `*args` / `**kwargs` 的必要入口和适用边界。
- **[Unit 03：函数为什么会意外共享或修改状态？](04-functions-and-contracts/03-state-and-scope/)** 通过 mutable default argument 和作用域问题讲清参数绑定、mutation / rebinding、LEGB 与尽量显式的数据流。

本 Module 开始利用 Stage 00 的基础测试能力，为纯函数和关键规则增加自动化测试；完整 pytest 体系仍属于 Stage 06。

### Module 01.05 — Modules & Packages

核心问题：函数已经分清职责以后，为什么仍然需要拆分单文件？

- **[Unit 01：哪些职责应该成为独立 Module？](05-modules-and-packages/01-separate-module-responsibilities/)** 从 CLI 交互、任务操作和数据模型的变化频率推导文件边界与 import。
- **[Unit 02：程序入口和导入行为是什么关系？](05-modules-and-packages/02-entry-points-and-imports/)** 讲清 `__name__`、绝对 / 相对导入、Package 入口和最小可执行结构。
- **[Unit 03：循环导入为什么是设计信号？](05-modules-and-packages/03-break-circular-dependencies/)** 通过一次可复现失败识别双向依赖，调整责任方向和公开边界；完整 Import System 后置。

拆包不是为了模仿企业目录。只有当前职责和依赖关系需要时才增加文件与 Package。

### Module 01.06 — Classes & Object Collaboration

核心问题：什么时候“任务数据放在 dict、任务行为散落在函数”已经成为主要维护成本？

- **[Unit 01：为什么现在需要 class？](06-classes-and-object-collaboration/01-from-records-to-objects/)** 从字符串 Key、脆弱数据形状和散落行为出发，让 `Task` 成为数据与自身行为的稳定边界。
- **[Unit 02：实例状态和方法为什么需要 `self`？](06-classes-and-object-collaboration/02-instance-state-and-methods/)** 讲 class、instance、attribute、`__init__` 与 instance method，并用已有函数迁移验证模型。
- **[Unit 03：多个对象怎样协作而不互相创建一切？](06-classes-and-object-collaboration/03-compose-task-collaborators/)** 使用组合、依赖传入和清晰职责，让 CLI 与任务集合协作；不在本阶段展开完整 OOP。

本 Module 只覆盖 class、instance、state、method、`self`、`__init__`、composition 和 object collaboration。继承、多态、ABC、Protocol 与 Python Data Model 留在 Stage 02。

### Module 01.07 — Integration & Stage Project

核心问题：学习者能否不依赖逐行指令，把前六个 Module 的能力组合成可交付、可测试、可扩展的应用？

- **[Unit 01：怎样把需求转成实现与验收计划？](07-integration-and-stage-project/01-plan-requirements-and-acceptance/)** 固定命令、数据规则、错误场景、Package 边界和测试清单，识别前六版遗留问题。
- **[Unit 02：怎样完成并验证完整 Task Tracker？](07-integration-and-stage-project/02-complete-and-verify-task-tracker/)** 加入修改、删除、按状态筛选、可靠输入处理、运行文档和基础自动化测试，形成最终完整状态。
- **[Unit 03：能否闭卷完成一个未在正文出现的变化？](07-integration-and-stage-project/03-closed-book-transfer/)** 在不提供逐行答案的情况下增加 `due_in_days`、按既有优先级排序和 `list --due` 能力，并同步修改模型、函数、Package 与测试。

这不是“最后再做一次项目”。Module 07 负责集成、验收和迁移；项目的前六次实质演进已经分别属于前六个 Module。

## 5. 七个源码里程碑

| 状态 | 归属 Module | 上一版为什么不够 | 当前状态证明什么 |
|---|---|---|---|
| [`01-interactive-script`](01-first-useful-python-program/03-trust-user-input/01-interactive-script/) | 01 | 只有运行环境，没有业务程序 | 能接收、转换、校验并输出一条任务 |
| [`02-collection-model`](02-collections-and-mutable-state/03-shared-mutable-state/02-collection-model/) | 02 | 单条任务不能表达一组任务 | 能用合适容器管理内存状态并解释共享修改 |
| [`03-control-flow-cli`](03-control-flow/03-compose-interactive-cli/03-control-flow-cli/) | 03 | 数据没有形成业务流程 | 能用规则、遍历和交互循环完成基础操作 |
| [`04-function-oriented`](04-functions-and-contracts/03-state-and-scope/04-function-oriented/) | 04 | 单文件中的逻辑重复且难测试 | 职责由有明确参数和返回值的函数承接 |
| [`05-package-structured`](05-modules-and-packages/03-break-circular-dependencies/05-package-structured/) | 05 | 函数数量增加后文件与依赖边界模糊 | 应用可从明确入口运行，Module / Package 职责清楚 |
| [`06-object-model`](06-classes-and-object-collaboration/03-compose-task-collaborators/06-object-model/) | 06 | `dict` Key 脆弱且行为散落 | `Task` 对象稳定承接状态和自身行为，对象通过组合协作 |
| [`07-complete-task-tracker`](07-integration-and-stage-project/02-complete-and-verify-task-tracker/07-complete-task-tracker/) | 07 | 分项能力尚未经过完整交付 | 完整需求、错误路径、测试、文档和迁移任务通过验收 |

七个里程碑均归属实际产生变化的 Unit，独立保存完整源码、运行文档和测试。概念章节没有重复应用，闭卷参考解是练习答案，不计为第八个主线状态。

保存新状态前必须回答：

```text
上一版有什么？
→ 哪里开始难受？
→ 为什么当前知识能解决？
→ 修改了哪些责任、文件和行为？
→ 什么运行或测试证据证明变化？
→ 新设计又引入了什么成本？
```

## 6. Focused Lab 策略

以下五个 Focused Lab 已建设；仅在控制变量或隔离失败确有价值时使用：

| Lab | 归属 | 隔离理由 |
|---|---|---|
| [`float-precision`](01-first-useful-python-program/03-trust-user-input/float-precision-lab/) | Module 01 / Unit 03 | 与 Task Tracker 主线关系弱，但基础数值语义需要可观察证据 |
| [`shared-mutable-state`](02-collections-and-mutable-state/03-shared-mutable-state/shared-mutable-state-lab/) | Module 02 / Unit 03 | 需要控制变量观察 aliasing、mutation 与复制边界 |
| [`mutable-default-argument`](04-functions-and-contracts/03-state-and-scope/mutable-default-argument-lab/) | Module 04 / Unit 03 | 需要重复调用证明默认对象被意外共享 |
| [`scope-and-rebinding`](04-functions-and-contracts/03-state-and-scope/scope-and-rebinding-lab/) | Module 04 / Unit 03 | 需要最小实验区分查找、mutation 与 rebinding |
| [`circular-import`](05-modules-and-packages/03-break-circular-dependencies/circular-import-lab/) | Module 05 / Unit 03 | 独立进程比较双向依赖失败与职责修复 |

`append`、`pop`、负索引、keyword argument、`return` 等普通知识不单独建立 Lab 或工程。

## 7. Stage Project 验收

最终 `CLI Task Tracker` 至少支持：

```text
创建任务
查看全部任务
完成任务
修改任务
删除任务
按状态筛选
可靠输入处理与明确错误反馈
内存状态管理
清晰的 Module / Package 结构
基础自动化测试
从终端运行的清晰文档
```

验收分成两道 Gate：

### Guided Build Gate

学习者能够沿正文完成七次演进，并解释每次变化解决的问题、保存该状态的理由和新增成本。

### Closed-book Transfer Gate

学习者在不照抄正文的情况下完成以下变化：

> 给 `Task` 增加 `due_in_days`，支持按既有优先级排序，并新增 `list --due`，筛选今天到期且未完成的任务。0 与 None 必须区分；排序不改变正式集合顺序。

验收必须同时看到：

```text
数据模型修改正确
职责落在合适函数或对象
Package 边界没有被绕过
输入错误得到处理
原有与新增测试通过
学习者能解释自己的设计判断
```

Stage 只有经过真实学习者完成正文跟做与闭卷迁移，才有资格从 `BUILT` 进入 `VALIDATED`。

## 8. 本阶段明确不提前讲什么

```text
Iterator / Generator / Decorator / Context Manager
Python Data Model 与特殊方法体系
继承、Polymorphism、ABC、Protocol 与完整 OOP 设计
dataclass / Enum 的系统数据建模
高级 Typing、Generic、ParamSpec
Bytecode、PyObject、GC、GIL、Free Threading
Packaging、Wheel、PyPI 与依赖解析原理
完整 pytest / Mock / Property-based Testing
```

这些内容都有后续 Stage。必要时可以建立入口，但不能把后续答案倒灌到当前主线。

本项目也不提前使用：

```text
FastAPI / Django / Flask
Pydantic
SQLAlchemy / Database
Redis / Celery / MQ
Typer / Click
Docker
```

Stage 01 允许简单的内存状态、标准库 CLI 和朴素目录。它只因当前痛点自然变好，不从最终企业架构倒推第一天的设计。

## 9. 阶段验收能力

完成后，学习者应能够：

1. 用自己的话解释名字、绑定、对象、重新绑定和可变对象修改。
2. 根据数据语义选择基础类型与容器，并识别共享可变状态 Bug。
3. 写出包含分支、循环、集合处理和可靠输入处理的程序。
4. 用参数与返回值建立函数契约，解释默认参数和作用域的常见边界。
5. 把单文件程序拆成可运行、依赖方向清楚的 Module / Package。
6. 判断何时应该引入 class，并正确使用实例状态、方法和组合。
7. 用基础测试验证关键行为，说明测试证明了什么、没有证明什么。
8. 独立扩展 CLI Task Tracker 的新需求，而不是照抄正文。

## 10. 当前建设结果与学习验证

本阶段已完成 7 个 Module、21 个 Unit、七个主线源码里程碑、五个 Focused Lab，以及闭卷迁移题与独立参考解。源码从脚本、集合、控制流、函数、Package、对象到完整 CLI 连续演进，先前状态均保留。

- [整阶段验证与审查记录](VERIFY.md)：命令、覆盖范围、保留边界。
- [完整 Task Tracker](07-integration-and-stage-project/02-complete-and-verify-task-tracker/07-complete-task-tracker/)：编辑、删除、状态筛选和输入中断。
- [闭卷迁移验收](07-integration-and-stage-project/03-closed-book-transfer/)：新字段、排序、到期筛选与设计解释。

没有空 Unit 占位；概念章节不伪造源码副本。原 phase 课程仍独立维护，未被本次建设替换。

下一道门禁是收集真实学习者的 Guided Build 与 Closed-book Transfer 记录，而不是继续增加本 Stage 的术语数量。作者测试通过、目录完整和参考解可运行，都不能替代 Learning Gate；在有真实证据前，Stage、Module 与 Unit 最高保持 `BUILT`。
