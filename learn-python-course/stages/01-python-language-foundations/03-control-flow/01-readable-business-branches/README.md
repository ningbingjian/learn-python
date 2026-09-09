# Unit 01 — 怎样把业务规则写成可读分支？

> 状态：`BUILT`<br>
> 类型：`CONCEPT` + Rule Comparison<br>
> Python 基线：3.14<br>
> 前置：能够访问 `list[dict]` 中的任务、修改字段，并解释 `None`、输入转换与 `ValueError`<br>
> 完成证据：能预测分支路径、定位重复反馈，并根据规则重叠关系组织互斥判断

## 1. 数据已经能改，为什么还需要判断？

本 Unit 基于 Module 02 的 [`02-collection-model`](../../02-collections-and-mutable-state/03-shared-mutable-state/02-collection-model/)。其中的 [task_tracker.py](../../02-collections-and-mutable-state/03-shared-mutable-state/02-collection-model/task_tracker.py) 通过 `tasks[0]["done"] = True` 固定完成第一条任务。

这个动作证明了嵌套字典可以修改，却没有回答用户再次完成同一条任务时应该发生什么。已有标题、优先级和备注校验，也只负责让一次新增成功或失败；现在需要把“什么条件下做什么”明确写出来。

本节先假定已经拿到目标 task dict。按 ID 查找任务和反复接收命令分别属于后两个 Unit。我们要先把单次决策做对：任务未完成时修改状态，任务已完成时保持状态，并且每次只给出一种反馈。

下面每个 Python 代码块都可独立运行，不依赖前一个代码块留下的名字。可复制到临时脚本，用 Stage 00 已掌握的 `python <脚本文件名>` 执行；紧随代码的文本块是该段原样运行的输出。先预测，再运行，最后改动输入验证另一条路径。本 Unit 使用正文片段，不另存完整 CLI 里程碑。

## 2. 一个 `if` 决定一组语句是否执行

先处理“已经完成”的情况：

```python
task = {"id": 1, "title": "Learn Python", "done": True}

if task["done"]:
    print(f"Task #{task['id']} is already complete.")

print("Decision finished.")
```

```text
Task #1 is already complete.
Decision finished.
```

Python 先计算条件，再根据条件的真值决定是否执行缩进代码。冒号开始语句块，缩进界定块内有哪些语句；这里统一使用四个空格。

最后一行已经退回外层，所以无论 `done` 是 `True` 还是 `False`，正常执行到这里都会打印 `Decision finished.`。把 `done` 改成 `False` 再运行，应该只剩这一行。`if` 不会自动把后面所有语句都纳入条件。

需要处理互补的两种情况时，把它们写成一个决策：

```python
task = {"id": 1, "title": "Learn Python", "done": False}

if task["done"]:
    print(f"Task #{task['id']} is already complete.")
else:
    task["done"] = True
    print(f"Completed task #{task['id']}.")

print(task["done"])
```

```text
Completed task #1.
True
```

进入 `else` 时，`done` 原先为 `False`。字段赋值改变了状态，但程序不会回头重新判断同一个 `if`。下次处理这条任务时才会看到新的 `True`，走“已经完成”的路径。

因此，“执行前用什么状态判断”和“执行后状态变成什么”必须分开观察。

## 3. 为什么两个正确条件会产生重复反馈？

下面的代码看似把刚才的两种情况都写全了。先预测会打印几行：

```python
task = {"id": 1, "done": False}

if not task["done"]:
    task["done"] = True
    print("Completed.")

if task["done"]:
    print("Already complete.")
```

```text
Completed.
Already complete.
```

一个合理猜测是同一条任务被处理了两次；另一个猜测是第一次处理改变了第二次判断的输入。沿执行路径观察字段就能区分：这里没有循环，也只有一个字典，但第一个分支结束时 `done` 已经变为 `True`。

两个独立 `if` 是两个先后发生的判断，第二个会读取当时的状态。即使 `done` 与 `not done` 在同一时刻互补，也不能保证它们在不同时间只触发一个分支。

