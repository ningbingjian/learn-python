# 01-006：检查并选择项目解释器

[阶段导航](../README.md) · [上一课：01-005](../005-errors-and-tracebacks/README.md) · [下一课：01-007](../007-virtual-environment/README.md)

## 1. 本课目标与准备

能打印相同文字，只能证明两边都能跑这段简单代码，不能证明编辑器和终端用了同一个 Python。本课让解释器报告自身路径与版本，按证据选择运行入口。

前置：完成 01-005。沿用第一课检查成功的 Python 3 与编辑器，不重复安装。代码只用内置功能或本课明确讲解的标准库，不需要第三方依赖。

在自己的 `python-practice` 下创建 `006-interpreter-selection` 作为**本课目录**，按下文路径创建步骤文件；也可打开仓库的同名目录核对源码。文件用 UTF-8 保存。每步的完整代码均独立保留，不能覆盖前一步。

凡标注“从本课目录开始”的命令，先在编辑器资源管理器中右键这个目录，选择“在集成终端中打开”。不要默认终端还停在上一步所需位置。macOS/Linux 示例使用 bash/zsh 和 `python3`；Windows 示例使用 PowerShell 和已确认可用的 `python`，只有 `py` 可用时替换该入口。虚拟环境的明确解释器路径不做这种替换。

验证基线为 Linux / bash / CPython 3.12.13。macOS、PowerShell 与编辑器界面未实测；实际检查范围见 [本课验证记录](VERIFICATION.md)。完成运行验证不表示读者已学完。

## 2. 理论：版本号、命令名称与实际路径

### 2.1 同一个命令名称可能指向不同程序

终端里的 `python3` 是一个命令入口。shell 会根据自身的命令查找规则找到对应程序；PATH 可以先理解为一组用来查找程序的目录。同一台电脑的不同终端，或激活环境前后，查找结果可能不同。

编辑器又有自己的解释器选择。点击运行、调试或在终端手动输入命令，并不天然使用同一个入口。某些编辑器会为新终端自动激活所选环境，但不能据此假设所有旧终端也已经切换。

### 2.2 为什么只看版本不够

两个安装都可能显示 Python 3.12.13，却在不同目录，拥有不同依赖。版本号回答“是什么版本”，路径回答“从哪个位置启动”。先同时收集这两个证据。

路径不同也不能立刻断言安装完全不同：某些入口可能是符号链接或别名。课程的目标是选择明确、可复现的入口；虚拟环境是否归属于同一位置将在 007 加上 prefix 信息继续判断，而不是用一行路径比较替代所有环境诊断。

### 2.3 为什么使用 sys

`sys` 是 Python 提供的标准库模块，提供解释器相关信息。`import sys` 让当前程序可以使用这个模块；`sys.executable` 中的点表示读取模块提供的属性，而不是字符串拼接。

| 代码 | 本课含义 |
| --- | --- |
| `import sys` | 导入标准库模块，让后面的语句可以引用它 |
| `sys.executable` | 当前解释器可执行文件路径，在普通安装中通常是绝对路径 |
| `sys.version` | 当前解释器的版本与构建信息，可能包含换行 |
| `print(sys.executable)` | 将实际属性值显示出来，不能给整段表达式加引号 |

