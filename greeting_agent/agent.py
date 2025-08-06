from google.adk.agents import Agent

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.5-flash",
    description="Grreeting agent",
    instruction="""
    あなたは親切なアシスタントです。
    ユーザーに名前を尋ね、その名前で挨拶してください。
    """,
)
