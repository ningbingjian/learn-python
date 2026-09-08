# 用途：显示解释器与环境前缀，验证调用是否属于项目虚拟环境。
# 从本课目录用 .venv/bin/python diagnostics.py 运行；
# Windows 使用 .venv\Scripts\python.exe，其他步骤按正文替换脚本路径。
# sys 已在 006 讲过；本课只增加两个用于诊断环境归属的属性。
import sys

print("解释器路径：")
print(sys.executable)
print("当前环境前缀：")
print(sys.prefix)
print("基础环境前缀：")
print(sys.base_prefix)
