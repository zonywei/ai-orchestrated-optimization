# AI-Orchestrated Optimization

> AI + 运筹优化：面向下一代决策自动化的开源框架。
>
> AI + Operations Research for the next generation of decision automation.

## 中文简介

AI-Orchestrated Optimization 是一个全新的 AI + 运筹优化框架方向，目标是把大语言模型的语义理解、规则抽取、方案诊断能力，与运筹优化的可行性、最优性、约束推理能力结合起来。

它不是一个垂直业务系统，也不是把私有求解器或行业规则库直接开源。这个仓库只发布通用、脱敏、可运行的框架骨架：智能体如何接收业务目标，如何把人类语言转换成规则、变量、约束、目标函数，如何在求解前做可追溯校验，如何把结果和不可行原因反馈给人。

如果说过去很多 AI 应用停留在“给建议”，那么 AI + 运筹优化的潜力在于：把建议变成可以执行、可以审计、可以迭代的决策系统。

## 为什么值得关注

组织真正稀缺的通常不是数据，而是把复杂政策、偏好、例外、成本和资源冲突转化为可执行决策的能力。AI 可以理解上下文和业务语言，运筹优化可以处理约束、搜索解空间并给出可验证的权衡。

这个组合可能成为未来运营管理的新范式，尤其适用于：

- **排班与人力配置：** 平衡覆盖率、公平性、疲劳、合规、技能结构和人工成本；
- **制造业调度：** 协调设备、工单、物料、换型、瓶颈、交付承诺和产能利用；
- **物流优化：** 处理路径、装载、时间窗、车辆容量、节点分拨和异常响应；
- **库存与产能规划：** 在需求波动和产能冲突下决定生产、储备、调拨和补货；
- **降本增效：** 量化约束代价，暴露隐藏浪费，在不失控的前提下寻找更优权衡；
- **韧性运营：** 当现实变化时快速重算，而不是依赖人工反复协调。

长期看，企业的日常运营可能从“人工协商 + 表格流转”升级为“人定义规则，AI 组织模型，优化引擎搜索方案，诊断结果反哺规则”的闭环系统。

## 核心思路

这个框架采用 rule-first 的流程：

```text
业务目标
  -> AI 智能体交接
  -> 规则目录
  -> 决策变量
  -> 约束
  -> 目标函数
  -> 校验门
  -> 求解执行
  -> 诊断与下一步
```

规则是一等公民。硬规则定义可行性，软规则定义偏好、惩罚和权衡。每个变量、约束和目标项都应该能追溯到产生它的业务规则。

这条可追溯链路，是黑盒模型和可信运营系统之间的关键区别。

## 智能体框架

默认智能体链路如下：

```text
Business Expert
  -> Chief Architect Agent
    -> Mathematical Modeling Agent
    -> Reduction and Optimization Agent
      -> Code Execution Agent
        -> Diagnostics Agent
```

各角色的职责分别是：澄清业务意图，区分硬规则和软偏好，设计建模结构，缩小搜索空间，执行优化流程，并用业务语言解释结果、不可行原因和下一步动作。

## 这个仓库包含什么

- 面向公开示例的 typed contracts：brief、rule、variable、constraint、objective、plan、report；
- 通用 AI OR 智能体拓扑；
- rule-first 规划器；
- 用于规则追溯和变量引用检查的 contract validation；
- 一个很小的穷举 demo optimizer；
- 与私有垂直应用无关的通用示例；
- release-boundary 检查，防止私有实现材料进入公开仓库。

## 这个仓库不包含什么

本仓库不发布私有垂直应用、客户数据、生产级建模代码、专有求解器内部逻辑、业务专属规则库、历史输出、日志、压缩包或表格数据。

