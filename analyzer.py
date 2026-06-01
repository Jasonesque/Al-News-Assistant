import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MIMO_API_KEY = os.getenv("MIMO_API_KEY")
MIMO_BASE_URL = os.getenv("MIMO_BASE_URL")
MIMO_MODEL_NAME = os.getenv("MIMO_MODEL_NAME", "mimo-v2.5")

client = OpenAI(
    api_key=MIMO_API_KEY,
    base_url=MIMO_BASE_URL
)

def evaluate_news(news_item: dict) -> dict:
    """使用大模型对新闻进行评分和总结"""
    
    prompt = f"""
你是一个高度专业的大厂 AI 产品专家。你的任务是为一位资深的【AI产品经理】过滤、提炼全球每天海量的 AI 资讯，只呈现最有商业价值和产品指导意义的“干货”。
请阅读以下新闻，判断其是否值得推送，并进行综合打分（1-10分）。

【高分标准】（AI产品经理最关心的核心干货）
1. 全球及国内所有主流 AI 公司（不仅限于头部大厂，也包括极具潜力的 AI 独角兽和底层模型公司）的重大商业化进展、产品发布或战略方向调整。
2. 大模型（LLM）的重大能力飞跃、多模态演进、API 降价或商业模式创新。
3. AI Agent（智能体）以及 AI Native 应用的最佳实践、新交互范式或落地案例。
4. 能够直接影响 AI 产品规划、用户体验设计、商业化落地或个人效率的实质性更新。

【低分过滤】
偏向底层的晦涩学术论文（除非引发技术革命）、纯个人开发者的玩具项目、标题党炒作、没有实质产品落地的八卦传闻，请直接打低分（1-3分）。

如果符合高分标准，请提取核心摘要，并以 AI 产品经理的视角，提炼这篇新闻的干货与启示。

新闻来源: {news_item['source']}
新闻标题: {news_item['title']}
新闻摘要: {news_item['summary']}

请严格以 JSON 格式输出结果，不要输出任何其他内容。格式要求如下：
{{
    "score": 8,
    "zh_summary": "一句话简明扼要的核心摘要，直击痛点。",
    "zh_details": "详细的中文干货概括。必须包含两个部分：1. 这则新闻到底发布了什么实质性内容；2. 【PM视角解读】：作为AI产品经理，这则资讯对产品策略、交互设计或行业趋势有什么启发和影响？"
}}
注意：score请给出一个综合评分(1-10的整数)。
"""

    try:
        response = client.chat.completions.create(
            model=MIMO_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful AI news analyst. Always output valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        result_content = response.choices[0].message.content
        # 清理可能包含的 markdown json 标记
        if result_content.startswith("```json"):
            result_content = result_content.replace("```json", "", 1)
            if result_content.endswith("```"):
                result_content = result_content[:-3]
                
        result_json = json.loads(result_content.strip())
        
        return {
            **news_item,
            "score": result_json.get("score", 0),
            "zh_summary": result_json.get("zh_summary", news_item['title']),
            "zh_details": result_json.get("zh_details", "")
        }
    except Exception as e:
        print(f"Error evaluating news '{news_item['title']}': {e}")
        return {
            **news_item,
            "score": 0,
            "zh_summary": news_item['title'],
            "zh_details": ""
        }

def filter_and_analyze(news_list: list, threshold: int = 7) -> list:
    """过滤并分析新闻列表，只返回高分内容"""
    analyzed_news = []
    for i, item in enumerate(news_list):
        print(f"Analyzing {i+1}/{len(news_list)}: {item['title'][:30]}...")
        result = evaluate_news(item)
        if result["score"] >= threshold:
            analyzed_news.append(result)
            
    # 按分数降序排序
    return sorted(analyzed_news, key=lambda x: x["score"], reverse=True)
