# Unit 02 — 赋值时到底发生了什么？

> 状态：`BUILT`<br>
> 类型：`CONCEPT` + Mechanism Observation<br>
> 前置：能够接收、清理并回显一段文本<br>
> 完成证据：能够根据代码画出名字与对象关系，并预测重新绑定后的结果

## 1. 一条任务已经不只需要标题

第一版程序只有一个字段：

```python
title = "Learn Python"
```

为了正确描述一条任务，我们还需要回答：

```text
标题是什么？
优先级是多少？
是否已经完成？
有没有备注？
```

用当前已经具备的能力，可以先写成：

```python
title = "Learn Python"
priority = 2
done = False
note = None
```

这四行看起来像四种“变量声明”，但这个说法容易带来一个不准确的盒子模型：名字像盒子，值被装进盒子。理解后续共享引用和可变对象之前，需要先建立更可靠的最小模型。

## 2. Name、Object 与 Binding

对代码：

```python
priority = 2
```

当前最有用的解释是：

```text
先计算右侧表达式 2
→ 得到一个 int 对象
→ 在当前命名空间中，让名字 priority 绑定这个对象
```

关系可以画成：

```text
名字 priority ─────→ int 对象 2
```

三个词分别回答不同问题：

- **Name**：代码用什么名字找到数据，例如 `priority`。
- **Object**：运行中的 Python 值；它具有类型、值和身份。
- **Binding**：名字与对象之间当前建立的关联。

名字本身不是对象的容器，也不携带一个永久固定的类型。它是当前命名空间里的引用入口。

## 3. 四个字段为什么使用不同类型

运行：

```python
title = "Learn Python"
priority = 2
done = False
note = None

print(type(title))
print(type(priority))
print(type(done))
print(type(note))
```

会得到：

```text
<class 'str'>
<class 'int'>
<class 'bool'>
<class 'NoneType'>
```

类型选择来自字段语义：

| 字段 | 当前对象 | 为什么这样表达 |
|---|---|---|
| `title` | `str` | 标题是文本 |
| `priority` | `int` | 当前规则使用离散整数等级 |
| `done` | `bool` | 这里只有完成 / 未完成两个状态 |
| `note` | `None` | 当前没有备注，而不是备注内容为空格或数字零 |

不要为了“练完所有类型”给任务硬加浮点进度。`float` 的精度问题会在 Unit 03 的 Focused Lab 中隔离观察，不污染当前业务模型。

## 4. 对象有类型，名字可以重新绑定

任务完成后，可以写：

```python
done = False
print(done)

done = True
print(done)
```

第二次赋值没有把 `False` 对象“改成” `True`。发生的是重新绑定：

```text
之前：名字 done ─────→ bool 对象 False

之后：名字 done ─────→ bool 对象 True
```

这就是 **rebinding**。右侧先求值，随后左侧名字改为关联新的结果。

Python 允许同一个名字后来绑定不同类型的对象：

```python
priority = 2
priority = "high"
```

代码能够运行，不代表模型合理。Task Tracker 已经约定优先级是 `1～3` 的整数；把同一个业务字段改成任意字符串，会把校验负担推给所有使用它的代码。

准确说法是：

> Python 在运行时由对象携带类型，名字可以重新绑定；业务代码仍然应该保持稳定、清楚的数据契约。

## 5. 赋值与比较不是一回事

```python
done = False
```

`=` 建立绑定。它不提出问题，也不判断两边是否相等。

```python
done == False
```

`==` 计算相等性，并产生布尔结果。更自然的布尔判断通常直接写成 `done` 或 `not done`，但系统控制流会在 Module 03 正式展开。

现在只需避免一个常见错误：

```text
=   assignment / binding
==  equality comparison
```

## 6. 表达式先产生结果，再发生绑定

赋值右侧不必只是字面值：

```python
priority = 1 + 1
```

可以按顺序理解：

```text
计算 1 + 1
→ 得到 int 对象 2
→ 名字 priority 绑定结果对象
```

再看：

```python
title = "  Learn Python  ".strip()
```

`.strip()` 先产生清理后的字符串，随后 `title` 绑定这个结果。原字符串对象并没有被原地修改。

这种“右侧求值 → 左侧绑定”的顺序会贯穿函数调用、容器操作和对象创建。现在建立准确模型，后面遇到 Bug 时就不必依赖“变量盒子里神秘变化”的猜测。

## 7. Identity 是观察线索，不是业务编号

`id()` 可以在当前进程中观察一个对象的身份标识：

```python
title = "Learn Python"
print(id(title))

title = "Review Python"
print(id(title))
```

两次结果可能不同，因为 `title` 已经重新绑定。这里需要守住三个边界：

- `id()` 用于观察当前运行中的对象身份。
- 数字的具体大小没有业务含义，也不应该写进测试。
- 它不能充当 Task Tracker 的任务 ID；业务 ID 需要由业务规则稳定定义。

`is` 用于判断两个表达式是否得到同一个对象，`==` 用于比较值或语义是否相等。Stage 01 当前只要求正确处理 `None`：

```python
note is None
```

不要把字符串和数字的 `is` 结果当作相等性判断。

## 8. `None` 与空字符串不是同一个状态

观察：

```python
missing_note = None
empty_note = ""

print(missing_note is None)
print(empty_note is None)
print(bool(missing_note))
print(bool(empty_note))
```

结果是：

```text
True
False
False
False
```

`None` 和空字符串都属于 falsy 值，但它们表达的状态不同：

```text
None  → 没有提供备注
""    → 提供的是空文本，或者输入尚未完成规范化
```

因此：

> falsy 是布尔上下文中的行为，不等于“这些值完全相同”。

Unit 03 会在输入边界把清理后的空备注转换为 `None`，让程序内部只保留一个明确的“缺失”状态。

## 9. Prediction Exercise

先不要运行，写出每次输出和最终绑定关系：

```python
title = "Learn Python"
priority = 1 + 1
done = False
note = ""

print(type(priority))
print(note is None)

note = None
done = True

print(note is None)
print(done)
```

然后运行验证。若预测错误，不要只修改答案，要指出误解发生在：

```text
右侧求值
名字绑定
对象类型
重新绑定
None 与 falsy
```

## 10. Modeling Exercise

为一个“会议提醒”选择当前阶段足够简单的类型：

```text
会议标题
提前多少分钟提醒
是否已经确认
可选会议室
```

要求：

1. 写出四个有业务含义的名字与示例值。
2. 写出每个对象的类型。
3. 用一句话说明为什么缺失会议室使用 `None`，而不是 `0`。
4. 把“是否已经确认”从 `False` 重新绑定为 `True`，画出前后关系。

## 11. 完成检查

你应该能够不看正文解释：

1. `priority = 1 + 1` 中，求值和绑定按什么顺序发生？
2. 类型属于名字还是对象？
3. `done = True` 是修改了 `False`，还是让名字重新绑定？
4. `None` 和 `""` 为什么都 falsy，却不能互相替代？
5. `id()` 为什么不能作为任务的业务 ID？

下一 Unit 会把这些字段重新连接到用户输入。那时我们会看到一个关键事实：用户键入的优先级最初仍然是 `str`，业务模型却需要 `int`。
