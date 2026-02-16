"""
V2 完整题库：29 题
- 4 道基础信息（single_choice）
- 9 道职业与财务硬件（dual_select：Q4-Q8 五档，Q9-Q12 三档）
- 9 道身份与生活方式（single_choice）
- 7 道家庭、情感与社会资本（single_choice）

所有题目均为 single_choice 或 dual_select，移除了 V1 的 age_input 类型。
双轴题(dual_select)：用户分别为"在美情况"和"在华情况"各选一个档位。
- 5档题：档位值 1-5 直接作为 base_score
- 3档题：档位值 1/2/3 映射为 base_score 1/3/5

分数信息仅后端使用，不暴露给前端。
"""

# 3档 -> 5分制映射
TIER3_TO_SCORE = {1: 1, 2: 3, 3: 5}

QUESTIONS = [
    # ===== 第一部分：基础信息 (ID 0-3) =====
    {
        "id": 0,
        "category": "基础信息",
        "title": "性别",
        "type": "single_choice",
        "auto_weight": 3,
        "options": [
            {"label": "A", "text": "女性", "scores": (4, 2)},
            {"label": "B", "text": "男性", "scores": (3, 3)},
            {"label": "C", "text": "非二元性别/不愿透露", "scores": (5, 1)},
        ],
    },
    {
        "id": 1,
        "category": "基础信息",
        "title": "家庭在国内所属的城市级别",
        "type": "single_choice",
        "auto_weight": 3,
        "options": [
            {"label": "A", "text": "超一线城市（北上广深）", "scores": (2, 5)},
            {"label": "B", "text": "一线/强二线城市（杭州、南京、成都等）", "scores": (3, 4)},
            {"label": "C", "text": "普通二线/地级市", "scores": (3, 3)},
            {"label": "D", "text": "三线城市及以下/县区", "scores": (4, 2)},
            {"label": "E", "text": "暂无国内固定落脚点/海外长居", "scores": (5, 1)},
        ],
    },
    {
        "id": 2,
        "category": "基础信息",
        "title": "你的来美年数",
        "type": "single_choice",
        "auto_weight": 3,
        "options": [
            {"label": "A", "text": "< 1 年（新鲜人）", "scores": (2, 4)},
            {"label": "B", "text": "1-3 年（逐步适应）", "scores": (3, 3)},
            {"label": "C", "text": "3-5 年（关键转型期）", "scores": (4, 2)},
            {"label": "D", "text": "5-10 年（深度扎根）", "scores": (5, 1)},
            {"label": "E", "text": "10 年以上", "scores": (5, 1)},
        ],
    },
    {
        "id": 3,
        "category": "基础信息",
        "title": "你的年龄",
        "type": "single_choice",
        "auto_weight": 3,
        "options": [
            {"label": "A", "text": "20-22 岁", "scores": (1, 5)},
            {"label": "B", "text": "23-25 岁", "scores": (2, 4)},
            {"label": "C", "text": "26-28 岁", "scores": (3, 3)},
            {"label": "D", "text": "29-31 岁", "scores": (4, 2)},
            {"label": "E", "text": "32 岁以上", "scores": (5, 1)},
        ],
    },

    # ===== 第二部分：职业与财务硬件 (ID 4-12) =====
    # --- Q4-Q8: 双轴5档 ---
    {
        "id": 4,
        "category": "职业与财务硬件",
        "title": "预期薪资购买力对比",
        "type": "dual_select",
        "tiers": 5,
        "us_label": "你在美国的薪资/收入水平",
        "cn_label": "你回国后的薪资/收入预期",
        "us_options": [
            {"tier": 1, "text": "<$80k"},
            {"tier": 2, "text": "$80k-$150k"},
            {"tier": 3, "text": "$150k-$300k"},
            {"tier": 4, "text": "$300k-$600k"},
            {"tier": 5, "text": "$600k+"},
        ],
        "cn_options": [
            {"tier": 1, "text": "<15万"},
            {"tier": 2, "text": "15-30万"},
            {"tier": 3, "text": "30-60万"},
            {"tier": 4, "text": "60-120万"},
            {"tier": 5, "text": "120万+"},
        ],
    },
    {
        "id": 5,
        "category": "职业与财务硬件",
        "title": "住房支出压力对比",
        "type": "dual_select",
        "tiers": 5,
        "us_label": "你在美国的住房压力",
        "cn_label": "你回国后的住房压力",
        "us_options": [
            {"tier": 1, "text": "极重（>45%收入）"},
            {"tier": 2, "text": "较重 (35-45%)"},
            {"tier": 3, "text": "一般 (25-35%)"},
            {"tier": 4, "text": "较轻 (15-25%)"},
            {"tier": 5, "text": "极轻 (<15%/已有房)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "极重（>45%收入）"},
            {"tier": 2, "text": "较重 (35-45%)"},
            {"tier": 3, "text": "一般 (25-35%)"},
            {"tier": 4, "text": "较轻 (15-25%)"},
            {"tier": 5, "text": "极轻 (<15%/已有房)"},
        ],
    },
    {
        "id": 6,
        "category": "职业与财务硬件",
        "title": "工作强度与边界感 (WLB)",
        "type": "dual_select",
        "tiers": 5,
        "us_label": "你在美国的工作强度",
        "cn_label": "你回国后的工作强度预期",
        "us_options": [
            {"tier": 1, "text": "极其高压 (>60h/随时待命)"},
            {"tier": 2, "text": "较忙碌 (50-60h)"},
            {"tier": 3, "text": "标准 (40-50h)"},
            {"tier": 4, "text": "较平衡 (35-40h)"},
            {"tier": 5, "text": "极度平衡 (<35h/不加班)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "极其高压 (>60h/随时待命)"},
            {"tier": 2, "text": "较忙碌 (50-60h)"},
            {"tier": 3, "text": "标准 (40-50h)"},
            {"tier": 4, "text": "较平衡 (35-40h)"},
            {"tier": 5, "text": "极度平衡 (<35h/不加班)"},
        ],
    },
    {
        "id": 7,
        "category": "职业与财务硬件",
        "title": "全年带薪年假 (PTO)",
        "type": "dual_select",
        "tiers": 5,
        "us_label": "你在美国的带薪假天数",
        "cn_label": "你回国后的带薪假预期",
        "us_options": [
            {"tier": 1, "text": "<5天"},
            {"tier": 2, "text": "5-10天"},
            {"tier": 3, "text": "10-15天"},
            {"tier": 4, "text": "15-20天"},
            {"tier": 5, "text": "20天+"},
        ],
        "cn_options": [
            {"tier": 1, "text": "<5天"},
            {"tier": 2, "text": "5-10天"},
            {"tier": 3, "text": "10-15天"},
            {"tier": 4, "text": "15-20天"},
            {"tier": 5, "text": "20天+"},
        ],
    },
    {
        "id": 8,
        "category": "职业与财务硬件",
        "title": "职场年龄文化压力",
        "type": "dual_select",
        "tiers": 5,
        "us_label": "你在美国的职场年龄压力",
        "cn_label": "你回国后的职场年龄压力",
        "us_options": [
            {"tier": 1, "text": "压力极大 (有硬性门槛)"},
            {"tier": 2, "text": "较有压力"},
            {"tier": 3, "text": "中规中矩"},
            {"tier": 4, "text": "压力较小"},
            {"tier": 5, "text": "极无压力 (看重资历)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "压力极大 (有硬性门槛)"},
            {"tier": 2, "text": "较有压力"},
            {"tier": 3, "text": "中规中矩"},
            {"tier": 4, "text": "压力较小"},
            {"tier": 5, "text": "极无压力 (看重资历)"},
        ],
    },

    # --- Q9-Q12: 双轴3档 ---
    {
        "id": 9,
        "category": "职业与财务硬件",
        "title": "裁员风险与失业缓冲",
        "type": "dual_select",
        "tiers": 3,
        "us_label": "你在美国的失业风险与缓冲",
        "cn_label": "你回国后的失业风险与缓冲",
        "us_options": [
            {"tier": 1, "text": "高风险 (签证强绑定)"},
            {"tier": 2, "text": "中等"},
            {"tier": 3, "text": "低风险 (身份自由/福利好)"},
        ],
        "cn_options": [
            {"tier": 1, "text": "高风险 (行业下行/35岁)"},
            {"tier": 2, "text": "中等"},
            {"tier": 3, "text": "低风险 (编制/铁饭碗)"},
        ],
    },
    {
        "id": 10,
        "category": "职业与财务硬件",
        "title": "副业与额外收入可能性",
        "type": "dual_select",
        "tiers": 3,
        "us_label": "你在美国做副业的可行性",
        "cn_label": "你回国后做副业的可行性",
        "us_options": [
            {"tier": 1, "text": "受限/极难"},
            {"tier": 2, "text": "一般/有空间"},
            {"tier": 3, "text": "自由/土壤肥沃"},
        ],
        "cn_options": [
            {"tier": 1, "text": "受限/极难"},
            {"tier": 2, "text": "一般/有空间"},
            {"tier": 3, "text": "自由/土壤肥沃"},
        ],
    },
    {
        "id": 11,
        "category": "职业与财务硬件",
        "title": "创业环境与资源获取",
        "type": "dual_select",
        "tiers": 3,
        "us_label": "你在美国的创业条件",
        "cn_label": "你回国后的创业条件",
        "us_options": [
            {"tier": 1, "text": "不利/缺资源"},
            {"tier": 2, "text": "一般"},
            {"tier": 3, "text": "有利/资源丰富"},
        ],
        "cn_options": [
            {"tier": 1, "text": "不利/缺资源"},
            {"tier": 2, "text": "一般"},
            {"tier": 3, "text": "有利/资源丰富"},
        ],
    },
    {
        "id": 12,
        "category": "职业与财务硬件",
        "title": "行业长期发展天花板",
        "type": "dual_select",
        "tiers": 3,
        "us_label": "你所在行业在美国的前景",
        "cn_label": "你所在行业在国内的前景",
        "us_options": [
            {"tier": 1, "text": "前景欠佳/下行"},
            {"tier": 2, "text": "稳定期"},
            {"tier": 3, "text": "极具潜力/风口"},
        ],
        "cn_options": [
            {"tier": 1, "text": "前景欠佳/下行"},
            {"tier": 2, "text": "稳定期"},
            {"tier": 3, "text": "极具潜力/风口"},
        ],
    },

    # ===== 第三部分：身份与生活方式 (ID 13-21) =====
    {
        "id": 13,
        "category": "身份与生活方式",
        "title": "留美的客观身份状态（硬壁垒）",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "身份极度稳固（绿卡/公民/I-140已批）", "scores": (5, 1)},
            {"label": "B", "text": "身份过渡期，有明确预期（H1B平稳/排期中）", "scores": (4, 2)},
            {"label": "C", "text": "身份观察期（OPT/STEM中，有抽签机会）", "scores": (3, 3)},
            {"label": "D", "text": "身份不确定性大（OPT首年/抽签多次未中）", "scores": (2, 4)},
            {"label": "E", "text": "身份面临断档（需挂靠CPT/即将到期）", "scores": (1, 5)},
        ],
    },
    {
        "id": 14,
        "category": "身份与生活方式",
        "title": "目标城市落户及安居门槛",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极难落户且无配套资源（如北京严苛指标）", "scores": (5, 1)},
            {"label": "B", "text": "有一定门槛但可通过积分/时间解决", "scores": (4, 2)},
            {"label": "C", "text": "门槛适中，符合留学生基本政策", "scores": (3, 3)},
            {"label": "D", "text": "门槛极低，基本实现自由迁徙", "scores": (2, 4)},
            {"label": "E", "text": "零门槛（已有户口或老家即目标地）", "scores": (1, 5)},
        ],
    },
    {
        "id": 15,
        "category": "身份与生活方式",
        "title": "本地文娱内容共鸣度",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "高度共鸣北美文娱（英文脱口秀/美式社交/本土赛事）", "scores": (5, 1)},
            {"label": "B", "text": "较偏好北美形式，但也能欣赏国内内容", "scores": (4, 2)},
            {"label": "C", "text": "跨文化自洽，两边均能获得同等乐趣", "scores": (3, 3)},
            {"label": "D", "text": "较偏好国内语境（中文线下演出/社交游戏/国内生态）", "scores": (2, 4)},
            {"label": "E", "text": "深度绑定国内语境（极度依赖中文圈层和线下形式）", "scores": (1, 5)},
        ],
    },
    {
        "id": 16,
        "category": "身份与生活方式",
        "title": "休闲旅行偏好梯度",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极度推崇硬核自然/国家公园/极限运动", "scores": (5, 1)},
            {"label": "B", "text": "较偏好自然风光，偶尔享受城市便利", "scores": (4, 2)},
            {"label": "C", "text": "兼而有之，随遇而安", "scores": (3, 3)},
            {"label": "D", "text": "较偏好城市繁华，喜欢高密度商业探店", "scores": (2, 4)},
            {"label": "E", "text": "极度依赖现代都市便利/商圈/高度发达的服务业", "scores": (1, 5)},
        ],
    },
    {
        "id": 17,
        "category": "身份与生活方式",
        "title": "饮食基因与生活成本感官",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "完全适应当地饮食，或享受自炊生活", "scores": (5, 1)},
            {"label": "B", "text": "以西餐为主，偶尔调节中餐", "scores": (4, 2)},
            {"label": "C", "text": "混合型，有基础亚超即可满足", "scores": (3, 3)},
            {"label": "D", "text": "较依赖中餐，对当地外卖/餐饮便捷度有要求", "scores": (2, 4)},
            {"label": "E", "text": "极度依赖国内餐饮体系（外卖/夜宵/极致地道中餐）", "scores": (1, 5)},
        ],
    },
    {
        "id": 18,
        "category": "身份与生活方式",
        "title": "物理出行方式偏好",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极度热爱驾驶/汽车文化，享受路权", "scores": (5, 1)},
            {"label": "B", "text": "习惯驾驶，不排斥开车出行", "scores": (4, 2)},
            {"label": "C", "text": "随环境切换，对出行方式不敏感", "scores": (3, 3)},
            {"label": "D", "text": "较依赖公共交通，觉得开车是负担", "scores": (2, 4)},
            {"label": "E", "text": "极度依赖高铁/地铁/打车，拒绝自驾", "scores": (1, 5)},
        ],
    },
    {
        "id": 19,
        "category": "身份与生活方式",
        "title": "社交性格与边界感需求",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极度追求人际边界/隐私/独立生活空间", "scores": (5, 1)},
            {"label": "B", "text": "比较享受美式简单社交关系", "scores": (4, 2)},
            {"label": "C", "text": "适应力强，能融入不同社交氛围", "scores": (3, 3)},
            {"label": "D", "text": "比较喜欢热闹，渴望紧密的朋友连接", "scores": (2, 4)},
            {"label": "E", "text": "极度渴望\"烟火气\"与深度高频的人情社交", "scores": (1, 5)},
        ],
    },
    {
        "id": 20,
        "category": "身份与生活方式",
        "title": "性取向与少数群体权利诉求",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "有强烈的平权法案/少数群体社会保障需求", "scores": (5, 1)},
            {"label": "B", "text": "对相关社会包容度有较高期待", "scores": (4, 2)},
            {"label": "C", "text": "无特殊诉求，环境适应性强", "scores": (3, 3)},
        ],
    },
    {
        "id": 21,
        "category": "身份与生活方式",
        "title": "性别角色与社会期待压力",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极度抗拒传统的婚育压力和社会时钟期待", "scores": (5, 1)},
            {"label": "B", "text": "比较喜欢北美相对宽松的个人选择环境", "scores": (4, 2)},
            {"label": "C", "text": "无明显感触或能平衡两地压力", "scores": (3, 3)},
        ],
    },

    # ===== 第四部分：家庭、情感与社会资本 (ID 22-28) =====
    {
        "id": 22,
        "category": "家庭、情感与社会资本",
        "title": "原生家庭照料义务现状",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "毫无物理绑定压力（非独生/父母极其独立）", "scores": (5, 1)},
            {"label": "B", "text": "压力较小，短期内无需回国处理家庭事务", "scores": (4, 2)},
            {"label": "C", "text": "处于平衡状态，可跨国远程兼顾", "scores": (3, 3)},
            {"label": "D", "text": "有潜在照料需求（独生/父母开始老龄化）", "scores": (2, 4)},
            {"label": "E", "text": "物理绑定极强（父母患病/必须在身边照料）", "scores": (1, 5)},
        ],
    },
    {
        "id": 23,
        "category": "家庭、情感与社会资本",
        "title": "父母财务支持与兜底能力",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "需反哺：父母无保障，需子女持续经济支援", "scores": (3, 3)},
            {"label": "B", "text": "自给自足：无负担但也无大额支持", "scores": (3, 3)},
            {"label": "C", "text": "有一定支持：能提供部分首付或资源助力", "scores": (2, 4)},
            {"label": "D", "text": "强力支持：能在一线城市全款供房或提供事业启动资金", "scores": (1, 5)},
        ],
    },
    {
        "id": 24,
        "category": "家庭、情感与社会资本",
        "title": "父母对去留的主观施压程度",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极度支持留美，甚至主动要求你留下", "scores": (5, 1)},
            {"label": "B", "text": "比较倾向你留下，但尊重个人意愿", "scores": (4, 2)},
            {"label": "C", "text": "完全中立，不给任何建议", "scores": (3, 3)},
            {"label": "D", "text": "比较希望你回国，经常口头催促", "scores": (2, 4)},
            {"label": "E", "text": "极度施压，以各种方式强制要求回国", "scores": (1, 5)},
        ],
    },
    {
        "id": 25,
        "category": "家庭、情感与社会资本",
        "title": "国内社会关系与资源杠杆（人脉）",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "零背景：反感应酬文化，国内职场需从零起步", "scores": (5, 1)},
            {"label": "B", "text": "普通背景：仅有基本社交圈，无职场助力", "scores": (4, 2)},
            {"label": "C", "text": "有一定熟人网：能解决琐碎生活问题", "scores": (3, 3)},
            {"label": "D", "text": "较强资源：在特定行业有深厚人脉，能获职业优待", "scores": (2, 4)},
            {"label": "E", "text": "核心特权：家族资源可直接变现或继承事业", "scores": (1, 5)},
        ],
    },
    {
        "id": 26,
        "category": "家庭、情感与社会资本",
        "title": "伴侣的职业地域对口度 (Two-body Problem)",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "单身/伴侣极其适合在美发展（或已有身份）", "scores": (5, 1)},
            {"label": "B", "text": "伴侣偏好留美，职业有一定竞争力", "scores": (4, 2)},
            {"label": "C", "text": "伴侣两地均可，随你而动", "scores": (3, 3)},
            {"label": "D", "text": "伴侣偏好回国，国内有更好发展机会", "scores": (2, 4)},
            {"label": "E", "text": "伴侣极度依赖国内环境（赴美即失业）", "scores": (1, 5)},
        ],
    },
    {
        "id": 27,
        "category": "家庭、情感与社会资本",
        "title": "择偶池与婚恋市场适配度",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "美国择偶环境极佳（社交圈广/接受跨文化）", "scores": (5, 1)},
            {"label": "B", "text": "比较适应目前的海外婚恋节奏", "scores": (4, 2)},
            {"label": "C", "text": "已婚或对婚恋无所谓", "scores": (3, 3)},
            {"label": "D", "text": "感觉海外池子太小，期待国内更高的匹配效率", "scores": (2, 4)},
            {"label": "E", "text": "极度依赖国内婚恋市场（家庭介绍/相亲/共同背景）", "scores": (1, 5)},
        ],
    },
    {
        "id": 28,
        "category": "家庭、情感与社会资本",
        "title": "对下一代教育模式的客观倾向",
        "type": "single_choice",
        "options": [
            {"label": "A", "text": "极度推崇北美素质/快乐教育模式", "scores": (5, 1)},
            {"label": "B", "text": "比较认可海外教育环境", "scores": (4, 2)},
            {"label": "C", "text": "丁克或认为教育不应成为决定因素", "scores": (3, 3)},
            {"label": "D", "text": "比较认可国内基础教育的扎实程度", "scores": (2, 4)},
            {"label": "E", "text": "极度依赖国内体制内名校/学区资源", "scores": (1, 5)},
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
        if "auto_weight" in q:
            item["auto_weight"] = True
        if q["type"] == "dual_select":
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
