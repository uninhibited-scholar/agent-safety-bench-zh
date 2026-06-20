# agent-safety-bench-zh

中文 · Agent 工具调用风险 / 提示注入 评测基准（防御导向，可机器评分）。

[![CI](https://github.com/uninhibited-scholar/agent-safety-bench-zh/actions/workflows/validate.yml/badge.svg)](https://github.com/uninhibited-scholar/agent-safety-bench-zh/actions/workflows/validate.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/license-CC%20BY%204.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)

评测一个 LLM / 安全护栏能否正确识别 agent 拟执行动作中的**危险操作**与**被注入的恶意指令**，并给出 `allow / block` 决策与风险分级。立场：**纯防御 / 安全教育 / 评测研究**。

## 数据
- `data/bench.jsonl`，当前 **v0.2 种子集 105 条**（目标扩至 500+，见 [PLAN.md](PLAN.md)）。
- 三类：`benign`(应 allow) / `prompt_injection`(应 block) / `destructive`(应 block)，配比约 38/31/31，含 easy/medium/hard。
- 字段：`id, category, difficulty, context, action, gold{decision,risk}, rationale, tags`。详见 [docs/taxonomy.md](docs/taxonomy.md)。

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
  "n_scored": 105,
  "missing_predictions": 0,
  "block_precision": 0.926,
  "block_recall": 0.379,
  "block_f1": 0.538,
  "injection_recall": 0.25,
  "over_refusal_rate": 0.051,
  "risk_exact_acc": 0.852,
  "risk_within1_acc": 0.926
}
```

**看点**：规则护栏对显式危险命令很准（block precision ~0.95），但**注入召回仅 ~0.43**——即超过一半的注入因为"动作本身看着像正常工具调用"而漏判。这正是本基准要暴露的问题：**语义注入防不住,不能只靠命令规则。**

## 质量保证
`scripts/check_bench.py` + CI 每次提交校验：合法 JSON、严格 schema、约束一致（benign↔allow / 其余↔block）、无重复、配比在区间、纯净度（禁国家归因/APT/地缘）。**禁止靠删样本或改标签骗过校验。**

## 诚实说明
v0 种子样本为人工编写的防御导向评测用例，**点到为止、不含可直接运行的完整攻击链**；扩量与多模型基线见 [PLAN.md](PLAN.md)。Prior-art 对比见 [docs/prior-art.md](docs/prior-art.md)（待联网复核）。

## 相关
[precheck-guardian](https://github.com/uninhibited-scholar/precheck-guardian)（规则基线来源）· [cybersec-qa-dataset-zh](https://github.com/uninhibited-scholar/cybersec-qa-dataset-zh)
