#!/usr/bin/env python3
"""Netlify Function: 问卷分析 + 案例匹配 + 方向卡生成"""
import json, os, re, sys

# ---- DeepSeek API ----
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

# ---- 静态案例库（可被定时脚本覆盖） ----
STATIC_CASES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "api-data", "cases.json")

def load_cases():
    """加载案例库，优先从静态文件读取"""
    try:
        with open(STATIC_CASES_PATH) as f:
            return json.load(f)
    except:
        return CASE_LIBRARY

# 内置案例库
CASE_LIBRARY = [
  {"id":"case001","name":"油气井生产优化设计系统","author":"村长","category":"工具","views":"116.6K","likes":"3.4K","description":"油气井生产优化设计专用工具","targetUsers":"工业从业者","interactionMode":"工具/助手","tags":["工具效率"]},
  {"id":"case002","name":"星途｜爱豆人生模拟器","author":"师法自然","category":"游戏","views":"24.3K","likes":"2.7K","description":"模拟偶像养成路线，生成专属爱豆人生剧本","targetUsers":"追星族、Z世代年轻人","interactionMode":"模拟器/沙盒","tags":["人格测试","游戏互动"]},
  {"id":"case003","name":"粽遇父爱 · 秒哒寄温情","author":"秒哒官方","category":"推荐","views":"2.8K","likes":"569","description":"端午节+父爱主题温情互动应用","targetUsers":"节日用户","interactionMode":"信息展示","tags":["社交互动","内容创作"]},
  {"id":"case004","name":"海王套路识别模拟器（校园慎用版）","author":"爽朗的琳紫","category":"游戏","views":"24.7K","likes":"522","description":"模拟海王套路识别","targetUsers":"校园年轻人","interactionMode":"模拟器/沙盒","tags":["游戏互动","社交互动"]},
  {"id":"case005","name":"退休魔女的开荒日记","author":"爽朗的琳紫","category":"游戏","views":"13.5K","likes":"1.2K","description":"叙事驱动的冒险日记互动","targetUsers":"轻小说/游戏爱好者","interactionMode":"内容创作","tags":["内容创作","游戏互动"]},
  {"id":"case006","name":"FBTI看球人格测试","author":"也非","category":"问卷","views":"3.5K","likes":"594","description":"看球风格人格测试","targetUsers":"球迷群体","interactionMode":"问卷调查","tags":["人格测试","社交互动"]},
  {"id":"case007","name":"端午渔趣·粽钓江南","author":"慎独","category":"游戏","views":"2K","likes":"525","description":"端午节主题小游戏","targetUsers":"节日用户","interactionMode":"闯关/游戏","tags":["游戏互动"]},
  {"id":"case008","name":"码上制片厂","author":"黄啊码","category":"工具","views":"26.9K","likes":"765","description":"开发者内容制作工具","targetUsers":"开发者/内容创作者","interactionMode":"工具/助手","tags":["工具效率","内容创作"]},
  {"id":"case009","name":"出轨模拟器","author":"爽朗的琳紫","category":"游戏","views":"5.9K","likes":"583","description":"情感话题互动模拟器","targetUsers":"年轻人","interactionMode":"模拟器/沙盒","tags":["情感心理","社交互动"]},
  {"id":"case010","name":"龙虾像素空间","author":"爽朗的琳紫","category":"游戏","views":"15.8K","likes":"723","description":"像素风格虚拟空间探索","targetUsers":"像素游戏爱好者","interactionMode":"闯关/游戏","tags":["游戏互动"]},
  {"id":"case011","name":"【可复制】Offer神器","author":"小枚","category":"工具","views":"1.3K","likes":"443","description":"求职面试辅助工具","targetUsers":"求职者/应届生","interactionMode":"工具/助手","tags":["工具效率","学习成长"]},
  {"id":"case012","name":"全家福生成器","author":"clover睿","category":"推荐","views":"152.4K","likes":"838","description":"AI生成全家福合影","targetUsers":"异地过年人群","interactionMode":"图片生成","tags":["AI原生","社交互动"]},
  {"id":"case013","name":"减肥搭子","author":"师法自然","category":"工具","views":"8.2K","likes":"1.1K","description":"AI陪伴式减肥助手","targetUsers":"减脂人群","interactionMode":"工具/助手","tags":["工具效率","AI原生"]},
  {"id":"case014","name":"遇见未来的你","author":"师法自然","category":"游戏","views":"12.1K","likes":"978","description":"虚拟未来人生体验","targetUsers":"年轻人","interactionMode":"模拟器/沙盒","tags":["人格测试","游戏互动"]},
  {"id":"case015","name":"MBTI城市漫游指南","author":"小枚","category":"工具","views":"6.7K","likes":"834","description":"MBTI人格城市旅行推荐","targetUsers":"旅行爱好者","interactionMode":"工具/助手","tags":["人格测试","工具效率"]},
  {"id":"case016","name":"我的AI男友日记","author":"clover睿","category":"游戏","views":"45.3K","likes":"3.2K","description":"AI男友角色扮演互动","targetUsers":"女性用户","interactionMode":"模拟器/沙盒","tags":["社交互动","AI原生","游戏互动"]},
  {"id":"case017","name":"深夜食堂故事会","author":"爽朗的琳紫","category":"游戏","views":"3.8K","likes":"456","description":"叙事驱动的深夜故事分享","targetUsers":"年轻人","interactionMode":"内容创作","tags":["内容创作","社交互动"]},
  {"id":"case018","name":"万词王-背单词游戏化","author":"村长","category":"游戏","views":"33.2K","likes":"4.1K","description":"游戏化背单词，闯关式学习","targetUsers":"学生/英语学习者","interactionMode":"闯关/游戏","tags":["学习成长","游戏互动"]},
  {"id":"case019","name":"AI简历优化助手","author":"黄啊码","category":"工具","views":"18.9K","likes":"2.3K","description":"AI辅助简历优化","targetUsers":"求职者","interactionMode":"工具/助手","tags":["工具效率","AI原生"]},
  {"id":"case020","name":"宠物表情翻译器","author":"小枚","category":"工具","views":"67.8K","likes":"5.6K","description":"AI分析宠物表情和声音","targetUsers":"宠物主","interactionMode":"工具/助手","tags":["AI原生","工具效率"]},
  {"id":"case021","name":"自习室·专注番茄钟","author":"也非","category":"工具","views":"5.2K","likes":"689","description":"联机番茄钟自习室","targetUsers":"学生/自习人群","interactionMode":"工具/助手","tags":["工具效率","学习成长"]},
  {"id":"case022","name":"AI塔罗占卜师","author":"clover睿","category":"工具","views":"92.1K","likes":"8.9K","description":"AI塔罗牌解读与运势分析","targetUsers":"年轻女性","interactionMode":"工具/助手","tags":["工具效率","人格测试","AI原生"]},
  {"id":"case023","name":"三十天挑战打卡","author":"师法自然","category":"工具","views":"4.5K","likes":"567","description":"30天习惯养成打卡","targetUsers":"自律人群","interactionMode":"工具/助手","tags":["工具效率","社交互动"]},
  {"id":"case024","name":"声音日记本","author":"村长","category":"工具","views":"2.1K","likes":"334","description":"语音记录心情日记","targetUsers":"年轻人","interactionMode":"内容创作","tags":["内容创作","工具效率"]},
  {"id":"case025","name":"聊天记录年度报告","author":"黄啊码","category":"工具","views":"156.3K","likes":"12.3K","description":"微信聊天记录分析年报告","targetUsers":"所有人","interactionMode":"工具/助手","tags":["工具效率","社交互动","AI原生"]},
  {"id":"case026","name":"AI小说续写助手","author":"小枚","category":"工具","views":"8.9K","likes":"1.2K","description":"AI辅助小说创作","targetUsers":"写作者","interactionMode":"工具/助手","tags":["AI原生","内容创作"]},
  {"id":"case027","name":"毕业纪念册生成器","author":"也非","category":"工具","views":"34.5K","likes":"4.5K","description":"AI生成毕业纪念册","targetUsers":"毕业生","interactionMode":"图片生成","tags":["AI原生","社交互动"]},
  {"id":"case028","name":"游戏化待办清单","author":"师法自然","category":"工具","views":"7.8K","likes":"956","description":"打怪升级式待办管理","targetUsers":"年轻职场人","interactionMode":"工具/助手","tags":["学习成长","游戏互动","工具效率"]},
  {"id":"case029","name":"失物招领社区","author":"慎独","category":"工具","views":"1.6K","likes":"298","description":"社区失物招领互助平台","targetUsers":"社区居民","interactionMode":"工具/助手","tags":["工具效率","社交互动"]},
  {"id":"case030","name":"AI简历面试模拟","author":"黄啊码","category":"工具","views":"22.4K","likes":"2.8K","description":"AI面试官模拟练习","targetUsers":"求职者","interactionMode":"工具/助手","tags":["学习成长","AI原生","工具效率"]},
]

