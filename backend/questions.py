"""
完整题库：26 题
- 1 道年龄题（自动权重）
- 9 道职业与财务硬件（Q1-Q5 双轴5档，Q6-Q9 双轴3档）
- 9 道身份与生活方式
- 7 道家庭、情感与社会资本

双轴题(dual_select)：用户分别为"在美情况"和"在华情况"各选一个档位。
- 5档题：档位值 1-5 直接作为 base_score
- 3档题：档位值 1/2/3 映射为 base_score 1/3/5

分数信息仅后端使用，不暴露给前端。
"""

# 3档 -> 5分制映射
TIER3_TO_SCORE = {1: 1, 2: 3, 3: 5}

QUESTIONS = [
    # ===== Q0: 年龄题 (自动权重，不让用户选权重) =====
    {
        "id": 0,
        "category": "基础信息",
        "title": "你的年龄",
        "type": "age_input",
        "description": "请输入你的年龄（20岁起，可填35+）",
        "auto_weight": 3,
        "age_ranges": [
            {"min": 20, "max": 22, "scores": (1, 5)},
            {"min": 23, "max": 25, "scores": (2, 4)},
            {"min": 26, "max": 28, "scores": (3, 3)},
            {"min": 29, "max": 31, "scores": (4, 2)},
            {"min": 32, "max": 999, "scores": (5, 1)},  # 35+ 归入最高档
        ],
    },

    # ===== 大类一：职业与财务硬件 =====
    # --- Q1-Q5: 双轴5档 (中美分别选档) ---
    {
        "id": 1,
        "category": "职业与财务硬件",
        "title": "薪资水平",
        "type": "dual_select",
        "tiers": 5,
        "us_label": "你在美国的薪资/收入水平",
        "cn_label": "你回国后的薪资/收入预期",
        "us_options": [
            {"tier": 1, "text": "很低 (<$80k)"},
            {"tier": 2, "text": "偏低 ($80k-$150k)"},
            {"tier": 3, "text": "中等 ($150k-$300k)"},
            {"tier": 4, "text": "较高 ($300k-$600k)"},
            {"tier": 5, "text": "很高 ($600k+)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "很低 (<15万)"},
            {"tier": 2, "text": "偏低 (15-30万)"},
            {"tier": 3, "text": "中等 (30-60万)"},
            {"tier": 4, "text": "较高 (60-120万)"},
            {"tier": 5, "text": "很高 (120万+)"},
        ],
    },
    {
        "id": 2,
        "category": "职业与财务硬件",
        "title": "住房压力",
        "type": "dual_select",
        "tiers": 5,
        "us_label": "你在美国的住房压力",
        "cn_label": "你回国后的住房压力",
        "us_options": [
            {"tier": 1, "text": "压力极大 (房收比>45%/买不起)"},
            {"tier": 2, "text": "压力较大 (房收比35-45%)"},
            {"tier": 3, "text": "压力一般 (房收比25-35%)"},
            {"tier": 4, "text": "压力较小 (房收比15-25%)"},
            {"tier": 5, "text": "几乎无压力 (房收比<15%/已有房)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "压力极大 (一线无房无指标/地狱级房贷)"},
            {"tier": 2, "text": "压力较大 (需大额贷款)"},
            {"tier": 3, "text": "压力一般 (公积金部分覆盖)"},
            {"tier": 4, "text": "压力较小 (家里有部分支持)"},
            {"tier": 5, "text": "几乎无压力 (家里已备房/老家有房)"},
        ],
    },
    {
        "id": 3,
        "category": "职业与财务硬件",
        "title": "工作节奏与生活平衡 (WLB)",
        "type": "dual_select",
        "tiers": 5,
        "us_label": "你在美国的工作节奏",
        "cn_label": "你回国后的工作节奏预期",
        "us_options": [
            {"tier": 1, "text": "非常高压 (60h+/PIP淘汰制)"},
            {"tier": 2, "text": "较高压 (50-60h)"},
            {"tier": 3, "text": "正常 (40-50h)"},
            {"tier": 4, "text": "较轻松 (35-40h)"},
            {"tier": 5, "text": "非常轻松 (<35h/极致WLB)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "非常高压 (996/大小周/55h+)"},
            {"tier": 2, "text": "较高压 (经常加班)"},
            {"tier": 3, "text": "正常 (40-50h/偶尔加班)"},
            {"tier": 4, "text": "较轻松 (955体制内)"},
            {"tier": 5, "text": "非常轻松 (极度稳定955/弹性)"},
        ],
    },
    {
        "id": 4,
        "category": "职业与财务硬件",
        "title": "全年带薪休假 (PTO)",
        "type": "dual_select",
        "tiers": 5,
        "us_label": "你在美国的带薪假天数",
        "cn_label": "你回国后的带薪假预期",
        "us_options": [
            {"tier": 1, "text": "很少 (<5天)"},
            {"tier": 2, "text": "偏少 (5-10天)"},
            {"tier": 3, "text": "一般 (10-15天)"},
            {"tier": 4, "text": "较多 (15-20天)"},
            {"tier": 5, "text": "很多 (20天+/无限PTO)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "很少 (5天基础/请假极难)"},
            {"tier": 2, "text": "偏少 (5-10天)"},
            {"tier": 3, "text": "一般 (10-15天)"},
            {"tier": 4, "text": "较多 (15-20天)"},
            {"tier": 5, "text": "很多 (20天+/体制内)"},
        ],
    },
    {
        "id": 5,
        "category": "职业与财务硬件",
        "title": "职场寿命与年龄压力",
        "type": "dual_select",
        "tiers": 5,
        "us_label": "你在美国的职场年龄压力",
        "cn_label": "你回国后的职场年龄压力",
        "us_options": [
            {"tier": 1, "text": "压力极大 (行业有隐性年龄歧视)"},
            {"tier": 2, "text": "压力较大"},
            {"tier": 3, "text": "一般 (不明显)"},
            {"tier": 4, "text": "压力较小 (反年龄歧视法保护)"},
            {"tier": 5, "text": "几乎无压力 (越老越值钱)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "压力极大 (面临35岁裁员红线)"},
            {"tier": 2, "text": "压力较大 (行业偏好年轻人)"},
            {"tier": 3, "text": "一般 (行业不太看年龄)"},
            {"tier": 4, "text": "压力较小 (体制内/专业领域)"},
            {"tier": 5, "text": "几乎无压力 (越老越吃香)"},
        ],
    },

    # --- Q6-Q9: 双轴3档 (中美分别选档) ---
    {
        "id": 6,
        "category": "职业与财务硬件",
        "title": "裁员风险与失业缓冲",
        "type": "dual_select",
        "tiers": 3,
        "us_label": "你在美国的失业风险与缓冲",
        "cn_label": "你回国后的失业风险与缓冲",
        "us_options": [
            {"tier": 1, "text": "高风险 (签证受限，失业60天内必须离境)"},
            {"tier": 2, "text": "中等 (有一定缓冲期，但仍受身份约束)"},
            {"tier": 3, "text": "低风险 (绿卡/公民，充足失业保障)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "高风险 (行业不稳/35岁危机)"},
            {"tier": 2, "text": "中等 (普通行业波动)"},
            {"tier": 3, "text": "低风险 (体制内/铁饭碗)"},
        ],
    },
    {
        "id": 7,
        "category": "职业与财务硬件",
        "title": "副业与额外收入渠道",
        "type": "dual_select",
        "tiers": 3,
        "us_label": "你在美国做副业的可行性",
        "cn_label": "你回国后做副业的可行性",
        "us_options": [
            {"tier": 1, "text": "受限 (签证明确禁止W2外收入)"},
            {"tier": 2, "text": "一般 (身份允许但机会有限)"},
            {"tier": 3, "text": "自由 (无身份限制，副业空间大)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "受限 (行业/精力限制，难以开展)"},
            {"tier": 2, "text": "一般 (有一定空间)"},
            {"tier": 3, "text": "自由 (自媒体/电商土壤极佳)"},
        ],
    },
    {
        "id": 8,
        "category": "职业与财务硬件",
        "title": "创业环境与资源",
        "type": "dual_select",
        "tiers": 3,
        "us_label": "你在美国的创业条件",
        "cn_label": "你回国后的创业条件",
        "us_options": [
            {"tier": 1, "text": "不利 (身份壁垒大/人力成本高/无资源)"},
            {"tier": 2, "text": "一般 (有一定资源和可能性)"},
            {"tier": 3, "text": "有利 (有技术/风投/本土创业资源)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "不利 (无资源/高竞争/缺人脉)"},
            {"tier": 2, "text": "一般 (有一定供应链和市场渠道)"},
            {"tier": 3, "text": "有利 (供应链优势/政策补贴/家族资源)"},
        ],
    },
    {
        "id": 9,
        "category": "职业与财务硬件",
        "title": "行业发展前景与晋升空间",
        "type": "dual_select",
        "tiers": 3,
        "us_label": "你所在行业在美国的前景",
        "cn_label": "你所在行业在国内的前景",
        "us_options": [
            {"tier": 1, "text": "前景不佳 (行业衰退/天花板明显)"},
            {"tier": 2, "text": "前景一般 (行业稳定，无明显优势)"},
            {"tier": 3, "text": "前景很好 (行业上升期/技术前沿)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "前景不佳 (行业严重内卷/下行)"},
            {"tier": 2, "text": "前景一般 (行业稳定)"},
            {"tier": 3, "text": "前景很好 (高速发展/政策扶持/风口)"},
        ],
    },

    # ===== 大类二：身份与生活方式 =====
    {
        "id": 10,
        "category": "身份与生活方式",
        "title": "留美的客观身份状态（硬壁垒）",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "已拥有绿卡、国籍，或 I-140 已批，无任何身份焦虑", "scores": (5, 1)},
            {"label": "B", "text": "抽中 H1B/OPT 期间，仍在排期初期，有路径但存隐患", "scores": (3, 3)},
            {"label": "C", "text": "OPT 即期未中签或依靠 CPT 挂靠，随时面临断档被动回国", "scores": (1, 5)},
        ],
    },
    {
        "id": 11,
        "category": "身份与生活方式",
        "title": "预想回国常驻地的户口难度",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "目标一线城市且完全无指标，面临长期排队或严苛购房/落户条件", "scores": (4, 2)},
            {"label": "B", "text": "目标城市无落户门槛，留学生身份随时可落", "scores": (3, 3)},
            {"label": "C", "text": "老家即是目标城市，或早已拥有户口，毫无阻力", "scores": (1, 5)},
        ],
    },
    {
        "id": 12,
        "category": "身份与生活方式",
        "title": "本地文娱内容与生态偏好",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极度享受北美文娱 (Livehouse / 体育赛事 / 英文脱口秀 / 派对)", "scores": (5, 1)},
            {"label": "B", "text": "双语/跨文化自洽型，两边文娱形式都能获得快乐", "scores": (3, 3)},
            {"label": "C", "text": "深度绑定国内语境 (中文脱口秀 / 剧本杀 / 密室 / 国内互联网生态)", "scores": (1, 5)},
        ],
    },
    {
        "id": 13,
        "category": "身份与生活方式",
        "title": "休闲旅行导向",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极致自然派：热爱硬核户外、国家公园探险、高山滑雪", "scores": (5, 1)},
            {"label": "B", "text": "兼而有之：自然与都市都喜欢，无明显偏好", "scores": (3, 3)},
            {"label": "C", "text": "繁华都市派：热爱 Citywalk、密集的高端餐饮探店、便利商业", "scores": (1, 5)},
        ],
    },
    {
        "id": 14,
        "category": "身份与生活方式",
        "title": "饮食硬性基因（中国胃）",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "全球胃：完全适应欧美沙拉/简餐，或极其享受自己下厨做饭", "scores": (5, 1)},
            {"label": "B", "text": "混合型：有普通中餐馆和亚超即可存活", "scores": (3, 3)},
            {"label": "C", "text": "顽固中国胃：极度依赖国内丰富廉价的地道外卖/夜宵且厌恶做饭", "scores": (1, 5)},
        ],
    },
    {
        "id": 15,
        "category": "身份与生活方式",
        "title": "物理出行依赖度",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "车轮上的生活：热爱自驾与北美汽车文化，极其讨厌公共交通", "scores": (5, 1)},
            {"label": "B", "text": "无缝切换：两边都能适应", "scores": (3, 3)},
            {"label": "C", "text": "极度抗拒开车：严重依赖国内发达的高铁与城市地铁网络", "scores": (1, 5)},
        ],
    },
    {
        "id": 16,
        "category": "身份与生活方式",
        "title": "核心社交性格",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极度看重人际边界感 / 享受孤独与独处 / 俗称「社恐」", "scores": (5, 1)},
            {"label": "B", "text": "适应性强，动静皆宜", "scores": (3, 3)},
            {"label": "C", "text": "极度渴望「烟火气」与深度的熟人高频社交", "scores": (1, 5)},
        ],
    },
    {
        "id": 17,
        "category": "身份与生活方式",
        "title": "性取向与少数群体身份",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "属于 LGBTQ+ 等群体，极其依赖美国婚姻合法化与职场平权法案", "scores": (5, 1)},
            {"label": "B", "text": "顺性别异性恋，无特殊诉求", "scores": (3, 3)},
        ],
    },
    {
        "id": 18,
        "category": "身份与生活方式",
        "title": "性别与社会时钟期待",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "女性，且极其看重北美职场对婚育的宽容度，抗拒国内催婚催育氛围", "scores": (4, 2)},
            {"label": "B", "text": "无显著性别带来的发展/催婚阻力", "scores": (3, 3)},
        ],
    },

    # ===== 大类三：家庭、情感与社会资本 =====
    {
        "id": 19,
        "category": "家庭、情感与社会资本",
        "title": "原生家庭结构与照料义务",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "非独生子女，国内有兄弟姐妹分担尽孝压力，可安心在海外", "scores": (5, 1)},
            {"label": "B", "text": "独生子女，父母目前健康，暂无物理绑定需求", "scores": (3, 3)},
            {"label": "C", "text": "独生子女，父母有基础病需物理照料，隐性推力拉满", "scores": (1, 5)},
        ],
    },
    {
        "id": 20,
        "category": "家庭、情感与社会资本",
        "title": "父母财务兜底与房产赞助",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "无赞助：父母无力提供购房支持，甚至需要子女寄钱反哺", "scores": (3, 3)},
            {"label": "B", "text": "中产自给：父母有完善退休金，无需反哺也无法提供大额赞助", "scores": (3, 3)},
            {"label": "C", "text": "强力兜底：父母已在一线备好全款婚房，或能提供巨额启动资金", "scores": (1, 5)},
        ],
    },
    {
        "id": 21,
        "category": "家庭、情感与社会资本",
        "title": "父母口头/精神施压度",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "父母极其开明，明确要求/支持你在海外定居发展", "scores": (5, 1)},
            {"label": "B", "text": "父母态度中立，尊重子女选择", "scores": (3, 3)},
            {"label": "C", "text": "父母在精神/情绪上极度依赖，长期高压要求必须回国", "scores": (1, 5)},
        ],
    },
    {
        "id": 22,
        "category": "家庭、情感与社会资本",
        "title": "国内核心特权与人脉资产",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "国内零背景，极其反感人情社会酒桌文化，回国面临高内卷", "scores": (5, 1)},
            {"label": "B", "text": "有普通熟人网，能解决看病排号等小事，但不构成核心壁垒", "scores": (3, 3)},
            {"label": "C", "text": "家族有硬核政商资源，能安排体制内/垄断行业，或有企业接班", "scores": (1, 5)},
        ],
    },
    {
        "id": 23,
        "category": "家庭、情感与社会资本",
        "title": "伴侣的职业地域对口度 (Two-body Problem)",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "单身；或伴侣在美国拥有极佳的职业发展/稳定身份", "scores": (5, 1)},
            {"label": "B", "text": "伴侣在美国的发展整体优于国内", "scores": (4, 2)},
            {"label": "C", "text": "伴侣职业两地均可无缝衔接", "scores": (3, 3)},
            {"label": "D", "text": "伴侣在国内的发展整体优于美国", "scores": (2, 4)},
            {"label": "E", "text": "伴侣职业极度依赖国内土壤 (国内自媒体/演艺/体制)，赴美即失业", "scores": (1, 5)},
        ],
    },
    {
        "id": 24,
        "category": "家庭、情感与社会资本",
        "title": "单身状态下的择偶基数（已婚选B）",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "身处大农村或性别极度失衡行业，符合标准的择偶池极小", "scores": (1, 5)},
            {"label": "B", "text": "身处大都会，或接受跨文化恋爱，当地华人/非华人池子庞大", "scores": (3, 3)},
        ],
    },
    {
        "id": 25,
        "category": "家庭、情感与社会资本",
        "title": "对下一代基础教育的偏好",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "推崇北美素质/快乐教育，反感国内做题家内卷", "scores": (5, 1)},
            {"label": "B", "text": "无所谓，教育不影响去留决策", "scores": (3, 3)},
            {"label": "C", "text": "丁克一族，无生育计划", "scores": (3, 3)},
            {"label": "D", "text": "推崇国内公立体制扎实的数理化，或已拥有国内顶尖学区房", "scores": (1, 5)},
        ],
    },
]

