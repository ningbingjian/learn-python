# Unit 03 — 多个对象怎样协作而不互相创建一切？

> 状态：`BUILT` · 类型：BUILD / DESIGN<br>
> 起点：[05-package-structured](../../05-modules-and-packages/03-break-circular-dependencies/05-package-structured/)<br>
> 完整结果：[06-object-model](06-object-model/)

## 两个“完成”并不重复

Task 负责改变一条任务；TaskTracker 负责管理一组任务，按 ID 找到目标并转交操作：

```python
def complete(self, task_id):
    return self.find(task_id).complete()
```

这是 TaskTracker 内的方法摘录。它看似只有一行，但承担集合选择的边界。CLI 不应该先取内部列表、自己搜索、再修改 done；否则集合规则又会散回界面。

组合表示 TaskTracker 持有多个 Task。它不是 Task 的子类，也不需要继承、ABC 或 Protocol。两个对象因为责任互补而协作，而不是因为目录需要更多类。

## 构造顺序保护集合状态

```python
def add(self, title, priority, note=None):
    task = Task(self._next_id, title, priority, note)
    self._tasks.append(task)
    self._next_id += 1
    return task
```

正式源码在 __init__ 内创建 `self._tasks = []` 和 `self._next_id = 1`。Task 构造先验证字段；失败时后两行不会执行，因此不留下记录、不消耗 ID。这里的顺序继承了控制流版本的承诺，只是拥有者从 run_cli 转移到 TaskTracker。

前导下划线是内部使用约定，不是访问控制墙。课程代码不从 CLI 直接读取 _tasks；如果调用者主动绕过约定，Python 并不会自动阻止他。

## 返回列表副本保护了什么？

`all_tasks()` 返回 `self._tasks.copy()`。调用者清空返回列表，不会删除正式集合成员；但列表里的 Task 仍是相同对象，调用其 complete 会被正式集合观察到。

这与 Module 02 的浅复制完全相同。我们只保护集合成员关系，不承诺只读对象，也不声称返回了历史快照。想要不可变快照需要另一种数据约定，不能把 copy 的名字当成完整隔离保证。

对象测试同时断言“clear 返回列表不影响集合”和“返回列表中的 Task 与 find 返回的是同一实例”。正反两条证据比一句“这里用了复制所以安全”准确得多。

## CLI 接收协作者，入口负责创建

这一版 `run_cli(tracker, read=input, write=print)` 不在内部创建 TaskTracker。`__main__.py` 在启动时创建一次并传入：

```python
from .cli import run_cli
from .tracker import TaskTracker

if __name__ == "__main__":
    run_cli(TaskTracker())
```

如果每次命令都构造新的 Tracker，数据仍会丢失；如果 Tracker 在类体共享列表，不同会话仍会串数据。class 不能代替生命周期设计。

read 与 write 是可调用对象参数。默认使用终端输入输出；测试可以传入普通函数与 `list.append` 收集结果，不需要 mock 框架。把函数当参数不要求先掌握装饰器；它只是已有函数对象的另一种绑定方式。

默认 input/print 在定义函数时绑定，这与默认参数的求值规则一致。当前测试显式传入替代函数，不依赖事后更换内置名字。

## 迁移过程与回归范围

从拆包版开始：

1. 在 models.py 定义 Task，复用 validation 的字段规则。
2. 用 tracker.py 取代 operations 中的集合函数，状态由实例拥有。
3. 将 format_task 移到 cli.py，并把字典访问改成属性访问。
4. __main__ 组合对象；CLI 只调用公开方法。
5. 保留全部旧会话测试，规则测试改为对象契约，并增加实例隔离和浅复制边界。

包内依赖为 CLI → Tracker → Task → validation，CLI 也使用输入解析；models 和 tracker 不导入 CLI。完整目录运行 `python3.14 -m task_tracker`；验证 `python3.14 -m unittest discover -s tests -v`。

这些测试证明四个基础命令未因重构改变，以及对象边界符合约定；不证明多线程安全、数据持久化或不可变模型。当前内存规模很小，按 ID 线性查找足够，不为优化猜测引入索引同步。

## 练习：用替代输入完成一次会话

不启动子进程，创建一个 Tracker，传入预置 add / list / quit 输入，将输出收集到列表。要求会话结束后 Tracker 仍可被测试读取，而不是只断言打印过“成功”。

<details>
<summary>参考调用</summary>

在完整源码目录运行以下 Python 片段：

```python
from task_tracker.cli import run_cli
from task_tracker.tracker import TaskTracker

lines = ["add", "Read", "2", "", "list", "quit"]
output = []


def read(prompt):
    return lines.pop(0)


tracker = TaskTracker()
run_cli(tracker, read, output.append)
assert tracker.find(1).title == "Read"
assert "#1 [ ] Read | priority=2 | note=(none)" in output
assert output[-1] == "Goodbye."
```

空备注对应列表中的空字符串。测试输入耗尽会暴露 IndexError，说明模拟会话不完整；不应捕获所有异常让它假通过。

</details>

对象版仍没有编辑、删除与筛选。下一 Module 会以它为唯一基线完成交付，并验证新需求是否真的落在已有边界中。
