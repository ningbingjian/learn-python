# 01-004：交互模式与脚本模式

[阶段导航](../README.md) · [上一课：01-003](../003-paths-and-execution/README.md) · [下一课：01-005](../005-errors-and-tracebacks/README.md)

## 1. 本课目标与准备

同一个字符串，输入交互窗口会出现结果，放进脚本却可能什么也不显示。这一课用完全相同的输入做对照，学会识别当前是在 shell 还是 Python 中，并解释回显与输出的区别。

前置：完成 01-003。沿用第一课检查成功的 Python 3 与编辑器，不重复安装。代码只用内置功能或本课明确讲解的标准库，不需要第三方依赖。

在自己的 `python-practice` 下创建 `004-interactive-and-script` 作为**本课目录**，按下文路径创建步骤文件；也可打开仓库的同名目录核对源码。文件用 UTF-8 保存。每步的完整代码均独立保留，不能覆盖前一步。

凡标注“从本课目录开始”的命令，先在编辑器资源管理器中右键这个目录，选择“在集成终端中打开”。不要默认终端还停在上一步所需位置。macOS/Linux 示例使用 bash/zsh 和 `python3`；Windows 示例使用 PowerShell 和已确认可用的 `python`，只有 `py` 可用时替换该入口。虚拟环境的明确解释器路径不做这种替换。

验证基线为 Linux / bash / CPython 3.12.13。macOS、PowerShell 与编辑器界面未实测；实际检查范围见 [本课验证记录](VERIFICATION.md)。完成运行验证不表示读者已学完。

## 2. 理论：两种运行方式，多了哪一个环节

### 2.1 交互模式的循环

不带脚本参数启动 Python，通常会进入交互模式。它等待输入，求值，再把合适的结果显示出来，随后等待下一次输入；这个过程常叫 REPL。这里“显示表达式结果”是交互环境提供的帮助，不等于每种 Python 程序都会这样显示。

直接输入字符串表达式 `"模式实验"`，交互解释器通常显示 `'模式实验'`。这是一种表示形式，帮助你看出结果是字符串；输出的引号样式不必与输入相同。调用 `print("模式实验")` 则明确要求输出文本，显示时不带界定字符串的引号。

`print` 调用还有一个返回结果 `None`。本课只需知道：它表示这里没有有用的返回值，交互环境不会把这个 `None` 自动回显，因此不会在文本后多显示一行 `None`。None 的完整含义在阶段 02 学习。

### 2.2 脚本模式为什么不自动显示表达式

给解释器一个文件，它会执行文件里的语句；普通脚本没有交互窗口那种自动回显。写一条裸字符串表达式不会自动将它打印到终端。程序“执行了内容”和“产生了可见输出”是两件事。

这也解释了为什么后面写函数时不能把“算出结果”直接等同于“打印结果”。当前先用字符串对比，不需要引入计算或变量。

### 2.3 输入应交给哪个程序

| 当前状态 | 常见界面线索 | 这里接收什么 |
| --- | --- | --- |
| shell | 路径及 shell 提示符，形式因系统不同 | `python3 main.py`、目录命令 |
| Python 交互模式 | `>>>` | Python 语句或表达式 |
| Python 未完成输入 | `...` | 上一段输入的后续内容，不是需要照抄的字符 |

