# Module 01.07 — Integration & Stage Project

> 状态：`BUILT`<br>
> 核心问题：能否将已有能力组合成交付物，并独立完成新需求？<br>
> 当前进度：三个 Unit 的正文、练习和必要源码已建设；尚未经过真实 Learning Gate。

## 为什么在这里出现

在对象版上增加编辑、删除、状态筛选与输入结束策略。 本 Module 不是最后另做一次新项目，而是验收前六次演进的结果。

## Unit 阅读顺序

1. [怎样把需求转成实现与验收计划？](01-plan-requirements-and-acceptance/)：明确命令、完整替换式编辑、稳定 ID、筛选与输入中断契约。
2. [怎样完成并验证完整 Task Tracker？](02-complete-and-verify-task-tracker/)：增量完成编辑、删除、状态筛选与入口退出；提供领域和会话证据。
3. [能否闭卷完成一个未在正文出现的变化？](03-closed-book-transfer/)：新增截止天数、优先级排序、到期筛选；独立题面、验收与完整参考解。

## 完整源码与证据

[07-complete-task-tracker](02-complete-and-verify-task-tracker/07-complete-task-tracker/) 由 Unit 02 承接，是本 Module 唯一主线源码状态。前两个概念章节使用正文片段，不复制完整应用；闭卷参考解是独立练习答案，不计为第八个主线状态。

最终测试覆盖编辑整体性、删除后 ID、筛选不改源集合和输入中断；参考解另验新字段与排序。

验证从源码目录运行 `python3.14 -m unittest discover -s tests -v`；整阶段方法见 [VERIFY.md](../VERIFY.md)。正文每个练习都明确约束、验收与解题判断，测试通过仅证明材料可运行，不替代学习者解释。

## 本 Module 的边界与退出能力

不引入持久化、数据库、网络或框架；退出时应能独立扩展模型、操作、CLI 与测试，并提交 Guided Build 和 Closed-book Transfer 的真实学习证据。

`BUILT` 不等于 `VALIDATED`。只有真实学习者完成跟做与迁移，才提升学习验证状态；全 Stage 的状态与因果链见 [Stage README](../README.md)。
