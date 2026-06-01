import time
import hmac
import hashlib
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")
FEISHU_SECRET = os.getenv("FEISHU_SECRET")

def gen_sign(timestamp, secret):
    """生成飞书 Webhook 签名"""
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign

def push_to_feishu(news_list: list):
    """将新闻推送到飞书"""
    if not FEISHU_WEBHOOK_URL:
        print("Error: FEISHU_WEBHOOK_URL not set in .env")
        return
        
    if not news_list:
        print("No high-impact news to push today.")
        return

    timestamp = str(int(time.time()))
    
    # 组装飞书卡片 (Message Card)
    elements = []
    for i, item in enumerate(news_list):
        emoji = "🥇" if i == 0 else ("🥈" if i == 1 else "📰")
        
        # 标题
        elements.append({
            "tag": "markdown",
            "content": f"**{emoji} [{item['title']}]({item['link']})**"
        })
        # 核心摘要
        elements.append({
            "tag": "markdown",
            "content": f"🎯 **核心摘要**: {item['zh_summary']}"
        })
        # 详细影响和来源
        elements.append({
            "tag": "markdown",
            "content": f"📝 **详细解读与影响**: {item.get('zh_details', '')}\n\n*来源: {item['source']}*"
        })
        # 分割线
        if i < len(news_list) - 1:
            elements.append({"tag": "hr"})
            
    # 底部说明
    elements.append({"tag": "hr"})
    elements.append({
        "tag": "note",
        "elements": [
            {
                "tag": "plain_text",
                "content": "🤖 由 AI News Assistant 自动聚合与打分分析"
            }
        ]
    })

    card = {
        "header": {
            "template": "blue",
            "title": {
                "content": "📰 今日高价值 AI 资讯速递",
                "tag": "plain_text"
            }
        },
        "elements": elements
    }

    body = {
        "msg_type": "interactive",
        "card": card
    }

    if FEISHU_SECRET:
        body["timestamp"] = timestamp
        body["sign"] = gen_sign(timestamp, FEISHU_SECRET)

    try:
        response = requests.post(FEISHU_WEBHOOK_URL, json=body)
        print(f"Feishu response: {response.text}")
    except Exception as e:
        print(f"Error pushing to Feishu: {e}")