上一节的 `if / else` 正好表达“一次完成操作只选一种反馈”。回归时分别用 `False` 和 `True` 作为初始状态：应分别只打印完成消息和已完成消息，最终 `done` 都为 `True`。

不过，独立 `if` 本身没有问题。如果需要给任务同时显示两个互不排斥的提示，就应该独立判断：

```python
task = {"priority": 1, "note": None}

if task["priority"] == 1:
    print("Priority 1 task.")

if task["note"] is None:
    print("No note.")
```

```text
Priority 1 task.
No note.
```

这两种事实可以同时成立。分支结构应由“能否同时发生”决定，而不是看到两个条件就统一改成 `elif`。

## 4. 比较表达式把字段值变成条件

Task Tracker 的优先级必须是整数 `1～3`。对已经转换好的整数，可以直接计算比较结果：

```python
priority = 2

print(priority == 2)
print(priority != 2)
print(priority < 1)
print(priority > 3)
print(priority >= 1)
print(priority <= 3)
print(1 <= priority <= 3)
```

```text
True
False
False
False
True
True
True
```

在这里，`==` 比较值是否相等，`!=` 比较是否不等；`<`、`>` 不包括边界，`<=`、`>=` 包括边界。赋值用的 `=` 不承担比较职责。`is` 检查对象身份，不能用来判断优先级数值是否相等；判断缺失标记仍用已学过的 `is None`。

`1 <= priority <= 3` 是链式比较。对这里已经绑定的整数，它表达 `priority >= 1 and priority <= 3`。链式写法让允许区间一眼可见，也能避免误把“同时满足上下界”写成“满足任一边界”。

边界验收不能只试 `2`：

| priority | `1 <= priority <= 3` | 应有结果 |
|---:|---|---|
| 0 | `False` | 拒绝 |
| 1 | `True` | 接受下界 |
| 2 | `True` | 接受中间值 |
| 3 | `True` | 接受上界 |
| 4 | `False` | 拒绝 |

这些比较依赖输入已经是整数。字符串 `"2"` 要先经 `int()` 转换；`"high"` 引发的转换失败继续由之前学过的窄范围 `try / except ValueError` 处理。比较分支无法替代转换边界。

## 5. 组合条件时，先说清“同时”还是“任一”

“未完成且优先级为 1”要求两个事实同时成立；“低于 1 或高于 3”则只要一项成立就表示无效：

```python
task = {"done": False, "priority": 1}
priority = 4

print(not task["done"] and task["priority"] == 1)
print(priority < 1 or priority > 3)
print(not 1 <= priority <= 3)
```

```text
True
True
True
```

`not` 对条件取反；`and` 要求两边都为真值，`or` 接受任一真值。通常比较先于 `not`，然后是 `and`，最后是 `or`。混合条件较长时，用括号显示业务分组，或给中间结果取有意义的名字。

每个条件都要写完整。下面这个常见错误不会检查“priority 等于 1 或 2”：

```python
priority = 3

if priority == 1 or 2:
    print("BUG: accepted as 1 or 2.")

if priority == 1 or priority == 2:
    print("Accepted as 1 or 2.")
else:
    print("Not 1 or 2.")
```

```text
BUG: accepted as 1 or 2.
Not 1 or 2.
```

第一条条件实际组合了 `priority == 1` 和整数 `2`，不是两个比较。非零整数 `2` 为真值，因此错误分支仍然执行。关键问题是表达式的结构，而不是运算符失灵。

### 5.1 短路决定右边是否执行

Task Tracker 可能还没有任何任务，此时不能访问 `tasks[0]`。条件顺序可以守住访问的前提：

```python
tasks = []

if tasks and tasks[0]["done"]:
    print("First task is complete.")
else:
    print("No completed first task.")
```

```text
No completed first task.
```

