# Prior-art 对比（2026-06-20 联网复核）

经 2026-06-20 检索确认下述格局。结论：**"中文 + agent 工具调用风险/注入 + 可机器评分 + 防御网安语境"这一交叉点仍基本空白**（高置信度）。

## 英文：agent 注入 / 工具安全（已很拥挤，非本项目语言/语境）
- **InjecAgent**（arXiv:2403.02691）——工具集成 agent 的间接提示注入基准。
- **ToolEmu**（arXiv:2309.15817）——用 LM 模拟工具执行暴露 agent 风险。
- **AgentDojo / AgentHarm / AgentDyn（2026 动态开放式注入基准）/ Risky-Bench（arXiv:2602.03100，真实部署下的 agentic 风险）** 等——均英文为主。
- 2026 上半年该方向论文密集（QueryIPI、Progent 权限控制、TRUSTDESC 工具投毒防御等），说明**赛道热但全是英文**。

## 中文：安全评测（存在，但都是"通用有害性/价值对齐/越狱"，不是 agent 工具调用风险）
- **SuperCLUE-Safety / SuperCLUE-Agent**——前者多轮对抗安全、后者 agent 能力评测；二者是**分开的两个轴**，没有"agent 工具调用是否该拦截"的交叉。
- **CHiSafetyBench**（arXiv:2406.10311）——中文分层安全(5 域/31 类)，任务是"识别风险内容 + 拒答风险问题"，**不是判工具调用/注入轨迹**。
- **Flames**（arXiv:2311.06899）——中文价值对齐。
- **JAILJUDGE**（HKUST）——越狱评判。

## 本项目差异化（确认成立）
中文 · **判 agent 拟执行动作是否该 block + 风险分级** · 含**注入轨迹**(藏在工具返回/网页/邮件) · **可机器评分** · 防御网安语境 · 规则护栏可解释基线（复用 precheck-guardian）。
已知中文基准里没有同时满足这些的。**注意潜在重叠**：若 SuperCLUE 后续推出 agent-safety 子项需再比对；当前公开范围内无直接撞车。

## 来源
- https://arxiv.org/abs/2403.02691 · https://arxiv.org/pdf/2309.15817 · https://arxiv.org/pdf/2602.03100
- https://arxiv.org/abs/2406.10311 · https://arxiv.org/abs/2311.06899
- https://www.cluebenchmarks.com/superclue.html
