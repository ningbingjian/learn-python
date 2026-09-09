# Unit 03 — 用户输入为什么不能直接相信？

> 状态：`BUILT`<br>
> 类型：`BUILD` + `FAILURE` + `MECHANISM`<br>
> 前置：能够解释 name、object、binding、type、rebinding、`None` 与 falsy<br>
> 完成证据：[`01-interactive-script`](01-interactive-script/) 通过运行验收和自动化测试

## 1. 业务需要整数，输入交付文本

Task Tracker 现在要接收优先级 `1～3`。先观察最直接的写法：

```python
priority = input("Priority (1-3): ")

print(priority)
print(type(priority))
```

即使输入 `2`，结果仍是：

```text
2
<class 'str'>
```

这不是 `input()` 出错，而是输入边界的基本事实：终端交付的是文本。程序必须决定这段文本能否转换成业务需要的对象。

可以把边界画成：

```text
外部文本 "2"
→ 清理
→ 转换
→ 业务校验
→ 内部 int 对象 2
```

省略任何一层都可能让无效状态进入程序内部。

## 2. 清理解决格式噪声，不解决业务正确性

标题和备注先去除首尾空白：

```python
title = input("Task title: ").strip()
note_text = input("Note (optional): ").strip()
```

`.strip()` 可以把：

```text
"   Learn Python   "
```

规范化为：

```text
"Learn Python"
```

但清理后的标题也可能是空字符串：

```python
title = "   ".strip()
print(repr(title))
```

结果是：

```text
''
```

因此清理只能移除格式噪声，不能证明数据满足业务规则。

## 3. 第一条业务规则：标题不能为空

最小校验可以写成：

```python
title = input("Task title: ").strip()

if not title:
    print("Error: title cannot be empty.")
    raise SystemExit(1)
```

这里暂时只建立够用的模型：

- 空字符串在布尔上下文中是 falsy，因此 `not title` 为 `True`。
- 缩进代码只在条件满足时执行。
- `SystemExit(1)` 让程序以失败退出码结束，避免继续创建无效任务。

完整分支设计属于 Module 03，异常与退出策略的系统学习属于 Stage 06。当前先用最小控制流守住真实输入边界。

## 4. 转换失败必须成为可理解的结果

整数转换：

```python
priority_text = input("Priority (1-3): ").strip()
priority = int(priority_text)
```

输入 `2` 时，`int()` 产生整数对象 `2`。输入 `high` 时，它无法猜测用户意图，会抛出 `ValueError`：

```text
ValueError: invalid literal for int() with base 10: 'high'
```

若让 traceback 直接暴露给普通用户，程序虽然提供了技术细节，却没有给出当前业务需要的修复方向。只处理已经理解且能够回应的失败：

```python
try:
    priority = int(priority_text)
except ValueError:
    print("Error: priority must be an integer from 1 to 3.")
    raise SystemExit(1)
```

这个边界的含义是：

```text
尝试把外部文本转换为 int
→ 只捕获预期的 ValueError
→ 给用户业务语境中的错误消息
→ 明确以失败结束
```

不要在这里写 `except:` 捕获一切。无法解释的故障不应该被伪装成“优先级输入错误”。

## 5. 类型正确仍不代表业务有效

`int("9")` 可以成功，但 Task Tracker 只允许 `1～3`：

```python
if not 1 <= priority <= 3:
    print("Error: priority must be between 1 and 3.")
    raise SystemExit(1)
```

现在可以区分两种校验：

| 校验 | 问题 | 失败示例 |
|---|---|---|
| 转换校验 | 文本能否成为目标类型？ | `"high"` 不能成为 `int` |
| 业务校验 | 类型正确的值是否在允许范围？ | `9` 是 `int`，但不是有效优先级 |

把转换和业务范围混成一个模糊的“输入错了”，会让测试和错误反馈都难以准确。

## 6. 可选输入在边界统一为 `None`

备注允许留空：

```python
note_text = input("Note (optional): ").strip()
note = note_text or None
```

表达式 `a or b` 会在 `a` 为 truthy 时得到 `a`，否则得到 `b`。因此：

```text
输入 "Read chapter 1"
→ note_text 是非空字符串
→ note 得到该字符串

直接按 Enter
→ note_text 是空字符串
→ note 得到 None
```

这让程序内部只保留一种“没有备注”的状态。后续代码不必同时猜测 `None`、`""` 和纯空格是不是同一个意思。

