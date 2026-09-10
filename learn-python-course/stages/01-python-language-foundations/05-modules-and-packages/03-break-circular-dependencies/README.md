# Unit 03 — 循环导入为什么是设计信号？

> 状态：`BUILT` · 类型：FAILURE / BUILD<br>
> 起点：[04-function-oriented](../../04-functions-and-contracts/03-state-and-scope/04-function-oriented/)<br>
> 完整结果：[05-package-structured](05-package-structured/)

## 两个函数单独看没错，导入为什么失败？

假设为了复用提示文案，operations 导入 cli 的成功消息；cli 又必须导入 operations 的新增操作。它们形成双向依赖。本基线实际报错为 `ImportError: cannot import name 'success_message' from 'cli'`，有时附带改名建议；其他版本可能提到 `partially initialized module`。不能只按最后一句建议猜原因，需要沿调用链确认初始化顺序。

[故障实验](circular-import-lab/)保留两个极小文件，并用独立进程运行。开始前先预测：是函数拼错了、搜索路径错了，还是其中一个模块尚未执行到函数定义？

错误版的关键关系：

```python
# cli.py
from operations import add_task


def success_message(title):
    return f"Added {title}"


# operations.py 中又执行：
# from cli import success_message
```

执行 `import cli` 时，cli 开始加载并导入 operations；operations 反过来索取 cli 的 success_message，此时定义尚未执行。模块名存在，但需要的名字还不存在。这与“整个包完全找不到”是不同证据。

## 推迟导入有时能绕开时机，却没有回答责任

把 `from cli import success_message` 移进 add_task 函数，可能让调用发生时 cli 已加载完，从而绕开此次错误。它仍然让业务操作依赖终端文案。改 CLI 文案可能影响领域模块，测试也必须知道界面存在。

修复应先问：业务函数为什么要返回“Added ...”而不是返回创建结果？让 operations 返回记录，cli 自己展示，依赖就恢复单向：

```text
__main__ → cli → operations → validation
              → validation
```

这里只表达依赖，不引入依赖注入框架。也不把所有共享内容扔进 `utils.py`，否则双向关系只是换了一个隐蔽名字。

## 完整状态如何从上一版得到

保留上一文件中已有函数行为，将字段解析移入 validation，集合操作移入 operations，交互移入 cli；__main__ 只负责调用入口，__init__ 不执行会话。修改测试导入路径，同时继续使用原来八条 CLI 行为测试。

目录如下：

```text
05-package-structured/
├── README.md
├── task_tracker/
│   ├── __init__.py
│   ├── __main__.py
│   ├── validation.py
│   ├── operations.py
│   └── cli.py
└── tests/
    ├── test_cli.py
    ├── test_rules.py
    └── test_imports.py
```

每个文件都有实际责任。没有空 src、空 unit、空测试或依赖配置。这个里程碑与函数版的外部行为相同；它证明可运行入口和依赖边界，不宣称功能比上一版更多。

运行 `python3.14 -m task_tracker`；测试 `python3.14 -m unittest discover -s tests -v`。导入测试使用新进程，避免当前测试进程已导入过模块而掩盖初始化问题。

## 对“公开接口”的朴素约定

现在测试从 operations 导入 add_task，而不是通过 cli 间接访问。Python 不会因为模块名以外的文档说明就强制禁止访问；公开边界首先是维护约定。__init__ 不批量转发所有实现，避免让每个内部函数都变成需要长期兼容的包顶层接口。

一个下划线名字只是非公开约定，不是安全隔离机制。复杂的导出控制和完整 Import System 留在 Stage 02，不需要现在解释所有加载路径。

## 迁移练习：错误文案来自谁？

新需求：同一次业务失败可以由英文 CLI 或中文 CLI 展示。不要立即给领域函数加入 `language` 参数。提出两种设计，并说明什么时候当前 ValueError 文本契约开始不够。

<details>
<summary>参考判断</summary>

最小版本可让两种 CLI 根据明确错误类别选择文案；随着错误种类增多，领域层需要稳定错误类型或错误码，展示层负责语言。当前课程没有多语言需求，所以保留简单 ValueError 文本，不能把尚未需要的异常层级倒灌进本章。

不可取的是 operations 导入两个 CLI 的翻译函数，那会重新建立反向依赖。练习验收看依赖方向和责任解释，不要求提前实现 Stage 02 的继承体系。

</details>

拆包解决了文件边界，却没有解决 `task["priorty"]` 这种脆弱字段访问，也没有把单条任务的行为放回数据旁边。下一 Module 在这一具体成本出现之后引入 class。