`and` 先计算左边，左边为假值就已经能决定整体为假，不再计算右边；所以这里没有索引越界。把条件反写成 `tasks[0]["done"] and tasks`，访问会发生在空集合检查之前，触发 `IndexError`。

`or` 则在左边为真值时跳过右边。短路只保护没有被求值的表达式，不会修复缺失 Key：如果非空列表里的记录没有 `done` 字段，读取仍会触发 `KeyError`。

这个组合条件还把“没有第一条任务”和“第一条未完成”合并到了同一个 `else`。如果用户需要区分两种反馈，就应先用 `if not tasks` 分支处理空集合，再在 `elif` 中判断首条状态。

### 5.2 `and`、`or` 返回操作数，不保证返回 bool

上一模块使用 `note_text or None` 规范化备注，其结果不是布尔值：

```python
print(repr("Read chapter 3" or None))
print(repr("" or None))
print(repr([] and "not reached"))
print(repr("title" and "note"))
print(not "title")
```

```text
'Read chapter 3'
None
[]
'note'
False
```

`and` 遇到左边为假值就返回左操作数，否则返回右操作数；`or` 遇到左边为真值就返回左操作数，否则返回右操作数。`not` 才总是给出布尔结果。`if` 再对表达式的结果做真值判断。

如果只需选择语句是否执行，无须把每个表达式都包进 `bool()`。但若要保存一个真正的布尔字段，不能因为使用了 `and` 或 `or` 就假定结果一定是 `True` 或 `False`。

## 6. 真值相同，业务含义仍可能不同

观察几个已经熟悉的值：

```python
print(bool(None))
print(bool(False))
print(bool(0))
print(bool(""))
print(bool([]))
print(bool({}))
print(bool("   "))
print(bool("False"))
```

```text
False
False
False
False
False
False
True
True
```

`None`、`False`、数值零和空容器在条件中为假值，但并不表示相同业务状态。纯空格和 `"False"` 都是非空字符串；`bool()` 不负责去除空白，也不把文字解析成真假。

因此，标题必须先 `.strip()` 再判断，`done` 则依赖输入模型保证它是 bool。记录如果错误地保存了字符串 `"False"`，`if task["done"]` 会进入真分支；修复应回到数据来源，而不是到处与字符串比较。

本课后面的迁移练习会引入可选预计分钟数，并规定 `0` 表示“立即处理”、`None` 表示“尚未估计”。对这种新契约，照搬备注的默认值写法就会出错：

```python
estimated_minutes = 0

print(estimated_minutes or "Not estimated")

if estimated_minutes is None:
    print("Not estimated")
else:
    print(f"Estimate: {estimated_minutes} minutes")
```

```text
Not estimated
Estimate: 0 minutes
```

两个结果不同，是因为第一种写法把所有假值都当成缺失，第二种只把 `None` 当成缺失。这个预计分钟数字段只用于练习，不修改当前主线数据模型。

## 7. 规则重叠时，分支顺序就是业务优先关系

假设界面要给一条任务显示一个摘要：已经完成时显示 `Complete`；未完成且优先级为 1 时显示 `Pending (priority 1)`；其他未完成任务显示 `Pending`。

先看一个故意把“未完成”宽条件放在前面的版本：

```python
task = {"done": False, "priority": 1}

if not task["done"]:
    label = "Pending"
elif not task["done"] and task["priority"] == 1:
    label = "Pending (priority 1)"
else:
    label = "Complete"

print(label)
```

```text
Pending
```

第二个条件可能为真，却没有机会被计算。一条 `if / elif / else` 链自上而下选择第一个真条件，执行对应块后离开整个选择结构；`else` 是前面条件都不成立时的兜底。

本需求可以先处理“完成优先显示”，再利用这条路径已经排除完成状态的事实：

```python
task = {"done": False, "priority": 1}

if task["done"]:
    label = "Complete"
elif task["priority"] == 1:
    label = "Pending (priority 1)"
else:
    label = "Pending"

print(label)
```

```text
Pending (priority 1)
```

