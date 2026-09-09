# Module 01.03 — Control Flow

> 状态：`DESIGNED`<br>
> 当前进度：Unit 01 `BUILT`；Unit 02～03 尚未建设<br>
> 核心问题：已经保存的数据怎样变成有规则、会重复执行并能正确结束的程序？<br>
> 进入状态：[`02-collection-model`](../02-collections-and-mutable-state/03-shared-mutable-state/02-collection-model/) 已能保存和修改多条任务，但只能按固定顺序运行一次<br>
> 退出状态：`03-control-flow-cli`

## 1. Module 目标

Module 02 已经建立 `list[dict]` 数据模型，却仍然只能：

```text
启动程序
→ 固定新增一条任务
→ 固定修改第一条任务
→ 固定显示第一条和最新任务
→ 程序结束
```

只要任务数量或用户意图变化，固定索引和线性语句就不再够用。本 Module 用同一条因果链引出控制流：

```text
业务规则需要在不同条件下选择行为
→ 任意数量的任务需要逐条处理
→ 用户不知道会执行多少次命令
→ 查找任务需要区分“找到并停止”和“遍历完仍未找到”
→ 命令、分支和循环组合成持续交互的 CLI
```

退出时，Task Tracker 第一次成为可连续使用的内存 CLI，支持：

```text
add
list
complete
quit
```

它仍然是一个开始变长的单文件脚本。重复、嵌套和难以独立测试的规则会成为 Module 04 引入函数的真实压力，而不是在本 Module 提前隐藏。

## 2. 已固定的行为决策

| 决策 | 本 Module 的选择 | 理由 |
|---|---|---|
| 初始任务集合 | 每次运行从空 `tasks` 开始 | 移除上一状态的教学预置数据，让空集合与首次新增都成为真实流程 |
| 数据生命周期 | 只保存在当前进程内存中 | 持久化不是控制流问题，不在本 Module 引入文件或数据库 |
| 业务 ID | `next_task_id` 从 `1` 开始，成功新增后递增 | ID 不依赖列表位置；无效输入不消耗 ID |
| 命令输入 | 去除首尾空白并转成小写 | ` ADD ` 与 `add` 表示同一意图 |
| 命令路由 | 对固定字面量使用 `match` | 命令词已经稳定，是离散模式选择；字段校验仍使用 `if` |
| 会话循环 | 一个 `while` 维持命令会话 | 执行次数由用户决定，不应猜测固定次数 |
| 集合处理 | `for` 直接遍历 `tasks`，每轮取得一个 task dict | 业务关心任务记录，不需要用 `range(len(tasks))` 绕回索引 |
| 查找任务 | `for...else` 表达“完整遍历后仍未找到” | `break` 与 loop `else` 在真实搜索语义中出现 |
| 错误恢复 | 当前命令失败后给出反馈，再返回命令提示 | 一个错误不应让整个交互会话崩溃或悄悄修改状态 |
| 正常结束 | 只有 `quit` 结束主循环并返回退出码 `0` | 终止条件明确、可测试；外部信号处理留到后续阶段 |

这些是本 Module 的施工契约。正式写 Unit 时可以优化文字和局部变量名，但不能无说明改变行为。

## 3. Unit 地图

| Unit | 计划目录 | 核心问题 | 教学形态 | 完成后多出的能力 |
|---|---|---|---|---|
| [01 — Readable Business Branches](01-readable-business-branches/) | `01-readable-business-branches/`（`BUILT`） | 怎样把业务规则写成可读分支？ | `CONCEPT` + Rule Comparison | 能用布尔条件和互斥分支表达任务规则，并解释分支顺序 |
| 02 — Traverse & Terminate Loops | `02-traverse-and-terminate-loops/` | 怎样处理一组任务并正确终止？ | `MECHANISM` + `BUILD` | 能为有限集合和未知次数交互选择不同循环，并证明终止条件 |
| 03 — Compose Interactive CLI | `03-compose-interactive-cli/` | 怎样把命令、规则和循环组合成可用 CLI？ | `BUILD` + `PROJECT` | 能完成、运行并验证 `add / list / complete / quit` 命令循环 |

