import feedparser
import re
from typing import List, Dict

# 预置的高质量 RSS 信源
DEFAULT_FEEDS = [
    # 机器之心 (国内优质 AI 深度媒体，聚焦大事件和前沿研究)
    {"name": "机器之心", "url": "https://www.jiqizhixin.com/rss"},
    # TechCrunch AI (全球顶级科技媒体，聚焦大公司动态、融资和重要发布)
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    # 谷歌新闻 - 全球 AI 产品与大模型动态聚合
    {"name": "Google News (AI PM)", "url": "https://news.google.com/rss/search?q=%22%E5%A4%A7%E6%A8%A1%E5%9E%8B%22+OR+%22AI%E4%BA%A7%E5%93%81%22+OR+%22AI+Agent%22+OR+%22%E7%94%9F%E6%88%90%E5%BC%8F+AI%22+OR+%22AIGC%22&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"}
]

def clean_html(raw_html: str) -> str:
    """清理 HTML 标签，保留纯文本"""
    if not raw_html:
        return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

def fetch_news(feeds: List[Dict[str, str]] = None, max_items_per_feed: int = 5) -> List[Dict]:
    """获取 RSS 新闻"""
    if feeds is None:
        feeds = DEFAULT_FEEDS
    
    news_items = []
    
    for feed_info in feeds:
        print(f"Fetching news from: {feed_info['name']}")
        try:
            feed = feedparser.parse(feed_info["url"])
            
            for entry in feed.entries[:max_items_per_feed]:
                title = entry.get('title', 'No Title')
                link = entry.get('link', '')
                summary = clean_html(entry.get('summary', '') or entry.get('description', ''))
                
                if len(summary) > 800:
                    summary = summary[:800] + "..."
                    
                news_items.append({
                    "source": feed_info["name"],
                    "title": title,
                    "link": link,
                    "summary": summary
                })
        except Exception as e:
            print(f"Error fetching {feed_info['name']}: {e}")
            
    return news_items

if __name__ == "__main__":
    # 简单测试测试
    news = fetch_news()
    print(f"Fetched {len(news)} news items.")
    for n in news[:2]:
        print(n)