提示符是环境显示的标记，不是源码。官方交互模式说明见 [解释器教程](https://docs.python.org/3/tutorial/interpreter.html)。

### 理论总结

交互环境会帮你展示某些表达式结果；脚本只执行你的程序，是否输出要看程序有没有输出动作。接下来用同一文本分别验证。

## 3. 第一步：进入、输入并退出交互模式

本步骤是交互操作，完整输入和会话记录保存在 [step01-interactive/README.md](step01-interactive/README.md)，不强行创建一个假装交互操作的 `.py` 文件。

**从本课目录的 shell 开始**：

```bash
# 没有附带脚本参数，因此进入 Python 交互模式。
python3
```

```powershell
# 进入交互模式；只有 py 可用时输入 py。
python
```

看到 `>>>` 后，下面每条输入分别提交，不把注释和多行代码一次性混成一段 shell 命令：

```python
# 第一次输入：求值一个字符串，观察交互环境的回显。
"模式实验"
```

预期回显：

```text
'模式实验'
```

```python
# 第二次输入：显式调用 print，比较输出是否带引号。
print("模式实验")
```

预期显示：

```text
模式实验
```

```python
# 第三次输入：退出这个交互会话，回到 shell。
exit()
```

**原理与小总结：** 两次输入都与字符串有关，但第一次看到的是自动回显，第二次看到的是输出函数的效果。退出后 shell 重新接管输入；不要在 Python 模式里继续输入脚本启动命令。

## 4. 第二步：把相同内容放进脚本

创建 `step02-script/main.py`。前一课已经讲过 `print`，这里只复述它的输出职责；新增观察对象是前面的裸字符串表达式。

<!-- source: step02-script/main.py -->
```python
# 用途：对照交互模式，观察普通脚本不会自动回显裸字符串表达式。
# 运行：在本目录执行 python3 main.py；Windows 使用 python main.py。
# 这段文本不会主动输出；若位于模块开头还可作为文档字符串，当前不展开该用途。
"模式实验"
# 明确调用 print 才产生这里需要的终端文本。
print("模式实验")
```
**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd step02-script
# 执行本目录的 main.py，文件必须先保存。
python3 main.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location step02-script
# 执行已经保存的 main.py。
python main.py
```

预期只有一行：

```text
模式实验
```
**观察：** 如果输出两行，检查自己是否额外写了第二个 `print`，或把上次命令的历史输出一起数进来了。为了独立验证裸表达式的行为，再创建同一步中的对照文件：

<!-- source: step02-script/expression_only.py -->
```python
# 用途：只有裸字符串的脚本；预期成功退出，但没有标准输出。
# 在本目录运行 python3 expression_only.py；Windows 使用 python expression_only.py。
# 没有 print 调用，不要求终端显示这个表达式的值。
"模式实验"
```
**留在 step02-script 目录**：

```bash
# 运行只含裸字符串的对照文件；预期没有文本输出。
python3 expression_only.py
```

```powershell
# 没有文本输出但正常回到 shell，这是本实验的成功结果。
python expression_only.py
```

**小总结：** 没有可见输出不一定失败。要看程序是否要求输出，以及是否有错误。这里没有输出是设计的结果。

## 5. 排错实验：在错误的模式下输入内容

1. 在本课目录启动 Python，看到 `>>>` 后故意输入 `python3 main.py`（Windows 也可用这段文字作错误案例）。它是 shell 命令形态，Python 不能按合法语句解析，预期 `SyntaxError`。
2. 输入 `exit()` 回到 shell，再从 `step02-script` 运行文件，成功输出一行。不要在交互模式里用 shell 的目录命令修复它。
3. 若在交互模式只输入了未闭合的 `print(`，会看到 `...`。按 Ctrl+C 取消这次未完成输入，看到 `>>>` 后重新输入完整语句。这是取消当前输入，不是把三个点加到代码里。

把提示符抄进脚本也会失败。下面单独保留错误和修复，便于比较：

<!-- source: errors/broken.py -->
```python
# 故意失败：>>> 是交互提示符，不属于 Python 源码。
# 在 errors 目录运行 python3 broken.py；Windows 使用 python broken.py。
>>> print("模式实验")
```
<!-- source: errors/fixed.py -->
```python
# 修复：移除提示符，只保留实际需要执行的调用。
# 在 errors 目录运行 python3 fixed.py；Windows 使用 python fixed.py。
print("模式实验")
```
**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd errors
# 执行本目录的 broken.py，文件必须先保存。
python3 broken.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location errors
# 执行已经保存的 broken.py。
python broken.py
```
预期 `SyntaxError`，无正常输出。**留在 errors 目录**运行修复版：

```bash
# 正确源码只包含要执行的 Python 语句。
python3 fixed.py
```

```powershell
# 应显示一行“模式实验”。
python fixed.py
```

## 6. 练习与课程总结

完成 [预测两种模式的结果](exercises/README.md)，答案与输入记录单独保存。

自测：裸字符串脚本没有输出是不是没执行？为什么 `print` 的交互输出没有多一行 None？`>>>` 应该由谁写出来？

关键结论：成功执行可以没有输出；交互环境不回显 None；提示符由环境显示，用户输入不包含它。下一课把“失败发生在哪个环节”讲透，而不再只看到报错就改引号。
