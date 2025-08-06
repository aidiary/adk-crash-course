from google.adk.agents import Agent

# instructionのプレースホルダには状態から値が挿入される
question_answering_agent = Agent(
    name="question_answering_agent",
    model="gemini-2.5-flash",
    description="Question answering agent",
    instruction="""
    あなたはユーザーの好みに関する質問に答える、親切なアシスタントです。

    以下はユーザーに関する情報です：
    名前：
    {user_name}
    好み：
    {user_preferences}
    """,
)
