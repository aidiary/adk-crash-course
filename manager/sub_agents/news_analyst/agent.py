from google.adk.agents import Agent
from google.adk.tools import google_search

news_analyst = Agent(
    name="news_analyst",
    model="gemini-2.5-flash",
    description="News analyst agent",
    instruction="""あなたはニュース記事を分析し、その要約を提供できる有能なアシスタントです。

ニュースについて尋ねられた場合、`google_search` ツールを使用してニュースを検索してください。

ユーザーが相対的な時間（例：「最近のニュース」「今朝のニュース」など）を使ってニュースを求めた場合は、`get_current_time` ツールを使って現在の時刻を取得し、それを検索クエリに活用してください。
""",
    tools=[google_search],
)
