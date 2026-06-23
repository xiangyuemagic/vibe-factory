#!/usr/bin/env python3
"""
Vibe Coding 造星工厂 - 本地版后端
基于 Flask + DeepSeek LLM 的参赛方向决策工具
"""

import os, json, sys
from flask import Flask, request, jsonify, send_from_directory

# ---- DeepSeek LLM Client ----
env_path = os.path.expanduser("~/.hermes/.env")
DEEPSEEK_KEY = ""
with open(env_path) as f:
    for line in f:
        s = line.strip()
        if s.startswith("DEEPSEEK_API_KEY=") and not s.startswith("#"):
            DEEPSEEK_KEY = s.split("=", 1)[1].strip().strip('"').strip("'")
            break

def call_llm(system_prompt, user_prompt):
    import urllib.request, urllib.error
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

# ---- Built-in Case Library ----
CASE_LIBRARY = [
  {"id":"case001","name":"油气井生产优化设计系统","author":"村长","category":"工具","views":"116.6K","likes":"3.4K","description":"油气井生产优化设计专用工具","targetUsers":"工业从业者","interactionMode":"工具/助手","tags":["工具效率"]},
  {"id":"case002","name":"星途｜爱豆人生模拟器","author":"师法自然","category":"游戏","views":"24.3K","likes":"2.7K","description":"模拟偶像养成路线，生成专属爱豆人生剧本","targetUsers":"追星族、Z世代年轻人","interactionMode":"模拟器/沙盒","tags":["人格测试","游戏互动"]},
  {"id":"case003","name":"粽遇父爱 · 秒哒寄温情","author":"秒哒官方","category":"推荐","views":"2.8K","likes":"569","description":"端午节+父爱主题温情互动应用","targetUsers":"节日用户","interactionMode":"信息展示","tags":["社交互动","内容创作"]},
  {"id":"case004","name":"海王套路识别模拟器（校园慎用版）","author":"爽朗的琳紫","category":"游戏","views":"24.7K","likes":"522","description":"模拟海王套路识别，娱乐互动教学","targetUsers":"校园年轻人","interactionMode":"模拟器/沙盒","tags":["游戏互动","社交互动"]},
  {"id":"case005","name":"退休魔女的开荒日记","author":"爽朗的琳紫","category":"游戏","views":"13.5K","likes":"1.2K","description":"叙事驱动的冒险日记互动","targetUsers":"轻小说/游戏爱好者","interactionMode":"内容创作","tags":["内容创作","游戏互动"]},
  {"id":"case006","name":"FBTI看球人格测试","author":"也非","category":"问卷","views":"3.5K","likes":"594","description":"看球风格人格测试，球迷版MBTI","targetUsers":"球迷群体","interactionMode":"问卷调查","tags":["人格测试","社交互动"]},
  {"id":"case007","name":"端午渔趣·粽钓江南","author":"慎独","category":"游戏","views":"2K","likes":"525","description":"端午节主题小游戏","targetUsers":"节日用户","interactionMode":"闯关/游戏","tags":["游戏互动"]},
  {"id":"case008","name":"码上制片厂","author":"黄啊码","category":"工具","views":"26.9K","likes":"765","description":"开发者内容制作工具","targetUsers":"开发者/内容创作者","interactionMode":"工具/助手","tags":["工具效率","内容创作"]},
  {"id":"case009","name":"出轨模拟器","author":"爽朗的琳紫","category":"游戏","views":"5.9K","likes":"583","description":"情感话题互动模拟器","targetUsers":"年轻人","interactionMode":"模拟器/沙盒","tags":["情感心理","社交互动"]},
  {"id":"case010","name":"龙虾像素空间","author":"爽朗的琳紫","category":"游戏","views":"15.8K","likes":"723","description":"像素风格虚拟空间探索","targetUsers":"像素游戏爱好者","interactionMode":"闯关/游戏","tags":["游戏互动"]},
  {"id":"case011","name":"【可复制】Offer神器","author":"小枚","category":"工具","views":"1.3K","likes":"443","description":"求职面试辅助工具","targetUsers":"求职者/应届生","interactionMode":"工具/助手","tags":["工具效率","学习成长"]},
  {"id":"case012","name":"全家福生成器","author":"clover睿","category":"推荐","views":"152.4K","likes":"838","description":"AI生成全家福合影，满足异地过年团圆需求","targetUsers":"异地过年人群","interactionMode":"图片生成","tags":["AI原生","社交互动"]}
]