进入 `elif` 时已经知道 `done` 为 `False`，所以无需再写一遍 `not task["done"]`。不过这个简化依赖当前分支顺序；单独拿走条件时，要重新确认它依赖的前提。

用重叠处验收规则比只跑默认数据更有价值：

| done | priority | 摘要 |
|---|---|---|
| `True` | 1、2 或 3 | `Complete` |
| `False` | 1 | `Pending (priority 1)` |
| `False` | 2 或 3 | `Pending` |

摘要只是解释分支优先关系的正文片段，最终 CLI 的显示格式仍由 Module README 约定。规则是否先检查某个条件，应由业务优先关系决定；并不存在脱离需求的“条件越长就必须越靠前”。

## 8. 校验分支必须真正阻止后续修改

只打印错误不等于拒绝数据：

```python
tasks = []
title = "   ".strip()

if not title:
    print("Error: title cannot be empty.")

tasks.append({"title": title})
print(len(tasks))
```

```text
Error: title cannot be empty.
1
```

`append()` 在 `if` 外，程序完成错误提示后会继续执行它。这段故意精简的反例表明：错误反馈和控制路径是两件事。原里程碑用 `raise SystemExit(1)` 终止当前单次运行，才避免无效任务进入集合。

本节也可以在普通分支中明确圈住允许修改的区域。下面假设文本已清理、优先级已完成整数转换，只观察业务校验：

```python
tasks = []
title = "Review branches"
priority = 2
note = None

if not title:
    print("Error: title cannot be empty.")
elif not 1 <= priority <= 3:
    print("Error: priority must be between 1 and 3.")
else:
    task = {
        "id": 1,
        "title": title,
        "priority": priority,
        "done": False,
        "note": note,
    }
    tasks.append(task)
    print("Added task #1.")

print(len(tasks))
```

```text
Added task #1.
1
```

只有前面校验都没有拒绝数据，才会执行 `else` 中的记录创建和 `append()`。将标题改为 `""`，应打印标题错误和 `0`；将优先级改为 `0` 或 `4`，应打印范围错误和 `0`。两个字段同时无效时，这份规则优先报告标题错误。

如果改回真实 `input()`，仍要先清理文本并处理整数转换失败，才能到达这里。这个片段没有取代完整输入处理，也没有生成第三个源码里程碑。

Unit 03 的会话将改为命令失败后继续接收命令，届时 `continue` 会表达“结束本轮”。当前先明确每条校验到底阻止了哪些操作。

## 9. 简单值选择可以写成条件表达式

显示完成标记只需要在两个字符串中选一个：

```python
task = {"done": False}
marker = "[x]" if task["done"] else "[ ]"
print(marker)
```

```text
[ ]
```

条件表达式先求条件，再只求被选中的那个分支表达式，最后得到一个值。虽然真分支在文本中位于条件前面，它并不是先执行的。

这里两个选项都短，结果又赋给了 `marker`，读者很容易辨认它的职责。如果要修改字典、打印不同反馈并记录额外信息，普通 `if / else` 更能显示执行顺序。把多个动作挤进条件表达式并不会减少决策的复杂度。

## 10. 迁移：用重叠规则决定一条任务能否开始

基于本 Unit 引用的 `02-collection-model` 中一条任务记录，在临时脚本里新增 `blocked` 和 `estimated_minutes` 两个练习字段。直接处理一条记录，不实现搜索或菜单。

输入契约：`done`、`blocked` 均为 bool，`estimated_minutes` 为 `None` 或非负整数，其中 `0` 合法。此题只验证内部规则，不要求新增终端解析。

规则按下面顺序决定唯一的 `decision`：

1. 已完成：`Already complete`，不允许开始。
2. 未完成但被阻塞：`Blocked`，不允许开始。
3. 未完成、未阻塞但尚未估计：`Estimate required`，不允许开始。
4. 其余情况：`Ready`，允许开始，包括预计分钟数为 `0` 的情况。

要求得到一个字符串 `decision` 和一个 bool `can_start`；判断过程中不修改原任务。验收至少覆盖：

