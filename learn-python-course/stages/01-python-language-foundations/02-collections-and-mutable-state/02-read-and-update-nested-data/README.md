# Unit 02 — 嵌套数据怎样读取和修改？

> 状态：`BUILT`<br>
> 类型：`BUILD` + Failure Observation<br>
> 前置：能够说明为什么当前任务模型选择 `list[dict]`<br>
> 完成证据：能够沿明确路径新增、读取和修改任务，并解释常见索引与 Key 失败

## 1. 数据形状决定访问路径

从两条任务开始：

```python
tasks = [
    {
        "id": 1,
        "title": "Learn Python",
        "priority": 2,
        "done": False,
        "note": None,
    },
    {
        "id": 2,
        "title": "Review notes",
        "priority": 1,
        "done": True,
        "note": "Focus on binding",
    },
]
```

要读取第一条任务标题，需要按结构逐层进入：

```python
first_task = tasks[0]
first_title = first_task["title"]

print(first_title)
```

也可以写成：

```python
print(tasks[0]["title"])
```

两种写法行为相同，但前者更容易观察每层对象：

```text
tasks[0]            → 第一条 dict
tasks[0]["title"]   → 这条 dict 中的 title 字符串
```

嵌套访问不是一段神秘语法，而是按数据形状连续执行多次访问。

## 2. 正向与负索引表达位置语义

列表从索引 `0` 开始：

```python
first_task = tasks[0]
second_task = tasks[1]
```

负索引从末尾反向定位：

```python
latest_task = tasks[-1]
```

在 Task Tracker 中，`tasks[-1]` 可以自然表达“当前最后加入的任务”。但位置不是稳定业务 ID：

- 在列表头部插入任务会改变后续位置。
- 删除一条任务后，其他位置会移动。
- 用户说“任务 #2”时，通常需要业务字段 `id`，而不是当前列表索引 `1`。

因此：

```text
index → 当前容器位置
id    → 业务标识
```

两者可能暂时看起来有关联，语义却不同。

## 3. 索引越界是数据假设失败

空列表没有第一条任务：

```python
tasks = []
print(tasks[0])
```

会得到 `IndexError`。它说明代码假定位置存在，但当前数据不满足这个假定。

本 Module 暂时不引入完整分支策略。先形成调试问题：

```text
当前列表长度是多少？
准备访问哪个索引？
这个位置为什么应该存在？
```

`len()` 提供直接证据：

```python
print(len(tasks))
```

Module 03 会在真实业务流程中根据集合是否为空选择分支，而不是让索引错误成为用户体验。

## 4. 字典 Key 是字段契约

```python
task = tasks[0]
print(task["priority"])
```

Key 拼写错误：

```python
print(task["priorty"])
```

会触发 `KeyError`。这不是 Python 不知道“你大概想写 priority”，而是当前字典不存在精确 Key。

可以用 membership 先观察：

```python
print("priority" in task)
print("priorty" in task)
```

也可以使用：

```python
note = task.get("note")
```

`.get()` 在 Key 缺失时默认返回 `None`。这不等于它永远更安全：

- `note` 本来就是可选字段，缺失时使用 `None` 可能合理。
- `title` 是必需字段，静默得到 `None` 可能把模型错误隐藏到更远处。
- `.get()` 的默认结果还会把“Key 不存在”和“Key 存在且值为 None”合并；需要区分时应先用 `in` 明确判断。

选择 `task["title"]` 还是 `task.get("note")`，取决于字段契约，而不是“哪个不会报错”。

## 5. `append()` 在原列表上新增任务

创建一条完整记录：

```python
new_task = {
    "id": 3,
    "title": "Write exercises",
    "priority": 3,
    "done": False,
    "note": None,
}
```

加入集合：

```python
tasks.append(new_task)
```

`append()` 的结果不是新列表。它修改 `tasks` 当前绑定的列表对象：

```python
result = tasks.append(new_task)
print(result)
```

会看到 `None`。这是 Python 常见约定：原地修改方法通过对象状态产生效果，不把修改后的同一个对象作为结果返回。

因此不要写：

```python
tasks = tasks.append(new_task)
```

这会让 `tasks` 重新绑定到 `None`，丢失原列表的名字入口。

## 6. 修改字段也是 mutation

完成第一条任务：

```python
first_task = tasks[0]
first_task["done"] = True
```

