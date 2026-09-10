# Unit 01 — 为什么现在需要 class？

> 状态：`BUILT` · 起点：[拆包版本](../../05-modules-and-packages/03-break-circular-dependencies/05-package-structured/)<br>
> 对象版完整状态归属 Unit 03，本章先解释模型变化。

## dict 没有错，但维护约定开始分散

当前任务记录使用 id、title、priority、done、note 五个键。新增函数负责构造，完成函数负责修改，展示函数记住键名。若另一个调用者手写字典，可能漏 note；拼写错误的 `task["priorty"]` 只有执行到访问时才暴露。

问题不是字典“低级”。输入尚不稳定、只做短暂转换时，字典非常合适。现在任务的字段和行为已经稳定，且多个调用点必须维持同一约定，我们希望给这个边界一个明确名字：`Task`。

class 也不会自动拦截所有错误属性。对象上的拼写错误仍可能出错，甚至某些赋值会创建新属性。本阶段选择类是为了统一构造与行为位置，不是宣称静态类型安全。

## 先只迁移一条记录

把“创建合法任务”与“将任务标为完成”放在同一个定义里：

```pycon
>>> class Task:
...     def __init__(self, task_id, title, priority):
...         if not title.strip():
...             raise ValueError("title cannot be empty.")
...         self.id = task_id
...         self.title = title.strip()
...         self.priority = priority
...         self.done = False
...
...     def complete(self):
...         if self.done:
...             return False
...         self.done = True
...         return True
>>> task = Task(1, " Read ", 2)
>>> task.title
'Read'
>>> task.complete(), task.complete(), task.done
(True, False, True)

```

这是隔离完成行为的缩小示例，尚未包含优先级和备注的完整校验；正式模型复用已有 `clean_fields`，不会删除规则。`Task(...)` 创建实例并通过 `__init__` 初始化状态。__init__ 不返回任务对象；不要在其中 `return self`。

原先 `complete_task(tasks, id)` 同时查找集合和改变单条记录；现在任务自身只知道如何完成自己，集合查找留给下一章之后的协作者。一个任务不需要知道“自己在列表第几个位置”才能完成。

## 状态边界不是把所有代码塞进类

Task 不调用 input、不打印、不创建任务集合、不发放下一个 ID。那些不是单条任务的责任。

| 原写法 | 对象版 | 保留的意义 |
|---|---|---|
| task["title"] | task.title | 标题是状态 |
| task["done"] = True | task.complete() | 通过行为表达状态变化 |
| clean_fields(...) | __init__ 中调用 clean_fields | 构造仍需验证 |
| find_task(tasks, id) | 后续 TaskTracker.find(id) | 集合关系不塞入 Task |

并不是每个函数都必须变成方法。解析终端文本的 `parse_priority` 与展示行的 `format_task` 继续是普通函数。若一个方法除了把所有实参原样转发外没有对象责任，它可能根本不需要类。

## 构造失败为什么不能留下“半条任务”？

正式 Task 先调用校验，校验失败会抛出 ValueError；集合拥有者必须等构造成功后再追加并消耗 ID。即使构造过程已经给临时实例设置了 id，这个失败实例也不会成为正式集合成员。

这依赖调用顺序，不是 class 自动提供事务。若先往集合放入占位对象、再填字段，就仍会泄漏无效记录。对象只能帮助组织约定，不能替我们选择修改边界。

## 练习：取消完成是否应直接赋值？

新增 `reopen()`：已完成任务恢复未完成并返回 True；已经未完成则返回 False。要求两次调用幂等，不改变标题、ID、备注和优先级。基于本章缩小示例实现即可，不提前加入 CLI 命令。

<details>
<summary>参考方法与验收判断</summary>

```python
def reopen(self):
    if not self.done:
        return False
    self.done = False
    return True
```

此方法应放进 Task。验收先 complete，再连续 reopen 两次，结果 True、False；另建从未完成的任务，第一次 reopen 就应 False。直接在 CLI 写 `task.done = False` 虽然能改变状态，却会让幂等结果判断散落到调用处。

这不是禁止属性读写的强制机制。当前公开属性仍可直接改坏；课程约定使用构造与行为方法维护规则，后续阶段才讨论更严格的模型工具与访问控制方案。

</details>

现在看到的“对象”不是把字典换成点号这么简单：它让一项稳定行为与所需状态共同出现。下一章解释方法中的 self，以及多个实例为什么不能共享同一份可变状态。
