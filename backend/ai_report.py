"""AI 个性化分析报告：构建 prompt、调用 OpenAI、频率限制"""

import os
import time

import httpx
from sqlalchemy import func
from sqlalchemy.orm import Session as DBSession

from models import Answer
from questions import QUESTIONS
from scoring import WEIGHT_MULTIPLIER, THRESHOLD, DIAGNOSIS

# ---------- Rate limiter (in-memory) ----------

_rate_limit_store: dict[str, float] = {}
RATE_LIMIT_SECONDS = 3600  # 1 hour


def check_rate_limit(ip: str) -> bool:
    """Returns True if allowed, False if rate-limited."""
    now = time.time()
    last = _rate_limit_store.get(ip, 0)
    if now - last < RATE_LIMIT_SECONDS:
        return False
    return True


def record_rate_limit(ip: str) -> None:
    """Record that this IP has used the feature."""
    _rate_limit_store[ip] = time.time()


def get_rate_limit_remaining(ip: str) -> int:
    """Seconds remaining until the IP can make another request."""
    now = time.time()
    last = _rate_limit_store.get(ip, 0)
    remaining = RATE_LIMIT_SECONDS - (now - last)
    return max(0, int(remaining))


# ---------- Aggregate stats ----------

def get_aggregate_stats(db: DBSession) -> dict[int, dict[str, float]]:
    """Per-question option distribution: {qid: {"A": 0.42, "US:3,CN:2": 0.15, ...}}"""
    total_sessions = db.query(func.count(func.distinct(Answer.session_id))).scalar()
    if total_sessions == 0:
        return {}

    rows = (
        db.query(Answer.question_id, Answer.selected_option, func.count(Answer.id).label("cnt"))
        .group_by(Answer.question_id, Answer.selected_option)
        .all()
    )

    stats: dict[int, dict[str, float]] = {}
    for qid, opt, cnt in rows:
        if qid not in stats:
            stats[qid] = {}
        stats[qid][opt] = round(cnt / total_sessions, 4)
    return stats


# ---------- Question lookup ----------

_Q_MAP = {q["id"]: q for q in QUESTIONS}

WEIGHT_LABELS = {1: "不在乎", 2: "不太看重", 3: "一般", 4: "比较看重", 5: "核心诉求"}


# ---------- Prompt builder ----------

