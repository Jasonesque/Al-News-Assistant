# AI News Assistant

An automated news aggregator and filter that leverages Large Language Models (LLMs) to score, summarize, and push high-quality tech news directly to your Feishu (Lark) workspace.

## Features

*   **Automated RSS Fetching**: Pulls the latest articles from top-tier tech and AI news sources.
*   **LLM-Powered Filtering & Scoring**: Uses an LLM to read through news summaries, score them based on their impact and relevance to the industry, and filter out low-value noise.
*   **Smart Summarization**: Generates a concise core summary and a detailed explanation of the news impact.
*   **Feishu Webhook Integration**: Pushes beautifully formatted Markdown message cards to your Feishu group.
*   **Fully Automated**: Designed to be run via a daily cron job or Windows Task Scheduler.

## Prerequisites

*   Python 3.8+
*   An OpenAI-compatible LLM API Key (e.g., OpenAI, DeepSeek, MIMO, etc.)
*   A Feishu Custom Bot Webhook URL

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Jasonesque/Al-News-Assistant.git
    cd Al-News-Assistant
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables Setup**:
    Create a `.env` file in the root directory and configure it. (Note: `.env` is ignored by Git to protect your secrets).
    ```ini
    # LLM API Configuration
    MIMO_API_KEY=your_api_key_here
    MIMO_BASE_URL=https://api.your-llm-provider.com/v1
    MIMO_MODEL_NAME=your_model_name

    # Feishu Webhook Configuration
    FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your_webhook_id
    FEISHU_SECRET=your_feishu_secret_here
    ```

## Usage

Run the main script manually:

```bash
python main.py
```

**Automating the Script (Windows)**

You can use the included `run.bat` script with the Windows Task Scheduler to run the assistant daily at a specific time.

## License

MIT License
