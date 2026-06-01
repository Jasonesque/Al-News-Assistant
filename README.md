# AI 个人新闻助手

这是一个自动化的新闻聚合与过滤工具，利用大语言模型 (LLM) 对最新的科技新闻进行智能打分、深度提炼，并将高价值的资讯直接推送到你的飞书 (Feishu) 工作区。

## 功能特性

*   **自动抓取 RSS**：自动获取全球顶级科技和 AI 媒体的最新动态。
*   **LLM 智能过滤与评分**：利用大模型阅读新闻，根据其对行业的影响力和相关性进行打分，精准剔除低价值的“噪音”。
*   **深度内容概括**：不仅生成简明扼要的核心摘要，还会详细解读该资讯对行业的实质性影响。
*   **飞书 Webhook 推送**：将排版精美的 Markdown 消息卡片无缝推送到飞书群组。
*   **完全自动化**：非常适合通过服务器的 Cron 任务或 Windows 任务计划程序实现每日无人值守运行。

## 环境依赖

*   Python 3.8+
*   一个兼容 OpenAI 格式的大模型 API Key（例如 OpenAI, DeepSeek, MIMO 等）
*   飞书自定义机器人的 Webhook URL

## 安装指南

1.  **克隆仓库**：
    ```bash
    git clone https://github.com/Jasonesque/Al-News-Assistant.git
    cd Al-News-Assistant
    ```

2.  **安装依赖**：
    ```bash
    pip install -r requirements.txt
    ```

3.  **配置环境变量**：
    在项目根目录创建一个 `.env` 文件，并参考以下模板进行配置（注：`.env` 已被 Git 忽略，你的敏感密钥绝对安全）：
    ```ini
    # 大模型 API 配置
    MIMO_API_KEY=你的_api_key
    MIMO_BASE_URL=https://api.your-llm-provider.com/v1
    MIMO_MODEL_NAME=你的_模型名称

    # 飞书 Webhook 配置
    FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/你的_webhook_id
    FEISHU_SECRET=你的_飞书_secret
    ```

## 使用说明

手动运行主程序：

```bash
python main.py
```

**自动化运行 (Windows)**

你可以使用项目中提供的 `run.bat` 脚本，配合“Windows 任务计划程序”，设置在每天的指定时间自动运行该助手。

## 开源协议

MIT License
