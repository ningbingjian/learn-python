# Learn Python Curriculum v3.0

本文定义从零基础到高级 / 资深 Python 工程师、Python 架构师以及 AI 平台工程师的完整能力地图。

课程地图不是要求所有人机械串行完成 29 个 Stage。不同目标共享基础能力，然后进入不同专业路径。

## 1. 能力路线与专业路径

```text
00～07  Python 基础与工程能力
08～12  系统、并发、运行时与设计能力
13～17  Web 与数据库服务能力
18～24  分布式生产平台与云原生能力
25～28  数据、AI 与毕业级架构能力
```

推荐路径：

### Python 工程师主线

```text
00 → 01 → 02 → 03 → 04 → 05 → 06 → 07
→ 08 → 09 → 10 → 11 → 12
```

### Web 后端主线

```text
Python 工程师主线
→ 13 → 14 → 15 → 16
→ 18 → 19 → 22 → 23 → 24
```

Django / DRF / Flask 的 Stage 17 根据项目需要选择，不要求与 FastAPI 同等深度全部掌握。

### 分布式与平台架构主线

```text
Web 后端核心能力
→ 18 → 19 → 20 → 21 → 22 → 23 → 24 → 28
```

### 数据与 AI 主线

```text
00～11 的必要基础
→ 25 → 26 → 27
→ 补齐 22～24 的生产化能力
→ 28
```

## 2. Stage 00 — Developer Bootstrap

**目标**：建立后续课程所需的最小开发、运行、调试、依赖管理和 Git 能力。

核心领域：

```text
文件与路径
Terminal / Shell 最小能力
Python Interpreter / REPL / Process
IDE / Debugger
Git branch / commit / diff / merge
uv project / environment / dependency
```

能力证明：从空目录创建可运行、可测试、可由他人恢复的最小 Python 项目，并完成一次分支开发。

目录：[`stages/00-developer-bootstrap/`](stages/00-developer-bootstrap/)

## 3. Stage 01 — Python Language Foundations

**总问题**：一个简单 Python 脚本，怎样一步一步成长为结构清晰、可维护的 CLI 应用？

**目标**：沿同一个 `CLI Task Tracker` 的连续演进，独立实现、拆分、测试并解释一个结构清晰的命令行应用。

核心 Module：

```text
First Useful Python Program
Collections & Mutable State
Control Flow
Functions & Contracts
Modules & Packages
Classes & Object Collaboration
Integration & Stage Project
```

七个关键源码状态：

```text
01-interactive-script
→ 02-collection-model
→ 03-control-flow-cli
→ 04-function-oriented
→ 05-package-structured
→ 06-object-model
→ 07-complete-task-tracker
```

关键边界：Stage 00 已经负责源码、解释器、进程和运行工作流，Stage 01 从第一条真实任务开始写 Python。Iterator、Generator、Decorator、Context Manager、完整 Python Data Model、继承、ABC、Protocol、Bytecode、GC、GIL、复杂 Typing 和完整 Packaging 后置。

能力证明：闭卷为 CLI Task Tracker 增加 `priority`、排序与 `list --pending` 能力，能够同步修改数据模型、函数、Package、对象与测试，并解释名字绑定、可变对象、函数契约、模块拆分和基础对象协作。

目录：[`stages/01-python-language-foundations/`](stages/01-python-language-foundations/)

## 4. Stage 02 — Python Data Model & Pythonic Design

**目标**：从“会写 Python 语法”提升到“理解对象协议并设计符合 Python 生态习惯的模型与 API”。

核心 Module：

```text
Python Data Model 与特殊方法
Iterator / Iterable / Generator
First-class Function / Closure
Decorator
Context Manager
dataclass / Enum / Value Object
Inheritance / Composition / ABC
Duck Typing 与 Protocol 入口
EAFP、truthiness、iteration idioms
Pythonic API 与对象协作
```

重点问题：对象怎样参与比较、哈希、迭代、调用、上下文管理和容器协议；什么时候组合优于继承；怎样避免“用 Python 写 Java”。

能力证明：把 Stage 01 的领域模型重构成协议清晰、可扩展、可测试的 Pythonic Library，同时解释每个特殊方法带来的契约和代价。

## 5. Stage 03 — Typing, API Design & Metaprogramming

**目标**：建立现代 Python 大型代码库需要的静态契约、扩展机制和元编程边界。

核心 Module：

