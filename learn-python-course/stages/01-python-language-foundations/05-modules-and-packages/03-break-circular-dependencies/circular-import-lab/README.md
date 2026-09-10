# 循环导入故障的可重复证据

归属：[Unit 03](../)。broken 与 fixed 不是额外主线应用，只隔离双向依赖。

在本目录运行 `python3.14 verify.py`，预期：

```text
broken: ImportError from partial initialization
fixed: Added Read
```

也可进入 broken 运行 `python3.14 -c "import cli"`，观察 ImportError 与稳定片段 `cannot import name 'success_message'`；此命令应非零退出。fixed 中相同导入应静默成功，再调用 cli.run() 得到显示文本。验证器为两个状态分别启动新进程，避免模块缓存互相干扰。

Python 3.14 还可能附带改名建议；本实验中 cli → operations → cli 的调用链以及 success_message 定义尚未执行，才是部分初始化的证据。同一失败也可能显示 `from partially initialized module 'cli'`；验证器只断言缺失名字与参与文件，不绑定后半段诊断或建议文案。

错误版不是路径故障：解释器已经找到 cli 和 operations，只是在双向初始化途中索取尚未定义的名字。修复将输出责任留在 cli，operations 只返回记录，不靠改变导入时机隐藏依赖。
