# 01-005：认识语法错误与异常回溯

[阶段导航](../README.md) · [上一课：01-004](../004-interactive-and-script/README.md) · [下一课：01-006](../006-interpreter-selection/README.md)

## 1. 本课目标与准备

报错不是一个统一的“程序坏了”。本课分别制造语法错误、运行期名字错误和多余缩进，对比哪几行已经执行，再按文件、位置、类型和原因修复。所有故障文件都有独立正确版本。

前置：完成 01-004。沿用第一课检查成功的 Python 3 与编辑器，不重复安装。代码只用内置功能或本课明确讲解的标准库，不需要第三方依赖。

在自己的 `python-practice` 下创建 `005-errors-and-tracebacks` 作为**本课目录**，按下文路径创建步骤文件；也可打开仓库的同名目录核对源码。文件用 UTF-8 保存。每步的完整代码均独立保留，不能覆盖前一步。

凡标注“从本课目录开始”的命令，先在编辑器资源管理器中右键这个目录，选择“在集成终端中打开”。不要默认终端还停在上一步所需位置。macOS/Linux 示例使用 bash/zsh 和 `python3`；Windows 示例使用 PowerShell 和已确认可用的 `python`，只有 `py` 可用时替换该入口。虚拟环境的明确解释器路径不做这种替换。

验证基线为 Linux / bash / CPython 3.12.13。macOS、PowerShell 与编辑器界面未实测；实际检查范围见 [本课验证记录](VERIFICATION.md)。完成运行验证不表示读者已学完。

## 2. 理论：先问错误发生在执行前还是执行中

### 2.1 语法检查失败

对本课这些普通脚本，解释器会先检查、处理整个文件的语法，再进入其中的正常执行。若后面一行字符串未闭合，前面即使有正确的 `print` 也不会先执行。这不是“执行到坏行才发现”的情况。

`SyntaxError` 表示语法结构不合法，例如缺少引号或括号。提示中常有文件、行号和指示位置；提示位置可能是发现无法继续解析的地方，真正遗漏也可能在附近上一行。

### 2.2 语法正确也可能运行失败

`prnit("执行中")` 在形式上像一个合法的函数调用，所以可以通过语法检查。但运行到这里，需要查找名为 `prnit` 的功能，本程序没有定义它，就会产生 `NameError`。之前已经完成的输出不会撤回；后续语句没有机会执行。

这里仅认识“名字查找失败”，不提前学习定义函数或变量作用域。修复本例是把拼写改回已有的内置 `print`。

### 2.3 回溯怎么看

运行期异常常显示 `Traceback (most recent call last):`，接着是调用位置，最后是错误类型和原因。先读末尾类型与原因，再回到最近相关的文件行定位；以后多层函数调用时才需要追完整调用链。语法错误通常直接给文件位置与语法诊断，不一定有同样的 Traceback 标题。

终端把标准输出与标准错误同时显示，顺序可能受缓冲影响。判断“前面是否执行”应检查输出内容，不能只根据错误文字视觉上出现在哪一行。测试时会分别检查两个输出流。

### 2.4 缩进也是语法结构

Python 用缩进表达代码块关系，不能把任意顶层语句向右多缩几个空格当成装饰。本课没有需要缩进的结构，顶层输出语句应从行首开始。`IndentationError` 属于 `SyntaxError` 的一类；后续学习条件和函数时再详细学习正确缩进。

### 理论总结

语法期失败：本文件正常语句尚未执行。运行期失败：失败前的语句可能已执行。用“开始/结束”输出作为观察标记，下面三步就能验证这一区别。

## 3. 第一步：字符串未闭合

新建 `step01-syntax-error/broken.py` 与 `fixed.py`。先抄故障版，注意漏引号是故意设计，不要把它当最终答案：

