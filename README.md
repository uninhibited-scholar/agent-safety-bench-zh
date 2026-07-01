# agent-safety-bench-zh

中文 · Agent 工具调用风险 / 提示注入 评测基准（防御导向，可机器评分）。

[![CI](https://github.com/uninhibited-scholar/agent-safety-bench-zh/actions/workflows/validate.yml/badge.svg)](https://github.com/uninhibited-scholar/agent-safety-bench-zh/actions/workflows/validate.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/license-CC%20BY%204.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)

评测一个 LLM / 安全护栏能否正确识别 agent 拟执行动作中的**危险操作**与**被注入的恶意指令**，并给出 `allow / block` 决策与风险分级。立场：**纯防御 / 安全教育 / 评测研究**。

## 为什么需要它

Agent 安全是 2026 的前沿，但公开评测**几乎全是英文**（InjecAgent、ToolEmu、AgentDyn…）；中文侧的安全基准（SuperCLUE-Safety、CHiSafetyBench、Flames）评的是**通用有害性/价值对齐**，不评"**这个工具调用该不该被拦、这条轨迹是不是被注入了**"。本基准填的就是这个交叉点：**中文 · 防御网安语境 · agent 工具调用风险与注入 · 可机器评分**（详见 [docs/prior-art.md](docs/prior-art.md)）。

它不只是数据，还提出并**用数字证明了一个观点**：把一套常见命令规则当护栏跑本基准，对显式危险命令尚可（block precision ~0.86），但**注入召回只有 ~0.26**——大量注入因"动作本身看着像正常工具调用"而漏判。**只靠命令规则防不住语义注入**——这正是需要专门评测的理由。

> 现状诚实定位：**v1.0、500 条、单人编写、规则基线**——一个**能跑通、有论点、可复现**的基准（达 PLAN 验收规模）；多模型基线与真实样本掺入见 [PLAN.md](PLAN.md)。


## 数据
- `data/bench.jsonl`，共 **500 条**（达 PLAN 验收线）。
- 三类：`benign`(应 allow) / `prompt_injection`(应 block) / `destructive`(应 block)，配比约 41/31/28（均在配比区间内），每类均含 easy/medium/hard 三档。
- 注入覆盖 20+ 载体（web/email/sms/csv/wiki/api 文档/表单/通知/工单/markdown/日历/电子书等）；破坏覆盖误删根/boot wipe/无 WHERE 的 SQL/未校验变量/危险通配等。
- 字段：`id, category, difficulty, context, action{type,tool,args}, gold{decision,risk}, rationale, tags`。详见 [docs/taxonomy.md](docs/taxonomy.md)。

## 评测方法
让被测模型/护栏对每条样本输出 `{id, decision, risk}`，然后：
```bash
python3 scripts/score.py your_predictions.jsonl
```
指标：block 的 precision/recall/F1、**注入子集召回**、过度拒绝率、风险分级准确率。

## 规则护栏基线（precheck-guardian 风格）
把一套危险命令规则当护栏跑全基准（`baselines/rules_baseline.py`），结果：

```json
{
  "n_scored": 500,
  "missing_predictions": 0,
  "block_precision": 0.856,
  "block_recall": 0.342,
  "block_f1": 0.489,
  "injection_recall": 0.261,
  "over_refusal_rate": 0.083,
  "risk_exact_acc": 0.712,
  "risk_within1_acc": 0.873
}
```

**看点**：规则护栏对显式危险命令尚可（block precision ~0.86），但**注入召回仅 ~0.26**——即近四分之三的注入因为"动作本身看着像正常工具调用"而漏判。这正是本基准要暴露的问题：**语义注入防不住,不能只靠命令规则。**

## 跑真实模型（排行榜）
```bash
export OPENAI_API_KEY=sk-...     # 任意 OpenAI 兼容端点
python3 scripts/run_model.py --model <模型名> [--base-url <端点>]
python3 scripts/score.py predictions_<模型名>.jsonl
```

| 模型 | block F1 | injection recall | over-refusal | 备注 |
|---|---:|---:|---:|---|
| rules baseline | 0.489 | 0.261 | 0.083 | 命令规则，作下限 |
| doubao-1.5-pro-32k | 0.742 | 1.0 | 1.0 | 火山引擎；全拦策略，不可用 |
| glm-4-plus | 0.954 | 0.856 | 0.010 | 智谱，2024 |

**看点**：三种防线泾渭分明——规则护栏**漏判 74% 注入**（recall 0.261）；doubao 走向另一个极端**全部拦截**（over-refusal 1.0，不可用）；GLM-4-plus **精准拦截**（injection recall 0.856，同时 over-refusal 仅 1%）。**规则防不住、弱模型乱拦、强模型才能兼顾安全与可用**——这正是本基准的价值。

## 质量保证
`scripts/check_bench.py` + CI 每次提交校验：合法 JSON、严格 schema、约束一致（benign↔allow / 其余↔block）、无重复、配比在区间、纯净度（禁国家归因/APT/地缘）。**禁止靠删样本或改标签骗过校验。**

## 诚实说明
v1.0 样本为人工编写的防御导向评测用例，**点到为止、不含可直接运行的完整攻击链**；多模型基线与真实样本掺入见 [PLAN.md](PLAN.md)。Prior-art 对比见 [docs/prior-art.md](docs/prior-art.md)（待联网复核）。

## 相关
[precheck-guardian](https://github.com/uninhibited-scholar/precheck-guardian)（规则基线来源）· [cybersec-qa-dataset-zh](https://github.com/uninhibited-scholar/cybersec-qa-dataset-zh)
