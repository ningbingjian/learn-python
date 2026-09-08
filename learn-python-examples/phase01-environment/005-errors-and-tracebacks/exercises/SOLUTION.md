# 01-005 参考解答

[返回练习](README.md)

| 文件 | 故障期的标准输出 | 类型与修复 |
| --- | --- | --- |
| 01-quotes.py | 空 | SyntaxError；补齐结尾引号 |
| 02-name.py | 练习开始 | NameError；Print 改为 print |
| 03-indent.py | 空 | IndentationError；移除顶层多余缩进 |

三种修复最终可得到下面相同的正确逻辑。工作目录是本课目录时，按下方命令进入 exercises 运行公共参考答案；自己的三份修复版需分别验证。

<!-- source: exercises/solution.py -->
```python
# 用途：三道故障练习修复后的公共输出参考；不依赖故障文件。
# 在 exercises 目录运行 python3 solution.py；Windows 使用 python solution.py。
print("练习开始")
# 名称小写、字符串闭合、顶层不缩进，三项条件同时满足。
print("练习结束")
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
练习开始
练习结束
```
