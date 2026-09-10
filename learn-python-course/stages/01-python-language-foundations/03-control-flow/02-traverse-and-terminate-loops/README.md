# Unit 02 — 怎样处理一组任务并正确终止？

> 状态：`BUILT` · 前置：Unit 01 的业务分支、Module 02 的 `list[dict]`<br>
> 本章不保存另一份应用；完整控制流版本归属下一 Unit。

## 从“第一条”转向“每一条”

[集合版本](../../02-collections-and-mutable-state/03-shared-mutable-state/02-collection-model/)能访问 `tasks[0]`，但它不能回答“用户添加五条以后怎样显示全部”。手写五次索引既遗漏第六条，又会在只有两条时越界。真正稳定的规则不是“访问几个位置”，而是“对集合里的每条记录执行相同行为”。

`for` 每轮把下一个元素绑定给循环变量，不会自动复制记录。这里的 `task` 与列表里的字典指向同一个对象：

```pycon
>>> tasks = [{"id": 1, "done": False}, {"id": 2, "done": False}]
>>> for task in tasks:
...     task["done"] = True
>>> [task["done"] for task in tasks]
[True, True]

```

最后一行只是提前展示收集结果的简写，下一 Unit 会解释；这里也可以直接 `print(tasks)` 观察两个字典。若循环体改成 `task = {"done": True}`，就只会重新绑定临时名字，列表不会替换。这是 Module 02 的引用模型，不是循环新增的特殊复制规则。

空集合会执行零次循环体。因此空状态应在循环外判断，不能把“没有任务”放进循环体期待它执行。

## 数的是次数，还是数据？

如果业务要处理记录，就直接遍历记录。若要生成三次尝试的编号，才需要 `range`：

```pycon
>>> list(range(1, 4))
[1, 2, 3]
>>> list(range(3))
[0, 1, 2]
>>> list(range(3, 0, -1))
[3, 2, 1]
>>> list(range(3, 0))
[]

```

结束值不包含在结果中；步长方向也必须能走向结束值。`range` 是表示整数序列的对象，不是已经展开的列表；上面用 `list` 只是为了观察内容。零步长会产生 `ValueError`。

“显示第 1 项”与“任务 ID 为 1”不是同一件事。将来删除任务以后，位置会移动，业务 ID 不应移动。不要用 `tasks[task_id - 1]` 实现按 ID 查找。

## 查找有两种结束方式

要完成任务 7，应该逐条比较记录的 `id`。找到后停止；遍历结束仍未找到才报错：

```pycon
>>> tasks = [{"id": 3, "done": False}, {"id": 7, "done": False}]
>>> target_id = 7
>>> for task in tasks:
...     if task["id"] == target_id:
...         task["done"] = True
...         print("completed", target_id)
...         break
... else:
...     print("missing", target_id)
completed 7
>>> tasks
[{'id': 3, 'done': False}, {'id': 7, 'done': True}]

```

这个 `else` 与 `for` 对齐，不属于 `if`。它表达“循环没有被 `break` 中断而正常耗尽”。空列表也属于正常耗尽，因此会进入 `else`。不是“循环体从未执行”才进入，也不是“最后一次条件为假”才进入。

把 `target_id` 改成 99：每次比较都不成立，最终输出 `missing 99`。把列表改成空列表，结果相同。把 `break` 删掉：即使已经修改任务，仍会输出 missing。这是最有价值的回归用例，因为它同时检验成功路径和失败提示是否互斥。

异常向外传播时不会补执行 loop `else`。`continue` 只结束本轮、继续取下一个元素；若最终正常耗尽，仍执行 `else`。不要把 loop `else` 理解成清理资源的保证。

## 未知次数的交互为什么用 while

任务集合是有限的数据，命令会话却可能执行一次，也可能执行一百次。`while` 在每轮开始前重新判断条件；`while True` 需要循环体中真实可达的退出路径。先不用 `input`，用预置命令观察同一种控制关系：

```pycon
>>> commands = ["", "list", "quit", "add"]
>>> index = 0
>>> while index < len(commands):
...     command = commands[index]
...     index += 1
...     if not command:
...         continue
...     if command == "quit":
...         break
...     print(command)
list
>>> index
3

```

更新 `index` 必须发生在可能 `continue` 之前，否则遇到空命令时位置永远不变，循环不能前进。实际 CLI 每轮重新调用 `input`，新的输入就是推进条件；`quit` 是终止条件。

`break` 和 `continue` 只作用于最内层循环。完成任务时在内部 `for` 中 `break`，只停止查找，不退出外部命令会话。退出程序的 `break` 必须位于外部 `while` 的直接分支。这一区别会在下一 Unit 的测试中通过“完成之后继续 list”验证。

## 改记录与改集合是两件事

遍历时修改当前字典的 `done` 不会改变列表成员位置；遍历时删除列表成员却会移动后续元素，让某些元素被跳过：

```pycon
>>> ids = [1, 2, 3, 4]
>>> for task_id in ids:
...     ids.remove(task_id)
>>> ids
[2, 4]

```

这不是“Python 随机漏处理”。删除 1 后，2 移到位置 0，而下一轮前进到位置 1，拿到的是 3。修复取决于意图：若只需输出未完成任务，就跳过完成记录，不修改集合；若要批量删除，先收集目标，再单独删除，或构造新集合。不要为了规避一次 Bug 就无条件深复制整个应用。

## 迁移练习：只显示前两条未完成任务

使用下面的固定输入，不改原列表；显示遇到的前两条未完成任务的 ID。若没有未完成任务，输出 `No pending tasks.`。未完成任务只有一条时也必须正确。

```python
tasks = [
    {"id": 4, "done": True},
    {"id": 8, "done": False},
    {"id": 12, "done": False},
    {"id": 20, "done": False},
]
```

先决定计数器统计“检查过的记录”还是“实际显示的记录”，再写代码。这里的 `for...else` 不能直接判断是否显示过记录：只有一条待办时循环正常耗尽，但不应该输出空状态。

<details>
<summary>完成后对照：计数位置决定了契约</summary>

```pycon
>>> tasks = [
...     {"id": 4, "done": True},
...     {"id": 8, "done": False},
...     {"id": 12, "done": False},
...     {"id": 20, "done": False},
... ]
>>> shown = 0
>>> for task in tasks:
...     if task["done"]:
...         continue
...     print(task["id"])
...     shown += 1
...     if shown == 2:
...         break
8
12
>>> if shown == 0:
...     print("No pending tasks.")

```

验收还要替换成空集合、全完成、一条未完成，以及第一条就是未完成的输入。计数器属于一次展示，不能跨下一次 list 命令累积。程序是否终止、显示是否完整、源数据是否保持不变，是三个不同断言。

</details>

下一章把这些局部机制接回命令会话。到这里应能解释一次循环为什么继续、为什么停止，以及停止的是哪一层；不能只凭“运行后没卡住”判断正确。