再读取：

```python
print(tasks[0]["done"])
```

会得到 `True`。`first_task` 和 `tasks[0]` 此刻找到的是同一个字典对象，字段赋值修改了该对象。

这不是让名字 `first_task` 重新绑定新字典：

```text
tasks[0] ─────┐
              ├──→ 同一个 task dict
first_task ───┘
```

当前代码已经出现共享引用，只是这次共享符合意图。Unit 03 会说明什么时候同样的结构会变成 Bug。

## 7. 新增、修改与删除字段

字典字段可以演进：

```python
task = tasks[0]
task["category"] = "learning"
task["priority"] = 1
removed_note = task.pop("note")
```

分别表示：

```text
不存在的 Key 赋值 → 新增字段
已有 Key 赋值     → 修改字段
pop(Key)          → 删除字段并返回旧值
```

在业务模型中随意删除必需字段会让其他代码得到 `KeyError`。能执行某个容器操作，不代表这个操作符合当前领域约束。

例如 `title` 是必需字段，就不应该只因为会用 `pop()` 而删除它。容器 API 提供能力，业务规则决定是否使用。

## 8. 删除列表元素会改变位置

```python
removed_task = tasks.pop()
```

没有参数时，`.pop()` 删除并返回最后一项。指定索引时：

```python
removed_task = tasks.pop(0)
```

会删除第一项，后续元素向前移动。这再次证明索引不是稳定任务 ID。

完整“根据任务 ID 删除”的流程需要遍历、匹配和分支，将在 Module 03 出现。本 Unit 只观察容器层行为和位置变化。

## 9. 切片复制了外层列表，没有复制内部任务

取前两条任务：

```python
first_two = tasks[:2]
```

`first_two` 是一个新列表。向它追加元素不会改变 `tasks` 的长度：

```python
first_two.append({"id": 99, "title": "Temporary"})

print(len(first_two))
print(len(tasks))
```

但两个列表中的原有元素仍然是同一批字典对象：

```python
first_two[0]["done"] = True
print(tasks[0]["done"])
```

原集合也会看到 `True`。

可以画成：

```text
tasks ─────────────→ list A ──┐
                              ├──→ task dict 1
first_two ─────────→ list B ──┘
```

“新外层容器”和“内部对象独立”是两个不同结论。Unit 03 会用控制变量正式定义 shallow copy。

## 10. `len()`、membership 与当前能力边界

本 Unit 已经能直接回答：

```python
print(len(tasks))
print(tasks[0])
print(tasks[-1])
print("title" in tasks[0])
```

但还不能优雅回答：

```text
显示所有任务
找到 id 为 7 的任务
筛选所有未完成任务
持续接收新增命令
```

这些问题需要对集合重复处理，正是 Module 03 引入循环和控制流的理由。现在不要用大量手工索引假装已经解决。

## 11. Mutation Exercise

从两条任务的 `list[dict]` 开始，完成：

1. 使用 `append()` 新增第三条完整任务。
2. 使用负索引读取最新任务标题。
3. 把第一条任务的 `done` 修改为 `True`。
4. 给第二条任务增加 `category` 字段。
5. 删除最后一条任务并保存返回值。
6. 打印操作前后的 `len(tasks)`。

每次操作标记它属于：

```text
读取
外层列表 mutation
内部字典 mutation
名字 rebinding
```

## 12. Failure Exercise

分别制造并解释：

```python
tasks[99]
tasks[0]["missing"]
tasks = tasks.append({"title": "Broken"})
```

要求：

- 记录异常类型或最终错误状态。
- 指出是哪一层数据假设失败。
- 不用 `try / except` 把问题全部吞掉。
- 修复根因后再次打印数据形状。

## 13. 完成检查

不看正文，回答：

1. `tasks[0]["title"]` 按什么顺序访问对象？
2. 索引与任务业务 ID 有什么区别？
3. 为什么 `tasks = tasks.append(task)` 会丢失列表入口？
4. `first_task["done"] = True` 为什么能被 `tasks[0]` 看见？
5. 切片得到新列表后，为什么内部字典仍可能共享？
6. 哪些集合问题必须等循环出现后才能自然解决？

下一 Unit 会把“符合意图的共享引用”改造成一个备份 Bug，迫使我们明确 aliasing 和复制边界。