| done | blocked | estimated_minutes | decision | can_start |
|---|---|---|---|---|
| `True` | `True` | `None` | `Already complete` | `False` |
| `True` | `False` | 0 | `Already complete` | `False` |
| `False` | `True` | `None` | `Blocked` | `False` |
| `False` | `True` | 0 | `Blocked` | `False` |
| `False` | `False` | `None` | `Estimate required` | `False` |
| `False` | `False` | 0 | `Ready` | `True` |
| `False` | `False` | 15 | `Ready` | `True` |

先独立写出代码，再与表格逐行核对。这里的难点是多个条件同时为真时谁优先，以及怎样让合法零值通过；只把 Task 改名无法完成判断。

<details>
<summary>完成后展开：参考实现与判断理由</summary>

先把唯一的决策结果确定下来，再从它推导是否允许开始，可避免维护两套可能矛盾的条件：

```python
task = {
    "id": 1,
    "title": "Review branches",
    "priority": 2,
    "done": False,
    "note": None,
    "blocked": False,
    "estimated_minutes": 0,
}

if task["done"]:
    decision = "Already complete"
elif task["blocked"]:
    decision = "Blocked"
elif task["estimated_minutes"] is None:
    decision = "Estimate required"
else:
    decision = "Ready"

can_start = decision == "Ready"
print(decision)
print(can_start)
print(task["done"])
```

```text
Ready
True
False
```

第一条分支优先处理终态，第二条排除阻塞，第三条只识别 `None`。因此 `0` 可以到达 `Ready`。赋值目标是新的名字，代码没有对 `task` 做字段赋值。

另一种可行方案是在每个分支同时赋值 `decision` 和 `can_start`，但需要确保所有分支都赋值且两个结果始终一致。当前方案的成本是 `can_start` 依赖 `"Ready"` 这个字符串约定；以后状态种类增加，才需要重新评估表示方式。

</details>

完成后再回答：为什么两个独立 `if` 会看到不同的状态？为什么 `or` 不一定返回 bool？为什么用 `if not estimated_minutes` 会破坏这份新契约？修改哪一组重叠输入最能证明你的分支顺序正确？

## 11. 本 Unit 的完成边界

目前已经能为一条记录选择路径、解释判断顺序，并把状态修改限制在允许的分支中。材料采用正文中的独立片段，不需要第三方运行依赖；这些纯语言示例没有平台专用路径或终端操作。

本次作者验证在 Python 3.14 下完成：17 段独立片段与各自输出逐一对应，补测完成状态、空集合保护、六种摘要组合、七组新增校验和十二种迁移组合，共 30 组补充输入；反转短路顺序及缺失 `done` 字段分别产生预期的 `IndexError` 和 `KeyError`。所有片段通过 Ruff 隔离模式下的 `E4,E7,E9,F` 检查与格式检查。此处保留了用于教学的恒真条件和常量真值观察；启用简化规则时会出现提示，不能把它们自动改写后仍声称保留了原实验。

本 Unit 的 `BUILT` 表示正文、练习和上述技术及教学审查完成；尚无真实学习者跟做与闭卷迁移证据，因此不是 `VALIDATED`。Module 03 整体仍为 `DESIGNED`。

下一 Unit 将处理任意数量的任务和未知次数的交互。循环职责与终止规则见 [Module 03 设计](../README.md#5-unit-02--traverse--terminate-loops)。完整命令路由、`match` 和 `03-control-flow-cli` 源码里程碑由 Unit 03 承接。

语言语义可对照 Python 3.14 官方资料：[if 语句](https://docs.python.org/3.14/tutorial/controlflow.html#if-statements)、[真值测试](https://docs.python.org/3.14/library/stdtypes.html#truth-value-testing)、[布尔运算](https://docs.python.org/3.14/reference/expressions.html#boolean-operations)与[条件表达式](https://docs.python.org/3.14/reference/expressions.html#conditional-expressions)。
