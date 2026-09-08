# 01-003：从不同目录运行同一个文件

[阶段导航](../README.md) · [上一课：01-002](../002-output-and-comments/README.md) · [下一课：01-004](../004-interactive-and-script/README.md)

## 1. 本课目标与准备

这一课保持输出逻辑简单，把注意力放到文件位置：同目录、父目录、绝对路径、带空格路径分别如何运行。学完要能区分“找不到解释器”和“解释器找不到脚本”。

前置：完成 01-002。沿用第一课检查成功的 Python 3 与编辑器，不重复安装。代码只用内置功能或本课明确讲解的标准库，不需要第三方依赖。

在自己的 `python-practice` 下创建 `003-paths-and-execution` 作为**本课目录**，按下文路径创建步骤文件；也可打开仓库的同名目录核对源码。文件用 UTF-8 保存。每步的完整代码均独立保留，不能覆盖前一步。

凡标注“从本课目录开始”的命令，先在编辑器资源管理器中右键这个目录，选择“在集成终端中打开”。不要默认终端还停在上一步所需位置。macOS/Linux 示例使用 bash/zsh 和 `python3`；Windows 示例使用 PowerShell 和已确认可用的 `python`，只有 `py` 可用时替换该入口。虚拟环境的明确解释器路径不做这种替换。

验证基线为 Linux / bash / CPython 3.12.13。macOS、PowerShell 与编辑器界面未实测；实际检查范围见 [本课验证记录](VERIFICATION.md)。完成运行验证不表示读者已学完。

## 2. 理论：路径总要从某个位置解释

### 2.1 当前目录与脚本所在目录

每个终端里的 shell 有自己的当前工作目录。`cd`（PowerShell 中对应 `Set-Location`）改变它；在编辑器里切换文件标签通常不会同步改变已经打开的终端目录。

`python3 main.py` 没有告诉解释器完整位置，因此它会按当前工作目录寻找 `main.py`。如果你站在父目录，而文件在子目录中，就应给出子目录部分。解释器不负责遍历整个项目猜测你想执行哪一个同名文件。

### 2.2 相对路径与绝对路径

相对路径从当前目录出发：`.` 表示当前目录，`..` 表示父目录，`step02-parent-directory/main.py` 表示当前目录下的一层子目录中的文件。绝对路径从文件系统根或 Windows 的驱动器根开始，不随当前目录改变。

| 当前目录 | 文件参数 | 指向哪里 |
| --- | --- | --- |
| 本课目录 | `step02-parent-directory/main.py` | 第二步的文件 |
| 第二步目录 | `main.py` | 同一个第二步文件 |
| 第一阶段目录 | `003-paths-and-execution/step02-parent-directory/main.py` | 仍是同一个文件 |

这张表说明的是运行入口定位，不代表 Python 运行脚本会自动把 shell 切到脚本目录。脚本里的文件读写和 `__file__` 放到阶段 06。

### 2.3 为什么空格要特别处理

shell 通常用未引用的空白分开命令参数。如果脚本路径包含空格但没引用，它会被拆开。例如 `python3 step03-space-in-path/demo folder/main.py` 会把前半截当作脚本参数，后半截成为另一个参数。解释器看到的是被 shell 拆分后的结果。

用英文双引号包住整个路径，让它作为一个参数传递。这里的引号属于 shell 的语法，不是要写进 Python 文件的内容。相对路径的选择与参数引用是两件独立的事：路径指向正确，也要保证完整传递。

### 理论总结

先确定“我在哪”，再确定“文件在哪”，最后确定“路径有没有完整传给解释器”。下面每步都先明确当前目录，再运行。

## 3. 第一步：同目录运行

在本课目录创建 `step01-same-directory/main.py`：

