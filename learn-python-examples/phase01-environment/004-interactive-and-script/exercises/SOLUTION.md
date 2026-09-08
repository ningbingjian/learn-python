# 01-004 参考解答

[返回练习](README.md)

交互模式先回显字符串表示（通常带单引号），再显示“明确输出”；脚本只显示“明确输出”。决定差异的是执行环境是否自动回显，不是字符串换了内容。

<!-- source: exercises/solution.py -->
```python
# 用途：练习脚本模式只显示显式输出，不自动回显裸字符串。
# 在 exercises 目录运行 python3 solution.py；Windows 使用 python solution.py。
"只求值"
# 这一条调用产生唯一的输出行。
print("明确输出")
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
明确输出
```