三个 Unit 继续演进同一个 Task Tracker，不创建三套小项目。Unit 01 和 Unit 02 使用正文中的可运行片段建立模型；Unit 03 保存本 Module 唯一完整源码状态。

Unit 01 已建成，正文中的片段各自可运行，并附预期输出与迁移练习。Unit 02～03 的目录名和边界已固定，尚未创建目录；完整源码里程碑仍由 Unit 03 承接。

## 4. Unit 01 — Readable Business Branches

### 4.1 当前问题

上一状态已经有最小输入校验，但没有系统解释：

```text
一个 if 与另一个 if 是否都会执行？
什么时候应该使用 elif？
多个条件的先后顺序会不会改变结果？
空列表、空字符串、False 和 None 在条件中是什么关系？
```

### 4.2 必须讲清

- 比较表达式怎样产生布尔结果：`==`、`!=`、`<`、`<=`、`>`、`>=`。
- `and`、`or`、`not` 怎样组合条件，以及短路求值为什么会影响后续表达式是否执行。
- truthiness 怎样服务 `if not tasks`、`if not title` 和 `if task["done"]`。
- truthiness 是语言判断，不自动等于业务语义；需要区分 `None`、空文本和合法零值时必须显式判断。
- 多个独立 `if` 与互斥 `if / elif / else` 的行为区别。
- 分支顺序怎样从更具体规则走向兜底规则，避免宽条件遮住窄条件。
- 条件表达式只用于简单值选择；有多步副作用时仍使用普通分支。

### 4.3 Task Tracker 载体

围绕以下真实规则展开：

```text
标题为空            → 拒绝新增
优先级无法转换      → 拒绝新增
优先级不在 1～3     → 拒绝新增
任务集合为空        → list 显示明确空状态
任务已经完成        → complete 不重复修改
```

Unit 01 不建立完整命令循环，也不把所有规则写进最终脚本。它先让学习者能够预测一个条件为何进入某个分支，以及错误的分支结构会产生什么症状。

## 5. Unit 02 — Traverse & Terminate Loops

### 5.1 两类重复不能混为一谈

本 Module 同时存在两类重复：

```text
当前要处理的元素由 tasks 集合界定
→ 使用 for 逐个取得现有任务

用户接下来会输入多少次命令是未知的
→ 使用 while 维持会话直到 quit
```

学习者必须能根据终止条件选择循环，而不是只根据“我更熟悉哪个语法”。

### 5.2 必须讲清

- `for` 每次从 iterable 取得一个元素；当前直接遍历 `tasks`，每轮取得一个 task dict，不依赖业务 ID 与列表索引偶然相同。
- `while` 每轮先检查条件；条件设计错误会造成一次也不执行或无法终止。
- `break` 结束当前最近一层循环，不代表结束整个程序。
- `continue` 放弃当前轮剩余语句，适合无效命令或无效输入后回到会话入口。
- `for...else` 的 `else` 只在循环没有被 `break` 时执行；这里用于表达任务 ID 未找到。
- `range` 适合已知次数或整数序列，不因为学习了它就使用 `range(len(tasks))` 访问任务。
- 嵌套的命令循环、分支和搜索循环分别承担什么责任，避免把一个 `break` 的作用层级想错。

### 5.3 必须观察的失败

至少通过最小代码预测并验证：

```text
while 条件永远为真且没有可达 break
→ 会话无法正常终止

在找到目标后忘记 break
→ 搜索继续执行，for...else 语义也会改变

无效输入后忘记 continue
→ 后续代码可能使用不存在或不可信的数据

用任务 ID 直接当列表索引
→ 删除、空集合或 ID 不连续时访问错误记录
```

无限循环只能以受控、可立即停止的演示说明，不保存一个需要强制杀死的失败工程。

## 6. Unit 03 — Compose Interactive CLI

### 6.1 命令协议

主循环每轮读取一个命令：

```text
Command (add/list/complete/quit):
```

输入先执行：

```python
command = input("Command (add/list/complete/quit): ").strip().lower()
```

再通过字面量 `match` 路由：

```text
add       → 收集并校验一条任务，再加入集合
list      → 遍历并显示全部任务，空集合显示 No tasks.
complete  → 读取业务 ID，搜索并修改对应任务
quit      → 输出 Goodbye.，结束主循环
空命令     → 提示 Enter a command.，继续下一轮
其他命令   → 提示 Unknown command: <command>，继续下一轮
```