<!-- source: step01-syntax-error/broken.py -->
```python
# 故意失败：第二条调用的字符串缺少结尾引号。
# 在本目录执行 python3 broken.py；Windows 使用 python broken.py。
print("开始")
print("处理中)
print("结束")
```
<!-- source: step01-syntax-error/fixed.py -->
```python
# 修复：补齐字符串结尾的英文双引号，其他语句顺序保持不变。
# 在本目录执行 python3 fixed.py；Windows 使用 python fixed.py。
# 三条调用现在都能执行，用开始和结束标记验证完整流程。
print("开始")
print("处理中")
print("结束")
```
**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd step01-syntax-error
# 执行本目录的 broken.py，文件必须先保存。
python3 broken.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location step01-syntax-error
# 执行已经保存的 broken.py。
python broken.py
```
预期：标准输出为空，错误包含 `SyntaxError` 和 `unterminated string literal`，位置指向第 4 行附近；不会输出“开始”。这是语法检查阶段已终止的证据。

**留在当前步骤目录**执行修复版：

```bash
# 单独运行修复版，验证三个标记都出现。
python3 fixed.py
```

```powershell
# 运行结构完整的修复版。
python fixed.py
```

预期输出：

```text
开始
处理中
结束
```
**小总结：** 错误在后面的源码行，不意味着前面已经运行。先通过整个脚本的语法检查才进入正常执行。

## 4. 第二步：调用名字拼错

创建 `step02-runtime-error/broken.py` 和 `fixed.py`。这次引号与括号都配对，错误换成函数名拼写：

<!-- source: step02-runtime-error/broken.py -->
```python
# 故意失败：prnit 的拼写与内置 print 不同，预期 NameError。
# 在本目录运行 python3 broken.py；Windows 使用 python broken.py。
print("开始")
prnit("处理中")
print("结束")
```
<!-- source: step02-runtime-error/fixed.py -->
```python
# 修复：把不存在的 prnit 改回内置 print。
# 在本目录运行 python3 fixed.py；Windows 使用 python fixed.py。
# 不捕获或忽略错误，而是修正本次实验的真实原因。
print("开始")
print("处理中")
print("结束")
```
**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd step02-runtime-error
# 执行本目录的 broken.py，文件必须先保存。
python3 broken.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location step02-runtime-error
# 执行已经保存的 broken.py。
python broken.py
```
预期标准输出只有：

```text
开始
```
错误末尾包含 `NameError` 和 `prnit`。先找到出错文件，再查看第 4 行拼写。“开始”证明执行已进入程序；“结束”缺失说明异常中断了后续执行。

**留在 step02-runtime-error 目录**执行：

```bash
# 修正名字后的三条输出应全部出现。
python3 fixed.py
```

```powershell
# 修复版应正常退出，显示开始、处理中、结束。
python fixed.py
```

预期三行与第一步修复版相同。**小总结：** 运行期异常不会撤销已产生的输出；若程序还写入了文件等内容，之前的副作用也不能假设自动回滚，本课不引入这些操作。

## 5. 第三步：多余缩进

创建 `step03-unexpected-indent` 下两份文件。故障版第二条输出前保留四个空格：

<!-- source: step03-unexpected-indent/broken.py -->
```python
# 故意失败：顶层第二条输出没有所属代码块，却被额外缩进。
# 在本目录运行 python3 broken.py；Windows 使用 python broken.py。
print("开始")
    print("处理中")
print("结束")
```
<!-- source: step03-unexpected-indent/fixed.py -->
```python
# 修复：本课所有调用都在顶层，左侧统一从行首开始。
# 在本目录运行 python3 fixed.py；Windows 使用 python fixed.py。
print("开始")
print("处理中")
print("结束")
```
**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd step03-unexpected-indent
# 执行本目录的 broken.py，文件必须先保存。
python3 broken.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location step03-unexpected-indent
# 执行已经保存的 broken.py。
python broken.py
```
预期：标准输出为空，错误包含 `IndentationError: unexpected indent`。它是语法类错误，不会先输出“开始”。

**留在当前步骤目录**验证修复：

```bash
# 移除多余缩进后，运行三条正常输出。
python3 fixed.py
```

```powershell
# 修复版三条语句都从行首开始。
python fixed.py
```

预期仍为开始、处理中、结束三行。**小总结：** 空格在某些位置有结构意义。不要用“把所有空格删掉”作为通用修复；这里删除的是没有结构依据的行首缩进。

## 6. 从实验中得到一套排错方法

| 证据 | 第一步 | 第二步 | 第三步 |
| --- | --- | --- | --- |
| 主要类型 | SyntaxError | NameError | IndentationError |
| 开始是否输出 | 否 | 是 | 否 |
| 失败阶段 | 语法处理 | 运行期名字查找 | 语法处理 |
| 修复对象 | 缺失的字符串边界 | 拼错的名称 | 多余的顶层缩进 |

不要把正常文件的输出和故障文件的历史输出混在一起判断。记录运行了哪个文件、标准输出有哪些内容、错误类型和原因；修正后独立运行 `fixed.py`。失败文件重复运行仍应失败，它们是教学材料，不需要通过忽略异常来“变绿”。

更完整的官方解释见 [错误和异常教程](https://docs.python.org/3/tutorial/errors.html)。本课没有 try/except，后续阶段 06 才学习什么时候可以处理异常、什么时候应该继续传播。

## 7. 独立练习与课程总结

[练习目录](exercises/README.md) 提供三个单一故障文件。先判断哪些输出会出现，再运行、定位、修复，最后与单独答案比较。

自测：最后一行语法错误会先输出前两行吗？NameError 是否意味着 Python 根本没启动？IndentationError 与 SyntaxError 有什么关系？

结论：普通脚本的语法错误阻止正常执行；NameError 是运行中名字查找失败；IndentationError 属于语法错误。下一课把检查范围移到解释器本身，避免拿源码修复办法处理环境选择问题。
