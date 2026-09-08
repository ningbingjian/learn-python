# 信息卡运行说明参考

[返回课程](README.md)

## 环境和起点

Python 3，源码使用标准输出，无第三方依赖。以下起点都是本课 `008-information-card` 目录，不是仓库根目录或任意终端位置。复制本课到独立练习目录也可运行；环境在新位置重新创建，不复制旧 `.venv`。

第一次创建环境前确认此处没有需要保留的同名环境。创建会写入 `.venv`；正常信息卡脚本只输出，不写文件、数据库或网络。

## 首次准备并运行

```bash
# 当前目录必须是 008-information-card；用已确认的基础 Python 创建环境。
python3 -m venv .venv
# 初版输出标题、空行、编号、杭州、待投放。
.venv/bin/python step01-basic-card/main.py
# 第二版输出标题、空行、南京、编号、模拟渠道A、已暂停。
.venv/bin/python step02-revised-card/main.py
# 单独核对解释器与环境前缀，不把诊断混入业务输出。
.venv/bin/python diagnostics.py
```

```powershell
# 从本课目录创建环境；仅创建入口可按本机情况换为 py。
python -m venv .venv
# 后续明确选择环境解释器，不能换回基础入口。
.\.venv\Scripts\python.exe .\step01-basic-card\main.py
# 运行第二版。
.\.venv\Scripts\python.exe .\step02-revised-card\main.py
# 检查环境归属。
.\.venv\Scripts\python.exe diagnostics.py
```

完整输出逐行样本见课程两步正文。环境存在时可直接重复三条运行命令，不需要每次重新创建。每次业务输出相同，没有累积状态。

## 从第二版目录运行

重新从本课目录开始，选择一组执行：

```bash
# 切换工作目录。
cd step02-revised-card
# 环境解释器现在位于父目录中。
../.venv/bin/python main.py
```

```powershell
# 进入第二版目录。
Set-Location step02-revised-card
# 从父目录定位环境，当前目录定位源码。
..\.venv\Scripts\python.exe main.py
```

## 故障与清理

- 解释器文件不存在：检查是否完成环境创建、起始目录是否正确。
- `can't open file`：检查脚本路径和文件名；不修改输出代码解决路径错误。
- `SyntaxError`：检查实际运行文件的引号、括号与缩进，保留错误信息用于定位。
- 环境位置变动后重建；不要把源码存进 `.venv`。练习结束可保留环境供复习；要清理时先确认是自己的练习环境，并保留源码与运行说明。

## 验证限制

Linux / bash / CPython 3.12.13 已验证上述核心流程；PowerShell、macOS 与 IDE 界面未实测。个人执行记录按实际平台填写，不复制别人的验证结论。