```text
Annotation 语义与 deferred evaluation
Union / Literal / TypedDict / TypeAlias
Generic / TypeVar / ParamSpec / TypeVarTuple
Protocol 与 Structural Typing
Callable、Decorator typing
Reflection / inspect
Attribute Lookup
property / Descriptor
__init_subclass__ / Metaclass
Plugin Registry / Dependency Injection
Public API、兼容性与 deprecation
```

能力证明：实现一个类型安全的插件系统或最小框架，支持注册、发现、配置、扩展和静态检查；能够说明元编程何时值得、何时只是制造隐式复杂度。

## 6. Stage 04 — Data Structures & Algorithms

**目标**：能够根据数据规模、操作特征和复杂度选择结构，并把算法判断连接到 Python 实现成本。

核心 Module：

```text
Big-O 与实际成本
Array / Linked List / Stack / Queue / Deque
Hash Table、dict / set 机制
Heap / Priority Queue
Tree / Trie / Graph
Sorting / Binary Search
BFS / DFS
LRU / Top-K / Sliding Window
collections / heapq / bisect / itertools
算法测试与复杂度实验
```

能力证明：实现索引、缓存、Top-K、图遍历等组件，并使用可复现实验说明结构选择，而不是只背复杂度表。

## 7. Stage 05 — Standard Library, Files & CLI

**目标**：使用标准库完成可靠的文件、文本、数据转换、系统命令和自动化工具。

核心 Module：

```text
pathlib / os / shutil / tempfile / io
Text / Bytes / Encoding / Unicode
JSON / CSV / TOML / Pickle 边界
Datetime / ZoneInfo
Regex 与文本解析
logging
argparse / Typer / Click / Rich
subprocess
HTTP Client
BeautifulSoup / lxml / Playwright
幂等、重试、失败恢复
```

能力证明：交付一个文件与日志分析 CLI 或开发运维自动化工具，能够处理中断、重复执行、编码、错误输入和可观测输出。

## 8. Stage 06 — Testing, Debugging & Quality

**目标**：把“代码能跑”升级为“行为可验证、缺陷可定位、变化可审查”。

核心 Module：

```text
Exception hierarchy / chaining / traceback
pdb 与 IDE Debugger 深入
pytest fixture / parameterize / marker
Mock / patch / fake / stub
Unit / Integration / Contract / E2E
Hypothesis / Property-based Testing
coverage 的正确解释
Ruff / formatting
Pyright / Mypy
pre-commit
测试金字塔与可测试设计
```

能力证明：为已有应用建立稳定测试策略，定位一个非显而易见 Bug，并说明测试证明了什么、没有证明什么。

## 9. Stage 07 — Packaging & Dependency Management

**目标**：理解 Python 项目如何被解析、安装、构建、发布和复现，而不是只会执行安装命令。

核心 Module：

```text
venv / pip / requirements 历史模型
pyproject.toml
uv project / lock / sync / workspace
Dependency Resolution 与冲突
Dependency Group / Optional Dependency
src layout
Build Backend
sdist / wheel
Editable Install
Versioning / Compatibility
PyPI / Private Index / Supply-chain
CLI entry point 与 Library 发布
```

能力证明：开发并发布一个真实可安装 Package，验证构建产物、依赖边界、版本兼容和下游安装。

## 10. Stage 08 — OS, Linux & Networking Foundations

**目标**：为并发、Web、运行时和生产诊断建立必要的操作系统与网络模型。

核心 Module：

```text
Process / Thread / Scheduler / Context Switch
Virtual Memory / Page / mmap / Page Cache
File Descriptor / Signal / Pipe
Filesystem 与权限
Linux process / systemd / cgroup / namespace
CPU / memory / IO diagnosis
TCP/IP / DNS / Routing / NAT
Socket 与基础抓包
```

能力证明：在 Linux 上运行一个 Client/Server，使用系统工具定位 CPU、内存、FD、进程和基础网络问题。

## 11. Stage 09 — Threading, Multiprocessing & Parallelism

**目标**：根据 IO-bound、CPU-bound、隔离和共享状态要求选择同步、线程、进程与并行模型。

核心 Module：

```text
threading
Lock / RLock / Condition / Semaphore / Event
Queue
Race / Deadlock / Starvation
ThreadPoolExecutor
multiprocessing / Process / IPC
Shared Memory
ProcessPoolExecutor
Serialization cost
Worker lifecycle
Cancellation / timeout / shutdown
```

