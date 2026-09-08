# 01-008 参考解答

[返回练习](README.md)

实现变化分为固定文本替换与语句顺序调整。空行仍需要一次显式输出。下面代码是完整参考；通用命令可快速核对输出，环境验收按文末命令完成。

<!-- source: exercises/solution.py -->
```python
# 用途：综合任务变式；新的输出次序与前两版独立保存。
# 在 exercises 目录用 ../.venv/bin/python solution.py 运行；
# Windows 使用 ..\.venv\Scripts\python.exe，详见练习解答。
print("# 模拟投放检查")
# 显式保留标题后的空输出行。
print("")
# 新需求把状态放到字段第一位，不按原版顺序机械复制。
print("状态：检查完成")
print("城市：苏州")
print("订单编号：DEMO-009")
print("渠道：模拟渠道B")
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
# 模拟投放检查

状态：检查完成
城市：苏州
订单编号：DEMO-009
渠道：模拟渠道B
```

## 本课环境中的验证

已按 RUNBOOK 在本课目录创建 `.venv`，重新从本课目录开始：

```bash
# 从本课目录运行参考答案；自己的答案可替换为 exercises/main.py。
.venv/bin/python exercises/solution.py
# 进入练习目录后，环境入口回溯到父目录。
cd exercises
# 运行同一文件，输出应与前一次一致。
../.venv/bin/python solution.py
```

```powershell
# 从本课目录定位环境和答案。
.\.venv\Scripts\python.exe .\exercises\solution.py
# 切换起点。
Set-Location exercises
# 用父目录中的环境运行本目录答案。
..\.venv\Scripts\python.exe solution.py
```
