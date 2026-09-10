# Unit 03 — 怎样把命令、规则和循环组合成可用 CLI？

> 状态：`BUILT` · 类型：BUILD / PROJECT<br>
> 起点：[02-collection-model](../../02-collections-and-mutable-state/03-shared-mutable-state/02-collection-model/)<br>
> 完整结果：[03-control-flow-cli](03-control-flow-cli/)

## 一次命令不是整个程序

前两章已经能解释分支和循环，但用户还不能连续使用应用。上一里程碑按作者预定的顺序执行一次；这一版把“下一步做什么”交给用户。数据形状仍是 `list[dict]`，新增的是控制权和会话生命周期。

原版本的预置任务用于观察容器，不是用户创建的数据。这一版删除预置记录，从 `tasks = []` 与 `next_task_id = 1` 开始。它们只在循环前初始化一次。若把初始化移入循环，会出现“add 提示成功，list 却为空”的故障；先打印集合长度可以排除输入失败，再检查重建集合的位置。

本章唯一新增文件中的主体是 `task_tracker.py`。它没有函数、类或导入；重复逻辑仍然可见，便于下一 Module 判断如何拆分。测试工具使用标准库启动应用，是作者提供的运行证据，不要求现在掌握测试工具的全部实现。

## 将命令选择与业务条件分开

循环每轮读取一次命令，先 `strip()` 再 `lower()`。字段并不全部小写：标题属于用户数据，命令属于约定词汇。

```python
command = input("Command (add/list/complete/quit): ").strip().lower()
match command:
    case "list":
        print("show tasks")
    case "quit":
        print("leave session")
    case "":
        print("Enter a command.")
    case _:
        print(f"Unknown command: {command}")
```

这是路由形状的摘录，尚不维护会话。`match` 按顺序尝试模式，执行首个匹配分支；字面量模式适合有限命令。`_` 是兜底，不是一个必须存在的变量。

不能写 `case quit:` 代替 `case "quit":`：裸名字是捕获模式，不是比较同名字符串。这里不讲结构化解包或模式匹配大全；标题是否为空、优先级是否合法仍是普通 `if` 的责任。`match` 不比 `if` 更高级，只是对当前稳定命令更直接。

## 新增的关键不是 append，而是何时 append

新增分为读取、校验、提交。标题空时立即报错并 `continue` 外层循环；优先级无法转成整数或不在 1～3 时也返回命令提示。只有必填字段全部可信，才读取备注、构造记录、追加并递增 ID。

这里故意不在标题失败后继续读取优先级。否则用户输入的下一条命令可能被当成字段，造成交互错位。

```python
task = {
    "id": next_task_id,
    "title": title,
    "priority": priority,
    "done": False,
    "note": note,
}
tasks.append(task)
print(f"Added task #{next_task_id}.")
next_task_id += 1
```

以上是提交段摘录。`note` 在此前已经用 `strip() or None` 归一化；必填标题不能用 None 代替错误。ID 仅在成功路径递增，所以一次失败之后第一次成功仍是 #1。先递增再校验会把被拒绝的输入也当作创建事件。

这里所谓提交只是内存修改的边界，不涉及数据库事务。外部终止输入还没有专门处理：本版正常退出必须输入 `quit`，最终 Module 才补 EOF 和 Ctrl-C。

## 查看与完成共享集合，但停止规则不同

`list` 用 `for` 直接遍历，保持新增顺序；空列表先打印 `No tasks.`。展示只读取记录，没有修改副作用。状态显示成 `[ ]` 或 `[x]`，缺失备注显示 `(none)`，而不是把 None 直接当成用户文字。

`complete` 先转换任务 ID，再按记录的 `id` 搜索。`int("0")` 可以成功，但不代表 ID 存在，因此“格式合法”与“业务存在”是两次判断。查找成功后，如果已完成，只反馈，不重复改变状态；未完成才设置 `done = True`。两条成功分支之后都必须 `break` 内层查找循环。

`for...else` 负责找不到。空集合、0、负数、99 都走不存在路径；`abc` 则在转换阶段拒绝，尚未进入搜索。用这一组输入可以定位错误到底在解析、搜索还是修改，而不只看到一个笼统“失败”。

## comprehension 是产出集合，不是藏起循环

当需要“未完成任务的 ID”作为一个新值时，循环可以表达为 comprehension：

```pycon
>>> tasks = [{"id": 1, "done": True}, {"id": 2, "done": False}]
>>> pending_ids = [task["id"] for task in tasks if not task["done"]]
>>> pending_ids
[2]
>>> len(tasks)
2

```

阅读顺序是“遍历 tasks，保留未完成项，再取 id”。它构造新列表，不会删除原任务。本版 list 命令仍展示全部任务，不提前增加 `list --pending`。

写 `[print(task) for task in tasks]` 会创建一份无用的 None 列表，还把展示副作用藏在表达式里；普通 `for` 更清楚。涉及多条语句、错误恢复或提前结束时，也不要硬塞进 comprehension。最终版有真实筛选需求时，才把这种集合变换接入主线。

## 运行证据必须覆盖一次完整会话

进入本章源码目录，运行：

```bash
python3.14 task_tracker.py
python3.14 -m unittest discover -s tests -v
```

Windows 可将 `python3.14` 换成 `py -3.14`。无第三方依赖；不需要为这份脚本另建项目配置。提示符会与输入同行，下列只列出依次输入的内容：

```text
add
Read functions
2

complete
1
list
quit
```

空行是可选备注，不可省略。应依次出现 `Added task #1.`、`Completed task #1.`、`#1 [x] Read functions | priority=2 | note=(none)` 与 `Goodbye.`。

测试不仅验证这些文字，还验证错误后继续、失败不消耗 ID、两条任务顺序、重复完成与缺失 ID 不修改状态。应用每次启动都是独立空集合；这些测试并不证明持久化、并发或真实用户学习效果。

## 不看源码的验收与下一次变化

迁移任务：为当前脚本增加 `count`，输出全部、已完成、未完成三个数量；不能修改任务，也不能将计数器放在会话外累积。验收输入为空、两条全未完成、完成一条、重复执行 count 四种情况。

<details>
<summary>参考判断与实现片段</summary>

在 match 的兜底分支之前新增字面量分支：

```python
case "count":
    done_count = 0
    for task in tasks:
        if task["done"]:
            done_count += 1
    print(f"all={len(tasks)}, done={done_count}, pending={len(tasks) - done_count}")
```

这是需嵌入 match 的分支，不是独立脚本。变量每次进入 count 时重建；它描述一次计算，不是应用持久状态。不要为了这一条新命令引入 class。

</details>

现在修改“优先级合法”的规则，需要在交互和其他潜在调用者间反复寻找代码；“完成任务”也只能通过整段会话测试。这才是下一 Module 抽函数的理由：让规则获得名字、参数、结果和独立证据，而不只是缩短文件。
