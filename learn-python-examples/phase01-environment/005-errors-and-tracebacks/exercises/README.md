# 01-005 独立练习

[返回课程](../README.md)

## 任务

逐个打开并预测 01-quotes.py、02-name.py、03-indent.py 的错误类型、正常输出与修复方式。在自己的练习目录分别保存修复版，不能直接覆盖故障材料。验收：三份故障判断正确，修复后三个文件都输出“练习开始”和“练习结束”两行。

先独立完成，记录自己的命令、观察结果与原因；记录使用相对目录或虚构路径，不提交个人绝对路径。完成后再阅读 [参考解答](SOLUTION.md)。

## 逐个运行故障文件

从本课目录起步，下列三个失败都属于预期结果。每个文件运行结束后才执行下一个。

```bash
# 进入故障练习所在目录。
cd exercises
# 观察字符串边界错误。
python3 01-quotes.py
# 观察大小写导致的名字错误。
python3 02-name.py
# 观察顶层缩进错误。
python3 03-indent.py
```

```powershell
# 进入练习目录。
Set-Location exercises
# 预期字符串语法错误。
python 01-quotes.py
# 预期名字查找错误。
python 02-name.py
# 预期缩进错误。
python 03-indent.py
```
