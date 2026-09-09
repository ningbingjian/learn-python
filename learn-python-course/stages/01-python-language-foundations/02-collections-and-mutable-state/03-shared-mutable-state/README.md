# Unit 03 — 为什么修改一个名字会影响另一个名字？

> 状态：`BUILT`<br>
> 类型：`MECHANISM` + `FAILURE` + Focused Lab<br>
> 前置：能够读取和修改 `list[dict]`，并区分 mutation 与 rebinding<br>
> 完成证据：[`02-collection-model`](02-collection-model/) 与 [`shared-mutable-state-lab`](shared-mutable-state-lab/) 通过验收

## 1. 一个看起来合理的备份

Task Tracker 已经有任务集合：

```python
tasks = [
    {"id": 1, "title": "Learn Python", "done": False},
]
```

准备修改前，先“备份”：

```python
backup = tasks
```

然后向备份加入临时任务：

```python
backup.append({"id": 2, "title": "Temporary task", "done": False})

print(len(backup))
print(len(tasks))
```

两边都会得到 `2`。问题不在 `append()`，而在“备份”从未创建新列表。

## 2. Assignment 创建新绑定，不自动复制对象

执行：

```python
backup = tasks
```

可以画成：

```text
tasks ─────┐
           ├──→ 同一个 list 对象
backup ────┘
```

两个名字提供两个访问入口，列表对象仍然只有一个。这种多个引用访问同一个对象的关系称为 **aliasing**。

当代码执行：

```python
backup.append(...)
```

被修改的是共享列表，所以通过 `tasks` 读取也会看到变化。

如果改成 rebinding：

```python
backup = []
```

只是让 `backup` 指向新列表，`tasks` 仍然绑定原列表。mutation 与 rebinding 的差异在这里直接决定行为。

## 3. Aliasing 不一定是 Bug

Unit 02 中：

```python
first_task = tasks[0]
first_task["done"] = True
```

我们正是希望通过 `first_task` 修改集合里的同一条任务。这种共享引用符合意图。

真正的问题是契约不清：

```text
如果 backup 表示独立快照
→ 共享就是 Bug

如果 first_task 表示集合中原任务的入口
→ 共享就是预期行为
```

因此不能只背“共享引用危险”。更重要的是：

> 当前名字代表别名、只读视图、独立快照，还是可共同修改的状态？

## 4. 外层浅复制只切断第一层共享

创建新列表：

```python
backup = tasks.copy()
```

现在：

```text
tasks  ─────→ list A
backup ─────→ list B
```

向 `backup` 追加任务不会改变 `tasks` 的长度：

```python
backup.append({"id": 2, "title": "Temporary", "done": False})

print(len(tasks))
print(len(backup))
```

但 `.copy()` 是 shallow copy。它复制外层列表位置，位置中的字典引用仍然共享：

```text
list A ──┐
         ├──→ task dict 1
list B ──┘
```

因此：

```python
backup[0]["done"] = True
print(tasks[0]["done"])
```

仍会看到 `True`。

切片 `tasks[:]` 和 `list(tasks)` 在这个问题上也只创建新的外层列表，不会递归复制内部对象。

## 5. 复制一条记录时仍要看更深层数据

当前任务字段只有 `int`、`str`、`bool` 和 `None` 时：

```python
task_snapshot = tasks[0].copy()
task_snapshot["done"] = True
```

修改快照中的 `done` 不会修改原字典，因为最外层字典已经独立，而布尔值通过重新绑定字段替换。

如果任务以后加入可变标签：

```python
task = {
    "title": "Learn Python",
    "tags": ["python"],
}

task_snapshot = task.copy()
task_snapshot["tags"].append("course")
```

原任务也会看到 `course`，因为两个字典的 `"tags"` 仍然引用同一个列表。

结论不是“字典复制无效”，而是：

> shallow copy 创建一个新的外层容器，内部引用是否足够独立取决于当前数据形状和修改需求。

## 6. Deep Copy 是工具，不是默认设计

标准库可以递归复制对象图：