def build_prompt(session, user_answers: list, aggregate_stats: dict) -> tuple[str, str]:
    """Build (system_prompt, user_prompt) for OpenAI."""
    answer_map = {a.question_id: a for a in user_answers}

    question_sections = []
    for q in QUESTIONS:
        qid = q["id"]
        ans = answer_map.get(qid)
        if not ans:
            continue

        section = f"### Q{qid}: {q['title']} (分类: {q['category']})\n"
        section += f"用户权重: {ans.weight} ({WEIGHT_LABELS.get(ans.weight, '')})\n"

        if q["type"] == "dual_select":
            parts = ans.selected_option.split(",")
            us_tier = int(parts[0].split(":")[1])
            cn_tier = int(parts[1].split(":")[1])
            us_text = next((o["text"] for o in q["us_options"] if o["tier"] == us_tier), f"档{us_tier}")
            cn_text = next((o["text"] for o in q["cn_options"] if o["tier"] == cn_tier), f"档{cn_tier}")
            section += f"用户选择: 美国={us_text} (档{us_tier}), 中国={cn_text} (档{cn_tier})\n"
            us_opts_str = " | ".join(f"档{o['tier']}: {o['text']}" for o in q["us_options"])
            cn_opts_str = " | ".join(f"档{o['tier']}: {o['text']}" for o in q["cn_options"])
            section += f"美国选项: {us_opts_str}\n"
            section += f"中国选项: {cn_opts_str}\n"
        else:
            opt_label = ans.selected_option
            opt_text = next((o["text"] for o in q["options"] if o["label"] == opt_label), opt_label)
            section += f"用户选择: {opt_label}. {opt_text}\n"
            section += "所有选项: " + " | ".join(f"{o['label']}. {o['text']}" for o in q["options"]) + "\n"

        qstats = aggregate_stats.get(qid, {})
        if qstats:
            dist_parts = []
            for opt_val, pct in sorted(qstats.items(), key=lambda x: -x[1]):
                dist_parts.append(f"{opt_val}: {pct * 100:.1f}%")
            section += "全体用户选项分布: " + ", ".join(dist_parts) + "\n"

        question_sections.append(section)

    quadrant_label, _ = DIAGNOSIS[session.quadrant]
    total_sessions = sum(len(v) for v in aggregate_stats.values()) // 29 if aggregate_stats else 0
    # More accurate count from the stats
    if aggregate_stats:
        first_q_stats = aggregate_stats.get(0, {})
        total_sessions = int(round(sum(first_q_stats.values()) * 100)) if first_q_stats else 0

    system_prompt = (
        "你是一位专业的留学生职业发展与生活规划顾问。你正在为一位完成了「留学生去留决策量表 V2」的用户撰写个性化分析报告。\n\n"
        "这份量表有29道题，涵盖4大类别：基础信息、职业与财务硬件、身份与生活方式、家庭情感与社会资本。\n"
        "每道题用户会选择一个选项，并为该题设定权重（1-5，代表这个因素对其决策的重要程度）。\n\n"
        "计分规则：\n"
        "- 每题产生一个美国吸引力分(US)和中国吸引力分(CN)\n"
        "- 权重乘数: 1=不在乎(×1.0), 2=不太看重(×1.25), 3=一般(×1.5), 4=比较看重(×1.75), 5=核心诉求(×2.0)\n"
        f"- 中立基准线 = {THRESHOLD}\n"
        "- 四个象限: US高CN低=坚定留美派, US低CN高=果断回国派, 双高=跨国撕裂型, 双低=两难探索型\n\n"
        "注意：本测试面向已在美华人群体，打分机制天然偏向留美方向。请在分析中考虑这一点。"
    )

    us_delta = round(session.us_total_score - THRESHOLD, 1)
    cn_delta = round(session.cn_total_score - THRESHOLD, 1)
    us_dir = "高于" if us_delta >= 0 else "低于"
    cn_dir = "高于" if cn_delta >= 0 else "低于"

    user_prompt = (
        "以下是该用户的完整测试数据。请撰写一份简洁的中文个性化分析报告，严格控制在600-800字以内，不要超过800字。\n\n"
        f"## 用户总体结果\n"
        f"- 美国吸引力总分: {session.us_total_score} ({us_dir}基准线 {abs(us_delta)} 分)\n"
        f"- 中国吸引力总分: {session.cn_total_score} ({cn_dir}基准线 {abs(cn_delta)} 分)\n"
        f"- 基准线: {THRESHOLD}\n"
        f"- 所属象限: {quadrant_label} ({session.quadrant})\n\n"
        f"## 逐题数据（含全体用户统计）\n"
        + "\n".join(question_sections)
        + "\n\n## 分析要求\n"
        "请围绕以下几点展开分析：\n\n"
        "1. **核心关切识别**: 根据用户给出的权重（尤其是权重4-5的题目），识别该用户最在乎的决策因素是什么。\n\n"
        "2. **与群体对比**: 对比该用户的选择与全体用户的选项分布，找出用户明显偏离大众的选择（即用户选了一个只有少数人选择的选项），分析这些独特性意味着什么。\n\n"
        "3. **矛盾与张力**: 如果用户的答案中存在自相矛盾的倾向（比如职业偏好留美但情感强烈拉回国），指出这些内在张力。\n\n"
        "4. **综合建议**: 基于以上分析，给出具体、可操作的建议。避免空泛的鸡汤。\n\n"
        "## 写作风格\n"
        "- 使用亲和但专业的语气，直接称呼「你」\n"
        "- 不要重复罗列原始数据，要把数据转化为洞察\n"
        "- 不要使用markdown标题格式，用自然段落组织文章\n"
        "- 报告末尾不要加任何免责声明，系统会自动添加"
    )

    return system_prompt, user_prompt


# ---------- OpenAI caller ----------

async def call_openai(system_prompt: str, user_prompt: str) -> str:
    """Call OpenAI chat completions API and return the response text."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not configured")

    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.7,
                "max_tokens": 2000,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