显示时仍然明确区分：

```python
if note is None:
    print("Note: (none)")
else:
    print(f"Note: {note}")
```

## 7. 完整的第一版状态

正式源码位于：

- [`01-interactive-script/task_tracker.py`](01-interactive-script/task_tracker.py)
- [`01-interactive-script/tests/test_task_tracker.py`](01-interactive-script/tests/test_task_tracker.py)

它组合了本 Module 的全部必要能力：

```text
title      → str，清理后不能为空
priority   → 从 str 转换为 int，并限制为 1～3
done       → bool，创建时固定为 False
note       → 非空 str 或 None
```

运行：

```bash
cd 01-interactive-script
python task_tracker.py
```

一次成功交互：

```text
CLI Task Tracker — create one task
Task title: Learn Python
Priority (1-3): 2
Note (optional): Finish this module

Created task
Title: Learn Python
Priority: 2
Done: False
Note: Finish this module
```

测试所有主要路径：

```bash
python -m unittest discover -s tests -v
```

这些测试从用户边界启动整个脚本，证明退出码和可观察输出。测试实现使用了尚未学习的标准库工具；当前要求是能够运行测试并阅读用例名称，不要求提前掌握 `subprocess`。

## 8. 为什么现在仍然是单文件

当前脚本只有一条线性创建流程。此时拆成：

```text
domain/
services/
repositories/
cli/
```

不会解决已经发生的问题，只会让初学者在多个文件间跳转。

同样，本状态不增加独立 `pyproject.toml`：

- 只使用 Python 标准库。
- 它是单文件教学脚本，不是独立发布 Package。
- Stage 00 已经证明解释器和测试命令可用。
- 工程配置在责任或依赖边界真正出现时再引入。

简单不是临时羞耻，而是当前约束下更合适的设计。

## 9. Focused Lab：浮点数为什么不完全等于十进制直觉

Task Tracker 的优先级自然使用整数，没有理由硬加一个浮点字段。基础语义仍需要证据，因此单独进入：

[`float-precision-lab`](float-precision-lab/)

这个 Lab 只回答：

> 为什么 `0.1 + 0.2 == 0.3` 可能得到 `False`，比较浮点结果时应该怎样表达容差？

完成实验后返回主线，不把 `float` 变成 Task Tracker 的假需求。

## 10. Failure Matrix

运行正式脚本，逐项观察：

| 输入 | 预期行为 | 退出码 |
|---|---|---:|
| 合法标题、优先级与备注 | 显示完整任务 | `0` |
| 标题只有空格 | 显示标题不能为空 | `1` |
| 优先级为 `high` | 显示必须输入整数 | `1` |
| 优先级为 `0` 或 `4` | 显示范围必须为 1～3 | `1` |
| 备注留空 | 显示 `Note: (none)` | `0` |

如果实际行为与表格不同，先根据失败发生在“清理、转换、业务校验、显示”中的哪一层定位，而不是随机修改代码。

## 11. Transfer Exercise：增加预计用时

不复制最终源码，从当前里程碑增加可选的 `estimated_minutes`：

```text
提示：Estimated minutes (optional):
留空：保存为 None
合法：5～480 的整数
失败：非整数、0、负数或大于 480
输出：有值时显示分钟数；缺失时显示 (none)
```

验收场景至少包括：

```text
""      → None，成功
"30"    → int 30，成功
"fast"  → 转换错误，退出码 1
"0"     → 范围错误，退出码 1
"600"   → 范围错误，退出码 1
```

约束：

- 不引入 `list`、`dict`、函数或 class。
- 不用 `except:` 隐藏未知错误。
- 不把缺失值保存为 `0`。
- 为新增路径补充自动化测试；可以模仿现有测试结构，但必须能解释每个场景证明了什么。

## 12. 完成检查

完成本 Unit 后，你应该能回答：

1. 为什么 `input()` 得到的 `"2"` 不能直接承担整数优先级？
2. 清理、转换和业务校验分别解决什么问题？
3. 为什么只捕获 `ValueError`，而不是捕获所有异常？
4. 为什么范围外的 `9` 是类型正确但业务无效？
5. 为什么空备注在输入边界转换为 `None`？
6. 当前为什么不值得拆 Package 或引入 class？
7. 能否闭卷完成 `estimated_minutes` 变化并让测试通过？

通过这些检查后，下一 Module 才会让“一条任务”成长为“一组任务”，并用真实 Bug 深入共享可变状态。
