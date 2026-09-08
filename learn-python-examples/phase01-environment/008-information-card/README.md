# 01-008：独立完成信息卡程序

[阶段导航](../README.md) · [上一课：01-007](../007-virtual-environment/README.md) · 下一步：[阶段 02 详细大纲](../../phase02-values/README.md)

## 1. 本课目标与准备

这一课是阶段综合任务：从空目录做一张固定文本信息卡，保留需求变更前后两版，写运行说明，并能解释、复现和修复两个故障。先根据需求自己实现，再把下方代码当作核对用的完整版本。

前置：完成 01-007。沿用第一课检查成功的 Python 3 与编辑器，不重复安装。代码只用内置功能或本课明确讲解的标准库，不需要第三方依赖。

在自己的 `python-practice` 下创建 `008-information-card` 作为**本课目录**，按下文路径创建步骤文件；也可打开仓库的同名目录核对源码。文件用 UTF-8 保存。每步的完整代码均独立保留，不能覆盖前一步。

凡标注“从本课目录开始”的命令，先在编辑器资源管理器中右键这个目录，选择“在集成终端中打开”。不要默认终端还停在上一步所需位置。macOS/Linux 示例使用 bash/zsh 和 `python3`；Windows 示例使用 PowerShell 和已确认可用的 `python`，只有 `py` 可用时替换该入口。虚拟环境的明确解释器路径不做这种替换。

验证基线为 Linux / bash / CPython 3.12.13。macOS、PowerShell 与编辑器界面未实测；实际检查范围见 [本课验证记录](VERIFICATION.md)。完成运行验证不表示读者已学完。

## 2. 理论复盘：把已学机制连起来

### 2.1 需求、代码、运行环境各管什么

需求决定显示哪些字段及其顺序；代码通过输出语句实现它；运行环境负责把正确文件交给正确解释器。把“城市”从杭州改成南京，是需求内容变化；改用虚拟环境，是启动环境变化；在父目录运行，是文件定位方式变化。三者不要混在一起排查。

### 2.2 验收需要能看见的证据

只说“运行成功”不足以证明完成。对本课至少要给出：实际使用的入口、当前目录、运行文件、对应输出，以及变更前后两版仍然可用的证据。截图可作为辅助，但不能代替能重现的文字命令；对外记录不包含个人路径。

### 2.3 保留版本不是增加无意义目录

第一版代表原始需求，第二版代表需求变更。两个版本拥有自己的完整代码和运行入口，能对照解释变化。这里只保存文件快照，不引入 Git 分支操作作为门槛。

### 理论总结

001～007 学过的机制够用：固定字符串、输出与注释、当前目录、错误定位、解释器检查、虚拟环境。此课不借综合任务偷偷引入变量、用户输入、条件、循环、函数定义或框架。

## 3. 任务一：交付初版信息卡

### 3.1 先看需求，自行拆成输出动作

输入是一份文字需求，没有运行时键盘输入。初版要求：

1. 第一行显示 `# 模拟订单信息卡`。
2. 第二行为空行。
3. 随后按顺序显示编号 `DEMO-008`、城市 `杭州`、状态 `待投放`。
4. 每个字段各占一行；全部使用虚构固定文本。

在本课目录创建 `step01-basic-card/main.py`。先自己完成，再核对下面的完整代码。文件必须保存为 UTF-8。

<!-- source: step01-basic-card/main.py -->
```python
# 用途：综合任务初版；所有字段都是虚构固定文本，不读取输入。
# 从本目录执行 python3 main.py；Windows 使用 python main.py。
# 标题中的井号属于字符串，所以会显示；本行的井号用于注释。
print("# 模拟订单信息卡")
# 显式执行空字符串输出，为标题与内容之间产生一条空行。
print("")
# 字段顺序来自需求，语句按同样顺序排列；编号不参与计算。
print("订单编号：DEMO-008")
print("城市：杭州")
# 状态也是固定说明文本，当前不涉及业务状态判断。
print("状态：待投放")
```
**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd step01-basic-card
# 执行本目录的 main.py，文件必须先保存。
python3 main.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location step01-basic-card
# 执行已经保存的 main.py。
python main.py
```

预期 5 行，包括第 2 行的空行：

```text
# 模拟订单信息卡