# ---- Flask App ----
app = Flask(__name__, static_url_path="", static_folder="static")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """接受问卷答案 + 开放题，返回画像分析、匹配案例、方向卡"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400
    
    choices = data.get("choices", {})
    open_idea = data.get("open_idea", "")
    
    # 1. 用 LLM 分析开放题
    llm_analysis = None
    if open_idea and open_idea.strip():
        try:
            system_prompt = """你是一个参赛方向分析助手。请分析用户的创意描述，输出格式为 JSON：
{
  "theme": "核心主题（10字内）",
  "target_users": "目标用户（20字内）", 
  "interaction": "核心交互方式（20字内）",
  "feeling": "作品给人的感觉（好玩/有用/有故事/治愈等）",
  "key_points": ["关键特征1", "关键特征2", "关键特征3"],
  "product_name_hint": "建议的产品方向名称（10字左右，具体，不模板化）"
}
只输出 JSON，不要其他内容。"""
            llm_raw = call_llm(system_prompt, open_idea)
            # 尝试解析 JSON
            import re
            json_match = re.search(r'\{.*\}', llm_raw, re.DOTALL)
            if json_match:
                llm_analysis = json.loads(json_match.group())
        except Exception as e:
            llm_analysis = {"error": str(e)}
    
    # 2. 匹配案例
    matched_cases = match_cases(choices, llm_analysis)
    
    # 3. 生成方向卡（用 LLM）
    direction_cards = generate_cards(choices, llm_analysis, matched_cases)
    
    return jsonify({
        "llm_analysis": llm_analysis,
        "matched_cases": matched_cases,
        "direction_cards": direction_cards
    })

def match_cases(choices, llm_analysis):
    """基于选择题和LLM分析匹配案例"""
    # 简单规则匹配：根据 Q2(作品类型) 和 LLM 分析的标签
    tags_from_llm = set()
    if llm_analysis and "key_points" in llm_analysis:
        for kp in llm_analysis["key_points"]:
            for tag_group in [["学习","读书","阅读","教育","知识"], ["游戏","闯关","互动","模拟"], 
                            ["测试","人格","测评"], ["社交","互动","分享"], ["工具","效率","助手"],
                            ["创作","写作","内容"], ["AI","智能","生成"]]:
                if any(kw in kp for kw in tag_group):
                    tag_map = {"学习":"学习成长","游戏":"游戏互动","测试":"人格测试",
                              "社交":"社交互动","工具":"工具效率","创作":"内容创作","AI":"AI原生"}
                    for k,v in tag_map.items():
                        if k == tag_group[0]:
                            tags_from_llm.add(v)
    
    # 按标签匹配
    scored = []
    for c in CASE_LIBRARY:
        score = 0
        c_tags = set(c.get("tags", []))
        if tags_from_llm:
            score += len(tags_from_llm & c_tags) * 2
        # Choice-based matching
        q2 = choices.get("q2", "")
        if q2:
            q2_tag_map = {"创意生成型":"内容创作", "模拟互动型":"游戏互动", 
                         "实用工具型":"工具效率", "社交传播型":"社交互动",
                         "内容展示型":"内容创作"}
            mapped = q2_tag_map.get(q2, "")
            if mapped in c_tags:
                score += 1
        scored.append((score, c))
    
    scored.sort(key=lambda x: -x[0])
    return [c for s, c in scored[:4] if s > 0] or CASE_LIBRARY[:3]

def generate_cards(choices, llm_analysis, matched_cases):
    """生成3张方向卡"""
    product_hint = ""
    if llm_analysis and "product_name_hint" in llm_analysis:
        product_hint = llm_analysis["product_name_hint"]
    
    all_cards = []
    
    # 卡1：最推荐
    card1_name = product_hint or "互动创意工具"
    card1 = {
        "title": card1_name,
        "recommend": "⭐⭐⭐⭐⭐",
        "difficulty": "低",
        "collision_risk": "中",
        "description": f"基于你的创意，推荐做一个{card1_name}。",
        "why_you": [
            llm_analysis.get("interaction", "交互简洁") if llm_analysis else "你的创意方向清晰，适合快速落地",
            f"参考案例「{matched_cases[0]['name']}」浏览量 {matched_cases[0]['views']}，交互模式可借鉴"
        ],
        "mvp": "最小版本：一个核心交互页 + 结果展示页，3页以内完成",
        "prompt": f"应用目标：{card1_name}\n目标用户：{llm_analysis.get('target_users', '参赛者') if llm_analysis else '参赛者'}\n核心流程：\n1. 用户进入了解功能\n2. 核心交互操作\n3. 展示结果\n页面结构（3页以内）：\n- 首页：功能介绍\n- 核心页：主要交互区域\n- 结果页：展示和分享\n视觉风格：年轻活力、移动端优先\n注意：当前为Demo版本"
    }
    all_cards.append(card1)
    
    # 卡2：稳妥方向
    all_cards.append({
        "title": "轻量互动体验",
        "recommend": "⭐⭐⭐⭐",
        "difficulty": "低",
        "collision_risk": "低",
        "description": "做一个轻量互动型应用，适合初次参赛，完成度高。",
        "why_you": [
            "交互简单，技术门槛低",
            f"可参考案例「{matched_cases[1]['name'] if len(matched_cases) > 1 else matched_cases[0]['name']}」"
        ],
        "mvp": "单页交互+结果页，2页完成",
        "prompt": "应用目标：轻量互动体验\n目标用户：大众用户\n核心流程：用户操作→反馈结果\n页面结构：首页+结果页\n视觉风格：简洁卡通风\n注意：当前为Demo版本"
    })
    
    # 卡3：潜力方向
    all_cards.append({
        "title": "内容创作工具",
        "recommend": "⭐⭐⭐",
        "difficulty": "中",
        "collision_risk": "高",
        "description": "结合你的创意方向，做一个用户可参与内容创作的工具。",
        "why_you": [
            "有真实使用场景，容易做出差异化",
            "参考案例工具类应用浏览量普遍较高"
        ],
        "mvp": "一个内容编辑页+展示页，3页",
        "prompt": "应用目标：内容创作工具\n目标用户：内容创作者\n核心流程：输入→创作→输出\n页面结构：输入页+编辑页+成果展示页\n视觉风格：干净专业风\n注意：当前为Demo版本"
    })
    
    return all_cards

@app.route("/api/cases", methods=["GET"])
def get_cases():
    return jsonify(CASE_LIBRARY)

if __name__ == "__main__":
    print("Starting server at http://127.0.0.1:5000")
    print("DeepSeek Key:", DEEPSEEK_KEY[:10] + "..." if DEEPSEEK_KEY else "NOT FOUND")
    app.run(debug=True, port=5000)
