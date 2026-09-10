# Stage 01 验证与交付边界

Python 基线 3.14，仅标准库。所有源码状态各自独立运行，禁止从最终版借用实现来让早期状态通过。

在仓库根目录运行：

```bash
python3.14 learn-python-course/stages/01-python-language-foundations/verify_stage.py
uvx ruff check --isolated --select E4,E7,E9,F learn-python-course/stages/01-python-language-foundations
uvx ruff format --isolated --check learn-python-course/stages/01-python-language-foundations
```

Windows 可用 `py -3.14` 替换 `python3.14`。作者的标准库验证器可从任意工作目录通过其路径启动；应用自身应遵循各里程碑 README 的工作目录约定。

验证器检查七个 Module、21 个 Unit、七个主线状态；检查本地链接目标与 Python 语法；执行正文 pycon 交互例与保留分支章节的 17 个独立片段；分别运行七个主线版本、闭卷参考解与 Packing Checklist 迁移答案的行为测试；逐一核对五个 Lab 的预期输出。Markdown 中标作摘录的 python 片段不是独立应用，不能把它们全部盲目当脚本执行。链接锚点与教学衔接另行审查。

## 本次验证结果（2026-09-10）

环境：macOS、CPython 3.14.4；Ruff 0.16.6。七个主线状态的测试数分别为 5、5、8、13、14、14、24；闭卷参考解 15，Packing Checklist 答案 6，共 **104 项行为测试通过**（参数化子情形不重复计数）。

另外通过 **120 个 pycon 交互示例、17 个既有分支片段、五个 Lab 的输出核对**，以及本地链接目标、Python 语法、Ruff 基础规则、格式与差异空白检查。循环导入实验根据 3.14 的实际 ImportError 与调用链校验，不依赖旧版本的诊断措辞。

Ruff 使用明确的基础错误规则，避免自动简化教学反例；作用域 Lab 的 F823 在故意失败行局部豁免，错误仍由实验断言验证。没有全局忽略代码缺陷。

当前 Stage 的测试工具选择标准库 unittest；pytest 体系、Mock、完整静态类型检查属于后续 Stage，因此本次不宣称完成 Pyright/Mypy 或完整 pytest 门禁。CLI 文本入口有字段校验，内部 API 接收各章约定的类型，不承诺接受任意 Python 对象。

## 教学审查与未覆盖范围

- 保留前两 Module 与 Module 03 / Unit 01；新增内容从既有任务模型继续，不覆盖原 phase 课程。
- 七个完整主线状态分别归属产生变化的 Unit；闭卷参考解是答案，不计第八个主线里程碑。
- 函数、拆包、对象版本保留相同四命令契约；最终版本才增加编辑、删除、状态筛选与输入结束策略。
- 闭卷题避免重复已有 priority 字段与 pending 命令，改验新截止信息、稳定排序和到期筛选。
- 解释副作用、共享引用、失败前无修改、导入时机及抽象成本；高级语言机制和框架保持后置。

本次验证不证明持久化、并发安全、全部操作系统终端组合或真实学习者学习效果。当前状态为 BUILT；真实 Guided Build 与 Closed-book Transfer 记录缺失，不能标记 VALIDATED。
