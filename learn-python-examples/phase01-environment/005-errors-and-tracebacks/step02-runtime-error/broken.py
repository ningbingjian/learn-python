# 故意失败：prnit 的拼写与内置 print 不同，预期 NameError。
# 在本目录运行 python3 broken.py；Windows 使用 python broken.py。
print("开始")
prnit("处理中")
print("结束")