订单编号：DEMO-008
城市：杭州
状态：待投放
```
**观察与原理：** 程序没有自动理解订单，按顺序执行输出调用。空白源码行可以帮助阅读，但真正的分隔空行来自 `print("")`。

**小总结：** 初版验收不仅比对文字，还比对空行、顺序和末尾状态。下一步是明确的需求变化，不覆盖这一版。

## 4. 任务二：处理变更并保留原版

新需求：城市改成 `南京`，将城市放到编号之前；在编号后新增渠道 `模拟渠道A`；状态改成 `已暂停`。标题和空行保留。

先列出哪些输出语句要移动、哪些文字要修改，再创建独立的 `step02-revised-card/main.py`：

<!-- source: step02-revised-card/main.py -->
```python
# 用途：综合任务第二版；独立保存新需求，不导入或修改初版文件。
# 从本目录执行 python3 main.py；Windows 使用 python main.py。
print("# 模拟订单信息卡")
# 分隔空行保持不变，保证标题和字段之间的布局要求。
print("")
# 新需求让城市先于编号：通过语句位置实现，不靠注释说明代替修改。
print("城市：南京")
print("订单编号：DEMO-008")
# 新增渠道是一条实际输出调用；文本全部为模拟数据。
print("渠道：模拟渠道A")
# 状态按需求修改为固定文本，不在这里引入条件判断。
print("状态：已暂停")
```
**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd step02-revised-card
# 执行本目录的 main.py，文件必须先保存。
python3 main.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location step02-revised-card
# 执行已经保存的 main.py。
python main.py
```

预期输出：

```text
# 模拟订单信息卡

城市：南京
订单编号：DEMO-008
渠道：模拟渠道A
状态：已暂停
```
**原理与小总结：** 改动体现在字符串内容和调用顺序；两版相互独立，运行第二版不会改变第一版。下面还要证明你能从不同目录和环境中准确启动它们。

## 5. 任务三：写出可复现的运行说明

在本课目录创建自己的 `RUNBOOK.md`，至少说明环境要求、起始目录、两版文件、命令、预期输出和常见错误。仓库提供 [完整运行说明参考](RUNBOOK.md)，先自己写再对照。

使用本课新的 `.venv`，不依赖 007 的环境。若已存在重要同名环境，改在新的练习目录完成任务。**从本课目录开始**：


```bash
# 先用已确认的基础 Python 创建本课环境。
python3 -m venv .venv
# 从本课目录运行初版，环境解释器与脚本路径分别指定。
.venv/bin/python step01-basic-card/main.py
# 在同一环境中运行第二版。
.venv/bin/python step02-revised-card/main.py
# 进入第二版目录，当前目录变了，相对路径也相应变化。
cd step02-revised-card
# .. 回到本课层级定位环境；main.py 则在当前目录。
../.venv/bin/python main.py
```

```powershell
# 创建本课独立环境。
python -m venv .venv
# 从本课目录运行初版。
.\.venv\Scripts\python.exe .\step01-basic-card\main.py
# 从本课目录运行第二版。
.\.venv\Scripts\python.exe .\step02-revised-card\main.py
# 切换到第二版所在目录。
Set-Location step02-revised-card
# 解释器路径需返回上一层，文件名则直接使用本目录的 main.py。
..\.venv\Scripts\python.exe main.py
```

第二版两次输出必须一致。为验证环境本身，创建本课独立的 `diagnostics.py`，与业务文件分开：