公开目标是展示 AI + 运筹优化框架方向和最小可运行表面。生产级垂直系统应保留在单独的私有仓库，除非经过明确清理并决定公开发布。

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe examples\assignment_demo.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\check_release_boundary.py
```

预期 demo 输出：

```text
status=optimal
objective=9
assignments={'alpha': 'north', 'beta': 'south', 'gamma': 'east'}
```

## English Overview

Most organizations already have enough data to make better operational decisions. What they often lack is the translation layer between human policy and mathematical action: the messy rules, preferences, tradeoffs, and exceptions that live in meetings, spreadsheets, messages, and expert intuition.

AI-Orchestrated Optimization is an open framework direction for that missing layer. It treats AI agents as the front end of operations research: agents clarify intent, turn business language into rule-first optimization artifacts, run transparent model plans, and hand diagnostics back to humans. The result is not just "AI suggestions"; it is auditable decision automation.

## Why This Matters

The next wave of productivity will not come only from writing text faster or generating code snippets. It will come from changing how organizations allocate scarce resources.

AI plus operations research can become a new operating paradigm for:

- **workforce rostering:** balance coverage, fairness, fatigue, compliance, skill mix, and labor cost;
- **manufacturing dispatch:** coordinate machines, jobs, materials, changeovers, throughput, and delivery promises;
- **logistics optimization:** assign routes, loads, time windows, hubs, fleets, and disruption responses;
- **inventory and capacity planning:** decide what to produce, reserve, move, or replenish under uncertainty;
- **cost reduction:** expose the hidden price of constraints and find better tradeoffs without losing control;
- **resilience:** re-optimize quickly when reality changes.

Large language models are strong at understanding context, goals, and exceptions. Operations research is strong at feasibility, optimality, and tradeoff discipline. Put together, they can turn operational decision-making from a manual negotiation process into a repeatable, inspectable, continuously improving system.

## Core Idea

This framework is built around a rule-first flow:

```text
Business pain point
  -> AI agent handoff
  -> Rule catalog
  -> Decision variables
  -> Constraints
  -> Objective
  -> Validation gate
  -> Solver run
  -> Diagnostics and next action
```

Rules are first-class citizens. A hard rule defines feasibility. A soft rule defines a preference, penalty, or tradeoff. Every variable, constraint, and objective term can point back to the business rule that created it.

That trace is the difference between a black-box model and an operational system a team can trust.

## Agent Workflow

```text
Business Expert
  -> Chief Architect Agent
    -> Mathematical Modeling Agent
    -> Reduction and Optimization Agent
      -> Code Execution Agent
        -> Diagnostics Agent
```

Each agent has a distinct responsibility:

- clarify business intent;
- separate hard rules from soft preferences;
- design model structure;
- reduce search space;
- execute the optimization workflow;
- explain outcomes, infeasibility, and tradeoffs.

## What Is Included

This public repository contains a small, clean framework surface:

- typed contracts for briefs, rules, variables, constraints, objectives, plans, and reports;
- a canonical AI OR agent topology;
- a rule-first planner;
- contract validation for rule traceability and variable references;
- a tiny exhaustive demo optimizer for public examples;
- generic examples that do not depend on any private vertical application;
- release-boundary checks to keep private implementation material out.

## What Is Not Included

This repository does not publish private vertical applications, customer data, proprietary solver internals, production model-building code, historical outputs, or business-specific rule libraries.

The public goal is to share the AI + OR framework direction and a runnable minimal surface. Production-grade vertical systems should live in separate private repositories unless they are intentionally cleaned and released.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe examples\assignment_demo.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\check_release_boundary.py
```

Expected demo output:

```text
status=optimal
objective=9
assignments={'alpha': 'north', 'beta': 'south', 'gamma': 'east'}
```

## Public Repository Layout

```text
src/ai_or_optimization/
  agents.py       # AI OR role topology and handoff map
  contracts.py    # public optimization artifact contracts
  planner.py      # rule-first ordering
  validation.py   # contract-level traceability checks
  demo_solver.py  # small public exhaustive optimizer
examples/
  assignment_demo.py
  resource_allocation_brief.json
docs/
  architecture.md
  use_cases.md
  public_boundary.md
scripts/
  check_release_boundary.py
tests/
  test_public_framework.py
```

## Status

This is an early public framework seed. It is intentionally small, auditable, and domain-neutral. The immediate goal is to establish the vocabulary and release boundary for AI-assisted optimization systems before adding heavier solver integrations.

## License

Apache License 2.0.
