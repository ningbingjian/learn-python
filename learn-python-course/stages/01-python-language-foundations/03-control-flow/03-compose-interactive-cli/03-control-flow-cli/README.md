# 03 — 控制流 CLI

归属：[本 Unit 正文](../)。上一完整状态：[前一里程碑](../../../02-collections-and-mutable-state/03-shared-mutable-state/02-collection-model/)。

仍是单文件直线分支与循环；没有函数或类。 此目录保存完整结果，不依赖其他里程碑源码或 Git 历史。

## 运行

Python 3.14，仅标准库。在本目录执行：

```bash
python3.14 task_tracker.py
python3.14 -m unittest discover -s tests -v
```

Windows 可用 `py -3.14` 替换 `python3.14`。Package 版必须从 README 所在目录使用 -m，不直接运行包内 cli.py。无第三方依赖，不需要安装同名包或配置本机绝对路径。

## 交互契约

支持 add、list、complete、quit；本版不支持编辑、删除、筛选或排序。

add 依次读取标题、优先级（整数 1～3）、可选备注。标题不可空；备注空白存为 None。命令去首尾空白并转小写，标题保留大小写。complete 读取业务 ID，不把 ID 当列表索引；重复完成只反馈“已完成”。错误返回命令提示，不消耗新增 ID。

一次最小会话的输入如下，2 后的空行是备注：

```text
add
Read
2

list
quit
```

输出包含 `Added task #1.`、`#1 [ ] Read | priority=2 | note=(none)` 和 `Goodbye.`。input 提示与输入同行，自动测试不会把完整终端回显当作固定输出。

正常退出请输入 quit，返回 0；EOF/Ctrl-C 尚未纳入本版恢复契约，最终版本才提供专门处理。

每次启动从空集合、ID 1 开始。退出即丢失数据；没有文件保存、数据库或网络。这是当前 Stage 的明确边界。

## 验证与源码导航

task_tracker.py 是唯一应用源码。 tests/test_cli.py 继承控制流版本的会话契约，覆盖空集合、失败不消耗 ID、顺序与身份、重复完成、非法与缺失 ID，以及未知命令恢复。






测试运行在各自目录，不跨快照导入。这些证据不代表持久化、并发安全或真实学习者已通过迁移；整阶段验证方法见 [VERIFY.md](../../../VERIFY.md)。
