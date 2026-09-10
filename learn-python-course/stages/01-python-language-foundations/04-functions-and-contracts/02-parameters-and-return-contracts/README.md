# Unit 02 — 参数和返回值怎样形成稳定契约？

> 状态：`BUILT` · 前置：Unit 01 的职责划分<br>
> 应用落点：[04-function-oriented](../03-state-and-scope/04-function-oriented/)

## 调用能运行，不代表调用意图清楚

`add_task(tasks, 1, "Read", 2, None)` 可以表达合法新增，但参数一多，两个整数很容易放错。参数名不是给函数作者看的局部注释：它们也可以出现在调用端，成为接口的一部分。

```pycon
>>> def describe(title, priority=2, note=None):
...     return title, priority, note
>>> describe("Read")
('Read', 2, None)
>>> describe("Read", note="chapter 4", priority=1)
('Read', 1, 'chapter 4')
>>> describe("Read", 3, priority=1)
Traceback (most recent call last):
...
TypeError: describe() got multiple values for argument 'priority'

```

位置实参按顺序绑定；关键字实参按名字绑定。一个参数不能绑定两次。普通位置实参应放在关键字实参之前；本章不展开仅位置、仅关键字参数的全部设计。

默认参数表示“省略时有合理意义”，不表示“调用者填错时偷偷改成默认”。备注可以省略为 None；优先级的业务范围仍需要校验。命名参数改善可读性，也使参数名变化成为接口变化，不能只修改定义不检查调用者。

## 多值返回仍然只有一个结果对象

新增函数既需要返回记录，也需要返回下一可用 ID。Python 用逗号构成元组，调用端再解包：

```pycon
>>> def advance(next_id):
...     return {"id": next_id}, next_id + 1
>>> result = advance(7)
>>> type(result).__name__
'tuple'
>>> task, next_id = result
>>> task["id"], next_id
(7, 8)

```

“返回两个值”是方便说法，不是两个独立的返回通道。函数一旦执行 `return`，后面的语句不会继续。调用端解包数量必须与结果一致；不要让成功返回二元组、另一条成功路径却只返回一个字典。

我们没有让 `add_task` 修改一个全局 `next_id`。整数不可变，函数中的 `next_id += 1` 只重新绑定局部名字；显式返回才能让调用者拿到新的计数。列表可变，`append` 会被调用者观察到，这两种数据流必须同时写进契约。

## “没有变化”与“操作失败”不要合并

完成任务的三种结果：

| 情况 | 结果 | 是否改变状态 |
|---|---|---|
| 存在且未完成 | True | done 变成 True |
| 存在且已完成 | False | 不变 |
| 不存在 | ValueError | 不变 |

False 并不等于异常。重复完成是合法请求，调用者可以显示“已经完成”；不存在则违反操作前提，需要错误反馈。用 `-1`、`None`、`False` 随意混合作为失败值，会迫使每个调用者猜测。

当前 `clean_fields` 的契约是：title 为字符串；priority 必须是真正的整数 1～3；note 为字符串或 None。它验证业务值，不试图接收任意 Python 对象。源码使用 `type(priority) is int` 排除 True：Python 中 bool 可以参与整数比较，但业务优先级不接受布尔值。这是领域规则，不应推导为所有程序都必须拒绝 bool。

## *args 与 **kwargs 是收集，不是免除契约

先在与任务摘要有关的小例子里观察：

```pycon
>>> def join_titles(*titles, separator=" / "):
...     return separator.join(titles)
>>> join_titles("Read", "Test")
'Read / Test'
>>> join_titles("Read", "Test", separator=", ")
'Read, Test'
>>> def describe_options(**options):
...     return options
>>> describe_options(priority=1, note="today")
{'priority': 1, 'note': 'today'}

```

定义中的 `*titles` 收集额外位置参数为元组；`**options` 收集额外关键字参数为字典。调用时星号则做相反方向的展开：

```pycon
>>> titles = ["Read", "Test"]
>>> join_titles(*titles)
'Read / Test'
>>> options = {"priority": 3, "note": None}
>>> describe("Read", **options)
('Read', 3, None)

```

这适合真正可变数量的值或向已有接口转发参数。当前 Task Tracker 的字段固定，不需要把 `add_task` 改成 `**fields`。后者会让拼错 `priorty` 更晚才暴露，也把接口说明从函数签名转移到内部检查。灵活不是没有代价。

## 迁移练习：统计函数的契约设计

基于 Unit 01 的函数划分，设计 `summarize(tasks, *, include_done=True)`。星号表示后面的参数必须按名字传递，是为了让调用处清楚表达筛选意图；不要求把这种签名风格推广到所有函数。

要求返回 `(count, titles)`：count 与 titles 长度一致；include_done=False 时只统计未完成；保持原顺序；不修改任何记录；空集合返回 `(0, [])`。先写三条断言，再实现。

<details>
<summary>参考实现</summary>

```pycon
>>> def summarize(tasks, *, include_done=True):
...     titles = []
...     for task in tasks:
...         if include_done or not task["done"]:
...             titles.append(task["title"])
...     return len(titles), titles
>>> tasks = [{"title": "Read", "done": True}, {"title": "Test", "done": False}]
>>> summarize(tasks)
(2, ['Read', 'Test'])
>>> summarize(tasks, include_done=False)
(1, ['Test'])
>>> summarize([])
(0, [])

```

这里返回的是新字符串列表，不是可变任务字典的视图。若改成返回任务对象，就必须补充共享引用的契约。函数签名不必穷尽所有文档，但至少不能与实际返回形状冲突。

</details>

下一章将检查函数看似局部，状态却为何跨调用泄漏。参数与结果写清楚之后，仍需要理解名字究竟绑定到哪个对象。
