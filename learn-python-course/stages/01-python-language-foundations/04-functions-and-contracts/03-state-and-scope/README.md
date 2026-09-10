# Unit 03 — 函数为什么会意外共享或修改状态？

> 状态：`BUILT` · 类型：MECHANISM / FAILURE / BUILD<br>
> 起点：[03-control-flow-cli](../../03-control-flow/03-compose-interactive-cli/03-control-flow-cli/)<br>
> 完整结果：[04-function-oriented](04-function-oriented/)

## 第一次调用正确，第二次为什么带着旧数据？

如果把任务列表作为默认参数，单次测试往往看不出问题：

```pycon
>>> def collect(title, tasks=[]):
...     tasks.append(title)
...     return tasks
>>> first = collect("Read")
>>> second = collect("Test")
>>> first, second
(['Read', 'Test'], ['Read', 'Test'])
>>> first is second
True

```

先提出两个假设：返回时复制失败；或者两次调用从一开始就拿到了相同列表。最后的身份比较与函数刚进入时的列表内容可以区分它们。默认表达式在执行 `def` 时求值，而不是每次调用都求值；之后省略实参就重复绑定同一个默认对象。

修复要决定谁拥有列表，而不只是换一种写法：

```pycon
>>> def collect(title, tasks=None):
...     if tasks is None:
...         tasks = []
...     tasks.append(title)
...     return tasks
>>> collect("Read"), collect("Test")
(['Read'], ['Test'])
>>> owned = []
>>> collect("Read", owned) is owned
True

```

None 表示“调用者没有提供集合”，此时函数创建新的；显式传入集合则修改那个集合。不能写 `tasks = tasks or []`：调用者传入合法空列表时，它也是假值，会被新列表替换，破坏共享修改的承诺。

[默认参数实验](mutable-default-argument-lab/)保留错误与修复的连续输出，供先预测再运行。本应用更直接：`run_cli` 自己创建会话列表，`add_task` 必须显式接收它，根本不需要可变默认值。

## 作用域查找与对象修改不是同一个问题

LEGB 是普通函数中理解名字查找的入口：Local、Enclosing、Global、Builtins。外层函数局部名字不同于模块全局名字；“global”指所在模块，不是整个程序共享仓库。

```pycon
>>> label = "module"
>>> def outer():
...     label = "enclosing"
...
...     def inner():
...         return label
...
...     return inner()
>>> outer()
'enclosing'
>>> label
'module'

```

函数内对某个名字赋值，通常使这个名字成为该函数局部名字，即使赋值语句还没执行。下面故意复现 UnboundLocalError：

```pycon
>>> counter = 0
>>> def broken():
...     counter += 1
...     return counter
>>> broken()
Traceback (most recent call last):
...
UnboundLocalError: ...

```

`+=` 需要先读取局部 counter，再重新绑定，但它尚未有值。不是外层变量不存在，也不是整数“不允许加一”。可用 `global` 或 `nonlocal` 明确要重新绑定外层名字，但在当前应用里显式传入并返回更容易测试：

```pycon
>>> def advance(counter):
...     return counter + 1
>>> counter = advance(counter)
>>> counter
1

```

[作用域实验](scope-and-rebinding-lab/)对比列表 mutation 与局部 rebinding。不要为了修复作用域错误，给所有变量加 global；这样调用顺序就会成为隐藏输入。

## 参数传入的是对象绑定

```pycon
>>> def change(items):
...     items.append("visible")
...     items = ["local"]
...     return items
>>> original = []
>>> returned = change(original)
>>> original, returned
(['visible'], ['local'])

```

append 修改两端共同引用的对象；赋值只让函数内名字改指向。Python 不是自动深复制参数，也不是让函数任意重新绑定调用者变量。这个模型同时解释默认参数、列表修改和下一个 ID 必须回传，不需要三套互相矛盾的口诀。

## 将前两章的责任落到完整版本

函数版仍只有 `task_tracker.py`，但现在责任可单独访问：

| 函数 | 输入与结果 | 状态影响 |
|---|---|---|
| clean_fields | 字段 → 归一化三元组 | 无 |
| parse_priority / parse_task_id | 文本 → 整数或 ValueError | 无 |
| add_task | 集合、ID、字段 → 记录与下一 ID | 成功才 append |
| find_task | 集合、业务 ID → 原记录 | 无 |
| complete_task | 集合、ID → 是否发生完成 | 修改找到的记录 |
| format_task | 记录 → 显示行 | 无 |
| run_cli | 一次终端会话 | 拥有列表与计数器，负责输入输出 |

`run_cli` 的 `try` 接收当前命令中的预期 ValueError 并统一显示。它没有裸 `except`；程序错误不应该伪装成用户输入错误。此版仍要求 quit 正常退出，EOF 与 Ctrl-C 的产品契约放在最终集成章。

运行源码目录中的 `python3.14 task_tracker.py`；验证用 `python3.14 -m unittest discover -s tests -v`。旧会话测试仍在，新规则测试补充无副作用、原对象身份、失败不修改列表等断言。没有引入 pytest 体系或高级类型工具。

## 迁移：隔离两份调用方状态

给 `add_task` 传入两个独立列表，交替新增、完成；要求每份列表的 ID 从各自 1 开始，并证明修改 A 不影响 B。随后故意让两个名字绑定同一列表，解释为何隔离失效。

<details>
<summary>参考推理</summary>

隔离依赖于调用方提供不同列表以及维护不同 next_id，不是函数被调用了两次就自动隔离。用 `a = []; b = []` 创建不同容器；用 `a = b = []` 则共享同一个对象。分别保存 `task, next_a = add_task(a, next_a, ...)` 和 B 的返回结果。

判分时检查两个列表内容、对象身份及各自计数，不接受只比较两个变量名。函数版测试 `test_separate_lists_do_not_share_tasks` 是最小回归；练习还应覆盖交替调用与重复完成。

</details>

当前职责已经稳定，文件却同时放着字段规则、操作和终端交互。下一 Module 再据此拆文件；我们不会因为“写了函数就应该建 package”而跳过这个因果关系。
