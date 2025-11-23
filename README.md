# -MBTI-
🎭 MBTI Multi-Agent Interview Simulator
多人格智能体模拟面试系统（DeepSeek AI 驱动）

本项目基于 DeepSeek API + 多智能体系统（Multi-Agent） 构建，
模拟 多个不同 MBTI 性格的 AI 面试官 对用户进行面试。

用户可以选择自己要面试的岗位（如：产品经理 / 数据分析师 / UI 设计师）。
系统会根据岗位 + 不同人格面试官风格 动态生成真实面试问题，
并在多个环节对用户进行评估。

这是一个结合 人格心理学、AI Agent、面试模拟、职业探索 的互动式项目。

📌 功能特性（Features）

🔹 1. 多 MBTI 面试官

项目内置五位面试官，每位都有不同 MBTI 性格：

面试官	MBTI	面试风格
ENTJ	总指挥型	目标导向、决策果断、压力面深度问答
INTP	分析型	逻辑推理、因果拆解、结构化追问
ENFP	创意型	动机探索、价值观、故事化表达
ISTJ	稳定型	流程规范、细节验证、执行导向
INFJ	洞察型	情绪理解、关系洞察、人际敏感度

每位考官的提问、追问、点评都带有自己鲜明的人格风格。

🔹 2. 基于用户选择的“职业岗位”动态出题

用户进入后首先会被问到：

“你正在参加什么岗位的面试？”

然后所有智能体的提问都会围绕该岗位自动生成，例如：

数据分析师 → 数据验证、假设框架、模型构建、业务洞察

产品经理 → 用户体验、需求拆解、冲突协调、价值判断

UI 设计师 → 需求理解、审美判断、协作流程、反馈收集

让每场面试都高度个性化。

🔹 3. 强主题区分（避免面试官提问重复）

每位面试官拥有自己的 专属提问主题范围（Method 2），确保问题完全不重复。

示例：

ENTJ → 决策 / 效率 / 冲突

INTP → 假设 / 模型 / 推理

ENFP → 价值观 / 故事 / 动机

ISTJ → 流程 / 风险控制 / 细节

INFJ → 情绪 / 团队 / 沟通

每位面试官的问题都独具特色、不会撞车。

🔹 4. 多环节模拟专业面试流程

整个模拟包括六大环节：

岗位选择（新增）

MBTI 面试官介绍

快速轮问（Rapid Fire）

深度追问（Follow-up Pressure）

情境题（Scenario Simulation）

多面试官职业分析（Evaluation）

最终总结（Reflection）

整个体验非常像真实职场面试。

🔧 技术栈（Tech Stack）

Python 3.9+

DeepSeek API（OpenAI-style Chat API）

多智能体系统（Multi-Agent）

动态 Prompt 结构

自定义 MBTI 行为建模

🗂 项目结构（Project Structure）
.
├── multi-agent.py           # 主程序（你已上传）
├── README.md                # 项目说明文件
└── requirements.txt         # 依赖（可选）

▶️ 运行方法（Run Locally）
1. 安装依赖
pip install openai

2. 设置 DeepSeek API Key

你可以使用两种方式：

方式 A：在代码顶部设置
os.environ["DEEPSEEK_API_KEY"] = "your-api-key"

方式 B：设置为环境变量
export DEEPSEEK_API_KEY="yourkey"

3. 运行程序
python multi-agent.py


系统会自动进入：

岗位选择

多面试官面试

情境题

最终评估

💡 示例输出（Demo）
====== MBTI Multi-Agent Interview（职业定制版）======

你正在参加什么职业的面试？
> 数据分析师

===== 面试官介绍 =====
- ENTJ：目标导向，直击核心
- INTP：逻辑严谨，结构清晰
- ENFP：听你讲故事，看你的热情
...

===== 快速轮问 =====
ENTJ：如果数据结果与业务相反，你会如何处理？
你：我会先做数据源验证...

===== 深度追问 =====
INFJ：如果业务直觉与你的数据冲突，你会怎么理解？

===== 情境题 =====
ENTJ：团队质疑你的数据结果，你怎么解释？

===== 综合评价 =====
INTP：逻辑性：7/10，业务洞察力：6/10...

===== 最终总结 =====
你在哪些方面表现最佳？
你会如何改进？

🌱 Roadmap（未来计划）

 Web UI（Streamlit 或 Next.js front-end）

 多候选人竞争模式（你 vs AI 同事）

 添加“岗位题库模块”（PM/DA/Design/SWE 等）

 自动生成面试报告 PDF

 支持多轮面试（HR → 技术 → Leader）

 MBTI 互评系统（面试官之间争吵/讨论）

如果你需要，我也可以帮你把这些功能加入。

🤝 Contributing

欢迎提交 PR 或 Issue，一起扩展这个项目！