若写成 `print("sys.executable")`，输出的是这串字母，不是在读取实际路径。这里把“模块和属性访问”作为明确的诊断工具知识；模块搜索、包组织与完整导入机制留到阶段 06。属性边界参考 [sys 官方文档](https://docs.python.org/3/library/sys.html#sys.executable)，某些特殊嵌入环境可能没有可用 executable 路径，不把它们当普通安装处理。

### 理论总结

先确认启动入口，再让运行中的程序报告路径和版本。后面两步用相同诊断逻辑比较终端与编辑器，不引入第三方包制造依赖错误。

## 3. 第一步：在终端检查

创建 `step01-terminal-check/main.py`，完整抄写：

<!-- source: step01-terminal-check/main.py -->
```python
# 用途：让当前解释器报告自身信息；不读取账号或业务数据。
# 运行：在本目录执行 python3 main.py；Windows 使用已确认的 python main.py。
# sys 是随 Python 提供的标准库；导入后才能读取它提供的解释器属性。
import sys

# 标题与属性值分开输出，避免误把属性表达式写成固定字符串。
print("解释器路径：")
print(sys.executable)
# 版本信息可能含构建日期、编译器信息或换行，不强求各电脑文字相同。
print("版本信息：")
print(sys.version)
```
**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd step01-terminal-check
# 执行本目录的 main.py，文件必须先保存。
python3 main.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location step01-terminal-check
# 执行已经保存的 main.py。
python main.py
```
输出应有“解释器路径：”和“版本信息：”两个标题，标题后分别是真实值。以下仅为**虚构示意**，尖括号部分不是固定输出，也不应写进源码：

```text
解释器路径：
<本机实际解释器绝对路径>
版本信息：
<本机 Python 版本和构建信息，可能多行>
```

先把路径与版本记在自己的本地记录中；公开分享排错信息时用通用路径替换其中的个人目录。若输出只是 `sys.executable`，检查是否错误加了引号。

**小总结：** 终端成功运行和版本检查已有基础；新增加的是让运行中的解释器报告实际身份。

## 4. 第二步：选择编辑器解释器并对照

创建独立 `step02-editor-check/main.py`，抄写相同诊断逻辑，确保本步骤能独立运行：

<!-- source: step02-editor-check/main.py -->
```python
# 用途：让当前解释器报告自身信息；不读取账号或业务数据。
# 运行：在本目录执行 python3 main.py；Windows 使用已确认的 python main.py。
# sys 是随 Python 提供的标准库；导入后才能读取它提供的解释器属性。
import sys

# 标题与属性值分开输出，避免误把属性表达式写成固定字符串。
print("解释器路径：")
print(sys.executable)
# 版本信息可能含构建日期、编译器信息或换行，不强求各电脑文字相同。
print("版本信息：")
print(sys.version)
```
先在终端运行第二份副本作为基线：

**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd step02-editor-check
# 执行本目录的 main.py，文件必须先保存。
python3 main.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location step02-editor-check
# 执行已经保存的 main.py。
python main.py
```
预期两步标题一致；如果两次用相同入口且环境未变，路径和版本应一致。然后在 VS Code 中：

1. 打开第二步的 `main.py` 并保存。确保使用第一课的 Microsoft Python 扩展。
2. 打开命令面板：macOS `Command+Shift+P`，Windows/Linux `Ctrl+Shift+P`。
3. 运行 `Python: Select Interpreter`，或点击状态栏的环境选择入口，选择刚才记录的解释器路径。只看版本名称不够。
4. 列表没有该项时，可通过输入解释器路径入口定位可执行文件；具体入口随扩展版本变化，参考 [VS Code 环境说明](https://code.visualstudio.com/docs/python/environments)。不要选择项目的 `.py` 源码文件。
5. 使用 Python 扩展的 `Run Python File in Terminal` 运行当前文件。不要误用其他扩展提供的不同 Run Code 入口。
6. 对比新结果与终端基线。如果旧终端仍使用旧入口，新开终端再运行，并查看实际启动命令。最终以诊断输出为准。

| 观察 | 解释与下一步 |
| --- | --- |
| 路径与版本一致 | 普通场景下已对齐本课要求，保留记录 |
| 版本一致但路径不同 | 可能不同安装/环境，也可能别名；先明确选择同一已知入口再复查 |
| 编辑器指向不存在的路径 | 重新选择存在的可执行文件，不修改诊断源码 |
| 终端能运行，编辑器列表为空 | 检查扩展是否加载、工作区和环境发现情况，使用官方排查入口 |

**小总结：** 改编辑器选择影响它的运行入口，不是把整个操作系统的 Python 统一替换。GUI 操作需在自己的电脑完成，本课程验证环境未安装可运行 VS Code，因此不声称该部分实测通过。

## 5. 排错实验与不一致案例

可复现的源码层错误：在自己的临时副本中把属性访问加引号，运行后输出固定的 `sys.executable`；移除表达式外的引号，重新运行，恢复真实路径。这个变化不需要重装 Python。

以下是**虚构诊断案例**，不是要求安装多个解释器：

| 入口 | 路径 | 版本 |
| --- | --- | --- |
| 外部终端 | `/opt/python-a/bin/python3` | 3.12.13 |
| 编辑器 | `/opt/python-b/bin/python3` | 3.12.13 |

不能因为版本相同就宣布对齐；应明确要使用哪个环境，选择对应路径后重新运行两边。只有一个解释器也能完成前面的实测对照，案例用于理解差异，不需要删除、破坏系统安装制造故障。

直接验证固定字符串与属性读取的差别，可运行两份独立文件：

<!-- source: errors/literal.py -->
```python
# 逻辑错误演示：语法合法并正常退出，但没有读取真实解释器信息。
# 在 errors 目录运行 python3 literal.py；Windows 使用 python literal.py。
print("sys.executable")
```
<!-- source: errors/fixed.py -->
```python
# 修复：导入模块，读取属性；保留点号表达式而不加字符串引号。
# 在 errors 目录运行 python3 fixed.py；Windows 使用 python fixed.py。
import sys
print(sys.executable)
```
**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd errors
# 执行本目录的 literal.py，文件必须先保存。
python3 literal.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location errors
# 执行已经保存的 literal.py。
python literal.py
```
预期输出固定文本 `sys.executable`，退出成功却未完成诊断目标。**留在 errors 目录**运行修复版：

```bash
# 读取并显示真实解释器路径。
python3 fixed.py
```

```powershell
# 显示当前 Python 的可执行文件位置。
python fixed.py
```

## 6. 练习与课程总结

完成 [解释器诊断练习](exercises/README.md)。本课验收是会记录和判断入口，不是要求所有电脑打印同一条路径。

自测：为什么不把 sys.executable 加引号？同版本是否必然同环境？选择编辑器环境后，为什么还要重新运行诊断？

答案：加引号会变成固定文本；同版本可能有不同安装位置；配置界面选择不是实际执行证据，旧终端或其他运行入口还可能未对齐。下一课用 venv 实际创建一个项目环境，再观察它与基础解释器的关系。
