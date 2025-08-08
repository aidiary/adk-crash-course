from datetime import datetime

import yfinance as yf
from google.adk.agents import Agent


def get_stock_price(ticker: str) -> dict:
    """Retrieves current stock price and saves to session state."""
    print(f"--- Tool: get_stock_price called for {ticker} ---")

    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice")

        if current_price is None:
            return {
                "status": "error",
                "error_message": f"Could not fetch price for {ticker}",
            }

        # Get current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "status": "success",
            "ticker": ticker,
            "price": current_price,
            "timestamp": current_time,
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching stock data: {str(e)}",
        }


stock_analyst = Agent(
    name="stock_analyst",
    model="gemini-2.5-flash",
    description="An agent that can look up stock prices and track them over time.",
    instruction="""あなたは、ユーザーが関心のある株式を追跡するのを手助けする、有能な株式市場アシスタントです。

株価について尋ねられた場合には、次の手順に従ってください：

1. `get_stock_price` ツールを使用して、リクエストされた株式の最新価格を取得してください
2. 各株の現在の価格と取得時間を表示するように、レスポンスを整形してください
3. 株価を取得できなかった場合は、そのことをレスポンス内で明示してください

**レスポンスの例（形式）：**

「現在の株価はこちらです：

* GOOG: \$175.34（2024-04-21 16:30:00 に更新）
* TSLA: \$156.78（2024-04-21 16:30:00 に更新）
* META: \$123.45（2024-04-21 16:30:00 に更新）」
""",
    tools=[get_stock_price],
)