能力证明：实现可控的并发文件或计算处理平台，测量吞吐、CPU、内存、序列化和调度成本，并解释选择。

## 12. Stage 10 — asyncio & Async I/O

**目标**：真正理解 Coroutine、Task、Event Loop 和非阻塞 IO，并能构建可取消、有背压、可观测的异步系统。

核心 Module：

```text
Coroutine / Awaitable
Event Loop
Task / Future
TaskGroup 与 Structured Concurrency
Timeout / Cancellation
Async Queue / Lock / Semaphore
Stream / Socket
Backpressure
Rate Limit / Retry
Async resource lifecycle
同步、线程、进程、异步选型
```

能力证明：实现异步 HTTP 聚合器或任务调度器，处理限流、超时、取消、部分失败、背压和优雅关闭。

## 13. Stage 11 — CPython Runtime & Performance

**目标**：连接 Python 源码、对象模型、解释器、内存和性能证据。

核心 Module：

```text
Source → AST → Code Object → Bytecode
Frame / Evaluation Loop
PyObject / Type Object
Reference Counting / Cyclic GC
pymalloc 与内存行为
GIL
Free-threaded Python
Subinterpreters
C Extension / Cython / PyO3 边界
timeit / cProfile / tracemalloc / py-spy
CPU、allocation 与 memory leak 分析
```

能力证明：构建 Runtime Lab，围绕 Bytecode、GC、GIL、free-threaded、CPU hotspot 和内存泄漏形成可重复证据。

## 14. Stage 12 — Software Design & Architecture Foundations

**目标**：从函数和类的局部设计，进入模块边界、领域模型、依赖方向和架构决策。

核心 Module：

```text
SOLID 的适用边界
Composition over Inheritance
Strategy / Factory / Adapter / Observer / Command
Dependency Injection
Repository / Unit of Work
Layered / Clean / Hexagonal Architecture
DDD 基础与 bounded context
Library / Service API Design
Refactoring
ADR 与架构文档
```

能力证明：重构一个耦合应用，比较至少两种边界方案，保存 ADR，并通过测试证明替换性和行为稳定。

## 15. Stage 13 — HTTP, WSGI, ASGI & Server Internals

**目标**：理解 Python Web Framework 下方的协议、服务器和并发运行模型。

核心 Module：

```text
HTTP message / method / status / header
Cookie / Cache / CORS
HTTP/1.1 / HTTP/2 / HTTP/3 基础
REST
SSE / WebSocket
Reverse Proxy
WSGI
ASGI
Starlette / Uvicorn
Worker / Middleware / Lifespan
Connection、timeout 与部署模型
```

能力证明：实现最小 ASGI 应用或框架，包含 router、request、response、middleware、错误处理和生命周期。

## 16. Stage 14 — SQL & Relational Database Internals

**目标**：能够设计关系模型、写出可靠 SQL，并通过执行计划、事务和存储机制解释数据库行为。

核心 Module：

```text
Relational Model / Schema Design
CRUD / JOIN / Subquery / CTE / Window Function
Index / B+Tree
Transaction / ACID / Isolation
MVCC / Lock / Deadlock
Execution Plan / Statistics
MySQL InnoDB
PostgreSQL WAL / Vacuum
Partition
Backup / Restore
Slow Query Diagnosis
```

能力证明：构造真实数据集，诊断索引、执行计划、事务隔离、锁和慢 SQL 问题。

## 17. Stage 15 — DB-API, SQLAlchemy & Alembic

**目标**：理解 Python 数据访问从 Driver 到 ORM 的完整责任链，并避免 Session、事务、连接池和加载策略误用。

核心 Module：

```text
DB-API / Driver
Connection / Cursor
Connection Pool
SQLAlchemy Engine / Core
ORM Mapping
Session / Identity Map / Unit of Work
Transaction Boundary
Relationship / Lazy / Eager / N+1
AsyncEngine / AsyncSession
Alembic Migration
Repository / UoW
ORM Performance
```

能力证明：实现事务明确、可迁移、可测试的异步数据服务，并通过实验观察池、Session、Identity Map 和 N+1。

## 18. Stage 16 — FastAPI & Modern API Services

**目标**：构建生产级 ASGI API 服务，并把 FastAPI 能力连接到 Pydantic、Starlette、asyncio 和数据访问边界。

核心 Module：

