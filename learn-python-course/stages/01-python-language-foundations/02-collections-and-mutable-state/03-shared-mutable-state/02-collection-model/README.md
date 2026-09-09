# Source Milestone 02 — Collection Model

> 状态：`BUILT`<br>
> 所有者：[Unit 03 — Shared Mutable State](../README.md)<br>
> 基线：[Source Milestone 01 — Interactive Script](../../../01-first-useful-python-program/03-trust-user-input/01-interactive-script/)<br>
> 依赖：Python 标准库，无第三方依赖

## 1. 为什么需要这个新状态

上一状态已经可靠创建一条任务，却没有表达：

```text
多个字段属于同一条任务
多条任务属于同一个集合
集合能够新增和修改
```

本状态首次改变核心数据模型，因此值得保存新的完整源码。

## 2. 演进内容

上一状态的字段：

```python
title
priority
done
note
```

现在组成字典记录：

```python
new_task = {
    "id": 2,
    "title": title,
    "priority": priority,
    "done": False,
    "note": note,
}
```

记录进入有顺序的列表：

```python
tasks.append(new_task)
```

程序预置一条来自上一学习状态的任务，再接收一条新任务，因此集合从一条增长为两条。随后通过嵌套索引把第一条任务标记为完成，并分别显示第一条和最新任务。

## 3. 文件

```text
02-collection-model/
├── README.md
├── task_tracker.py
└── tests/
    └── test_task_tracker.py
```

- `task_tracker.py` 是当前完整主线源码。
- `tests/test_task_tracker.py` 从进程边界验证集合增长、嵌套 mutation、输入校验、输出和退出码。
- 没有独立 `pyproject.toml`，因为当前状态只使用标准库，也不是发布 Package。

## 4. 运行

```bash
python task_tracker.py
```

成功示例：

```text
CLI Task Tracker — collection model
Task title: Review collections
Priority (1-3): 3
Note (optional): Practice nested data

Task count: 2
First task: #1 Learn Python | priority=2 | done=True
Newest task: #2 Review collections | priority=3 | done=False
Newest note: Practice nested data
```

关键证据：

- `Task count: 2` 证明列表新增成功。
- 第一条任务 `done=True` 证明内部字典 mutation 可由列表路径观察。
- 最新任务保留本次输入和创建时的 `done=False`。
- 空备注继续统一为 `None`，输出 `(none)`。

## 5. 自动化验证

```bash
python -m unittest discover -s tests -v
```

测试固定：

| 场景 | 关键结果 |
|---|---|
| 有效任务与备注 | 集合大小为 2，两个任务状态彼此独立 |
| 备注留空 | 最新备注显示 `(none)` |
| 空标题 | 退出码 `1`，集合摘要不输出 |
| 非整数优先级 | 退出码 `1`，不暴露 traceback |
| 范围外优先级 | 退出码 `1`，不暴露 traceback |

测试仍使用 `sys.executable` 启动当前 Python。学习目标是运行测试、阅读场景并解释证据，不要求此时掌握 `subprocess`。

## 6. 源码阅读地图

```text
预置 task dict
→ 放入 tasks list
→ 沿用上一状态的输入清理与校验
→ 组装 new_task dict
→ append 到 tasks
→ 通过 tasks[0] 修改第一条记录
→ 通过 tasks[-1] 读取最新记录
→ 输出集合大小与两个位置
```

这里有意保留线性代码。函数职责要等重复与修改成本真正积累到 Module 04 再引入。

## 7. 当前局限就是下一阶段入口

当前版本只能：

```text
每次运行新增一条任务
用固定索引显示第一条和最新任务
在源码中预置已有任务
用固定字段 mutation 展示集合变化
```

它还不能：

```text
显示任意数量的所有任务
根据 id 查找任务
筛选未完成任务
持续接收 add / list / complete / quit 命令
```

这些问题都需要根据条件重复处理数据。它们属于下一状态 `03-control-flow-cli`，不能用大量复制粘贴或手工索引提前伪装完成。

## 8. 复制边界在哪里

主线源码只维护当前内存状态，不制造无需求的“万能备份”。共享引用、浅复制和嵌套复制通过所属 Unit 的 [`shared-mutable-state-lab`](../shared-mutable-state-lab/) 隔离证明。

当后续需求真的需要快照、撤销或并发读取时，再根据对象图与所有权选择复制策略。当前正确做法是先理解边界，而不是在所有 mutation 前调用 `deepcopy()`。
