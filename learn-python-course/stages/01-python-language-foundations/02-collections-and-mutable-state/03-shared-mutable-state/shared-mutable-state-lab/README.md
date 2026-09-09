# Focused Lab — Shared Mutable State

> 状态：`BUILT`<br>
> 所有者：[Unit 03 — Shared Mutable State](../README.md)<br>
> 核心问题：assignment、shallow copy 和 deep copy 分别切断哪一层共享？<br>
> 运行文件：[`shared_mutable_state.py`](shared_mutable_state.py)

## 1. 为什么需要隔离实验

Task Tracker 主线同时包含外层 `list` 和内部 `dict`。只观察最终业务输出，很难判断某次变化来自：

```text
两个名字绑定同一列表
两个列表引用同一字典
两个字典引用同一嵌套列表
```

本 Lab 每个阶段都重新创建数据，只改变一种引用关系。它不是另一套项目，也不负责教完整 `copy` 标准库。

## 2. 运行前先预测

```bash
python shared_mutable_state.py
```

运行前为每一阶段写下：

```text
有几个外层容器？
有几个内部记录？
修改哪个对象？
原名字是否应该看到变化？
```

预测的价值在于暴露心智模型。如果先看答案再说“我也是这么想的”，实验无法证明理解。

## 3. Phase 1 — Assignment Alias

```python
tasks = [{"title": "Learn Python", "done": False}]
alias = tasks
```

两个名字绑定同一列表。通过 `alias.append(...)` 修改后，两个名字看到相同长度。

关键问题：

> `alias = tasks` 是否执行了任何容器复制？

答案是否定的。它只创建新的名字绑定。

## 4. Phase 2 — Outer Shallow Copy

```python
outer_copy = tasks.copy()
```

现在外层列表不同：

```python
outer_copy is tasks
```

得到 `False`。向副本追加任务不会改变原列表长度。

但第一条内部字典仍共享：

```python
outer_copy[0] is tasks[0]
```

得到 `True`。通过副本修改 `done`，原集合也会看到。

## 5. Phase 3 — Record Shallow Copy

一条任务增加嵌套标签：

```python
task = {
    "title": "Learn Python",
    "done": False,
    "tags": ["python"],
}

record_copy = task.copy()
```

外层字典不同，因此：

```python
record_copy["done"] = True
```

不会修改原字典的 `done`。

但 `"tags"` 仍引用同一个列表：

```python
record_copy["tags"].append("course")
```

原任务标签也会增加。shallow copy 的效果随字段数据形状而变化，不是“字典复制后什么都独立”。

## 6. Phase 4 — Deep Copy 对照

```python
from copy import deepcopy

deep_snapshot = deepcopy(task)
```

这个对照让外层字典与嵌套标签列表都独立。修改快照标签时，原标签不变化。

实验只证明当前对象图的结果，不推导“以后所有备份都用 deepcopy”。工程代码仍应先明确快照范围、所有权、数据规模和资源语义。

## 7. 预期输出

```text
Phase 1 — assignment alias
same outer list: True
original length after alias append: 2

Phase 2 — outer shallow copy
same outer list: False
original length after copy append: 1
copy length after append: 2
same inner task: True
original done after copy mutation: True

Phase 3 — record shallow copy
same record: False
original done after record copy rebinding: False
same nested tags: True
original tags after copy mutation: ['python', 'course']

Phase 4 — deep copy
same record: False
same nested tags: False
original tags after deep copy mutation: ['python']
deep copy tags: ['python', 'course']
```

## 8. 实验结论表

| 操作 | 新外层对象 | 内部引用默认独立 | 当前适用意图 |
|---|---:|---:|---|
| `alias = original` | 否 | 否 | 明确共享同一状态 |
| `original.copy()` | 是 | 否 | 只隔离外层新增、删除或字段替换 |
| `deepcopy(original)` | 是 | 递归尝试独立 | 确实需要独立对象图并理解成本 |

## 9. Transfer Experiment

给 task 增加第二层可变结构：

```python
"metadata": {
    "reviewers": ["Nick"],
}
```

分别使用 assignment、dict shallow copy 和 `deepcopy()`，再向 reviewers 增加名字。

必须画出对象关系并解释：

1. 外层 task dict 是否共享。
2. metadata dict 是否共享。
3. reviewers list 是否共享。
4. 当前需求真正需要切断哪一层。

完成后返回主线。不要把机制实验中的嵌套复杂度带进当前 Task Tracker 业务模型。
