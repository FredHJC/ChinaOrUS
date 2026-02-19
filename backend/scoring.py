"""V2 计分引擎：权重映射、总分计算、象限判定、诊断话术"""

from questions import get_dual_scores, get_option_scores

# 权重 -> 乘数映射 (V2)
WEIGHT_MULTIPLIER = {
    1: 1.0,    # 不在乎
    2: 1.25,   # 不太看重
    3: 1.5,    # 一般
    4: 1.75,   # 比较看重
    5: 2.0,    # 核心诉求
}

# 29 题，每题 base 3（中立），multiplier 1.5（默认权重3）
# 中立基准 = 29 × 3 × 1.5 = 130.5
THRESHOLD = 130.5

DIAGNOSIS = {
    "us_high_cn_low": (
        "顺水推舟型 / 坚定留美派",
        "从当前各项指标来看，美国在职业发展、生活方式和个人自由度等方面都更契合你的现状。"
        "接下来可以把重心放在签证/绿卡等长期身份规划上，稳步推进在北美的扎根计划。",
    ),
    "us_low_cn_high": (
        "满级归乡型 / 果断回国派",
        "综合来看，国内的资源禀赋、行业机会或生活偏好与你的需求更加匹配。"
        "海外的学习和工作经历是宝贵的积累，带着这份国际视野回国发展，往往能打开独特的机会窗口。",
    ),
    "us_high_cn_high": (
        "跨国撕裂型 / 幸福的烦恼",
        "你在两边都有较强的吸引力因素——美国的职业环境和生活品质让你留恋，国内的家庭纽带和社会资源同样有很强的拉力。"
        "这其实说明你拥有不错的双边资源。建议在保持优势方的同时，通过灵活安排（如高频探亲、远程协作）来平衡另一方的需求。",
    ),
    "us_low_cn_low": (
        "两难探索型 / 蓄势待发派",
        "目前的测试结果显示，你在两边都还处于资源积累的早期阶段，尚未形成明显的单边优势。"
        "这并不意味着没有出路，而是说明你正处在一个关键的探索期。建议先聚焦于自身最核心的竞争力（如专业技能、行业经验），"
        "在其中一方建立起稳固的基础，再从容地做出长期规划。",
    ),
}


def calculate_scores(
    dual_answers: list[dict],
    single_answers: list[dict],
) -> dict:
    """
    计算 US / CN 总分并判定象限。

    参数:
        dual_answers: [{"question_id": int, "us_tier": int, "cn_tier": int, "weight": int}]
        single_answers: [{"question_id": int, "selected_option": str, "weight": int}]
    """
    us_total = 0.0
    cn_total = 0.0

    # 双轴题计分
    for ans in dual_answers:
        us_base, cn_base = get_dual_scores(ans["question_id"], ans["us_tier"], ans["cn_tier"])
        multiplier = WEIGHT_MULTIPLIER[ans["weight"]]
        us_total += us_base * multiplier
        cn_total += cn_base * multiplier

    # 单选题计分
    for ans in single_answers:
        us_base, cn_base = get_option_scores(ans["question_id"], ans["selected_option"])
        multiplier = WEIGHT_MULTIPLIER[ans["weight"]]
        us_total += us_base * multiplier
        cn_total += cn_base * multiplier

    # 象限判定
    if us_total >= THRESHOLD and cn_total < THRESHOLD:
        quadrant = "us_high_cn_low"
    elif us_total < THRESHOLD and cn_total >= THRESHOLD:
        quadrant = "us_low_cn_high"
    elif us_total >= THRESHOLD and cn_total >= THRESHOLD:
        quadrant = "us_high_cn_high"
    else:
        quadrant = "us_low_cn_low"

    quadrant_label, diagnosis = DIAGNOSIS[quadrant]

    return {
        "us_total_score": round(us_total, 2),
        "cn_total_score": round(cn_total, 2),
        "quadrant": quadrant,
        "quadrant_label": quadrant_label,
        "diagnosis": diagnosis,
        "threshold": THRESHOLD,
    }
