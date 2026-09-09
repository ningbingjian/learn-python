# Module 01.02 — Collections & Mutable State

> 状态：`BUILT`<br>
> 核心问题：一条任务怎样变成一组能够新增、访问和修改的任务？<br>
> 进入状态：[`01-interactive-script`](../01-first-useful-python-program/03-trust-user-input/01-interactive-script/) 只能处理单条任务<br>
> 退出状态：[`02-collection-model`](03-shared-mutable-state/02-collection-model/)

## 1. Module 目标

Module 01 已经能把外部文本转换成一条可信任务，但字段仍散落在多个名字中，本次运行也没有“一组任务”的概念。

本 Module 只解决数据模型的下一层问题：

```text
多个字段怎样组成一条任务
→ 多条任务怎样组成有顺序的集合
→ 怎样读取和修改嵌套数据
→ 为什么两个名字可能看到同一次修改
→ 复制哪一层才符合当前业务边界
```

退出时，Task Tracker 拥有明确的 `list[dict]` 内存模型。它仍然不是完整 CLI：遍历、菜单和重复交互要等 Module 03 的 Control Flow。

## 2. Unit 地图

| Unit | 核心问题 | 教学形态 | 完成后多出的能力 |
|---|---|---|---|
| [01 — Choose Task Data Shape](01-choose-task-data-shape/) | 任务集合应该选择什么数据形状？ | `CONCEPT` + Design Comparison | 能根据顺序、字段名、唯一性和可变性选择容器 |
| [02 — Read & Update Nested Data](02-read-and-update-nested-data/) | 嵌套数据怎样读取和修改？ | `BUILD` + Failure Observation | 能新增、访问和修改 `list[dict]`，并识别索引与 Key 失败 |
| [03 — Shared Mutable State](03-shared-mutable-state/) | 为什么修改一个名字会影响另一个名字？ | `MECHANISM` + `FAILURE` + Focused Lab | 能解释 aliasing、浅复制、嵌套共享与复制边界 |

三个 Unit 继续使用同一个 Task Tracker。前两个 Unit 在正文中演进数据模型；Unit 03 保存唯一完整源码状态，并用隔离实验解释主线中容易出现的共享修改 Bug。

## 3. 源码所有权

本 Module 只保存一个新的主线里程碑：

```text
03-shared-mutable-state/
└── 02-collection-model/
    ├── README.md
    ├── task_tracker.py
    └── tests/
        └── test_task_tracker.py
```

它完整继承 Module 01 的标题、优先级、完成状态、可选备注和输入校验，并增加：

```text
dict 组成一条任务记录
list 保存有顺序的多条任务
append 新增任务
索引读取第一条和最新任务
字段赋值修改完成状态
len 观察集合大小
```

[`shared-mutable-state-lab`](03-shared-mutable-state/shared-mutable-state-lab/) 只控制引用和复制变量，不承担另一套业务项目。

## 4. 建议学习顺序

1. 先为一条任务选择数据形状，不急着记容器方法。
2. 用 Unit 02 直接读取、追加和修改嵌套数据，记录 `IndexError` 与 `KeyError` 的触发条件。
3. 在 Unit 03 先预测 alias、浅复制和嵌套复制的结果，再运行 Lab。
4. 运行 `02-collection-model` 和全部黑盒测试。
5. 闭卷完成 Reading Queue 迁移练习，证明能在新领域选择数据形状。

## 5. Technical Gate

在 `03-shared-mutable-state/02-collection-model/` 中执行：

```bash
python task_tracker.py
python -m unittest discover -s tests -v
```

在 `03-shared-mutable-state/shared-mutable-state-lab/` 中执行：

```bash
python shared_mutable_state.py
```

必须满足：

- 正常输入后集合从一条任务增长到两条任务。
- 第一条任务可通过嵌套索引修改为完成，新增任务保持未完成。
- 空标题、非整数优先级和范围外优先级继续保留 Module 01 的失败行为。
- 自动化测试在 Python 3.14 下通过，不需要第三方依赖。
- Lab 能稳定证明 alias、浅复制和嵌套可变对象的不同共享边界。
- README、命令、路径、输出和当前源码一致。

## 6. Teaching Gate

审查本 Module 时必须确认：

- 容器由“一条任务无法表达多条任务”的真实问题引出。
- `list`、`tuple`、`dict`、`set` 按数据语义比较，不是方法清单。
- 主线只使用当前自然需要的 `list[dict]`，没有强迫所有容器进入项目。
- mutation、rebinding 和 aliasing 都通过可运行现象区分。
- 浅复制的边界被准确说明，没有把 `.copy()` 宣传成万能备份。
- `deepcopy` 只在 Focused Lab 中作为对照工具，不成为默认设计答案。
- 当前源码有意保留固定索引和单次新增的局限，为 Module 03 的循环留下真实理由。
- 没有提前引入函数、Package、class 或持久化。

## 7. Module Transfer Gate

不复制 Task Tracker，实现一个最小 Reading Queue 数据模型：

```text
books         → 保留阅读顺序，可新增和删除
每本书        → 有 title、author、finished、note 字段
known_isbns   → 只关心唯一性
可选 note     → 缺失时使用 None
```

要求：

1. 选择合适的 `list`、`dict`、`set` 或 `tuple` 并说明理由。
2. 预置一本书，再追加第二本书。
3. 修改第一本书的 `finished`，证明第二本书没有被误改。
4. 制造一次 aliasing Bug，再用符合当前数据层级的复制方式修复。
5. 解释为什么外层列表复制后，内部字典仍可能共享。

通过正文、技术检查和迁移练习，只说明本 Module 达到 `BUILT`。真实学习者尚未完成跟做与迁移时，不标记 `VALIDATED`。

## 8. 本 Module 不展开什么

```text
for / while / comprehension 与菜单循环  → Module 03
函数参数、返回值和责任拆分             → Module 04
Module / Package / import              → Module 05
Task class 与对象协作                  → Module 06
持久化、数据库和并发共享状态            → 后续 Stage
```

本 Module 只让数据模型变得足以承接下一次演进，不追求提前完成最终架构。
