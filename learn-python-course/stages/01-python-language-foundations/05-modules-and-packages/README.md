# Module 01.05 — Modules & Packages

> 状态：`DESIGNED`<br>
> 核心问题：函数已经分清职责以后，为什么仍然需要拆分单文件？<br>
> 进入状态：`04-function-oriented` 的函数边界已经形成，但文件和依赖边界不清。<br>
> 退出状态：`05-package-structured`

本 Module 从 CLI、任务操作与数据模型的不同职责推导 Module / Package 边界，并用入口、导入行为和循环导入失败验证设计。

计划中的 Unit 问题：

1. 哪些职责应该成为独立 Module？
2. 程序入口和导入行为是什么关系？
3. 循环导入为什么是设计信号？

本目录当前只是 Module 级设计骨架，不包含空 Unit 目录；详细边界见[Stage 01 设计](../README.md#4-module-与-unit-边界)。
