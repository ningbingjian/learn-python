# 01-007 参考解答

[返回练习](README.md)

**从本课目录开始**，先创建新练习环境，再调用它。此任务不依赖前面 .venv 的存在：

```bash
# 使用已经确认的基础 Python 创建一个新环境。
python3 -m venv .venv-exercise
# 明确选择新环境来执行完整练习答案。
.venv-exercise/bin/python exercises/solution.py
# 确认 pip 也在新环境内。
.venv-exercise/bin/python -m pip --version
```

```powershell
# 使用基础入口创建独立练习环境。
python -m venv .venv-exercise
# 显式路径不需要激活。
.\.venv-exercise\Scripts\python.exe .\exercises\solution.py
# 检查对应 pip 位置。
.\.venv-exercise\Scripts\python.exe -m pip --version
```

预期业务输出只有“独立环境练习完成”。pip 位置应包含 `.venv-exercise`；业务输出正确本身不能证明环境正确，所以两者都要核对。下面通用命令仅用于单独查看源码输出，完成本题环境验收必须使用上面明确的环境路径。

<!-- source: exercises/solution.py -->
```python
# 用途：独立环境练习的业务输出；不读取任何外部文件。
# 从本课目录运行 .venv-exercise/bin/python exercises/solution.py；
# Windows 使用 .venv-exercise\Scripts\python.exe，详见练习解答。
print("独立环境练习完成")
```

**重新从本课目录开始**，选自己系统的一组命令执行：

```bash
# 进入本步目录；cd 改变当前 shell 的工作目录。
cd exercises
# 执行本目录的 solution.py，文件必须先保存。
python3 solution.py
```

```powershell
# 进入本步目录；这里使用 PowerShell 的 Set-Location。
Set-Location exercises
# 执行已经保存的 solution.py。
python solution.py
```

预期输出：

```text
独立环境练习完成
```
