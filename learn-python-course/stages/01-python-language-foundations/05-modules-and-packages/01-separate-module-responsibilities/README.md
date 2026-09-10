# Unit 01 — 哪些职责应该成为独立 Module？

> 状态：`BUILT` · 起点：[函数版本](../../04-functions-and-contracts/03-state-and-scope/04-function-oriented/)<br>
> 本章确定拆分责任，完整可运行 Package 位于 Unit 03。

## 已经有函数，为什么还需要文件边界？

函数版把“做什么”命名了，却仍把所有变化放在同一文件：改提示语要翻过字段校验，测试业务操作会导入整份交互代码，两个作者也更容易修改相同区域。

拆文件首先是让相关责任共同变化，不是规定每个函数一个文件。`parse_priority` 和 `clean_fields` 都围绕合法字段，留在一起；`add_task` 与 `complete_task` 围绕集合操作，留在一起；终端提示和展示随界面变化，归 CLI。

本章确定三个 Module：

| Module | 从上一文件迁移的内容 | 依赖 |
|---|---|---|
| validation.py | clean_fields、parse_priority、parse_task_id | 无应用内依赖 |
| operations.py | add_task、find_task、complete_task、format_task | validation |
| cli.py | run_cli | operations、validation |

`format_task` 在这个中间版本仍随已有操作函数保留，避免拆包时同时改变所有责任。它是展示责任，下一次对象重构会明确移到 CLI。边界并非一次决定就永远正确，重要的是知道暂存成本和下一次调整理由。

## import 让调用者获得模块名字，不是粘贴文本

最小观察可以借助标准库：

```pycon
>>> import math
>>> math.isclose(0.1 + 0.2, 0.3)
True
>>> from math import isclose
>>> isclose(0.1 + 0.2, 0.3)
True

```

第一种绑定模块名，再通过属性访问；第二种直接绑定目标名字。它们不会把整个文件正文复制到调用处。应用里 `from .validation import clean_fields` 表明操作依赖字段规则，名字的来源明确可查。

不使用 `from ... import *`。通配导入会让读者难以判断一个名字在哪里定义，也容易把碰巧导入的辅助名字当成公开接口。当前模块小，明确列出依赖的成本很低。

## 将全局状态留在拥有者处

拆文件时最危险的“方便”是创建 `state.py`，让所有文件直接导入 `tasks` 与 `next_id`。集合的共享修改或许暂时能工作，但整数重新绑定不会像想象那样自动同步：

```pycon
>>> original = {"next_id": 1}
>>> imported_value = original["next_id"]
>>> original["next_id"] = 2
>>> imported_value
1

```

这只是绑定关系的最小类比，不是 import 实现。真正的模块例子是 `from state import next_id` 绑定当时的整数；以后 state 重新绑定，不会自动改写调用方的名字。与之相比，`import state` 后读取 `state.next_id` 是属性访问，但仍然引入全局共享状态。

当前会话列表与计数仍由 `run_cli` 创建，操作函数通过参数接收；拆包不改变其所有权。否则测试通过顺序可能开始影响结果，文件虽然更多，数据流反而更隐蔽。

## 先移动定义，再修复导入，最后运行旧契约

完整结构将是源码根目录包含 `task_tracker/` Package，与独立 `tests/` 并列。这里的源码根目录就是运行工作目录，不再创建无意义的 `src/app/project` 包装。

`operations.py` 中的关键变化只是增加导入：

```python
from .validation import clean_fields
```

原函数体不变。`cli.py` 明确导入它实际调用的操作和解析函数。测试改从定义所在的模块导入，CLI 会话测试改为 `python3.14 -m task_tracker` 启动。不要同时引入对象、持久化和新命令；否则旧测试失败时无法判断是移动文件还是行为变化。

## 练习：新增摘要应放在哪里？

沿上一 Module 的 summarize 练习，要求 CLI 新增 count 命令，统计全部与已完成数量。先画出文字依赖关系，再决定函数归属。约束：统计函数不得 input/print；测试不得先启动 CLI；validation 不得导入 CLI。

<details>
<summary>参考设计</summary>

`summarize(tasks)` 放 operations，返回计数值；cli 导入并负责格式化输出。它依赖任务数据形状，不依赖输入文本解析，因此不应放 validation。只要现有操作模块仍然紧凑，不必再建一个只有十行的 stats package。

验证直接调用 summarize，再运行一个 count 会话，两者分别证明计算与接线。不要把测试导入点写成 cli.summarize，即使那个名字当前因导入而可见；公开依赖应指向责任拥有者。

</details>

拆分完成后，新的问题是“为什么直接运行 cli.py 会失败，但 -m 能运行”。下一章从运行身份而不是目录习惯解释入口。
