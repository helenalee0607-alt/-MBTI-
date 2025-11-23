"""
MBTI Multi-Agent Interview Simulator (DeepSeek Version)
已加入方法二：每个 MBTI 面试官拥有独立提问主题，避免重复。
"""

import os
os.environ["DEEPSEEK_API_KEY"] = "sk-103e0da6c202412ea738eeb15b348d53hon"   # ←⚠ 请填入你的 key

from dataclasses import dataclass
from typing import List, Dict
from openai import OpenAI

# ========== 0. DeepSeek 配置 ==========
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    raise RuntimeError("请在代码顶部填入你的 DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)

MODEL = "deepseek-chat"


# ========== 1. 数据结构 ==========

@dataclass
class QARecord:
    stage: str
    interviewer: str
    question: str
    answer: str


# ========== 2. 面试官提问主题（方法二核心新增） ==========

TOPIC_SCOPE = {
    "ENTJ": "目标推进、执行效率、困难决策、资源分配、冲突管理、驱动结果",
    "INTP": "假设构建、因果推理、变量控制、模型框架、逻辑一致性、实验设计",
    "ENFP": "动机、价值观、愿景、团队文化、创造性表达、故事化沟通",
    "ISTJ": "流程规范、细节准确性、稳定性、风险控制、数据验证、可执行步骤",
    "INFJ": "人际关系、沟通策略、团队氛围、冲突洞察、情绪理解、组织协作",
}


# ========== 3. 基础 Agent ==========

class BaseAgent:
    def __init__(self, name: str, mbti: str, persona: str):
        self.name = name
        self.mbti = mbti
        self.persona = persona

    def chat(self, msg: str, temperature=0.6) -> str:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": self.persona},
                {"role": "user", "content": msg},
            ],
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()


# ========== 4. 面试官 Agent（已整合主题范围） ==========

class Interviewer(BaseAgent):
    def intro(self):
        return self.chat("用一句话介绍你的面试风格，不超过20字。")

    def ask_rapid(self, job):
        prompt = f"""
你是一名 {self.mbti} 面试官。
你的提问主题范围：
{TOPIC_SCOPE[self.mbti]}

任务：提出一个关于「{job}」岗位的快速问题。
要求：
- 必须来自你的主题范围
- 简短、直接、有深度
- 不超过一句话
- 不得与常见面试套话重复
只输出问题本身。
"""
        return self.chat(prompt)

    def ask_follow_up(self, prev_answer, job):
        prompt = f"""
候选人对 {job} 的回答是：{prev_answer}

作为 {self.mbti} 面试官，你的提问主题范围是：
{TOPIC_SCOPE[self.mbti]}

请基于你的主题范围提出一个“深入追问”的问题。
要求：
- 明显尖锐一点
- 明确聚焦岗位需求
- 一句话
"""
        return self.chat(prompt)

    def ask_scenario(self, job):
        prompt = f"""
设计一个「{job}」岗位的情境题，一句话长度。
必须来自你的主题范围：
{TOPIC_SCOPE[self.mbti]}

例：冲突、决策、合作、风险、情绪、框架等
"""
        return self.chat(prompt)

    def comment(self, question, answer, job):
        prompt = f"""
你是 {self.mbti} 面试官。

情境题：{question}
候选人回答：{answer}

请基于你的主题范围（{TOPIC_SCOPE[self.mbti]}）给一句评论：
- 可以夸赞、质疑、提醒
- 不超过两句话
"""
        return self.chat(prompt)

    def evaluate(self, transcript, job):
        history = ""
        for rec in transcript:
            history += f"[{rec.stage}] {rec.interviewer}：{rec.question}\n候选人：{rec.answer}\n\n"

        prompt = f"""
你是一名 {self.mbti} 面试官。
你的评价逻辑基于主题范围：
{TOPIC_SCOPE[self.mbti]}

以下是候选人应聘「{job}」的部分表现：
{history}

请给三段式正式评价：
1. 一句话总体评价（性格 + 岗位贴合度）
2. 三个维度的 10 分制评分（与岗位相关）
3. 一条改进建议（明确且可执行）
"""
        return self.chat(prompt)


# ========== 5. 面试官阵容 ==========

def build_interviewers():
    return [
        Interviewer("ENTJ 面试官", "ENTJ",
            "你是 ENTJ 面试官，决断、执行、结果导向。"),
        Interviewer("INTP 面试官", "INTP",
            "你是 INTP 面试官，逻辑强、爱推理、结构控。"),
        Interviewer("ENFP 面试官", "ENFP",
            "你是 ENFP 面试官，热情、关心动机、注重故事。"),
        Interviewer("ISTJ 面试官", "ISTJ",
            "你是 ISTJ 面试官，严谨、务实、注重稳定与流程。"),
        Interviewer("INFJ 面试官", "INFJ",
            "你是 INFJ 面试官，洞察深、善于看见人际关系与情绪。"),
    ]


# ========== 6. 面试流程 ==========

def run_interview():
    print("\n====== MBTI Multi-Agent Interview（职业定制版）======\n")

    # 0. 选择职业
    job = input("你正在参加什么职业的面试？例如：产品经理、UI设计师、数据分析师：\n> ").strip()
    print(f"\n好的，接下来所有面试问题都会围绕：「{job}」\n")

    interviewers = build_interviewers()
    transcript: List[QARecord] = []

    print("===== 环节一：面试官介绍 =====\n")
    for iv in interviewers:
        print(f"- {iv.name}（{iv.mbti}）：{iv.intro()}")
    print()

    # 2. 快速轮问
    print("===== 环节二：快速轮问 =====\n")
    for iv in interviewers:
        q = iv.ask_rapid(job)
        print(f"{iv.name}：{q}")
        ans = input("你的回答：")
        transcript.append(QARecord("rapid", iv.name, q, ans))
        print()

    # 3. 深度追问
    print("===== 环节三：深度追问 =====\n")
    base_ans = transcript[0].answer
    entj = interviewers[0]
    infj = interviewers[-1]

    q1 = entj.ask_follow_up(base_ans, job)
    print(f"{entj.name}：{q1}")
    ans = input("你的回答：")
    transcript.append(QARecord("follow_up", entj.name, q1, ans))
    print()

    q2 = infj.ask_follow_up(base_ans, job)
    print(f"{infj.name}：{q2}")
    ans2 = input("你的回答：")
    transcript.append(QARecord("follow_up", infj.name, q2, ans2))
    print()

    # 4. 情境题
    print("===== 环节四：情境题 =====\n")
    scenario_q = entj.ask_scenario(job)
    print(f"{entj.name}：{scenario_q}\n")
    s_ans = input("你的回答：")
    transcript.append(QARecord("scenario", entj.name, scenario_q, s_ans))

    print("\n—— 其他面试官即时点评 ——")
    for iv in interviewers:
        if iv is entj:
            continue
        print(f"{iv.name}：{iv.comment(scenario_q, s_ans, job)}")

    # 5. 综合评价
    print("\n===== 环节五：综合评价 =====\n")
    for iv in interviewers:
        print(f"【{iv.name} 的职业向评价】\n")
        print(iv.evaluate(transcript, job), "\n")

    # 6. 总结
    print("\n===== 最终总结 =====\n")
    print(f"你在「{job}」岗位的整体表现：")
    print("1）你最强的部分是什么？")
    print("2）哪些评价让你印象最深？")
    print("3）如果再答一次，你会如何改进？\n")
    print("面试结束 🎉 感谢参与！")


if __name__ == "__main__":
    run_interview()
