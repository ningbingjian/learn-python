# Source Milestone 01 — Interactive Script

> 状态：`BUILT`<br>
> 所有者：[Unit 03 — Trust User Input](../README.md)<br>
> 作用：保存 Module 01 结束后的唯一完整主线状态<br>
> 依赖：Python 标准库，无第三方依赖

## 1. 当前状态证明什么

这不是 `input()` API Demo，而是 `CLI Task Tracker` 的第一版完整业务状态。它证明程序能够：

```text
从终端接收一条任务
→ 清理文本边界
→ 把优先级转换成整数
→ 拒绝空标题、错误类型和范围外数字
→ 用 bool 表达初始完成状态
→ 用 None 表达缺失备注
→ 给用户明确反馈和退出码
```

## 2. 文件

```text
01-interactive-script/
├── README.md
├── task_tracker.py
└── tests/
    └── test_task_tracker.py
```

- `task_tracker.py` 是学习者阅读和修改的完整源码。
- `tests/test_task_tracker.py` 从进程边界验证输入、输出和退出码。
- 没有 `pyproject.toml`，因为当前状态只依赖标准库，也不是独立 Package。

## 3. 运行

从当前目录执行：

```bash
python task_tracker.py
```

成功示例：

```text
CLI Task Tracker — create one task
Task title: Learn Python
Priority (1-3): 2
Note (optional): Finish Module 01

Created task
Title: Learn Python
Priority: 2
Done: False
Note: Finish Module 01
```

备注留空时，内部使用 `None`，输出为：

```text
Note: (none)
```

## 4. 自动化验证

```bash
python -m unittest discover -s tests -v
```

测试固定以下用户可观察行为：

| 场景 | 关键结果 |
|---|---|
| 有效任务与备注 | 退出码 `0`，所有字段正确显示 |
| 有效任务、备注留空 | 退出码 `0`，显示 `(none)` |
| 空标题 | 退出码 `1`，显示标题错误，不出现 traceback |
| 非整数优先级 | 退出码 `1`，显示转换错误，不出现 traceback |
| 范围外优先级 | 退出码 `1`，显示范围错误，不出现 traceback |

测试使用 `sys.executable` 启动与当前测试环境相同的 Python，避免“测试的是另一个解释器”。`subprocess` 是课程维护证据的实现方式，不是 Module 01 的学习目标。

## 5. 源码阅读地图

按数据进入程序的顺序阅读：

```text
title
→ strip
→ 空值校验

priority_text
→ strip
→ int 转换
→ 1～3 范围校验

note_text
→ strip
→ 空字符串统一为 None

done
→ 创建时固定为 False

统一输出任务摘要
```

每个外部字段都在刚进入程序时完成规范化。后面的输出代码只处理已经可信的内部状态。

## 6. 当前设计边界

有意保留：

```text
单文件
顺序执行
一次创建一条任务
内存中只保存当前字段
标准库实现
```

有意不加入：

```text
任务集合、菜单循环       → Module 02 / 03
函数拆分                 → Module 04
Module / Package         → Module 05
Task class               → Module 06
数据库和第三方 CLI 框架  → 后续 Stage
```

下一状态只有在数据模型、责任或运行行为发生显著变化时才值得保存。Module 02 会基于本状态，让单条任务成长为一组可管理的任务。
