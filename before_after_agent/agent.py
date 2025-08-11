from datetime import datetime
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types


def before_agent_callback(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    state = callback_context.state
    timestamp = datetime.now()

    # setup state
    if "agent_name" not in state:
        state["agent_name"] = "SimpleChatBot"

    if "request_counter" not in state:
        state["request_counter"] = 1
    else:
        state["request_counter"] += 1

    state["request_start_time"] = timestamp

    # Log the request
    print("=== AGENT EXECUTION STARTED ===")
    print(f"Request #: {state['request_counter']}")
    print(f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    # Print to console
    print(f"\n[BEFORE CALLBACK] Agent processing request #{state['request_counter']}")

    return None


def after_agent_callback(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    state = callback_context.state
    timestamp = datetime.now()
    duration = None
    if "request_start_time" in state:
        duration = (timestamp - state["request_start_time"]).total_seconds()

    # Log the completion
    print("=== AGENT EXECUTION COMPLETED ===")
    print(f"Request #: {state.get('request_counter', 'Unknown')}")
    if duration is not None:
        print(f"Duration: {duration:.2f} seconds")

    # Print to console
    print(
        f"[AFTER CALLBACK] Agent completed request #{state.get('request_counter', 'Unknown')}"
    )
    if duration is not None:
        print(f"[AFTER CALLBACK] Processing took {duration:.2f} seconds")

    return None


root_agent = LlmAgent(
    name="before_after_agent",
    model="gemini-2.5-flash",
    description="A basic agent that demonstrates before and after agent callbacks",
    instruction="""あなたは親しみやすい挨拶エージェントです。あなたの名前は {agent_name} です。

あなたの仕事は次のとおりです：
- 利用者に丁寧に挨拶する
- 基本的な質問に答える
- 応答を親しみやすく簡潔に保つ
""",
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)
