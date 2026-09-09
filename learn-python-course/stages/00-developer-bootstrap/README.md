# Stage 00 — Developer Bootstrap

> 状态：`DESIGNED`<br>
> 目标：从一台具备基础操作系统环境的电脑出发，建立可复现的 Python 开发、运行、调试、依赖管理和 Git 工作流。

## 1. 阶段定位

Stage 00 不是 Terminal、Git、IDE 或 Packaging 的百科全书。它只建立后续课程必须依赖的最小工程能力：

```text
知道代码文件在哪里
→ 知道哪个 Python 在执行
→ 能从终端运行
→ 能在 IDE 中调试
→ 能用 uv 创建和同步项目
→ 能用 Git 保存一次可审查的变化
```

深层 Shell、Linux、依赖解析、Wheel、PyPI 和 CI/CD 分别放在后续阶段。这里不让工程工具压过第一次编程体验。

## 2. Module 与 Unit 地图

### Module 00.01 — 文件、路径与 Terminal

- **Unit 01：命令到底在哪里执行？** 建立当前工作目录、相对路径、绝对路径、命令、参数和退出码的第一层模型。
- **Unit 02：环境变量为什么会影响程序？** 只覆盖 PATH 和项目运行所需的最小环境变量知识。

### Module 00.02 — Python Runtime

- **Unit 01：电脑里“安装 Python”到底安装了什么？** 区分源码文件、解释器、进程、REPL 和标准库。
- **Unit 02：多个 Python 版本为什么容易混乱？** 学会确认实际执行的解释器，不在本阶段深入版本管理器原理。

### Module 00.03 — Editor & Debugger

- **Unit 01：编辑器与 Python 解释器是什么关系？** IDE 负责编辑、导航和调试，解释器负责运行。
- **Unit 02：如何用断点而不是 print 猜问题？** 建立断点、单步、调用栈和变量观察的最小能力。

### Module 00.04 — Git Workflow

- **Unit 01：为什么要把一次变化保存成 Commit？** 理解 working tree、staging area、commit 和 diff。
- **Unit 02：怎样完成最小分支开发？** 完成 branch、commit、merge 和冲突处理的可运行练习。

### Module 00.05 — uv & First Project

- **Unit 01：脚本什么时候需要成为项目？** 从单文件脚本演进到包含 `pyproject.toml` 的最小项目。
- **Unit 02：环境、依赖和锁文件各自解决什么？** 使用 uv 完成创建、同步、运行和添加开发依赖，不提前展开完整 Packaging 机制。

### Module 00.06 — Stage Project

- **Python Developer Bootstrap**：从空目录创建一个可运行的小程序，加入测试，使用 Git 分支完成修改并打 Tag；另一台干净环境应能按文档恢复和运行。

## 3. 源码与教学状态设计

本阶段不会给每条命令建立独立项目。只在出现有意义的新工程状态时保留完整源码：

```text
01-first-script
→ 能从终端运行的单文件程序

02-debuggable-program
→ 出现可复现 Bug，并能通过断点定位

03-uv-project
→ 正式项目、依赖和测试入口

04-release-ready-project
→ Git 流程、版本标记和可复现运行说明
```

这些名称是当前设计建议；正式建设时仍需通过 `COURSE_STRUCTURE.md` 的源码状态判断。

## 4. 阶段边界

本阶段不系统讲：

```text
Python 语言语义             → Stage 01
复杂 Git 协作与 CI          → Stage 24
pip / build / wheel / PyPI  → Stage 07
Linux 进程、FD、网络诊断    → Stage 08
pytest 完整体系             → Stage 06
```

## 5. 阶段验收

完成后，学习者应能够：

1. 解释源码、解释器和进程不是同一个东西。
2. 在不依赖 IDE 的情况下运行 Python 程序。
3. 确认当前项目实际使用的 Python 版本和环境。
4. 使用断点定位一个简单逻辑错误。
5. 使用 uv 创建、同步、运行项目并执行测试。
6. 使用 Git 分支完成一次变化，查看 diff 并合并。
7. 根据 README 在新目录重新恢复项目。

当前只有教学设计，尚未建设正式 Unit，因此 Stage 状态为 `DESIGNED`，不标记 `BUILT`。
