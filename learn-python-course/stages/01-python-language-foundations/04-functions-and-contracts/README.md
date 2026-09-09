# Module 01.04 — Functions & Contracts

> 状态：`DESIGNED`<br>
> 核心问题：重复和嵌套开始妨碍修改后，怎样用函数建立职责与可测试契约？<br>
> 进入状态：`03-control-flow-cli` 可用，但单文件流程开始重复和嵌套。<br>
> 退出状态：`04-function-oriented`

本 Module 从现有脚本的修改成本推导函数，而不是先枚举函数语法。参数、返回值、默认参数和作用域都必须连接到真实契约、Bug 或测试。

计划中的 Unit 问题：

1. 什么时候应该把代码抽成函数？
2. 参数和返回值怎样形成稳定契约？
3. 函数为什么会意外共享或修改状态？

本目录当前只是 Module 级设计骨架，不包含空 Unit 或 Lab 目录；详细边界见[Stage 01 设计](../README.md#4-module-与-unit-边界)。