def call_llm(system_prompt, user_prompt):
    """调 DeepSeek API"""
    import urllib.request
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.deepseek.com/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {DEEPSEEK_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]

def match_cases(choices, llm_analysis):
    """基于选择题和LLM分析匹配案例"""
    tags_from_llm = set()
    if llm_analysis and "key_points" in llm_analysis:
        for kp in llm_analysis["key_points"]:
            for tag_group, tag_name in [
                (["学习","读书","阅读","教育","知识"], "学习成长"),
                (["游戏","闯关","互动","模拟","娱乐"], "游戏互动"),
                (["测试","人格","测评","心理"], "人格测试"),
                (["社交","互动","分享","社区","群组"], "社交互动"),
                (["工具","效率","助手","管理"], "工具效率"),
                (["创作","写作","内容","日记","笔记"], "内容创作"),
                (["AI","智能","生成","大模型"], "AI原生"),
            ]:
                if any(kw in kp for kw in tag_group):
                    tags_from_llm.add(tag_name)

    all_cases = load_cases()
    scored = []
    for c in all_cases:
        score = 0
        c_tags = set(c.get("tags", []))
        if tags_from_llm:
            score += len(tags_from_llm & c_tags) * 2
        q2 = choices.get("q2", "")
        if q2:
            q2_tag_map = {"创意生成型": "内容创作", "模拟互动型": "游戏互动",
                         "实用工具型": "工具效率", "社交传播型": "社交互动",
                         "内容展示型": "内容创作"}
            mapped = q2_tag_map.get(q2, "")
            if mapped in c_tags:
                score += 1
        scored.append((score, c))

    scored.sort(key=lambda x: -x[0])
    return [c for s, c in scored[:4] if s > 0] or all_cases[:3]

