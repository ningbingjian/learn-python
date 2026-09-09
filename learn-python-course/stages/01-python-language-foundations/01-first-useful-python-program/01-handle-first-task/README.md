# Unit 01 — 怎样让程序处理第一条任务？

> 状态：`BUILT`<br>
> 类型：`CONCEPT` + Micro Exercise<br>
> 前置：能够创建并运行 Python 文件<br>
> 完成证据：能够不照抄地写出一个接收、清理并回显文本的交互脚本

## 1. 现在缺少的不是更多运行原理

完成 Stage 00 后，你已经可以创建文件并执行：

```python
print("Hello, Python")
```

这能证明运行链路可用，却还不能处理任何来自用户的数据。Task Tracker 的第一个真实需求很小：

> 用户输入任务标题，程序确认自己收到了什么。

这个需求足以引出本 Unit 真正需要的三个能力：

```text
接收文本
→ 给这段文本一个业务名字
→ 把处理后的结果反馈给用户
```

## 2. 第一条任务

创建一个临时 Python 文件，输入：

```python
title = input("Task title: ")
print(f"Created task: {title}")
```

运行并输入 `Learn Python`：

```text
Task title: Learn Python
Created task: Learn Python
```

程序现在不再只输出作者预先写死的内容。它读取本次运行中的输入，并把输入连接到一次具体的业务行为：创建任务。

## 3. `input()` 交付的是什么

表达式：

```python
input("Task title: ")
```

会先显示提示文本，然后等待用户输入一行内容。用户按下 Enter 后，这行内容以字符串形式交给程序。

此时只需要形成一个准确结论：

> `input()` 返回文本。即使用户键入的是 `123`，当前得到的仍然是字符串，而不是整数。

可以用一个观察验证：

```python
title = input("Task title: ")
print(type(title))
```

输入任何内容，都会看到：

```text
<class 'str'>
```

`type()` 在这里是观察工具，不是要求你背诵所有 Python 类型。为什么一个名字可以关联某种类型的对象，会在 Unit 02 建立更准确的模型。

## 4. 为什么先给数据一个业务名字

下面的写法也能运行：

```python
print(f"Created task: {input('Task title: ')}")
```

但它把读取输入和输出确认压在同一个表达式中。只要下一条需求要求清理标题、判断空输入或多次使用标题，就必须把表达式重新拆开。

使用：

```python
title = input("Task title: ")
```

不是为了多写一行，而是让后续代码能够用 `title` 表达业务含义。名字应该说明数据在当前程序里的角色，而不是它在内存中的位置。

比较：

```python
x = input("Task title: ")
data = input("Task title: ")
title = input("Task title: ")
```

三者都能保存结果，但只有 `title` 让下一位读者无需猜测这段文本是什么。

## 5. 输入边界先做最小清理

用户可能在标题前后意外输入空格：

```text
Task title: ···Learn Python···
```

这里用 `·` 显示原本不可见的空格。

任务标题通常不需要保留这些边界空白。字符串的 `.strip()` 会返回去除首尾空白后的新字符串：

```python
title = input("Task title: ").strip()
print(f"Created task: {title}")
```

这里有两个重要边界：

- `.strip()` 不会删除标题中间的空格，`Learn Python` 仍然包含两个单词。
- `.strip()` 不会修改原字符串，而是产生一个清理后的字符串结果。

字符串为什么不能原地修改，以及“产生新对象”意味着什么，会在下一 Unit 结合赋值解释。此刻先建立工程习惯：

> 外部文本刚进入程序时，先完成与业务规则一致的最小规范化。

## 6. f-string 负责组合反馈

代码：

```python
print(f"Created task: {title}")
```

字符串前的 `f` 允许 `{title}` 在运行时被当前值替换。它让固定文案和变化数据保持清楚：

```text
固定部分：Created task:
变化部分：title
```

本阶段优先使用这种直观写法。字符串格式化的完整能力不是当前问题，不需要在第一条任务后展开对齐、精度或自定义格式协议。

## 7. 先观察失败，不急着一次修完

再次运行程序，这次直接按 Enter：

```text
Task title:
Created task:
```

程序语法正确、退出码也是 `0`，但业务结果无效：它“创建”了一条没有标题的任务。

这个现象很重要，因为它区分了两类正确性：

```text
程序能够运行
≠
程序满足业务规则
```

本 Unit 不马上引入完整校验逻辑。先把失败记录下来：`input()` 能提供数据，却不会替程序判断数据是否可信。Unit 03 会让这个失败成为输入边界存在的理由。

## 8. Micro Exercise：接收任务负责人

在不复制第二套项目的情况下，修改你的临时脚本：

```text
依次询问任务标题和负责人
清理两段输入的首尾空白
输出一句完整确认
```

一组可接受的交互是：

```text
Task title: Review pull request
Owner: Nick
Created task: Review pull request (owner: Nick)
```

约束：

- 使用能表达业务含义的名字。
- 每次 `input()` 都提供清楚提示。
- 使用 f-string 组合最终反馈。
- 暂时不处理空输入；把观察到的错误行为写下来。

## 9. 完成检查

不看前文，回答并实际验证：

1. 用户输入 `123` 时，`input()` 返回的是什么类型？
2. 为什么把输入先绑定到 `title`，而不是直接嵌入 `print()`？
3. `.strip()` 会不会删除标题中间的空格？
4. 脚本能运行为什么仍可能在业务上失败？
5. 能否从空文件写出一个接收、清理并回显任务标题的程序？

如果第 5 项仍然需要逐字照抄，就先重复 Micro Exercise。下一 Unit 会从代码里的 `title = ...` 出发，解释赋值时实际发生了什么。
