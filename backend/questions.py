"""
完整题库：25 题（1 道年龄题 + 24 道选择题）
每个选项的 scores 为 (US_Base_Score, CN_Base_Score)，范围 1-5。
分数信息仅后端使用，不暴露给前端。
"""

QUESTIONS = [
    # ===== Q0: 年龄题 (特殊类型) =====
    {
        "id": 0,
        "category": "基础信息",
        "title": "你的年龄",
        "type": "age_input",
        "description": "请输入你的年龄（20-35岁）",
        "age_ranges": [
            {"min": 20, "max": 22, "scores": (1, 5)},
            {"min": 23, "max": 25, "scores": (2, 4)},
            {"min": 26, "max": 28, "scores": (3, 3)},
            {"min": 29, "max": 31, "scores": (4, 2)},
            {"min": 32, "max": 35, "scores": (5, 1)},
        ],
    },

    # ===== 大类一：职业与财务硬件 (Career & Finance) =====
    {
        "id": 1,
        "category": "职业与财务硬件",
        "title": "中美绝对薪资与购买力对标",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "美区大厂/高阶 ($200k以上) vs 国内普通水平", "scores": (5, 1)},
            {"label": "B", "text": "美区中坚力量 ($120k-200k) vs 国内优质外企/大厂 (¥30-60万)", "scores": (3, 3)},
            {"label": "C", "text": "美区基础/入门岗 (<$80k) vs 国内大厂核心/创业/高管 (¥60万以上)", "scores": (1, 5)},
        ],
    },
    {
        "id": 2,
        "category": "职业与财务硬件",
        "title": "房租/房贷占税后收入比（财务健康度）",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "留美轻松买房或房收比 <20% / 回国一线面临地狱级房贷", "scores": (5, 1)},
            {"label": "B", "text": "两边都要靠自己拼首付，压力相当 (约占 30%)", "scores": (3, 3)},
            {"label": "C", "text": "留美只能合租或房收比 >45% / 国内老家有房或公积金完全覆盖", "scores": (1, 5)},
        ],
    },
    {
        "id": 3,
        "category": "职业与财务硬件",
        "title": "每周实际工作时长（WLB）",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "美国极度 WLB (<40h) / 国内必然面临大小周或 55h+ 待机", "scores": (5, 1)},
            {"label": "B", "text": "两边都需要偶尔加班 (40h-50h 左右)", "scores": (3, 3)},
            {"label": "C", "text": "美国身处高压淘汰环境 / 国内属于极度稳定的体制内 955", "scores": (1, 5)},
        ],
    },
    {
        "id": 4,
        "category": "职业与财务硬件",
        "title": "全年带薪休假天数（PTO）",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "美国福利极佳 (15-25天以上) / 国内请假极难或仅有 5天基础年假", "scores": (5, 1)},
            {"label": "B", "text": "两边休假制度大致相当 (10-15天左右)", "scores": (3, 3)},
        ],
    },
    {
        "id": 5,
        "category": "职业与财务硬件",
        "title": "职场「35岁现象」与生命周期",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极其看重职场寿命，畏惧国内 35 岁裁员红线，倾向美国反年龄歧视", "scores": (5, 1)},
            {"label": "B", "text": "自身行业两边越老越吃香 (如医生、资深律师)，无视年龄红线", "scores": (3, 3)},
            {"label": "C", "text": "打算在国内考公进体制，追求绝对的终身稳定", "scores": (1, 5)},
        ],
    },
    {
        "id": 6,
        "category": "职业与财务硬件",
        "title": "裁员风险与失业缓冲",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "留美受制于签证 60 天宽限期，一旦失业面临立刻离境风险", "scores": (1, 5)},
            {"label": "B", "text": "两地行业波动差不多，都有足够缓冲", "scores": (3, 3)},
        ],
    },
    {
        "id": 7,
        "category": "职业与财务硬件",
        "title": "副业拓展与合规门槛",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "签证明文禁止 W2 外收入，留美做副业/创业不合法", "scores": (1, 5)},
            {"label": "B", "text": "已有自由身份，或压根不想做副业", "scores": (3, 3)},
            {"label": "C", "text": "极度渴望做自媒体/电商，国内土壤极佳无合规限制", "scores": (1, 5)},
        ],
    },
    {
        "id": 8,
        "category": "职业与财务硬件",
        "title": "创业土壤与投资渠道",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "留美受限高昂人力与身份壁垒 / 国内有极佳的供应链和政策补贴", "scores": (1, 5)},
            {"label": "B", "text": "不打算创业，安心做打工人", "scores": (3, 3)},
            {"label": "C", "text": "具备极强的海外本土技术/风投资源，专注出海或美国本土创业", "scores": (5, 1)},
        ],
    },

    # ===== 大类二：身份与生活方式 (Identity & Lifestyle) =====
    {
        "id": 9,
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
        "id": 10,
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
        "id": 11,
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
        "id": 12,
        "category": "身份与生活方式",
        "title": "休闲旅行导向",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极致自然派：热爱硬核户外、国家公园探险、高山滑雪", "scores": (5, 1)},
            {"label": "B", "text": "繁华都市派：热爱 Citywalk、密集的高端餐饮探店、便利商业", "scores": (1, 5)},
        ],
    },
    {
        "id": 13,
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
        "id": 14,
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
        "id": 15,
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
        "id": 16,
        "category": "身份与生活方式",
        "title": "性取向与少数群体身份",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "属于 LGBTQ+ 等群体，极其依赖美国婚姻合法化与职场平权法案", "scores": (5, 1)},
            {"label": "B", "text": "顺性别异性恋，无特殊诉求", "scores": (3, 3)},
        ],
    },
    {
        "id": 17,
        "category": "身份与生活方式",
        "title": "性别与社会时钟期待",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "女性，且极其看重北美职场对婚育的宽容度，抗拒国内催婚催育氛围", "scores": (4, 2)},
            {"label": "B", "text": "无显著性别带来的发展/催婚阻力", "scores": (3, 3)},
        ],
    },

    # ===== 大类三：家庭、情感与社会资本 (Family & Social Capital) =====
    {
        "id": 18,
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
        "id": 19,
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
        "id": 20,
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
        "id": 21,
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
        "id": 22,
        "category": "家庭、情感与社会资本",
        "title": "伴侣的职业地域对口度 (Two-body Problem)",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "单身；或伴侣在美国拥有极佳的职业发展/稳定身份", "scores": (5, 1)},
            {"label": "B", "text": "伴侣职业两地均可无缝衔接", "scores": (3, 3)},
            {"label": "C", "text": "伴侣职业极度依赖国内土壤 (国内自媒体/演艺/体制)，赴美即失业", "scores": (1, 5)},
        ],
    },
    {
        "id": 23,
        "category": "家庭、情感与社会资本",
        "title": "单身状态下的择偶基数（已婚选B）",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "身处大农村或性别极度失衡行业，符合标准的择偶池极小", "scores": (1, 5)},
            {"label": "B", "text": "身处大都会，或接受跨文化恋爱，当地华人/非华人池子庞大", "scores": (3, 3)},
        ],
    },
    {
        "id": 24,
        "category": "家庭、情感与社会资本",
        "title": "对下一代基础教育的偏好",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "推崇北美素质/快乐教育，反感国内做题家内卷", "scores": (5, 1)},
            {"label": "B", "text": "丁克一族，无生育计划", "scores": (3, 3)},
            {"label": "C", "text": "推崇国内公立体制扎实的数理化，或已拥有国内顶尖学区房", "scores": (1, 5)},
        ],
    },
]


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
            item["max_age"] = 35
        else:
            item["options"] = [
                {"label": opt["label"], "text": opt["text"]}
                for opt in q["options"]
            ]
        result.append(item)
    return result


def get_age_scores(age: int) -> tuple[int, int]:
    """根据年龄返回 (US_Base_Score, CN_Base_Score)"""
    age_q = QUESTIONS[0]
    for r in age_q["age_ranges"]:
        if r["min"] <= age <= r["max"]:
            return r["scores"]
    # 边界处理
    if age < 20:
        return (1, 5)
    return (5, 1)


def get_option_scores(question_id: int, selected_option: str) -> tuple[int, int]:
    """根据题号和选项返回 (US_Base_Score, CN_Base_Score)"""
    q = QUESTIONS[question_id]
    for opt in q["options"]:
        if opt["label"] == selected_option:
            return opt["scores"]
    raise ValueError(f"Invalid option '{selected_option}' for question {question_id}")
