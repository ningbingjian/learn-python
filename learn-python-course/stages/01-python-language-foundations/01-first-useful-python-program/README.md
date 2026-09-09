# Module 01.01 — First Useful Python Program

> 状态：`BUILT`<br>
> 核心问题：怎样从一个能运行的 Python 文件，写出第一个能接收、处理和输出业务数据的小程序？<br>
> 进入能力：能够从终端运行 Python 文件，并能根据 Stage 00 的说明执行基础测试<br>
> 退出状态：[`01-interactive-script`](03-trust-user-input/01-interactive-script/)

## 1. Module 目标

Stage 00 已经解决“文件在哪里、哪个 Python 在运行、怎样从终端执行”的问题。本 Module 不再从解释器、进程或工程工具重新开始，而是在第一课直接创建一条真实任务。

主问题链只有一条：

```text
让程序接收第一条任务
→ 发现任务需要多种业务状态
→ 用代码现象建立 name / object / binding 模型
→ 发现所有 input 都先得到文本
→ 在输入边界完成清理、转换和校验
→ 交付第一个可靠的交互脚本
```

完成后，学习者应该能独立写出一个处理单条业务记录的交互脚本，而不只是复述 `input()`、`int()` 或 `None` 的定义。

## 2. Unit 地图

| Unit | 核心问题 | 教学形态 | 完成后多出的能力 |
|---|---|---|---|
| [01 — Handle First Task](01-handle-first-task/) | 怎样让程序处理第一条任务？ | `CONCEPT` + Micro Exercise | 能接收、清理并回显一段文本 |
| [02 — Assignment & Binding](02-assignment-and-binding/) | 赋值时到底发生了什么？ | `CONCEPT` + Mechanism Observation | 能解释任务字段对应的名字、对象、类型与重新绑定 |
| [03 — Trust User Input](03-trust-user-input/) | 用户输入为什么不能直接相信？ | `BUILD` + `FAILURE` + Focused Lab | 能清理、转换、校验输入并交付完整脚本 |

三个 Unit 不是三套项目。前两个 Unit 使用正文中的最小代码观察现象；第三个 Unit 承接唯一完整源码状态，避免为每个术语复制工程。

## 3. 源码所有权

本 Module 只保存一个主线里程碑：

```text
03-trust-user-input/
└── 01-interactive-script/
    ├── README.md
    ├── task_tracker.py
    └── tests/
        └── test_task_tracker.py
```

它归属于真正完成输入边界的 Unit 03。Unit 01 和 Unit 02 的代码尚未形成值得独立保存的数据模型、责任边界或运行结构，因此只在正文中保留可直接运行的小例子。

浮点精度与 Task Tracker 主线没有自然关系，但基础数值语义值得观察，因此使用 Unit 03 内的独立 [`float-precision-lab`](03-trust-user-input/float-precision-lab/) 控制变量。

## 4. 建议学习顺序

1. 完成 Unit 01，亲手输入并回显第一条任务标题。
2. 完成 Unit 02，不运行代码也能预测赋值、重新绑定、`type()`、`None` 与空字符串的结果。
3. 完成 Unit 03，先观察失败，再运行最终脚本和自动化测试。
4. 闭卷完成 Unit 03 的 `estimated_minutes` 迁移练习。
5. 用下面的 Gate 检查能力，不按阅读时长判断完成。

## 5. Technical Gate

在 `03-trust-user-input/01-interactive-script/` 中执行：

```bash
python task_tracker.py
python -m unittest discover -s tests -v
```

在 `03-trust-user-input/float-precision-lab/` 中执行：

```bash
python float_precision.py
```

必须满足：

- 正常输入返回退出码 `0`，并显示标题、优先级、完成状态和可选备注。
- 空标题、非整数优先级和范围外优先级返回退出码 `1`，且不暴露 traceback。
- 标准库自动化测试全部通过，不需要安装第三方依赖。
- 浮点实验可以稳定观察 `0.1 + 0.2` 与 `0.3` 的差异。
- README 中的命令、文件名和输出与当前源码一致。

## 6. Teaching Gate

审查本 Module 时必须确认：

- 第一课直接写有业务意义的 Python，没有重复 Stage 00。
- name、object、binding、type 等术语都由 Task Tracker 代码现象引出。
- `str`、`int`、`bool` 和 `None` 服务真实字段，不是类型 API 清单。
- 浮点精度被隔离在 Focused Lab，没有给主线硬造虚假需求。
- `if` 和 `try / except` 只用于建立最小输入边界；系统控制流与异常设计仍留在后续 Module / Stage。
- 测试用于证明用户可观察行为，没有要求初学者先理解 `subprocess` 实现。
- 练习要求迁移当前能力，没有提前使用集合、函数、Package 或 class。

## 7. Module Transfer Gate

不查看最终源码，为 Task Tracker 增加一个可选的 `estimated_minutes` 输入：

```text
留空
→ 保存为 None

输入整数 5～480
→ 保存并显示该整数

输入非整数或范围外数字
→ 显示明确错误并以退出码 1 结束
```

学习者必须能够解释：

1. 为什么 `input()` 的结果不能直接当作整数。
2. 为什么空字符串与 `None` 不是同一个状态。
3. 转换和范围校验为什么都应该发生在输入边界。
4. 每个名字当前绑定到什么类型的对象。

通过正文、技术检查和迁移练习，只能说明本 Module 达到 `BUILT`。在真实学习者独立完成跟做与迁移前，不标记 `VALIDATED`。

## 8. 本 Module 不展开什么

```text
list / dict / set 与共享可变状态  → Module 02
完整 if / loop / match 模型       → Module 03
函数契约与作用域                  → Module 04
Module / Package / import         → Module 05
class 与对象协作                  → Module 06
异常体系与 pytest 深入            → Stage 06
Bytecode 与 CPython Runtime       → Stage 11
```

这里只建立后续课程需要的入口，不把后续答案倒灌到第一个程序。
