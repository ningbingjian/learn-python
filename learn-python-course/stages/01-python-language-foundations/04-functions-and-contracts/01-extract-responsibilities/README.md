# Unit 01 — 什么时候应该把代码抽成函数？

> 状态：`BUILT` · 前置：完整的 [控制流 CLI](../../03-control-flow/03-compose-interactive-cli/03-control-flow-cli/)<br>
> 本章先建立边界；Module 完整函数版本保存在 Unit 03。

## 文件变长不是唯一理由

上一版虽然已经可用，但如果另一个调用者也想新增任务，只能模拟终端输入，或复制标题校验、优先级检查、字典构造和 ID 递增。它需要的是“创建一条合法任务”，不是“运行一段交互”。

将连续十行随意搬进 `do_stuff()`，不会减少这种耦合。函数的价值在于给一项责任命名，并让调用者只依赖输入、结果和约定的副作用。一个名字解释不清，往往说明责任仍混在一起。

当前脚本有三类变化：文字提示随交互变化；合法字段随规则变化；新增与完成随业务操作变化。我们先把这些责任变成同一文件中的函数，不急着拆包。文件边界不能替代责任边界。

## 函数定义不是马上执行函数体

`def` 执行时建立函数对象并绑定名字；调用时才绑定实参并执行函数体。局部中间值不需要放进全局变量：

```pycon
>>> def normalize_note(text):
...     stripped = text.strip()
...     return stripped or None
>>> normalize_note(" read chapter ")
'read chapter'
>>> normalize_note(" ") is None
True

```

`return` 把结果交还调用者，并结束本次调用。`print` 只产生输出，不是返回那个输出的字符串：

```pycon
>>> def show_title(title):
...     print(title)
>>> result = show_title("Read")
Read
>>> result is None
True

```

漏写 `return`、或者执行到函数末尾，默认结果都是 None。若把“生成显示行”写成打印函数，测试或文件输出就必须截获终端；若返回字符串，CLI 可自行决定在哪里显示。最终函数版因此使用 `format_task(task)` 返回文本。

## 先抽没有副作用的规则

第一个适合抽出的责任是优先级解析。输入是字符串，成功结果是 1～3 的整数；失败抛出 `ValueError`，而不是返回某个看起来也可能合法的整数：

```pycon
>>> def parse_priority(text):
...     try:
...         priority = int(text)
...     except ValueError:
...         raise ValueError("priority must be an integer from 1 to 3.") from None
...     if not 1 <= priority <= 3:
...         raise ValueError("priority must be between 1 and 3.")
...     return priority
>>> parse_priority(" 2 ")
2
>>> parse_priority("4")
Traceback (most recent call last):
...
ValueError: priority must be between 1 and 3.

```

`raise` 让本次调用失败，调用者可以选择如何恢复；`from None` 隐藏转换异常的上下文展示，避免把同一次用户错误打印成两段原因，并不把失败变成功。本函数没有 `input` 或 `print`，所以可以直接验证而不用启动整个会话。

CLI 接收 `ValueError` 后显示 `Error: ...` 再读下一条命令。不要在解析器中打印并返回 None：调用者可能继续把 None 当作优先级写入记录，错误反而延迟暴露。

## 再抽有明确副作用的操作

新增不是纯计算，它会修改列表。我们不假装所有函数都必须纯，而是让修改明确：

```python
task, next_id = add_task(tasks, next_id, title, priority, note)
```

调用方可以据此读出：集合被传入；下一个 ID 通过结果回传；没有依赖某个隐藏全局列表。函数内部先调用 `clean_fields` 校验与归一化，再构造记录并追加。重复检查领域约束是有意的：CLI 提前检查可以尽快反馈；领域函数仍要保护从测试或将来另一界面进入的调用。

查找函数 `find_task(tasks, task_id)` 成功时返回集合内的原字典，不是复制；找不到则抛出 ValueError。完成函数借助查找修改同一记录，第一次返回 True，再次调用返回 False，CLI 决定显示哪条消息。这样“结果有没有变化”与“给用户写什么”就不再纠缠。

## 用旧测试约束重构，再用新测试观察边界

先保留 Module 03 的完整会话测试。只要新增、查看、完成和退出的行为未改变，它们应该继续通过。之后再补规则测试：解析 2、拒绝 4；新增非法任务后列表仍空；重复完成只第一次返回 True。

仅有新测试不够。一个解析函数可能完全正确，但 CLI 忘了使用它；仅有旧测试也不够。会话失败不容易指出是哪一项规则坏了。两组证据分别约束外部行为与内部契约。

函数版入口使用 `if __name__ == "__main__": run_cli()`，让测试导入函数时不启动输入循环。本 Module 先把它视为运行保护，下一 Module 专门解释导入与入口的关系。

## 练习：把显示与输出分离

基于上一控制流版本，将单条任务的展示提取成 `format_task(task)`，返回完全相同的显示行。验证完成与未完成、备注缺失与非空四种组合，并断言调用前后字典相等。

<details>
<summary>参考实现与不采用的方案</summary>

```pycon
>>> def format_task(task):
...     marker = "x" if task["done"] else " "
...     note = task["note"] if task["note"] is not None else "(none)"
...     return (
...         f"#{task['id']} [{marker}] {task['title']} | "
...         f"priority={task['priority']} | note={note}"
...     )
>>> task = {"id": 1, "title": "Read", "done": False, "priority": 2, "note": None}
>>> before = task.copy()
>>> format_task(task)
'#1 [ ] Read | priority=2 | note=(none)'
>>> task == before
True

```

这里不接收一个 `output_mode` 参数来同时处理终端、文件和网络。当前需要的是返回一行文本，过早设计三个不存在的输出场景只会增加分支。调用处改成 `print(format_task(task))` 即可。

</details>

完成本章后，应能指出函数“接受什么、返回什么、修改什么、失败时怎样”。这些问题答不清时，即使代码已经分成十个 def，也还没有形成稳定契约。
