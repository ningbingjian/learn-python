# Unit 02 — 实例状态和方法为什么需要 self？

> 状态：`BUILT` · 前置：Task 的构造与 complete 行为<br>
> 完整模型：[06-object-model](../03-compose-task-collaborators/06-object-model/)

## 同一个定义产生不同状态

class 定义一类对象的共同构造和行为；instance 保存这一次任务的具体状态。两个任务标题相同，也不意味着它们是同一个对象：

```pycon
>>> class Task:
...     def __init__(self, title):
...         self.title = title
...         self.done = False
...
...     def complete(self):
...         self.done = True
>>> first = Task("Read")
>>> second = Task("Read")
>>> first is second
False
>>> first.complete()
>>> first.done, second.done
(True, False)

```

`self` 是方法的普通参数名约定，不是需要背诵的神秘指令。调用 `first.complete()` 时，方法获得 first 作为这个参数；对当前普通实例方法，可用 `Task.complete(first)` 观察相同效果。绑定方法的底层机制留在 Data Model 阶段，不在这里展开。

## __init__ 里的赋值为什么有 self？

`title = title.strip()` 只重新绑定初始化函数中的局部名字；`self.title = title.strip()` 才把值保存到该实例属性。调用结束后还要读取的数据必须有合适的拥有者。

```pycon
>>> class BrokenTask:
...     def __init__(self, title):
...         title = title.strip()
>>> task = BrokenTask("Read")
>>> hasattr(task, "title")
False

```

hasattr 在这里仅作为观察工具。修复不是在模块顶层新建 title，而是把状态写到 self。函数局部变量与实例属性不是同一个命名空间，不能因为名字相同就当成同一处存储。

__init__ 应把实例带到可使用状态。需要 title 才能工作的 Task，不应先无参构造再要求调用者记得调用另一个 setup；那会增加一段外部可见的无效生命周期。

## 类属性为什么会制造跨实例泄漏？

下面故意把列表放在类体：

```pycon
>>> class BrokenTracker:
...     tasks = []
...
...     def add(self, title):
...         self.tasks.append(title)
>>> first, second = BrokenTracker(), BrokenTracker()
>>> first.add("Read")
>>> second.tasks
['Read']
>>> first.tasks is second.tasks
True

```

两个实例没有各自的 tasks 属性时，会找到类上的同一个列表；append 修改那个共享对象。它与 Module 04 的可变默认参数不是同一个求值位置，却都由“重复绑定到同一可变对象”解释。

修复应在每次初始化时创建列表：

```pycon
>>> class Tracker:
...     def __init__(self):
...         self.tasks = []
>>> first, second = Tracker(), Tracker()
>>> first.tasks.append("Read")
>>> second.tasks
[]

```

类属性适合确实共享的类级信息，不适合每次会话各自拥有的任务集合。`done = False` 这种不可变类默认值与可变列表的表现又不完全相同：实例赋值会遮蔽同名类属性，而不是修改所有实例。不过为避免把实例状态分散在不同位置，本课程统一在 __init__ 初始化它。

## 方法返回的是结果，不必总是 self

正式 `Task.complete()` 返回本次是否改变状态，服务 CLI 的“完成成功 / 已经完成”反馈。返回 self 适合某些链式 API，但不是所有方法的默认答案。初始化返回 None、完成返回布尔值、展示返回字符串，各自对应调用者真正需要的结果。

同样，不要为了“面向对象”给每个属性补一个仅转发的 getter/setter。当前类的价值是维护任务行为；完整属性协议与数据模型留在 Stage 02。

## 迁移练习：每个任务的标签独立

在缩小 Task 示例中新增 tags 列表与 `add_tag(tag)`。要求去除首尾空白；拒绝空标签；重复标签不新增并返回 False；成功新增返回 True；两个任务不能共享列表。不要使用默认列表参数。

<details>
<summary>参考实现</summary>

```pycon
>>> class TaggedTask:
...     def __init__(self, title):
...         self.title = title
...         self.tags = []
...
...     def add_tag(self, tag):
...         tag = tag.strip()
...         if not tag:
...             raise ValueError("tag cannot be empty.")
...         if tag in self.tags:
...             return False
...         self.tags.append(tag)
...         return True
>>> first, second = TaggedTask("A"), TaggedTask("B")
>>> first.add_tag(" python "), first.add_tag("python")
(True, False)
>>> first.tags, second.tags
(['python'], [])

```

选择 list 是因为这里希望保留添加顺序；若只关心唯一性，可以讨论 set，但不能无说明改变展示顺序契约。验收既看去重规则，也看每个实例的集合身份。

</details>

每条 Task 能维护自身状态后，还缺少集合与 ID 的拥有者。下一章用组合让对象协作，而不是让 Task 创建整个应用。