<!-- source: step01-same-directory/main.py -->
```python
# 用途：提供固定输出作为路径实验的对照；不读取外部数据。
# 可从本文件所在目录运行 python3 main.py；Windows 使用 python main.py。
# 从其他目录运行时，必须改用指向本文件的路径，代码本身不需要改变。
print("路径实验信息卡")
print("订单编号：PATH-001")
print("城市：杭州")
```
**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd step01-same-directory
# 执行本目录的 main.py，文件必须先保存。
python3 main.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location step01-same-directory
# 执行已经保存的 main.py。
python main.py
```

预期输出：

```text
路径实验信息卡
订单编号：PATH-001
城市：杭州
```
此时文件名可以省去父路径，因为 shell 已经在步骤目录。小总结：短文件名不是全局唯一定位，只在当前目录里有含义。

## 4. 第二步：从父目录运行同一副本

创建独立的 `step02-parent-directory/main.py`，抄写完整版本：

<!-- source: step02-parent-directory/main.py -->
```python
# 用途：提供固定输出作为路径实验的对照；不读取外部数据。
# 可从本文件所在目录运行 python3 main.py；Windows 使用 python main.py。
# 从其他目录运行时，必须改用指向本文件的路径，代码本身不需要改变。
print("路径实验信息卡")
print("订单编号：PATH-001")
print("城市：杭州")
```
**重新从本课目录开始**，先使用相对路径，然后进入子目录用短路径：

```bash
# 确认当前目录是 003-paths-and-execution。
pwd
# 从父目录运行第二步的文件。
python3 step02-parent-directory/main.py
# 进入第二步目录；代码没移动，当前目录变了。
cd step02-parent-directory
# 从同目录运行同一文件，输出应相同。
python3 main.py
# 读取该目录的绝对位置，供下面的绝对路径实验使用。
pwd
```

```powershell
# 确认本课目录位置。
Get-Location
# 从父目录运行第二步文件。
python .\step02-parent-directory\main.py
# 改变当前工作目录。
Set-Location step02-parent-directory
# 再次运行同一文件。
python main.py
# 读取目录的完整位置。
Get-Location
```

两次输出都与第一步三行文本相同。下面用绝对路径再运行一次：复制刚才显示的真实目录，追加文件名。以下是**虚构路径示例，必须替换为自己的位置**，不要原样运行：

```bash
# 将整个引号内内容换成第二步 main.py 的实际绝对路径；当前目录可以任意。
python3 "/tmp/python-practice/003-paths-and-execution/step02-parent-directory/main.py"
```

```powershell
# 将整个引号内内容换成第二步 main.py 的实际绝对路径；当前目录可以任意。
python "C:\python-practice\003-paths-and-execution\step02-parent-directory\main.py"
```

**观察与小总结：** 从不同目录启动，只要最终指向同一文件，固定输出就相同。绝对路径省去了“相对于哪里”的歧义，但复制到另一台电脑时通常需要改写位置；课程不把个人绝对路径写死到源码里。

## 5. 第三步：路径里有空格

在本课目录创建 `step03-space-in-path`，其下创建名称为 `demo folder` 的文件夹（中间一个空格），再创建 `main.py`：

<!-- source: step03-space-in-path/demo folder/main.py -->
```python
# 用途：提供固定输出作为路径实验的对照；不读取外部数据。
# 可从本文件所在目录运行 python3 main.py；Windows 使用 python main.py。
# 从其他目录运行时，必须改用指向本文件的路径，代码本身不需要改变。
print("路径实验信息卡")
print("订单编号：PATH-001")
print("城市：杭州")
```
**重新从本课目录开始**。先执行故意错误的命令，观察失败，再用完整引用修复：

```bash
# 故意不加引号：shell 会把带空格路径拆开，预期找不到脚本。
python3 step03-space-in-path/demo folder/main.py
# 双引号保护整条脚本路径，使其成为一个参数。
python3 "step03-space-in-path/demo folder/main.py"
```

```powershell
# 故意拆开路径，预期找不到脚本。
python .\step03-space-in-path\demo folder\main.py
# 整条路径加引号后再传给解释器。
python ".\step03-space-in-path\demo folder\main.py"
```

第一次错误通常含 `can't open file`，失败路径停在 `demo`；第二次输出完整三行信息卡。不要试图通过改 `print` 修复 shell 参数拆分。

**小总结：** 这个实验只改变路径传递方式，文件内容不变。后续可以优先使用没有空格的练习目录，但仍要理解遇到空格时为什么需要引号。

## 6. 排错顺序与易错点

| 现象 | 先验证什么 | 修复原因 |
| --- | --- | --- |
| `command not found` / 无法识别命令 | 已确认可用的 Python 入口 | shell 没能启动解释器 |
| `can't open file` | 当前目录与传入文件路径 | 解释器启动了，但无法打开指定文件 |
| 文件存在却指向别的输出 | 是否有同名文件、终端是否仍在旧目录 | 文件名相同不代表同一个文件 |
| Linux 上 `Main.py` 运行失败 | 用 `ls` 查看实际大小写 | 本实验文件名是 `main.py`；其他系统是否区分大小写取决于文件系统 |

路径少一层可以这样复现：在本课目录运行 `python3 main.py`（PowerShell 为 `python main.py`），此处没有该文件，预期失败；补上步骤目录后成功。命令的作用是验证当前目录定位，故意失败之后不需要重装环境。

## 7. 练习与课程总结

完成 [移动练习副本并重写命令](exercises/README.md)，不要移动或覆盖仓库步骤目录。

自测：`cd` 改的是源码还是当前目录？绝对路径是否一定不用引号？编辑器打开第二步文件后，第一步终端会自动切过去吗？

答案：`cd` 改当前目录；绝对路径含空格时仍需完整引用；已开的终端通常不会随文件标签切换。下一课将进一步区分 shell 命令和 Python 交互输入，避免在错误的窗口模式下输入正确内容。