```python
from copy import deepcopy

task_snapshot = deepcopy(task)
```

对于上面的嵌套标签，深复制可以让快照中的列表独立。但它也带来成本：

- 复制的数据更多，时间和内存成本更高。
- 对象图越复杂，复制语义越难确认。
- 某些资源对象根本不应该被“完整复制”。
- 随处深复制可能掩盖不清楚的所有权设计。

当前 Task Tracker 的主线不需要持续维护完整历史快照，因此不会把 `deepcopy()` 塞进每次操作。Focused Lab 使用它，是为了对照浅复制边界。

## 7. 复制策略必须从意图开始

遇到“需要备份”时，先问：

```text
要阻止外层新增和删除互相影响？
→ 外层 shallow copy 可能足够

要修改一条只有不可变字段的记录而不影响原记录？
→ 复制该 dict 可能足够

要让嵌套可变对象也完全独立？
→ 需要逐层复制、deepcopy 或重新设计模型

只是需要另一个名字方便访问原对象？
→ 不应该复制，但名字必须表达 alias 意图
```

复制层级不是语法偏好，而是数据所有权契约。

## 8. Mutable 与 Immutable 需要按操作理解

当前常见对象：

```text
mutable：list、dict、set
immutable：str、int、bool、None、tuple 的位置结构
```

mutable 表示对象内容可以在保持身份时修改。immutable 表示对象自身不能通过原地操作改变为另一个值；需要新结果时会产生或取得另一个对象，再发生 rebinding。

但“外层 immutable”不等于“整张对象图深层 immutable”。tuple 可以引用 list，dict 可以引用 list，多个容器也可以引用同一个 task dict。

因此调试共享状态时，要画对象关系，而不是只看最外层类型名称。

## 9. Focused Lab

进入：

[`shared-mutable-state-lab`](shared-mutable-state-lab/)

实验按四个阶段隔离变量：

```text
assignment alias
→ 外层 shallow copy
→ 单条 dict shallow copy + 嵌套 list
→ deepcopy 对照
```

运行前先预测每一次原对象是否变化。只看输出而不写预测，很容易把机制实验退化成“记住答案”。

## 10. 第二个主线状态

[`02-collection-model`](02-collection-model/) 基于 Module 01 的 [`01-interactive-script`](../../01-first-useful-python-program/03-trust-user-input/01-interactive-script/) 演进。

保留：

```text
标题、优先级和备注输入
strip、int 转换和范围校验
明确退出码与错误反馈
```

新增：

```text
dict 任务记录
list 任务集合
append 新增
嵌套索引读取
字段 mutation
集合大小证据
```

当前版本有意用固定索引显示第一条和最新任务。这个笨拙点不是遗漏，而是下一 Module 引入循环的真实压力。

## 11. Copy Boundary Exercise

从下面的数据开始：

```python
task = {
    "title": "Learn Python",
    "done": False,
    "tags": ["python"],
}
```

依次完成并预测：

1. `alias = task` 后修改 `alias["done"]`。
2. `snapshot = task.copy()` 后修改 `snapshot["done"]`。
3. 在同一个 shallow snapshot 中执行 `snapshot["tags"].append("course")`。
4. 使用 `deepcopy()` 创建对照，再修改嵌套标签。

每一步必须画出：

```text
有几个外层 dict？
有几个 tags list？
哪些名字或 Key 引用同一个对象？
```

## 12. 完成检查

不看正文，回答：

1. `backup = tasks` 为什么不是备份？
2. aliasing 什么时候符合意图，什么时候成为 Bug？
3. `tasks.copy()` 切断了哪一层共享？
4. 为什么修改 shallow copy 中的 task dict 仍会影响原任务？
5. 一条只有字符串和布尔字段的任务，`task.copy()` 为什么可能已经足够？
6. 加入 `tags: list` 后，复制判断为什么改变？
7. 为什么不应该把 `deepcopy()` 当作默认设计答案？

通过本 Unit 后，学习者应该能用对象关系解释共享修改，而不是用“Python 有时候会自动同步变量”之类模糊说法。