这里只使用 literal pattern 和 wildcard pattern。sequence、mapping、class pattern 与复杂 guard 不属于当前需求，不把 `match` 扩写成另一份语法清单。

### 6.2 `add` 契约

沿用前两版输入边界：

```text
title      → strip 后不得为空
priority   → 必须能转换为 int，范围 1～3
note       → strip 后为空则保存为 None
done       → 新任务固定为 False
id         → 使用 next_task_id
```

成功时：

```text
append 完整 task dict
→ 输出 Added task #<id>.
→ next_task_id 增加 1
→ 返回命令提示
```

任一校验失败时：

- 使用与前一源码状态一致的标题和优先级错误信息。
- 不追加半成品任务。
- 不增加 `next_task_id`。
- 不退出程序，直接回到下一轮命令提示。

### 6.3 `list` 契约

空集合输出：

```text
No tasks.
```

非空集合按加入顺序直接遍历，每条任务使用稳定格式：

```text
#1 [ ] Learn Python | priority=2 | note=(none)
#2 [x] Review control flow | priority=1 | note=Read loop else
```

`[ ]` 表示未完成，`[x]` 表示已完成。状态文本可以通过简单条件表达式得到；打印行为仍放在普通 `for` 中，不使用只为副作用服务的 comprehension。

### 6.4 `complete` 契约

```text
Task id: <text>
→ 转换为 int
→ for 遍历 tasks
→ 比较 task["id"]
```

结果只有三类：

```text
找到未完成任务  → 修改 done，输出 Completed task #<id>.，break
找到已完成任务  → 不重复修改，输出 Task #<id> is already complete.，break
完整遍历仍未找到 → 由 for...else 输出 Error: task #<id> does not exist.
```

非整数 ID 输出：

```text
Error: task id must be an integer.
```

错误之后会话继续，不暴露 traceback。

### 6.5 为什么不在主线强塞 comprehension

当前 `list` 命令需要逐条产生输出，`complete` 需要找到对象后修改并停止；普通 `for` 更直接。为了“覆盖 comprehension”而先创建临时列表，反而隐藏副作用与终止语义。

Unit 03 可以用最小对比解释：comprehension 适合从现有 iterable 构造一个新集合，不适合承载一串打印或混合修改。真正的 `list --pending` 集合筛选会在 Stage Project 中成为自然需求。

## 7. 源码所有权

本 Module 建成时只保存一个新主线里程碑：

```text
03-compose-interactive-cli/
└── 03-control-flow-cli/
    ├── README.md
    ├── task_tracker.py
    └── tests/
        └── test_task_tracker.py
```

它归属于真正组合完整业务流程的 Unit 03，并以 [`02-collection-model`](../02-collections-and-mutable-state/03-shared-mutable-state/02-collection-model/) 为明确基线。

主源码继续保持：

- 单文件、标准库、无第三方依赖。
- 不定义函数，不创建 Module 或 Package。
- 不使用 class、持久化、命令行参数解析库或第三方 CLI Framework。

黑盒测试可以继续使用测试辅助函数和 `subprocess`，但测试实现不是本 Module 的学习目标。学习者需要运行测试、阅读行为场景并解释证据。

本 Module 不规划 Focused Lab。分支、遍历、搜索和命令循环都能在同一业务主线中被清楚观察，拆出 Lab 只会割裂因果链。

## 8. 建设完成后的 Technical Gate

在未来的 `03-compose-interactive-cli/03-control-flow-cli/` 中执行：

```bash
python task_tracker.py
python -m unittest discover -s tests -v
```

黑盒测试至少覆盖：

| 输入会话 | 必须证明的行为 |
|---|---|
| `list → quit` | 空集合有明确反馈，`quit` 正常结束 |
| `add → list → quit` | 有效任务被规范化、分配 ID 并按稳定格式显示 |
| 连续两次 `add` | ID 依次为 1、2，加入顺序保持 |
| 三类无效 `add` 输入 | 空标题、非整数优先级和范围外优先级不修改集合，会话继续 |
| `add → complete → list` | 按业务 ID 找到任务并把 `done` 改为 `True` |
| 再次完成同一任务 | 状态保持完成，并给出幂等反馈 |
| 非整数或不存在的任务 ID | 明确报错，不修改其他任务，会话继续 |
| 空命令与未知命令 | 明确反馈后返回提示，不退出或卡死 |

