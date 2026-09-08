# 故意失败：顶层第二条输出没有所属代码块，却被额外缩进。
# 在本目录运行 python3 broken.py；Windows 使用 python broken.py。
print("开始")
    print("处理中")
print("结束")
