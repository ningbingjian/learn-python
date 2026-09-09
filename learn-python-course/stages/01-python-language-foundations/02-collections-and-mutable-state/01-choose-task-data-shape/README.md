# Unit 01 — 任务集合应该选择什么数据形状？

> 状态：`BUILT`<br>
> 类型：`CONCEPT` + Design Comparison<br>
> 前置：能够用多个名字表达一条任务的基础字段<br>
> 完成证据：能够根据数据语义选择容器，而不是根据“哪个写起来熟”做决定

## 1. 多个名字无法形成稳定记录

Module 01 结束时，一条任务由几个名字共同表达：

```python
title = "Learn Python"
priority = 2
done = False
note = None
```

只处理一条任务时，这些名字勉强够用。第二条任务出现后，很容易退化成：

```python
title_1 = "Learn Python"
priority_1 = 2
done_1 = False

title_2 = "Review notes"
priority_2 = 1
done_2 = True
```

问题不是名字不够，而是关系没有被数据结构表达：

- 哪些字段属于同一条任务，只能靠编号约定。
- 增加 `note` 时，每个编号都要新增一个名字。
- 想把某条任务作为整体保存、移动或删除时，没有“任务记录”可以操作。
- 任务数量写死在源码中，无法自然增长。

因此先解决两个层级：

```text
多个字段
→ 组成一条任务记录

多条任务记录
→ 组成任务集合
```

## 2. `tuple` 能组合位置，却隐藏字段含义

可以把一条任务写成：

```python
task = (1, "Learn Python", 2, False, None)
```

`tuple` 保留顺序，也不能通过位置赋值修改自身。但阅读：

```python
print(task[2])
```

必须记住位置 `2` 表示优先级。只要字段增删或顺序变化，所有位置访问都需要一起理解和修改。

`tuple` 更适合当前语义确实由固定位置表达的数据，例如一个不可变的二维坐标：

```python
point = (120, 80)
```

Task 字段需要名字、会逐步演进，也会修改完成状态。当前用位置表达不是最清楚的选择。

## 3. `dict` 让一条任务成为有字段名的记录

使用字典：

```python
task = {
    "id": 1,
    "title": "Learn Python",
    "priority": 2,
    "done": False,
    "note": None,
}
```

现在数据关系直接写进结构：

```python
print(task["title"])
print(task["priority"])
```

选择 `dict` 的理由不是它“功能多”，而是：

- 每个值由稳定字段名访问。
- 不同类型的字段能够组成一条业务记录。
- 字段值可以按业务变化修改。
- 整条任务可以作为一个对象加入更大的集合。

当前成本也必须看见：

- Key 是字符串，拼写错误只能在运行时暴露。
- 每条任务是否拥有相同字段仍靠代码约定。
- 数据和操作任务的行为仍然分离。

这些成本会积累到 Module 06，再成为引入 class 的真实理由。现在 `dict` 仍然是足够简单的选择。

## 4. `list` 让多条任务保持顺序并能够增长

Task Tracker 需要按加入顺序保存多条任务，也需要新增、修改和删除。因此使用列表承接多条字典记录：

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

数据形状可以读成：

```text
tasks
└── list：有顺序、可增长的任务集合
    ├── dict：第一条任务记录
    └── dict：第二条任务记录
```

常用简写 `list[dict]` 只描述外层和内层的形状，不代表当前已经进入静态 Typing。完整类型注解会在 Stage 03 系统学习。

## 5. 为什么主集合不是 `set`

`set` 适合表达唯一成员集合：

```python
known_categories = {"learning", "work"}
```

它擅长回答：

```text
这个分类是否已经存在？
集合中有哪些不同分类？
```

但 Task Tracker 的主集合还需要：

- 保持用户能够理解的加入顺序。
- 按位置读取第一条或最新任务。
- 保存包含 `dict` 的任务记录。

可变字典不能直接作为 `set` 成员，而且集合也不把“第一个任务”作为核心语义。因此 `set` 可以服务某个唯一性需求，却不适合替代当前的任务列表。

## 6. 四种容器不是互相竞争的等级

| 容器 | 当前最重要的语义 | Task Tracker 中的判断 |
|---|---|---|
| `list` | 有顺序、可重复、可增长 | 适合任务主集合 |
| `tuple` | 位置稳定、容器本身不可变 | 不适合字段会演进的任务记录 |
| `dict` | Key 映射 Value | 适合一条有命名字段的任务 |
| `set` | 成员唯一、强调 membership | 可用于唯一分类，不适合任务主集合 |

选择过程应该是：

```text
先问数据需要什么语义
→ 再选择能直接表达这些语义的结构
→ 最后才考虑具体方法
```

不是：

```text
我刚学到 set
→ 想办法把所有数据塞进 set
```

## 7. Mutable 与 Immutable 的第一层边界

当前涉及的容器中：

```text
list / dict / set  → mutable，可以在保持对象身份时修改内容
tuple              → immutable，不能替换、增加或删除自身位置
```

观察列表 mutation：

```python
tasks = []
print(id(tasks))

tasks.append({"title": "Learn Python"})
print(id(tasks))
```

两次 `id(tasks)` 在同一次运行中相同，因为 `append()` 修改了原列表对象，而不是让 `tasks` 重新绑定另一个列表。

再观察 rebinding：

```python
tasks = []
print(id(tasks))

tasks = [{"title": "Learn Python"}]
print(id(tasks))
```

第二次赋值让名字 `tasks` 绑定新列表对象。

这个区别会直接决定共享状态 Bug：如果两个名字绑定同一个列表，mutation 会被两个入口同时观察到。Unit 03 会专门隔离这个机制。

## 8. Tuple 不等于“所有内部内容都不可变”

一个需要提前守住的边界：

```python
task_group = (["Learn Python"], ["Review notes"])
```

`tuple` 不能把位置 `0` 重新替换成另一个对象，但位置中的列表仍然是 mutable：

```python
task_group[0].append("Write exercises")
```

因此更准确的说法是：

> tuple 的位置关系不可修改，不代表它引用的所有对象自动获得深层不可变性。

这也是为什么复制和不可变性必须按对象图的层级讨论，不能只看最外层类型。

## 9. Design Exercise

为下面四种数据选择容器，并写出理由：

```text
A. 按加入顺序保存任务
B. 用字段名表达一条任务
C. 保存已经出现过的唯一分类名
D. 表达固定的二维网格坐标
```

要求：

1. 不只写容器名称，必须说明顺序、唯一性、字段名或可变性需求。
2. 给每种选择写出一个最小 Python 值。
3. 指出哪个结构需要支持 mutation，哪个结构不需要。

## 10. Modeling Exercise

把下面的平行名字重构成 `list[dict]`：

```python
title_1 = "Read chapter 1"
done_1 = True
title_2 = "Read chapter 2"
done_2 = False
```

每条记录至少包含：

```text
id
title
priority
done
note
```

然后回答：

1. 哪个对象表达一条任务？
2. 哪个对象表达任务集合？
3. 增加第三条任务时，不再需要创建哪些编号名字？
4. 当前模型仍然依赖什么字符串约定？

## 11. 完成检查

不看正文，解释：

1. 为什么 Task 字段当前选择 `dict`，而不是 `tuple`？
2. 为什么任务主集合选择 `list`，而不是 `set`？
3. `append()` 是 mutation 还是 rebinding？
4. tuple 内部引用列表时，列表能否修改？
5. `list[dict]` 数据形状解决了什么，又留下什么成本？

下一 Unit 会开始直接访问和修改这个嵌套结构。到那时，索引与 Key 既提供精确路径，也会产生新的失败边界。
