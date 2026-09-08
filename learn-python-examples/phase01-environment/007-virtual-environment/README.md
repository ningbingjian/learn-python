# 01-007：创建并使用隔离环境

[阶段导航](../README.md) · [上一课：01-006](../006-interpreter-selection/README.md) · [下一课：01-008](../008-information-card/README.md)

## 1. 本课目标与准备

前一课会看解释器身份，这一课实际创建项目环境。重点理解激活为何能改变命令查找、为什么不激活也能使用环境，以及 pip 究竟归属于哪个解释器。

前置：完成 01-006。沿用第一课检查成功的 Python 3 与编辑器，不重复安装。代码只用内置功能或本课明确讲解的标准库，不需要第三方依赖。

在自己的 `python-practice` 下创建 `007-virtual-environment` 作为**本课目录**，按下文路径创建步骤文件；也可打开仓库的同名目录核对源码。文件用 UTF-8 保存。每步的完整代码均独立保留，不能覆盖前一步。

凡标注“从本课目录开始”的命令，先在编辑器资源管理器中右键这个目录，选择“在集成终端中打开”。不要默认终端还停在上一步所需位置。macOS/Linux 示例使用 bash/zsh 和 `python3`；Windows 示例使用 PowerShell 和已确认可用的 `python`，只有 `py` 可用时替换该入口。虚拟环境的明确解释器路径不做这种替换。

验证基线为 Linux / bash / CPython 3.12.13。macOS、PowerShell 与编辑器界面未实测；实际检查范围见 [本课验证记录](VERIFICATION.md)。完成运行验证不表示读者已学完。

## 2. 理论：项目环境解决什么问题

### 2.1 为什么需要隔离依赖

假设两个项目以后需要同一个库的不同版本，全部装到同一个环境里，会让项目相互影响。venv 为项目提供独立的包安装位置，让你明确“这一份依赖属于哪一个项目”。本课不安装包制造冲突，先通过路径与环境标识验证隔离的基础。

项目源码放在步骤目录，`.venv` 放环境文件。环境里提供解释器入口、配置以及包安装目录，依托创建它的基础 Python。它不是包含整个操作系统的容器，更不是执行不可信代码的安全沙箱。

### 2.2 激活改变了什么

激活通常把环境的命令目录放到当前 shell 的 PATH 前面，让简短的 `python` 优先找到环境解释器。它不会重写 `main.py`，也不会给所有终端同时切环境。退出激活恢复当前 shell 的查找状态，但磁盘中的环境仍然存在。

直接写出 `.venv/bin/python` 或 Windows 的 `.venv\Scripts\python.exe` 路径同样能选择环境。是否激活与是否使用环境不是同一个判断问题。

### 2.3 用哪些值确认环境归属

006 已讲 `sys.executable` 与属性访问，本课新增两个诊断字段：`sys.prefix` 是当前环境的前缀位置，`sys.base_prefix` 是基础 Python 的前缀位置。普通 venv 中两者不同；普通非 venv 运行时通常相同。这里由人观察比较，不引入条件判断代码。

`pip` 是安装和管理 Python 包的工具。`python -m pip --version` 的含义是：用这一个 python 执行 pip 模块，并只报告 pip 版本与位置。它不安装依赖。使用单独的 `pip` 命令还会经历一次 shell 查找，容易与预想的 Python 脱节，因此本课固定“解释器 + -m pip”的形式。

