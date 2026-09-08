# 01-002 参考解答

[返回练习](README.md)

先用 print 输出标题，再输出空字符串；城市与编号的顺序按新需求排列。添加状态是一条新的输出语句，不是只补一条注释。

<!-- source: exercises/solution.py -->
```python
# 用途：独立完成调整顺序并增加状态字段的练习；所有数据是虚构文本。
# 在 exercises 目录运行 python3 solution.py；Windows 使用 python solution.py。
print("# 模拟订单信息")
# 这一调用显式产生分隔空行。
print("")
# 新需求要求城市先于编号，保持语句顺序与需求一致。
print("城市：南京")
print("订单编号：DEMO-003")
# 状态必须作为字符串交给 print，注释本身不会显示。
print("状态：待投放")
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
# 模拟订单信息

城市：南京
订单编号：DEMO-003
状态：待投放
```
