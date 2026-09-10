# Module 01.06 — Classes & Object Collaboration

> 状态：`BUILT`<br>
> 核心问题：稳定字段与行为散落后，怎样让对象维护明确责任？<br>
> 当前进度：三个 Unit 的正文、练习和必要源码已建设；尚未经过真实 Learning Gate。

## 为什么在这里出现

Task 维护单条状态，TaskTracker 拥有集合与 ID，CLI 接收协作者。 保持 add/list/complete/quit 外部行为，先改变责任与结构；新增功能留给 Module 07。

## Unit 阅读顺序

1. [为什么现在需要 class？](01-from-records-to-objects/)：从脆弱字典约定引出 Task，不把所有函数强行变成方法。
2. [实例状态和方法为什么需要 self？](02-instance-state-and-methods/)：构造、属性、方法与类级可变状态泄漏，验证实例隔离。
3. [多个对象怎样协作而不互相创建一切？](03-compose-task-collaborators/)：TaskTracker 组合 Task，入口创建协作者，CLI 接收输入输出函数。

## 完整源码与证据

[06-object-model](03-compose-task-collaborators/06-object-model/) 由 Unit 03 承接，是本 Module 唯一主线源码状态。前两个概念章节使用正文片段，不复制完整应用；上一版本仍完整保留，不依赖 Git 历史恢复教材。

对象测试验证构造、幂等完成、实例隔离与浅复制边界。

验证从源码目录运行 `python3.14 -m unittest discover -s tests -v`；整阶段方法见 [VERIFY.md](../VERIFY.md)。正文每个练习都明确约束、验收与解题判断，测试通过仅证明材料可运行，不替代学习者解释。

## 本 Module 的边界与退出能力

只涉及 class、instance、self、__init__、方法和组合；继承、ABC、Protocol、dataclass 与 Data Model 留在 Stage 02。退出时应能解释状态由谁创建、谁拥有、哪些引用仍共享。

`BUILT` 不等于 `VALIDATED`。只有真实学习者完成跟做与迁移，才提升学习验证状态；全 Stage 的状态与因果链见 [Stage README](../README.md)。