详细语义参考 [Python 3.12 venv 官方说明](https://docs.python.org/3.12/library/venv.html)。不同版本的默认环境文件可能变化，不靠记住文件数量判断环境正确。

### 理论总结

环境是解释器与依赖的位置关系；激活只是方便当前 shell 调用它。下面分别测试直接调用、激活调用、退出后直接调用，而不是只观察提示符是否多出一个括号。

## 3. 第一步：创建环境，不激活直接使用

在本课目录创建 `step01-create-environment/main.py`。本课所有诊断文件可独立运行，环境由课目录统一管理，避免每个小文件建一套项目。

<!-- source: step01-create-environment/main.py -->
```python
# 用途：显示解释器与环境前缀，验证调用是否属于项目虚拟环境。
# 从本课目录用 .venv/bin/python step01-create-environment/main.py 运行；
# Windows 使用 .venv\Scripts\python.exe，其他步骤按正文替换脚本路径。
# sys 已在 006 讲过；本课只增加两个用于诊断环境归属的属性。
import sys

print("解释器路径：")
print(sys.executable)
print("当前环境前缀：")
print(sys.prefix)
print("基础环境前缀：")
print(sys.base_prefix)
```

开始前使用新开的普通终端，确认未继承其他激活环境；006 的路径记录可帮助确认基础解释器。若本课目录已存在自己使用中的 `.venv`，不要覆盖，另选新的练习目录再开始。

**从本课目录开始**：

```bash
# -m venv 表示用选定 Python 执行标准库 venv；.venv 是新环境目录名。
python3 -m venv .venv
# 明确调用环境解释器，不需要先激活；脚本仍在步骤目录。
.venv/bin/python step01-create-environment/main.py
```

```powershell
# 使用已确认的基础 Python 创建环境；只有 py 可用时此处替换为 py。
python -m venv .venv
# .\ 表示从当前目录起步；这是环境解释器，不替换为 py。
.\.venv\Scripts\python.exe .\step01-create-environment\main.py
```

预期：路径指向本课 `.venv` 内的解释器入口；当前环境前缀指向本课 `.venv`；基础前缀指向创建环境所依托的基础 Python。下面是字段示意，不能原样写进代码：

```text
解释器路径：
<本课目录>/.venv/bin/python
当前环境前缀：
<本课目录>/.venv
基础环境前缀：
<基础 Python 安装前缀>
```

Windows 的路径形式不同，判断规则一致。**小总结：** 还没有运行激活命令，却已处在环境里；真正起作用的是启动了哪一个解释器。

## 4. 第二步：激活，并检查 pip 归属

创建独立 `step02-activate-and-check/main.py`。代码复述 006 的模块读取，只保留本步需要的完整诊断，不从第一步导入：

<!-- source: step02-activate-and-check/main.py -->
```python
# 用途：显示解释器与环境前缀，验证调用是否属于项目虚拟环境。
# 从本课目录用 .venv/bin/python step02-activate-and-check/main.py 运行；
# Windows 使用 .venv\Scripts\python.exe，其他步骤按正文替换脚本路径。
# sys 已在 006 讲过；本课只增加两个用于诊断环境归属的属性。
import sys

print("解释器路径：")
print(sys.executable)
print("当前环境前缀：")
print(sys.prefix)
print("基础环境前缀：")
print(sys.base_prefix)
```

**重新从本课目录开始**，使用第一步创建的环境。若只单独学习本步，先在新练习目录执行第一步的环境创建命令；不会要求先运行第一步业务代码。

```bash
# source 在当前 shell 中加载激活脚本，修改的是当前 shell 的查找环境。
source .venv/bin/activate
# 查看 python 命令现在解析到哪里，预期属于本课 .venv。
command -v python
# 激活后使用简短 python；仍用诊断结果确认真正的环境。
python step02-activate-and-check/main.py
# 用同一解释器检查 pip；--version 只输出版本和位置，不安装包。
python -m pip --version
# 恢复当前 shell 激活前的状态，不删除磁盘环境。
deactivate
```

```powershell
# 在当前 PowerShell 会话中运行激活脚本。
.\.venv\Scripts\Activate.ps1
# 查看当前 python 命令来源；以随后诊断输出进一步核实。
Get-Command python
# 在环境中运行第二步完整副本。
python .\step02-activate-and-check\main.py
# 检查这一个解释器的 pip 位置。
python -m pip --version
# 退出当前会话的激活状态。
deactivate
```

以上 PowerShell 激活若被系统策略阻止，**停止执行该块后续依赖激活的命令**，直接改用下面这组；无需放开全局执行策略：

```powershell
# 无需激活也能明确使用项目解释器。
.\.venv\Scripts\python.exe .\step02-activate-and-check\main.py
# pip 也显式绑定到同一个环境解释器。
.\.venv\Scripts\python.exe -m pip --version
```

预期诊断中的当前前缀仍是本课 `.venv`。pip 输出形如 `pip <版本> from <本课环境内路径> (python 3.x)`，版本不是固定答案，关键是归属位置。激活成功时才运行 `deactivate`；没有激活，不应把“deactivate 不存在”当成环境损坏。

**原理与小总结：** `source` 让脚本影响当前 shell，所以不要改成启动一个子 shell 执行再期望父 shell 改变。直接调用和激活调用的诊断结果应归属同一环境；提示符上的 `.venv` 只是辅助提示。

## 5. 第三步：新会话直接运行，验证环境仍存在

创建 `step03-without-activation/main.py` 的完整副本：

<!-- source: step03-without-activation/main.py -->
```python
# 用途：显示解释器与环境前缀，验证调用是否属于项目虚拟环境。
# 从本课目录用 .venv/bin/python step03-without-activation/main.py 运行；
# Windows 使用 .venv\Scripts\python.exe，其他步骤按正文替换脚本路径。
# sys 已在 006 讲过；本课只增加两个用于诊断环境归属的属性。
import sys

print("解释器路径：")
print(sys.executable)
print("当前环境前缀：")
print(sys.prefix)
print("基础环境前缀：")
print(sys.base_prefix)
```

退出已激活会话，或新开一个普通系统终端并定位到本课目录。编辑器可能自动激活新终端，若发现已激活先退出；不要仅凭“新开”二字就假设状态。

**从本课目录开始**：

```bash
# 先用基础入口运行，观察本机实际前缀；不要猜它与环境入口相同。
python3 step03-without-activation/main.py
# 再直接选择环境入口，即使当前没有激活也应显示本课环境前缀。
.venv/bin/python step03-without-activation/main.py
```

```powershell
# 使用原来检查成功的基础入口；只有 py 可用时此处替换。
python .\step03-without-activation\main.py
# 明确选择项目环境进行对照。
.\.venv\Scripts\python.exe .\step03-without-activation\main.py
```

预期第二次的当前环境前缀是本课 `.venv`；第一次按基础入口实际状态判断，若也落在 `.venv`，应排查自动激活或命令指向，不伪造必须不同的结果。

**小总结：** `deactivate` 改的是会话，环境文件还在；搬移项目到新位置后应重建环境，不把旧 `.venv` 当作可随意复制的成品。

## 6. 排错与重复运行

| 问题 | 观察与处理 |
| --- | --- |
| 缺少 venv/ensurepip | 创建命令失败时先读错误，按 Linux 发行版官方说明补齐相应支持；当前目录里残留的半成品不等于完整环境 |
| 环境解释器可运行但没有 pip | 先检查 Python 是否提供 ensurepip；这是包管理入口问题，不是 print 错误 |
| pip 路径在别处 | 使用环境解释器的明确路径加 `-m pip --version`；检查激活和 shell 查找 |
| `.venv` 建在错误层级 | 用 pwd/Get-Location 查位置，再在期望的新目录创建；不盲目删除其他环境 |
| IDE 仍用基础解释器 | 用 006 的选择与诊断方法，指向本课环境解释器 |

若环境已创建但缺 pip，且标准 Python 安装提供 ensurepip，可以在**本课目录**使用下面的恢复命令。它只对指定环境引导安装 pip，不需要下载业务依赖：

```bash
# 仅在环境缺 pip 且 ensurepip 可用时执行；正常流程不需要它。
.venv/bin/python -m ensurepip
# 再验证结果与环境归属。
.venv/bin/python -m pip --version
```

```powershell
# 仅修复本课环境的 pip 引导，不修改系统全局安装。
.\.venv\Scripts\python.exe -m ensurepip
# 检查环境内 pip。
.\.venv\Scripts\python.exe -m pip --version
```

若连环境解释器都不存在，回到创建错误处理，不能运行不存在的路径。环境重建会写文件，诊断脚本本身不写文件；重复诊断不会累计数据。练习结束先退出激活，关闭相关终端，只清理自己确认无用的练习环境，保留步骤源码。仓库已忽略本阶段环境目录，不提交 `.venv`。

## 7. 练习与课程总结

完成 [独立重建环境并运行信息卡](exercises/README.md)。只需要现有标准库，不用安装新框架。

自测：未激活能否使用环境？deactivate 会删除它吗？为什么用 `python -m pip` 而不是随手输入 pip？

结论：明确调用环境解释器即可；退出只影响当前会话；`-m pip` 把包管理操作绑定到所选解释器。阶段 10 才系统学习依赖版本与锁文件。下一课从空目录独立交付一个可运行、可说明、能排错的小程序。
