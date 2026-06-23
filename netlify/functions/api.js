// Netlify Function: 案例库 + LLM 分析接口
// 调 DeepSeek API（支持 GPT 级别中文理解）

const CASES = [
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
  {"id":"case030","name":"AI简历面试模拟","author":"黄啊码","category":"工具","views":"22.4K","likes":"2.8K","description":"AI面试官模拟练习","targetUsers":"求职者","interactionMode":"工具/助手","tags":["学习成长","AI原生","工具效率"]}
];

// —— CORS ——
const HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Content-Type": "application/json"
};

// —— DeepSeek API ——
async function callDeepSeek(systemPrompt, userPrompt) {
  const key = process.env.DEEPSEEK_API_KEY;
  if (!key) throw new Error("DEEPSEEK_API_KEY not configured");

  const resp = await fetch("https://api.deepseek.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${key}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "deepseek-chat",
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt }
      ],
      temperature: 0.7,
      max_tokens: 2000
    })
  });

  const data = await resp.json();
  return data.choices[0].message.content;
}

// —— 案例匹配 ——
function matchCases(choices, llmAnalysis) {
  const tagsFromLLM = new Set();
  if (llmAnalysis && llmAnalysis.key_points) {
    const TAG_MAP = {
      "学习成长": ["学习","读书","阅读","教育","知识","课程"],
      "游戏互动": ["游戏","闯关","互动","模拟","角色"],
      "人格测试": ["人格","测试","测评","MBTI","心理"],
      "社交互动": ["社交","分享","社区","交友"],
      "工具效率": ["工具","效率","助手","管理"],
      "内容创作": ["创作","写作","内容","日记","笔记"],
      "AI原生": ["AI","智能","生成","大模型"]
    };
    for (const kp of llmAnalysis.key_points) {
      for (const [tag, kws] of Object.entries(TAG_MAP)) {
        if (kws.some(kw => kp.includes(kw))) tagsFromLLM.add(tag);
      }
    }
  }

  const q2 = choices.q2 || "";
  const Q2_MAP = {
    "创意生成型": "内容创作",
    "模拟互动型": "游戏互动",
    "实用工具型": "工具效率",
    "社交传播型": "社交互动"
  };
  if (Q2_MAP[q2]) tagsFromLLM.add(Q2_MAP[q2]);

  const scored = CASES.map(c => {
    let score = 0;
    const cTags = new Set(c.tags || []);
    tagsFromLLM.forEach(tag => { if (cTags.has(tag)) score += 2; });
    if (Q2_MAP[q2] && cTags.has(Q2_MAP[q2])) score += 1;
    return { score, c };
  });

  scored.sort((a, b) => b.score - a.score);
  const top = scored.filter(s => s.score > 0).map(s => s.c);
  return top.length > 0 ? top.slice(0, 4) : CASES.slice(0, 3);
}

// —— 方向卡生成（带 LLM） ——
async function generateCards(choices, llmAnalysis, matchedCases) {
  const hint = llmAnalysis?.product_name_hint || "互动创意工具";
  const target = llmAnalysis?.target_users || "参赛者";
  const interaction = llmAnalysis?.interaction || "交互体验";

  return [
    {
      title: hint,
      recommend: "⭐⭐⭐⭐⭐",
      difficulty: "低",
      collision_risk: "中",
      description: `基于你的创意，推荐做一个${hint}。`,
      why_you: [
        `${interaction}，适合你的方向`,
        matchedCases.length > 0 ? `参考案例「${matchedCases[0].name}」浏览量 ${matchedCases[0].views}` : "创意方向清晰，适合快速落地"
      ],
      mvp: "最小版本：一个核心交互页 + 结果展示页，3页以内完成",
      prompt: `应用目标：${hint} 目标用户：${target} 核心流程：交互→结果 页面：3页以内 视觉风格：年轻活力、移动端优先`
    },
    {
      title: "轻量互动体验",
      recommend: "⭐⭐⭐⭐",
      difficulty: "低",
      collision_risk: "低",
      description: "做一个轻量互动型应用，适合初次参赛。",
      why_you: ["交互简单，技术门槛低", matchedCases.length > 1 ? `可参考「${matchedCases[1].name}」` : "适合快速验证想法"],
      mvp: "单页交互+结果页，2页完成",
      prompt: "应用目标：轻量互动体验 核心流程：用户操作→反馈结果 页面：2页"
    },
    {
      title: "内容创作工具",
      recommend: "⭐⭐⭐",
      difficulty: "中",
      collision_risk: "高",
      description: "结合你的创意方向，做用户可参与内容创作的工具。",
      why_you: ["有真实使用场景，容易做出差异化", "参考案例工具类应用浏览量普遍较高"],
      mvp: "一个内容编辑页+展示页，3页",
      prompt: "应用目标：内容创作工具 核心流程：输入→创作→输出 页面：3页"
    }
  ];
}

// —— Handler ——
exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 200, headers: HEADERS, body: "" };
  }

  try {
    const path = event.path;

    // GET /api/cases
    if (event.httpMethod === "GET" && path.includes("cases")) {
      const params = event.queryStringParameters || {};
      let results = [...CASES];

      if (params.category) results = results.filter(c => c.category === params.category);
      if (params.tag) results = results.filter(c => (c.tags || []).includes(params.tag));
      if (params.keyword) {
        const kw = params.keyword.toLowerCase();
        results = results.filter(c =>
          c.name.toLowerCase().includes(kw) ||
          c.description.toLowerCase().includes(kw) ||
          (c.tags || []).some(t => t.includes(kw))
        );
      }

      results.sort((a, b) => (parseInt(b.views) || 0) - (parseInt(a.views) || 0));

      return {
        statusCode: 200,
        headers: HEADERS,
        body: JSON.stringify({ total: results.length, cases: results })
      };
    }

    // POST /api/analyze
    if (event.httpMethod === "POST" && path.includes("analyze")) {
      const body = JSON.parse(event.body || "{}");
      const choices = body.choices || {};
      const openIdea = body.open_idea || "";

      // LLM 分析开放题
      let llmAnalysis = null;
      if (openIdea && openIdea.trim()) {
        try {
          const systemPrompt = `你是一个参赛方向分析助手。请分析用户的创意描述，输出格式为 JSON：
{
  "theme": "核心主题（10字内）",
  "target_users": "目标用户（20字内）",
  "interaction": "核心交互方式（20字内）",
  "feeling": "作品给人的感觉",
  "key_points": ["关键特征1", "关键特征2", "关键特征3"],
  "product_name_hint": "建议的产品方向名称（10字左右，具体不模板化）"
}
只输出 JSON，不要其他内容。`;

          const llmRaw = await callDeepSeek(systemPrompt, openIdea);
          const jsonMatch = llmRaw.match(/\{.*\}/s);
          if (jsonMatch) {
            llmAnalysis = JSON.parse(jsonMatch[0]);
          }
        } catch (e) {
          // LLM 失败时用规则降级
          console.log("LLM error:", e.message);
        }
      }

      const matched = matchCases(choices, llmAnalysis);
      const cards = await generateCards(choices, llmAnalysis, matched);

      return {
        statusCode: 200,
        headers: HEADERS,
        body: JSON.stringify({
          llm_analysis: llmAnalysis,
          matched_cases: matched,
          direction_cards: cards
        })
      };
    }

    return { statusCode: 404, headers: HEADERS, body: JSON.stringify({ error: "not found" }) };
  } catch (e) {
    return {
      statusCode: 500,
      headers: HEADERS,
      body: JSON.stringify({ error: e.message })
    };
  }
};
