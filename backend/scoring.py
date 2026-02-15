"""计分引擎：权重映射、总分计算、象限判定、诊断话术"""

from questions import get_age_scores, get_option_scores

# 权重 -> 乘数映射
WEIGHT_MULTIPLIER = {
    5: 2.0,
    4: 1.75,
    3: 1.5,
    2: 1.25,
    1: 1.0,
}

# 25 题，每题 base 1-5，multiplier 1.0-2.0
# 中立基准 = 25题 × base3 × multiplier1.5 = 112.5
THRESHOLD = 112.5

DIAGNOSIS = {
    "us_high_cn_low": (
        "顺水推舟型 / 坚定留美派",
        "客观条件显示，无论是职场天花板、生活方式还是家庭羁绊，美国目前都能为你提供更高的情绪价值和经济回报。"
        "你的核心任务不是纠结去留，而是全力以赴解决签证/绿卡等硬性基建问题，扎根北美。",
    ),
    "us_low_cn_high": (
        "满级归乡型 / 果断回国派",
        "你属于典型的「回国更香」体质。无论是因为国内有现成的核心资产继承，还是你的专业在国内上限更高，"
        "抑或是你对中文文娱生态的刚需，都将你强力拉回国内。美国对你更像镀金副本，带上经历，回国开启主线任务吧。",
    ),
    "us_high_cn_high": (
        "跨国撕裂型 / 幸福的烦恼",
        "你是留学生中最纠结的一群人。美国的高薪和 WLB 紧紧抓住了你的肉身，但国内的家庭责任或丰富生活又在拉扯灵魂。"
        "由于两边筹码都很重，没有完美决策。建议用优势方的绝对资源（如强势美元）强行弥补另一方亏欠（如高频次探亲），接受双栖动态平衡。",
    ),
    "us_low_cn_low": (
        "双输陷阱 / 破局重组派",
        "客观数据显示你陷入了「两头不到岸」的窘境：在美面临身份失效或天花板危机，回国同样面临零人脉、高内卷的地狱开局。"
        "当下的你首先要停止无意义的对比内耗，挑选两边中「下限更高」的一端苟住发育，重新积累硬核筹码。",
    ),
}


def calculate_scores(age: int, age_weight: int, answers: list[dict]) -> dict:
    """
    计算 US / CN 总分并判定象限。

    参数:
        age: 用户年龄 (20-35)
        age_weight: 年龄题的权重 (1-5)
        answers: [{"question_id": int, "selected_option": str, "weight": int}, ...]

    返回:
        {
            "us_total_score": float,
            "cn_total_score": float,
            "quadrant": str,
            "quadrant_label": str,
            "diagnosis": str,
            "threshold": float,
        }
    """
    us_total = 0.0
    cn_total = 0.0

    # 年龄题计分
    us_base, cn_base = get_age_scores(age)
    multiplier = WEIGHT_MULTIPLIER[age_weight]
    us_total += us_base * multiplier
    cn_total += cn_base * multiplier

    # 24 道选择题计分
    for ans in answers:
        qid = ans["question_id"]
        option = ans["selected_option"]
        weight = ans["weight"]

        us_base, cn_base = get_option_scores(qid, option)
        multiplier = WEIGHT_MULTIPLIER[weight]
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
