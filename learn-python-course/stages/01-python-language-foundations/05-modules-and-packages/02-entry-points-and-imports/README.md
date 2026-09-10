# Unit 02 — 程序入口和导入行为是什么关系？

> 状态：`BUILT` · 前置：Module 与依赖方向<br>
> 运行载体：[05-package-structured](../03-break-circular-dependencies/05-package-structured/)

## 文件能被导入，不代表导入应该启动程序

函数版加入入口保护，是为了让测试导入函数时不陷入输入循环。现在明确它的机制：作为顶层程序执行的模块，其 `__name__` 为 `"__main__"`；普通导入的模块使用其模块名。

```python
if __name__ == "__main__":
    run_cli()
```

这不是“告诉解释器从这里开始读”。模块顶层仍自上而下执行，函数定义、赋值和导入都已经发生；只是这个条件决定是否调用会话函数。把 `input()` 留在保护之外，仍会在导入时读取输入。

在同一解释器进程中，普通重复导入通常复用已加载模块，不会每次从头执行；但启动新进程会重新加载。这不是应用状态持久化机制，也不应通过导入副作用创建用户数据。本阶段不展开缓存失效、导入钩子或 reload。

## Package 的入口是一小段组合代码

当前项目包含一个普通 Package，`__init__.py` 只有说明文字，不偷偷导入全部实现。`__main__.py` 保存明确入口：

```python
from .cli import run_cli

if __name__ == "__main__":
    run_cli()
```

在源码根目录运行 `python3.14 -m task_tracker` 时，Python 以模块方式寻找包并执行其 `__main__`。它知道包上下文，所以 `.cli` 能解释为当前包里的 cli 模块。

直接运行 `python3.14 task_tracker/cli.py` 则把文件当成脚本，没有相同的父包身份；其中相对导入会失败。这不是找不到某个 pip 依赖，也不应该靠往 `sys.path` 插入本机绝对路径修补。按照应用约定从源码根目录使用 -m 即可。

## 绝对与相对导入都必须知道依赖来自哪里

Package 内可写：

```python
from .validation import parse_priority
```

也可以写 `from task_tracker.validation import parse_priority`。前者相对于当前包，后者从顶层包名开始。测试是包外调用者，因此使用后者；包内短而稳定的关系使用前者。本课程不会在同一目录随机混用风格。

相对导入的点不是“当前工作目录”，因此不能简单把它理解成文件路径的 `./`。这一区别解释了为什么同一文件以不同方式启动可能有不同结果。

源码根目录没有第三方依赖，也不准备分发安装包，所以不新增 pyproject、build backend 或 wheel。可导入 Package 与可发布 Distribution 不是同一件事。若以后要从任意目录运行命令，需要安装入口等工程能力，属于后续 Packaging 内容。

## 三个只读实验排除入口故障

进入上述完整源码目录：

```bash
python3.14 -c "import task_tracker; import task_tracker.cli; import task_tracker.__main__"
python3.14 -m task_tracker
python3.14 task_tracker/cli.py
```

第一条应静默退出；第二条出现命令提示，输入 quit 结束；第三条是**故意失败实验**，应出现 `ImportError: attempted relative import with no known parent package`。最后一条不是正常启动方式。

若第一条也要求输入，检查顶层副作用；若第二条报告 `No module named task_tracker`，先检查工作目录与包目录是否并列，不要先安装一个同名第三方包。若只第三条失败，则证据符合入口身份差异。

自动测试 `test_imports.py` 在一个新进程中导入包、CLI 和 __main__，断言标准输出和错误输出都为空。这也验证入口保护，而不只是应用恰好能运行。

## 练习：增加一个可安全导入的健康检查

要求在源码根目录新建 `check_tracker.py`：直接运行时创建空集合并输出 `ready`；导入时不输出、不创建任务、不启动 CLI。只使用当前已有操作接口。

<details>
<summary>参考实现</summary>

```python
from task_tracker.operations import add_task


def check():
    tasks = []
    task, next_id = add_task(tasks, 1, "Probe", 2)
    assert task["id"] == 1 and next_id == 2
    return "ready"


if __name__ == "__main__":
    print(check())
```

check 调用时才创建用于探测的临时集合；导入只定义函数。分别执行脚本与 `python3.14 -c "import check_tracker"`，后者应完全静默。这个检查文件是练习产物，不进入课程主线快照。

</details>

入口已经可靠，拆分仍可能因双向依赖崩溃。下一章故意制造一次循环导入，检验文件之间的责任是否真的单向。
