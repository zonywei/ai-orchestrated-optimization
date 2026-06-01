<p align="right">
  <a href="README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/lang-中文-red.svg"></a>
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/lang-English-blue.svg"></a>
</p>

# AI-Orchestrated Optimization

[![CI](https://github.com/zonywei/ai-orchestrated-optimization/actions/workflows/ci.yml/badge.svg)](https://github.com/zonywei/ai-orchestrated-optimization/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)

> AI + 运筹优化：面向下一代决策自动化的开源框架。

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
- 用于求解前边界检查的 constraint audit；
- 把不可行约束映射回业务规则的 infeasibility diagnostics；
- 用统一公开契约接入不同执行引擎的 solver adapter interface；
- 用于解释成本或收益来源的 objective contribution analysis；
- 基于 OR-Tools CP-SAT 的公开 synthetic workforce rostering 示例；
- 一个很小的穷举 demo optimizer；
- 与私有垂直应用无关的通用示例；
- release-boundary 检查，防止私有实现材料进入公开仓库。

## 这个仓库不包含什么

本仓库不发布私有垂直应用、客户数据、生产级建模代码、专有求解器内部逻辑、业务专属规则库、历史输出、日志、压缩包或表格数据。

公开目标是展示 AI + 运筹优化框架方向和最小可运行表面。生产级垂直系统应保留在单独的私有仓库，除非经过明确清理并决定公开发布。

## 当前能力边界

当前仓库已经能证明一个很窄但可运行的公开闭环：

- 面向业务 brief、规则、模型工件、计划和报告的 rule-first 公开契约；
- 用于规则追溯、变量引用和报告一致性的 validation gate；
- 求解前 constraint audit 和基础 infeasibility diagnostics；
- 用统一框架契约连接不同执行引擎的 solver adapter protocol；
- 面向二元和整数线性模型的 OR-Tools CP-SAT 执行能力；
- 包含 30 个二元决策变量的 synthetic workforce rostering 示例；
- 能把解的成本或收益映射回规则的 objective contribution analysis。

它仍然刻意不提供真实 LLM 编排、生产级垂直系统、私有规则库、大规模 benchmark，或自动自然语言到模型生成。

## 维护与开源项目信号

这个仓库会按一个可维护的开源项目来组织，而不是一次性代码展示：

- CI 会在 push 和 pull request 上运行测试与公开边界检查；
- Dependabot 会跟踪 Python 与 GitHub Actions 依赖更新；
- contribution、security、issue 和 pull request 模板定义维护流程；
- roadmap 区分近期技术工作与非目标；
- Codex for Open Source 申请说明记录了如何把 Codex/API credits 用在维护自动化上。

参见 [CONTRIBUTING.md](CONTRIBUTING.md)、[SECURITY.md](SECURITY.md)、[docs/roadmap.md](docs/roadmap.md) 和 [docs/codex_for_oss.md](docs/codex_for_oss.md)。

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe examples\assignment_demo.py
.\.venv\Scripts\python.exe -m pip install -e ".[cp-sat]"
.\.venv\Scripts\python.exe examples\cp_sat_workforce_demo.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\check_release_boundary.py
```

预期 demo 输出：

```text
status=optimal
objective=9
assignments={'alpha': 'north', 'beta': 'south', 'gamma': 'east'}
```

预期 CP-SAT demo 输出：

```text
status=optimal
objective=5.0
slot_1=ava
slot_2=cy
slot_3=ben
slot_4=dia
slot_5=eli
```

## 公开仓库结构

```text
src/ai_or_optimization/
  agents.py       # AI OR role topology and handoff map
  contracts.py    # public optimization artifact contracts
  planner.py      # rule-first ordering
  validation.py   # contract-level traceability checks
  audit.py        # constraint-level pre-solve audit
  diagnostics.py  # infeasibility explanation helpers
  contributions.py # objective contribution analysis
  solver_adapters.py # solver adapter protocol and public demo adapter
  cp_sat_adapter.py # OR-Tools CP-SAT adapter
  demo_solver.py  # small public exhaustive optimizer
examples/
  assignment_demo.py
  cp_sat_workforce_demo.py
  resource_allocation_brief.json
  workforce_rostering_cp_sat.json
  reports/workforce_rostering_diagnosis.md
docs/
  architecture.md
  use_cases.md
  public_boundary.md
  roadmap.md
  codex_for_oss.md
scripts/
  check_release_boundary.py
tests/
  test_public_framework.py
  test_constraint_audit.py
  test_infeasibility_diagnostics.py
  test_solver_adapters.py
  test_objective_contributions.py
  test_cp_sat_adapter.py
.github/
  workflows/ci.yml
  dependabot.yml
  ISSUE_TEMPLATE/
  pull_request_template.md
```

## 当前状态

这是一个早期公开框架种子。它刻意保持小而清晰、可审计、领域中立。当前重点是先建立 AI 辅助优化系统的公共词汇、工程边界和可验证骨架，再逐步接入更重的求解器能力。

## 开源许可

Apache License 2.0.
