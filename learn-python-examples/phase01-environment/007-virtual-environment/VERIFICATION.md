# 01-007 验证记录

[返回课程](README.md) · [阶段验证汇总](../VERIFICATION.md)

## 环境与范围

- 日期：2026-09-08；Linux / bash / CPython 3.12.13。
- 本课 Python 文件逐一运行；正常输出与预期比较，故意失败文件单独检查退出状态和错误类型。
- 正常固定输出文件另复制到独立临时目录运行，验证没有隐藏的兄弟步骤依赖。
- 文档内带 source 标记的完整代码与对应源码逐字比较通过。
- macOS、Windows PowerShell、安装流程与 VS Code GUI 未实测；平台说明不等同于端到端验证。

## 实际结果

| 实验 | 结果与证据 |
| --- | --- |
| 创建与直接运行 | 在临时目录创建普通 venv，当前 prefix 指向该环境且不同于 base_prefix；未激活也能运行。 |
| 激活与退出 | 按文档 bash 块执行 source、command -v、诊断、pip、deactivate，退出后基础入口恢复。 |
| 新会话与包工具 | 新 shell 直接调用环境仍有效；pip 位置在该环境内。 |
| 缺 pip 恢复 | 专门创建 --without-pip 的临时环境，先验证缺 pip，再按文档 ensurepip 恢复并检查位置。 |
| 独立练习 | 独立 .venv-exercise 创建和答案运行通过；测试环境随临时目录清理。 |

## 文件执行清单

命令从各文件所在目录执行；路径表用于定位，具体逐条注释和环境命令见课程正文。007 与 008 另按上表在各自环境中执行了完整流程。

| 文件 | 工作目录（相对本课） | 检查结果 |
| --- | --- | --- |
| [exercises/solution.py](exercises/solution.py) | `exercises` | 正常退出，输出或诊断字段符合课文 |
| [step01-create-environment/main.py](step01-create-environment/main.py) | `step01-create-environment` | 正常退出，输出或诊断字段符合课文 |
| [step02-activate-and-check/main.py](step02-activate-and-check/main.py) | `step02-activate-and-check` | 正常退出，输出或诊断字段符合课文 |
| [step03-without-activation/main.py](step03-without-activation/main.py) | `step03-without-activation` | 正常退出，输出或诊断字段符合课文 |

## 完成含义

本记录证明上述源码及 Linux 实验已经验证，不表示读者已完成练习。真实界面操作、其他系统及本机安装问题按自己的实际结果记录；变量路径不写入公开文档。临时实验与环境没有作为课程依赖保存。
