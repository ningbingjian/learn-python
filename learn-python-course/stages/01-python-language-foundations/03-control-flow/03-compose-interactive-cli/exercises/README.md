# Module 03 迁移：Packing Checklist

不复制 Task Tracker 主线源码，独立写一个内存打包清单。命令 add/list/pack/quit，字段 id/name/packed；从空集合开始，成功新增才递增 ID。name 去首尾空白且不可空；pack 按业务 ID 查找，重复操作不反转状态。

必须使用 for 显示与查找、while 维持会话、break 结束成功搜索、loop else 反馈不存在。六组验收：

| 输入场景 | 必须观察到 |
|---|---|
| list → quit | Empty.，Bye.，退出 0 |
| add（空名称）→ add（Book）→ list | 报空名称；Book ID 为 1 |
| add Book → add Coat → list | 两条按新增顺序展示，均未打包 |
| add Book → pack 1 → pack 1 → list | 第一次 Packed，第二次 Already packed，仍为已打包 |
| pack abc → pack 99 → list | 格式错误与不存在分开，仍能继续 |
| 空命令 → unknown → quit | 提示后恢复，正常退出 |

再补充“pack 后继续 add/list”的序列，证明内层 break 没有结束外层会话。ID 不是列表索引，即使当前还没删除，也不能提前建立这个错误假设。

完成后对照 [reference.py](reference.py)，运行 `python3.14 reference.py`。参考输出格式为 `#1 [ ] Book` 或 `#1 [x] Book`；输入时 add 后接名称，pack 后接 ID。验证：`python3.14 -m unittest discover -s tests -v`。

参考判断：会话持有 items 与 next_id，计数在循环外初始化；新增先校验再 append；pack 的 else 与 for 对齐；重复 pack 只反馈，不用 `not packed` 翻转。源码是本迁移题的答案，不是新增主线里程碑。主线仍只有七个 Task Tracker 状态。
