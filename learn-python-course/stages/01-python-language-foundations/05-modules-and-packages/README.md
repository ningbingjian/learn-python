# Module 01.05 — Modules & Packages

> 状态：`BUILT`<br>
> 核心问题：函数职责已明确，怎样拆文件而不制造隐式依赖？<br>
> 当前进度：三个 Unit 的正文、练习和必要源码已建设；尚未经过真实 Learning Gate。

## 为什么在这里出现

validation、operations、cli 按职责拆分；__main__ 提供安全入口。 保持 add/list/complete/quit 外部行为，先改变责任与结构；新增功能留给 Module 07。

## Unit 阅读顺序

1. [哪些职责应该成为独立 Module？](01-separate-module-responsibilities/)：按变化原因拆分字段规则、集合操作与 CLI，状态仍归会话拥有。
2. [程序入口和导入行为是什么关系？](02-entry-points-and-imports/)：安全导入、__name__、绝对/相对导入与 -m Package 入口。
3. [循环导入为什么是设计信号？](03-break-circular-dependencies/)：复现部分初始化失败，调整依赖方向，保存独立可运行 Package。

## 完整源码与证据

[05-package-structured](03-break-circular-dependencies/05-package-structured/) 由 Unit 03 承接，是本 Module 唯一主线源码状态。前两个概念章节使用正文片段，不复制完整应用；上一版本仍完整保留，不依赖 Git 历史恢复教材。

循环导入 Lab 对照错误与修复，并在独立进程里验证。

验证从源码目录运行 `python3.14 -m unittest discover -s tests -v`；整阶段方法见 [VERIFY.md](../VERIFY.md)。正文每个练习都明确约束、验收与解题判断，测试通过仅证明材料可运行，不替代学习者解释。

## 本 Module 的边界与退出能力

不讲完整 Import System、发布安装包或构建后端；退出时应能安全导入、从明确入口运行，并解释依赖为何单向。

`BUILT` 不等于 `VALIDATED`。只有真实学习者完成跟做与迁移，才提升学习验证状态；全 Stage 的状态与因果链见 [Stage README](../README.md)。
