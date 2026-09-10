# Module 01.04 — Functions & Contracts

> 状态：`BUILT`<br>
> 核心问题：脚本重复且难以独立测试，怎样用显式契约划分职责？<br>
> 当前进度：三个 Unit 的正文、练习和必要源码已建设；尚未经过真实 Learning Gate。

## 为什么在这里出现

解析、字段规则、集合操作与交互分为函数，仍在同一文件。 保持 add/list/complete/quit 外部行为，先改变责任与结构；新增功能留给 Module 07。

## Unit 阅读顺序

1. [什么时候应该把代码抽成函数？](01-extract-responsibilities/)：从终端与规则混杂推导解析、操作、展示边界，区分 return 与 print。
2. [参数和返回值怎样形成稳定契约？](02-parameters-and-return-contracts/)：位置、关键字、默认参数、多值解包与必要的星号参数入口；明确错误与副作用。
3. [函数为什么会意外共享或修改状态？](03-state-and-scope/)：默认参数与作用域故障实验，形成显式数据流的完整函数版。

## 完整源码与证据

[04-function-oriented](03-state-and-scope/04-function-oriented/) 由 Unit 03 承接，是本 Module 唯一主线源码状态。前两个概念章节使用正文片段，不复制完整应用；上一版本仍完整保留，不依赖 Git 历史恢复教材。

两个 Focused Lab 隔离可变默认参数与作用域重新绑定。

验证从源码目录运行 `python3.14 -m unittest discover -s tests -v`；整阶段方法见 [VERIFY.md](../VERIFY.md)。正文每个练习都明确约束、验收与解题判断，测试通过仅证明材料可运行，不替代学习者解释。

## 本 Module 的边界与退出能力

不提前拆包或引入类；完整 pytest、Mock 与高级类型系统后置。退出时应能说清每个函数接受、返回、修改和抛出什么。

`BUILT` 不等于 `VALIDATED`。只有真实学习者完成跟做与迁移，才提升学习验证状态；全 Stage 的状态与因果链见 [Stage README](../README.md)。