def generate_cards(choices, llm_analysis, matched_cases):
    """生成3张方向卡"""
    product_hint = ""
    if llm_analysis and "product_name_hint" in llm_analysis:
        product_hint = llm_analysis["product_name_hint"]

    all_cards = []

    card1_name = product_hint or "互动创意工具"
    card1 = {
        "title": card1_name,
        "recommend": "⭐⭐⭐⭐⭐",
        "difficulty": "低",
        "collision_risk": "中",
        "description": f"基于你的创意，推荐做一个{card1_name}。",
        "why_you": [
            llm_analysis.get("interaction", "交互简洁") if llm_analysis else "你的创意方向清晰，适合快速落地",
            f"参考案例「{matched_cases[0]['name']}」浏览量 {matched_cases[0]['views']}"
        ],
        "mvp": "最小版本：一个核心交互页 + 结果展示页，3页以内完成",
        "prompt": f"应用目标：{card1_name} 目标用户：{llm_analysis.get('target_users', '参赛者') if llm_analysis else '参赛者'} 核心流程：交互→结果 页面：3页以内 视觉风格：年轻活力、移动端优先"
    }
    all_cards.append(card1)

    card2_name = "轻量互动体验"
    all_cards.append({
        "title": card2_name,
        "recommend": "⭐⭐⭐⭐",
        "difficulty": "低",
        "collision_risk": "低",
        "description": "做一个轻量互动型应用，适合初次参赛。",
        "why_you": [
            "交互简单，技术门槛低",
            f"可参考「{matched_cases[1]['name'] if len(matched_cases) > 1 else matched_cases[0]['name']}」"
        ],
        "mvp": "单页交互+结果页，2页完成",
        "prompt": f"应用目标：{card2_name} 核心流程：用户操作→反馈结果 页面：2页 注意：当前为Demo版本"
    })

    card3_name = "内容创作工具"
    all_cards.append({
        "title": card3_name,
        "recommend": "⭐⭐⭐",
        "difficulty": "中",
        "collision_risk": "高",
        "description": "结合你的创意方向，做用户可参与内容创作的工具。",
        "why_you": [
            "有真实使用场景，容易做出差异化",
            "参考案例工具类应用浏览量普遍较高"
        ],
        "mvp": "一个内容编辑页+展示页，3页",
        "prompt": f"应用目标：{card3_name} 核心流程：输入→创作→输出 页面：3页 注意：当前为Demo版本"
    })

    return all_cards

