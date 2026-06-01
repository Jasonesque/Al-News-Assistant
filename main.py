from fetcher import fetch_news
from analyzer import filter_and_analyze
from pusher import push_to_feishu

def main():
    print("=== AI News Assistant Started ===")
    
    # 1. 获取新闻
    print("\n[1/3] Fetching news from RSS feeds...")
    raw_news = fetch_news(max_items_per_feed=3) # 为了测试速度，每个源只取前 3 条最新新闻
    print(f"Fetched {len(raw_news)} raw news items.")
    
    if not raw_news:
        print("No news fetched. Exiting.")
        return
        
    # 2. AI 分析和过滤
    print("\n[2/3] Analyzing and scoring news using MIMO AI...")
    # 过滤综合评分 7 分以上的新闻
    high_impact_news = filter_and_analyze(raw_news, threshold=7)
    print(f"Found {len(high_impact_news)} high impact news items (score >= 7).")
    
    # 3. 飞书推送
    print("\n[3/3] Pushing to Feishu...")
    # 为了避免卡片过长，只推送得分最高的 Top 5
    push_to_feishu(high_impact_news[:5])
    
    print("\n=== Done ===")

if __name__ == "__main__":
    main()