# 按 id 建立快速查找索引
_QUESTION_MAP = {q["id"]: q for q in QUESTIONS}


def get_questions_for_frontend():
    """返回前端展示用的题目数据，不包含分数信息"""
    result = []
    for q in QUESTIONS:
        item = {
            "id": q["id"],
            "category": q["category"],
            "title": q["title"],
            "type": q["type"],
        }
        if q["type"] == "age_input":
            item["description"] = q["description"]
            item["min_age"] = 20
            item["auto_weight"] = True  # 前端不显示权重选择
        elif q["type"] == "dual_select":
            item["tiers"] = q["tiers"]
            item["us_label"] = q["us_label"]
            item["cn_label"] = q["cn_label"]
            item["us_options"] = [{"tier": o["tier"], "text": o["text"]} for o in q["us_options"]]
            item["cn_options"] = [{"tier": o["tier"], "text": o["text"]} for o in q["cn_options"]]
        else:  # single_choice
            item["options"] = [
                {"label": opt["label"], "text": opt["text"]}
                for opt in q["options"]
            ]
        result.append(item)
    return result


def get_age_scores(age: int) -> tuple[int, int]:
    """根据年龄返回 (US_Base_Score, CN_Base_Score)"""
    age_q = _QUESTION_MAP[0]
    for r in age_q["age_ranges"]:
        if r["min"] <= age <= r["max"]:
            return r["scores"]
    if age < 20:
        return (1, 5)
    return (5, 1)  # 35+ 同 32-35


def get_dual_scores(question_id: int, us_tier: int, cn_tier: int) -> tuple[int, int]:
    """双轴题：根据档位返回 (US_Base_Score, CN_Base_Score)"""
    q = _QUESTION_MAP[question_id]
    tiers = q["tiers"]
    if tiers == 5:
        return (us_tier, cn_tier)
    else:  # 3档 -> 映射为 1/3/5
        return (TIER3_TO_SCORE[us_tier], TIER3_TO_SCORE[cn_tier])


def get_option_scores(question_id: int, selected_option: str) -> tuple[int, int]:
    """单选题：根据题号和选项返回 (US_Base_Score, CN_Base_Score)"""
    q = _QUESTION_MAP[question_id]
    for opt in q["options"]:
        if opt["label"] == selected_option:
            return opt["scores"]
    raise ValueError(f"Invalid option '{selected_option}' for question {question_id}")