<!-- source: diagnostics.py -->
```python
# 用途：显示解释器与环境前缀，验证调用是否属于项目虚拟环境。
# 从本课目录用 .venv/bin/python diagnostics.py 运行；
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

**重新从本课目录开始**：

```bash
# 环境诊断与业务内容分开，明确验证当前环境归属。
.venv/bin/python diagnostics.py
```

```powershell
# 预期当前环境前缀指向本课 .venv。
.\.venv\Scripts\python.exe diagnostics.py
```

不通过“信息卡输出相同”推断环境相同，而通过诊断字段验证。**小总结：** 运行说明要包含起点，不能只给一条依赖隐含目录状态的命令。

## 6. 任务四：复现故障并解释修复

### 6.1 错误路径

**从本课目录开始，环境已经创建**：

```bash
# 故意省去步骤目录：本课根目录没有 main.py，预期找不到文件。
.venv/bin/python main.py
# 补上正确路径后成功，不需要改业务源码。
.venv/bin/python step01-basic-card/main.py
```

```powershell
# 故意运行不存在的根目录 main.py。
.\.venv\Scripts\python.exe main.py
# 修正文件路径。
.\.venv\Scripts\python.exe .\step01-basic-card\main.py
```

第一条预期错误含 `can't open file`，第二条输出初版信息卡。记录：失败环节是文件定位，解释器已经启动。

### 6.2 错误源码

在 `errors/broken.py` 保存一个只用于语法故障的副本，`fixed.py` 保存对应修复。不要修改两版正确业务代码。

<!-- source: errors/broken.py -->
```python
# 故意失败：缺少标题字符串的结尾引号；不覆盖正式业务版本。
# 在 errors 目录执行 python3 broken.py；Windows 使用 python broken.py。
print("# 模拟订单信息卡)
print("状态：待投放")
```
<!-- source: errors/fixed.py -->
```python
# 修复：补齐字符串边界；保留故障实验自身的两行输出，不冒充完整信息卡。
# 在 errors 目录执行 python3 fixed.py；Windows 使用 python fixed.py。
print("# 模拟订单信息卡")
print("状态：待投放")
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
预期 `SyntaxError` 且标准输出为空。**留在 errors 目录**运行修复版：

```bash
# 修复故障副本，预期输出标题和状态两行。
python3 fixed.py
```

```powershell
# 这是故障实验的修复，不是替换正式信息卡。
python fixed.py
```

修复版输出标题与状态两行；需要验收完整业务时仍运行前面的正式版本。小总结：同样是运行失败，路径故障改命令，语法故障改源码，修复对象由原因决定。

## 7. 独立变式练习与阶段验收

完成 [变式练习](exercises/README.md)：改变标题、字段顺序、渠道与状态，保留前两版。随后填写 [阶段验收清单](ASSESSMENT.md)。它包含独立创建、顺序预测、目录变化、故障定位、环境归属和运行说明，不把“已抄完”直接标为掌握。

## 8. 本课与本阶段总结

| 已具备的能力 | 本课的证据 |
| --- | --- |
| 创建、保存、运行 | 从新的课目录形成两版独立文件 |
| 解释文本与布局 | 字符串、注释、空行和调用顺序能够对应实际输出 |
| 修改需求 | 字段变更和顺序变化都体现在第二版，初版仍可运行 |
| 定位问题 | 路径错误和源码错误有不同的修复记录 |
| 选择环境 | 明确的环境解释器路径与 diagnostics 结果 |
| 复现过程 | RUNBOOK 给出起始目录、命令、输出和限制 |

自测：第二版运行为什么不会改变初版？换目录后为什么环境路径也要调整？输出正确为什么不能证明环境选对？

答案：两版是独立文件且程序没有写文件操作；环境入口同样是需要定位的文件；本阶段简单代码在不同 Python 3 中都可能产生相同输出，仍需看诊断信息。

下一阶段要解决“字段都写死，改动与计算不方便”的问题，再引入变量、类型与表达式。[阶段 02 详细大纲](../../phase02-values/README.md) 已完成，接下来按课生成内容；不用现在就在信息卡里提前加入没学过的高级写法。
