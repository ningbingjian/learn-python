# Python Course Stages

`stages/` 只保存已经进入正式设计或建设的 Stage。完整路线和所有计划阶段见 [`../CURRICULUM.md`](../CURRICULUM.md)。

## 状态总览

| Stage | 名称 | 状态 | 当前目录 |
|---:|---|---|---|
| 00 | Developer Bootstrap | `DESIGNED` | [`00-developer-bootstrap`](00-developer-bootstrap/) |
| 01 | Python Language Foundations | `DESIGNED` | [`01-python-language-foundations`](01-python-language-foundations/) |
| 02 | Python Data Model & Pythonic Design | `PLANNED` | 尚未创建 |
| 03 | Typing, API Design & Metaprogramming | `PLANNED` | 尚未创建 |
| 04 | Data Structures & Algorithms | `PLANNED` | 尚未创建 |
| 05 | Standard Library, Files & CLI | `PLANNED` | 尚未创建 |
| 06 | Testing, Debugging & Quality | `PLANNED` | 尚未创建 |
| 07 | Packaging & Dependency Management | `PLANNED` | 尚未创建 |
| 08 | OS, Linux & Networking Foundations | `PLANNED` | 尚未创建 |
| 09 | Threading, Multiprocessing & Parallelism | `PLANNED` | 尚未创建 |
| 10 | asyncio & Async I/O | `PLANNED` | 尚未创建 |
| 11 | CPython Runtime & Performance | `PLANNED` | 尚未创建 |
| 12 | Software Design & Architecture Foundations | `PLANNED` | 尚未创建 |
| 13 | HTTP, WSGI, ASGI & Server Internals | `PLANNED` | 尚未创建 |
| 14 | SQL & Relational Database Internals | `PLANNED` | 尚未创建 |
| 15 | DB-API, SQLAlchemy & Alembic | `PLANNED` | 尚未创建 |
| 16 | FastAPI & Modern API Services | `PLANNED` | 尚未创建 |
| 17 | Django, DRF, Flask & Framework Selection | `PLANNED` | 尚未创建 |
| 18 | Redis & Distributed State | `PLANNED` | 尚未创建 |
| 19 | Task Systems, MQ & Event-Driven Architecture | `PLANNED` | 尚未创建 |
| 20 | Search, NoSQL, Object Storage & Data Infrastructure | `PLANNED` | 尚未创建 |
| 21 | RPC, Distributed Systems & Microservices | `PLANNED` | 尚未创建 |
| 22 | Security, Identity & Multi-Tenancy | `PLANNED` | 尚未创建 |
| 23 | Observability, Reliability & SRE | `PLANNED` | 尚未创建 |
| 24 | CI/CD, Containers, Kubernetes & Cloud Native | `PLANNED` | 尚未创建 |
| 25 | Data Analysis & Data Engineering | `PLANNED` | 尚未创建 |
| 26 | Machine Learning, Deep Learning & Model Serving | `PLANNED` | 尚未创建 |
| 27 | LLM, RAG, Agent, MCP & AI Platform | `PLANNED` | 尚未创建 |
| 28 | Production Architecture & Graduation Project | `PLANNED` | 尚未创建 |

## 目录创建规则

不为完整路线预先生成空目录。一个 Stage 至少完成教学边界、Module/Unit 地图、前置关系和验收设计后，才进入 `DESIGNED` 并创建目录。

同理，Module 和 Unit 也不以“先把目录铺满”为进度。目录存在、README 存在或代码能运行，都不能单独代表课程已经完成。状态定义和质量要求见 [`../QUALITY_GATE.md`](../QUALITY_GATE.md)。

Stage 01 当前已完成 Module 01～02 的六个正式 Unit、前两个主线源码状态和必要 Focused Lab，以及 Module 03 / Unit 01 的业务分支正文与练习，共七个 `BUILT` Unit。Module 03 的后两个 Unit 尚未建设，Module 04～07 仍只有边界说明。Module 03 和 Stage 01 整体继续保持 `DESIGNED`。
