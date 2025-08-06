import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from question_answering_agent import question_answering_agent

load_dotenv()


session_service_stateful = InMemorySessionService()

# ここで定義した状態はエージェントのinstructionのプレースホルダに挿入される
initial_state = {
    "user_name": "mori",
    "user_preferences": """AIエンジニアとして働いています。好きな食べ物はかつ丼です。好きなテレビ番組はGame of Thronesです。趣味はプログラミングと読書です。""",
}


# 新しいセッションを作成
APP_NAME = "Chatbot"
USER_ID = "mori"
SESSION_ID = str(uuid.uuid4())


async def run_agent():
    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )
    print("CREATED NEW SESSION:")
    print(f"\tSession ID: {SESSION_ID}")
    print(f"\tState: {stateful_session}")

    # エージェントを動かすのに必要なRunnerを作成
    runner = Runner(
        agent=question_answering_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    # ユーザーからの新しいメッセージを作成
    new_message = types.Content(
        role="user", parts=[types.Part(text="moriの好きなテレビ番組は？")]
    )

    # LangGraphのイベントループのようなもの（session_id = thread_id）
    # ストリームで出力するにはどうする？
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Final Response: {event.content.parts[0].text}")

    print("==== Session Event Exploration ====")
    session = await session_service_stateful.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    # セッションの状態を表示
    print("==== Final Session State ====")
    for key, value in session.state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_agent())
