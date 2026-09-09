# Module 01.06 — Classes & Object Collaboration

> 状态：`DESIGNED`<br>
> 核心问题：什么时候“任务数据放在 dict、任务行为散落在函数”已经成为主要维护成本？<br>
> 进入状态：`05-package-structured` 的结构清楚，但领域数据形状仍然脆弱。<br>
> 退出状态：`06-object-model`

本 Module 让 `Task` class 解决已经积累的数据与行为分离问题，只覆盖实例状态、方法、`self`、`__init__`、组合和对象协作。

计划中的 Unit 问题：

1. 为什么现在需要 class？
2. 实例状态和方法为什么需要 `self`？
3. 多个对象怎样协作而不互相创建一切？

继承、多态、ABC、Protocol 和 Python Data Model 属于 Stage 02。本目录当前只是 Module 级设计骨架，不包含空 Unit 目录；详细边界见[Stage 01 设计](../README.md#4-module-与-unit-边界)。
