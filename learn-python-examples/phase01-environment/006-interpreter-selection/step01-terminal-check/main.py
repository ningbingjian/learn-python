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
