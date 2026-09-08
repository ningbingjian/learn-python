# 01-006 参考解答

[返回练习](README.md)

建议记录表：

| 入口 | 路径（本地记录，公开时脱敏） | 版本 | 结论 |
| --- | --- | --- | --- |
| 终端 | 按实际填写 | 按实际填写 | 基线 |
| 编辑器 | 按实际填写 | 按实际填写 | 对齐 / 待定位 / 未实测 |

下面的源码可以独立运行，输出内容随环境变化。虚构案例不能断言环境相同；明确选择入口并复查。若当前无法操作 GUI，诚实记录未实测，不能把两次终端运行当成编辑器验证。

<!-- source: exercises/solution.py -->
```python
# 用途：让当前解释器报告自身信息；不读取账号或业务数据。
# 运行：在本目录执行 python3 main.py；Windows 使用已确认的 python main.py。
# sys 是随 Python 提供的标准库；导入后才能读取它提供的解释器属性。
import sys

# 标题与属性值分开输出，避免误把属性表达式写成固定字符串。
print("解释器路径：")
print(sys.executable)
# 版本信息可能含构建日期、编译器信息或换行，不强求各电脑文字相同。
print("版本信息：")
print(sys.version)
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