```text
Pydantic validation / serialization / schema
Routing 与 request data
Dependency Injection
Exception / Middleware / Lifespan
Sync / Async endpoint boundary
OpenAPI
Authentication integration
WebSocket / SSE
Background task boundary
Testing / Contract
Configuration / Secrets
Deployment / Worker model
```

能力证明：交付具备数据库、认证、配置、测试、可观测和错误模型的 API 服务；能够解释何时不该在 endpoint 中直接做阻塞或长任务。

## 19. Stage 17 — Django, DRF, Flask & Framework Selection

**目标**：理解不同 Web 框架的抽象边界、生态优势和适用场景，而不是把三套 API 都背一遍。

核心 Module：

```text
Django project/app/model/admin/template
Django ORM 与 transaction
DRF serializer/viewset/permission
Flask application/context/extension
Convention vs flexibility
Monolith / API / Admin / content system
Migration、team fit 与 ecosystem
Framework selection case studies
```

能力证明：使用合适框架完成一个小型系统，并基于约束比较 FastAPI、Django/DRF 和 Flask，而非给出绝对排名。

## 20. Stage 18 — Redis & Distributed State

**目标**：掌握缓存和分布式状态的正确边界，并能诊断一致性、热点和失效问题。

核心 Module：

```text
Redis data structures
TTL / eviction / persistence
Cache-aside / write-through 等模式
Cache penetration / breakdown / avalanche
Hot Key / Big Key
Consistency 与 invalidation
Distributed Lock 边界
Rate limit / session / idempotency
Replication / Sentinel / Cluster
Memory 与 latency diagnosis
```

能力证明：为真实读写服务建立缓存方案，制造并修复一致性、热点和失效故障，并讨论是否值得引入 Redis。

## 21. Stage 19 — Task Systems, MQ & Event-Driven Architecture

**目标**：把同步请求外的长任务、可靠投递、消费和事件演进设计清楚。

核心 Module：

```text
Background task boundary
Celery architecture
Broker / result backend
Retry / timeout / idempotency
RabbitMQ
Kafka
Delivery semantics
Consumer group / partition / ordering
Dead-letter / compensation
Outbox / CDC
Event schema / versioning
Workflow / scheduler
```

能力证明：实现订单或工作流事件链，处理重复、乱序、失败恢复和可观测性，并比较任务队列与事件流。

## 22. Stage 20 — Search, NoSQL, Object Storage & Data Infrastructure

**目标**：根据访问模式和数据生命周期选择关系数据库之外的数据基础设施。

核心 Module：

```text
Elasticsearch / OpenSearch
Index / analyzer / relevance
MongoDB / document model
Object Storage / multipart / lifecycle
CDC
ClickHouse / OLAP
Batch / streaming infrastructure boundary
Data retention / archival
Consistency / cost / operability
```

能力证明：设计搜索、文档、对象和分析数据链路，比较多个存储方案的访问模式、成本、失败模式和迁移难度。

## 23. Stage 21 — RPC, Distributed Systems & Microservices

**目标**：理解服务拆分不是框架选择题，而是网络、数据、可靠性和团队边界的综合决策。

核心 Module：

```text
RPC / gRPC / Protobuf
API compatibility
Service discovery / configuration
Load balancing
Timeout / retry / circuit breaker / bulkhead
Consistency / CAP / consensus 入口
Distributed transaction / Saga / Outbox
Distributed lock / ID
Microservice boundary
Monolith vs modular monolith vs microservices
Kubernetes service communication
```

能力证明：从模块化单体演进或拒绝演进到微服务，完成约束分析、Failure Mode、接口契约和迁移计划。

## 24. Stage 22 — Security, Identity & Multi-Tenancy

**目标**：建立从密码学基础到应用认证授权、Secrets、租户隔离和安全运营的完整责任链。

核心 Module：

```text
Hash / MAC / Encryption / Signature
TLS / Certificate
Password storage
Session / Cookie / CSRF
JWT
OAuth2 / OIDC
RBAC / ABAC
API security
Secrets / key rotation
Dependency and supply-chain security
Tenant identity / data isolation
Audit / threat modeling
```

能力证明：为 SaaS API 设计认证授权与租户隔离，完成威胁模型、密钥管理、审计和负面测试。

## 25. Stage 23 — Observability, Reliability & SRE

**目标**：让系统状态可观察、故障可定位、容量可判断、可靠性可治理。

核心 Module：