def handler(event, context):
    """Netlify Function 主入口"""
    try:
        path = event.get("path", "")
        method = event.get("httpMethod", "GET")

        # CORS headers
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Content-Type": "application/json"
        }

        if method == "OPTIONS":
            return {"statusCode": 200, "headers": headers, "body": ""}

        # GET /api/cases - 查询案例库
        if method == "GET" and "cases" in path:
            all_cases = load_cases()
            # 支持搜索参数
            params = event.get("queryStringParameters") or {}
            category = params.get("category", "")
            keyword = params.get("keyword", "")
            tag = params.get("tag", "")

            results = all_cases
            if category:
                results = [c for c in results if c.get("category") == category]
            if keyword:
                kw = keyword.lower()
                results = [c for c in results if kw in json.dumps(c, ensure_ascii=False).lower()]
            if tag:
                results = [c for c in results if tag in c.get("tags", [])]

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"total": len(results), "cases": results}, ensure_ascii=False)
            }

        # POST /api/analyze - 问卷分析
        if method == "POST" and "analyze" in path:
            body = json.loads(event.get("body", "{}"))
            choices = body.get("choices", {})
            open_idea = body.get("open_idea", "")

            llm_analysis = None
            if open_idea and open_idea.strip():
                system_prompt = """你是一个参赛方向分析助手。请分析用户的创意描述，输出格式为 JSON：
{
  "theme": "核心主题（10字内）",
  "target_users": "目标用户（20字内）",
  "interaction": "核心交互方式（20字内）",
  "feeling": "作品给人的感觉",
  "key_points": ["关键特征1", "关键特征2", "关键特征3"],
  "product_name_hint": "建议的产品方向名称（10字左右，具体不模板化）"
}
只输出 JSON。"""
                llm_raw = call_llm(system_prompt, open_idea)
                json_match = re.search(r'\{.*\}', llm_raw, re.DOTALL)
                if json_match:
                    llm_analysis = json.loads(json_match.group())

            matched = match_cases(choices, llm_analysis)
            cards = generate_cards(choices, llm_analysis, matched)

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "llm_analysis": llm_analysis,
                    "matched_cases": matched,
                    "direction_cards": cards
                }, ensure_ascii=False, default=str)
            }

        return {"statusCode": 404, "headers": headers, "body": json.dumps({"error": "not found"})}

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}, ensure_ascii=False)
        }