全部场景必须满足：

- Python 3.14 下稳定完成，不依赖网络、时间或执行顺序。
- 最终输入流包含 `quit`，进程以退出码 `0` 结束。
- 错误路径不暴露 traceback，也不会产生半成品 mutation。
- 测试设置超时，能够发现不可终止的命令循环。
- 测试主要断言状态对应的行为证据，不把全部提示符拼成一个脆弱的大字符串。
- README 中的命令、输出、路径和源码一致。

## 9. Teaching Gate

审查本 Module 时必须确认：

- 分支由真实业务规则引出，循环由任意数量数据和未知次数交互引出。
- 学习者能解释两个独立 `if` 与互斥分支的区别，而不只是写出语法。
- truthiness 与业务缺失状态的边界准确，没有把所有 falsy 值混成同一含义。
- `for`、`while`、`break`、`continue` 和 loop `else` 都承担不同且可观察的责任。
- `match` 只在固定命令路由确实更清楚后出现，并与布尔条件分支区分。
- `range` 的适用条件被说明，但最终源码不使用 `range(len(tasks))` 绕开直接遍历。
- comprehension 的构造新集合语义被说明，没有为覆盖知识点强塞进副作用流程。
- `03-control-flow-cli` 真实继承前两版输入规则和 `list[dict]` 数据模型。
- 无效命令、无效字段和未找到任务都能恢复到会话循环，失败后状态不被污染。
- 单文件开始变长的成本被保留并解释，为 Module 04 创造真实函数需求。
- 没有提前引入函数、Package、class、持久化或异常体系设计。

## 10. Module Transfer Gate

不复制 Task Tracker，实现一个内存中的 Packing Checklist：

```text
add      → 新增有 id、name、packed 字段的物品
list     → 按加入顺序显示全部物品和打包状态
pack     → 按业务 ID 标记物品已打包
quit     → 正常结束会话
```

要求：

1. 从空集合启动，连续执行多条命令。
2. 空名称、未知命令、非整数 ID 和不存在的 ID 都给出反馈并继续会话。
3. `for` 负责显示和搜索，`while` 负责维持未知次数交互。
4. 找到物品后使用 `break`；完整搜索未找到时使用 loop `else`。
5. 重复 `pack` 同一物品不会把状态改回去。
6. 写出至少六条输入会话及其验收结果，不依赖手工临时观察。
7. 解释为什么物品 ID 不能直接当列表索引，为什么这里不需要 `range(len(items))`。

通过设计、正文、技术检查和迁移练习，只能说明本 Module 达到 `BUILT`。在真实学习者独立完成跟做与迁移前，不标记 `VALIDATED`。

## 11. 建设顺序

正式建设时按下面顺序推进：

```text
Unit 01 已完成正文、片段验证与教学审查
→ 写 Unit 02，审查循环选择和终止证明
→ 写 Unit 03 与唯一完整源码状态
→ 运行全部黑盒测试
→ 从 02-collection-model 重新走一遍演进
→ 完成 Technical Gate 与 Teaching Gate
→ 更新 Stage 01 状态导航
```

Unit 正文通过前不批量铺后续目录。只有三个 Unit、源码里程碑和完整门禁都完成后，Module 03 才从 `DESIGNED` 改为 `BUILT`。

## 12. 本 Module 不展开什么

```text
函数定义、参数、返回值与职责拆分       → Module 04
Module / Package / import             → Module 05
Task class 与对象协作                 → Module 06
编辑、删除、排序与 list --pending      → Module 07
Iterator / Generator 协议              → Stage 02
完整异常分类、恢复策略与 pytest         → Stage 06
文件、数据库与跨进程持久化              → 后续 Stage
信号、并发输入与终端控制                → 后续 Stage
```

本 Module 的完成标准不是“出现过所有控制流关键字”，而是学习者能根据业务条件、数据规模和终止规则选择正确结构，并用可运行会话证明程序能够继续、恢复和结束。
