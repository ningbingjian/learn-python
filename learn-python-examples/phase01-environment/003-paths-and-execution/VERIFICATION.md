# 01-003 验证记录

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
| 路径组合 | 同目录、父目录与另一工作目录的绝对路径都指向预期文件，三行输出一致。 |
| 空格与错误 | 未引用的带空格路径失败，完整引用后成功；根目录错误文件名和 Linux 大小写错误均符合预期。 |
| 练习 | 从 exercises 与本课目录运行移动副本，输出一致。 |

## 文件执行清单

命令从各文件所在目录执行；路径表用于定位，具体逐条注释和环境命令见课程正文。007 与 008 另按上表在各自环境中执行了完整流程。

| 文件 | 工作目录（相对本课） | 检查结果 |
| --- | --- | --- |
| [exercises/moved copy/main.py](exercises/moved%20copy/main.py) | `exercises/moved copy` | 正常退出，输出或诊断字段符合课文 |
| [step01-same-directory/main.py](step01-same-directory/main.py) | `step01-same-directory` | 正常退出，输出或诊断字段符合课文 |
| [step02-parent-directory/main.py](step02-parent-directory/main.py) | `step02-parent-directory` | 正常退出，输出或诊断字段符合课文 |
| [step03-space-in-path/demo folder/main.py](step03-space-in-path/demo%20folder/main.py) | `step03-space-in-path/demo folder` | 正常退出，输出或诊断字段符合课文 |

## 完成含义

本记录证明上述源码及 Linux 实验已经验证，不表示读者已完成练习。真实界面操作、其他系统及本机安装问题按自己的实际结果记录；变量路径不写入公开文档。临时实验与环境没有作为课程依赖保存。
