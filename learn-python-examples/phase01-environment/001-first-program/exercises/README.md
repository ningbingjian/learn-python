# 01-001 独立练习：修改并运行一行输出

[返回课程](../README.md)

## 练习目标

不查看参考答案，从空白文件写出一条输出语句，并证明自己运行的是修改后保存的正确文件。

## 任务与输入

输入是一份文字需求，不需要在运行时输入数据。程序必须只输出下面一行，不多加标题，也不把引号输出出来：

```text
我能独立修改并运行 Python 程序了！
```

1. 在自己的 `001-first-program` 练习文件夹中创建 `exercises`，再创建 `main.py`。
2. 使用一条 `print` 语句实现需求，并写中文注释说明文件用途、运行方式和引号的作用。
3. 保存文件。右键自己的 `exercises` 文件夹，在集成终端中打开。
4. 按下方平台命令确认目录、运行程序，核对文字和标点。
5. 将文本临时换成自己的另一句问候，先预测结果，保存并运行，再恢复规定文本并运行。
6. 在自己的 `notes.md` 中写三句话：我在哪个目录运行、使用什么命令、观察到了什么结果。该文件是自己的学习记录，不需要提交个人绝对路径。

## 运行自己的练习

当前工作目录：自己的 `001-first-program/exercises`，文件名是你创建的 `main.py`。

macOS/Linux：

```bash
# 核对当前目录是自己的 exercises 文件夹。
pwd
# 确认 main.py 已保存到这里。
ls
# 执行自己的练习答案。
python3 main.py
```

Windows PowerShell：

```powershell
# 核对当前目录是自己的 exercises 文件夹。
Get-Location
# 确认 main.py 已存在。
Get-ChildItem
# 使用前面检查成功的入口；只有 py 可用时改为 py main.py。
python main.py
```

## 验收标准

- 输出与需求一致，只有一条文本输出；中文标点正确。
- 注释说明原因，不只写“打印”。
- 修改前后都能运行；恢复后重新核对规定输出。
- 能解释代码里的引号为什么不显示，以及未保存为什么可能仍看到旧输出。
- 再运行原来的 `step01-hello` 与 `step02-change-output`，两版内容仍保留。

## 完成后再看参考答案

[参考源码 solution.py](solution.py) 与自己的答案文件名不同，避免混淆；它可以单独运行。

当前工作目录：下载的仓库课程中 `001-first-program/exercises`，这里保存的是 `solution.py`。

macOS/Linux：

```bash
# 运行仓库提供的参考答案，不是自己练习目录里的 main.py。
python3 solution.py
```

Windows PowerShell：

```powershell
# 运行参考答案；只有 py 可用时改为 py solution.py。
python solution.py
```

答案只需调用一次 `print`：括号内放需求指定的字符串，双引号负责界定文本范围。没有读取输入、判断分支或计算，因此不需要加入变量、循环或额外依赖。