```text
Structured Logging
Metrics
Tracing
OpenTelemetry
Prometheus / dashboard / alert
Profiling
SLI / SLO / Error Budget
Capacity / load / stress / soak test
Rate limit / degradation / recovery
Incident response / postmortem
Chaos / resilience experiment
Cost-aware reliability
```

能力证明：为现有服务建立可观测体系，使用证据定位一次跨服务故障，定义 SLO、告警和容量计划，并完成复盘。

## 26. Stage 24 — CI/CD, Containers, Kubernetes & Cloud Native

**目标**：把 Python 系统可靠地构建、测试、发布、部署、升级和回滚。

核心 Module：

```text
GitHub Actions / CI pipeline
Artifact / image / provenance
Docker image 与 runtime
Configuration / secret injection
Kubernetes workload / service / ingress
Probe / resource / autoscaling
Job / CronJob
Helm / Kustomize
GitOps
Progressive delivery / rollback
Supply-chain / SBOM
Production operations
```

能力证明：把服务部署到 Kubernetes，具备自动测试、镜像构建、配置、安全、观测、灰度和回滚证据。

## 27. Stage 25 — Data Analysis & Data Engineering

**目标**：从本地分析走向可重复、可扩展、可调度的数据处理系统。

核心 Module：

```text
NumPy
Pandas / Polars
PyArrow
DuckDB
Jupyter 与 reproducibility
Data quality / schema
ETL / ELT
PySpark
Airflow / Dagster
Batch / Stream processing
Partition / format / lineage
Warehouse / Lake / Lakehouse 基础
```

能力证明：从原始数据完成清洗、分析、质量检查和可调度 Pipeline，并比较单机、列式和分布式方案。

## 28. Stage 26 — Machine Learning, Deep Learning & Model Serving

**目标**：理解从特征、训练、评估到推理服务和模型运营的完整工程链路。

核心 Module：

```text
scikit-learn
Feature / leakage / split
Metric 与 experiment
PyTorch
Hugging Face
Training / checkpoint
Inference optimization
Batch / online serving
Model registry / versioning
Monitoring / drift
GPU / resource / cost basics
```

能力证明：训练并部署一个可版本化、可评估、可观测的模型服务，区分模型效果问题和系统性能问题。

## 29. Stage 27 — LLM, RAG, Agent, MCP & AI Platform

**目标**：构建可评估、可治理、可扩展的现代 AI 应用和内部 AI 平台。

核心 Module：

```text
LLM API / token / context / streaming
Prompt / structured output
Embedding / Vector DB
RAG ingestion / retrieval / rerank
Tool calling
Agent loop / planning / memory boundary
MCP
Workflow vs autonomous agent
Evaluation / dataset / regression
Guardrail / security / prompt injection
Model gateway / provider abstraction
Tracing / cost / latency
Multi-tenant AI platform
```

能力证明：交付 RAG/Agent 应用及平台能力，具备离线评估、在线观测、成本治理、安全边界和模型替换能力。

## 30. Stage 28 — Production Architecture & Graduation Project

**目标**：综合前面能力，从需求、约束、容量、可靠性、安全、交付和演进角度完成生产级系统。

核心 Module：

```text
Requirement / constraint / quality attribute
Architecture decomposition
Data model / API / event design
Capacity and cost model
Consistency / failure / recovery
Security / compliance
Observability / SLO
Deployment / migration / rollback
ADR / C4 / runbook / postmortem
Team boundary / governance
Legacy modernization
Build vs buy
Architecture review
```

毕业项目不要求堆齐全部组件。必须先给出约束，再证明每个重要技术选择的必要性。

可选方向：

```text
生产级 SaaS / 多租户平台
高可靠异步任务与数据平台
AI Agent / RAG 内部平台
数据处理与模型服务平台
模块化单体到分布式系统的演进案例
```

最终验收包括：实现、测试、性能证据、故障演练、安全审查、部署回滚、架构文档和条件变化后的重新决策。

## 31. 贯穿关系

课程不会强迫所有 Stage 修改同一个万能项目。使用三种互补载体：

```text
Architecture Spine
→ 适合连续业务与架构演进的阶段

Focused Lab
→ 适合严格隔离语言、运行时、故障和性能机制

Stage / Module Project
→ 适合阶段能力组合与验收
```

是否让长期平台继续演进，由当前知识与已有系统是否存在真实因果关系决定。连续性不能牺牲清晰度，独立性也不能成为复制脚手架的理由。
