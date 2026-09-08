# 第一阶段验证汇总

[返回阶段导航](README.md)

第一课于 2026-09-07 验证，后七课于 2026-09-08 验证。基线均为 Linux / bash / CPython 3.12.13。后七课共 39 个 Python 文件（包括故意失败材料），全部按预期行为检查；核心命令从文档提取后在独立临时副本中执行。正常文件不等于所有文件都应成功，错误教学文件的预期是指定失败。

| 课次 | 核心验证 | 记录 |
| --- | --- | --- |
| 01-001 | 单行程序、保存、路径与独立运行 | [原验证记录](001-first-program/VERIFICATION.md) |
| 01-002 | 打印多行模拟信息 | [验证记录](002-output-and-comments/VERIFICATION.md) |
| 01-003 | 从不同目录运行同一个文件 | [验证记录](003-paths-and-execution/VERIFICATION.md) |
| 01-004 | 交互模式与脚本模式 | [验证记录](004-interactive-and-script/VERIFICATION.md) |
| 01-005 | 认识语法错误与异常回溯 | [验证记录](005-errors-and-tracebacks/VERIFICATION.md) |
| 01-006 | 检查并选择项目解释器 | [验证记录](006-interpreter-selection/VERIFICATION.md) |
| 01-007 | 创建并使用隔离环境 | [验证记录](007-virtual-environment/VERIFICATION.md) |
| 01-008 | 独立完成信息卡程序 | [验证记录](008-information-card/VERIFICATION.md) |

跨课检查包含：文档代码与源码一致、导航与本地链接、编号、未完成状态、个人姓名残留和环境产物未入库。macOS、PowerShell、VS Code GUI 未实测；004 使用真实 PTY 并通过信号验证中断，不声称模拟了所有桌面快捷键。阶段验收清单留给读者自行完成，不自动标记“已学习”。

课程中的 venv、pip 引导修复与 RUNBOOK 在临时副本运行后清理。没有引入第三方测试框架作为入门课依赖，也没有让学习者先读验证脚本才能运行示例。
