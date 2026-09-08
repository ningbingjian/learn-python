# 01-003 参考解答

[返回练习](README.md)

在 `exercises/moved copy/main.py` 写注释和 `print("移动副本运行成功")`，完整核对文件见 [练习副本](moved%20copy/main.py)。下面展示移动后相对路径为什么要改变。

先从本课目录打开终端：

```bash
# 进入练习目录，注意从本课目录起步。
cd exercises
# 路径含空格，完整引用；此处从 exercises 寻找副本。
python3 "moved copy/main.py"
# 回到本课目录，.. 表示父目录。
cd ..
# 相对路径增加 exercises 这一层。
python3 "exercises/moved copy/main.py"
```

```powershell
# 从本课目录进入练习目录。
Set-Location exercises
# 从 exercises 定位副本。
python "moved copy\main.py"
# 返回本课目录。
Set-Location ..
# 新的起点需要新的相对路径。
python "exercises\moved copy\main.py"
```

每次只输出“移动副本运行成功”一行。绝对路径答案按本机位置编写；两种相对路径都通过起点加层级指向同一文件。
