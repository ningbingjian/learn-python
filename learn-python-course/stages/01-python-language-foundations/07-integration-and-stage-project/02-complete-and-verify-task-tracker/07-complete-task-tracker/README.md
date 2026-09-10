# 07 — 完整 Task Tracker

归属：[本 Unit 正文](../)。上一完整状态：[前一里程碑](../../../06-classes-and-object-collaboration/03-compose-task-collaborators/06-object-model/)。

在对象版上增加编辑、删除、状态筛选与输入结束策略。 此目录保存完整结果，不依赖其他里程碑源码或 Git 历史。

## 运行

Python 3.14，仅标准库。在本目录执行：

```bash
python3.14 -m task_tracker
python3.14 -m unittest discover -s tests -v
```

Windows 可用 `py -3.14` 替换 `python3.14`。Package 版必须从 README 所在目录使用 -m，不直接运行包内 cli.py。无第三方依赖，不需要安装同名包或配置本机绝对路径。

## 交互契约

支持 add、list、list --pending、list --done、complete、edit、delete、quit。edit 先输入 ID，再完整替换标题、优先级、备注；空白备注清除，ID 与 done 不变。delete 不重用旧 ID，筛选不修改原集合。

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

EOF 正常结束并返回 0；Ctrl-C 返回 130；两者均给出明确提示。发生在 add/edit 未完成输入处时不提交该操作。非预期程序异常不会被吞掉。

每次启动从空集合、ID 1 开始。退出即丢失数据；没有文件保存、数据库或网络。这是当前 Stage 的明确边界。

## 验证与源码导航

task_tracker/ 是应用 Package；__main__.py 是入口，cli.py 是交互层，validation.py 是字段规则。 tests/test_cli.py 继承控制流版本的会话契约，覆盖空集合、失败不消耗 ID、顺序与身份、重复完成、非法与缺失 ID，以及未知命令恢复。


tests/test_imports.py 在新进程中验证包、CLI 与入口模块安全导入。
models.py 与 tracker.py 分别承接单条任务和集合；tests/test_objects.py 验证实例独立、浅复制边界、合法构造和完成幂等。
tests/test_delivery.py 额外验证原子编辑、删除 ID 稳定、状态筛选、真实会话、每个输入点 EOF、Ctrl-C 与非预期 Bug 传播。

测试运行在各自目录，不跨快照导入。这些证据不代表持久化、并发安全或真实学习者已通过迁移；整阶段验证方法见 [VERIFY.md](../../../VERIFY.md)。
