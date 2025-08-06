import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# LiteLlmを使うことで任意のプロバイダーのLLMを使うことができる
model = LiteLlm(
    model="openrouter/openai/gpt-4.1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def get_dad_joke():
    """Get a random dad joke."""
    jokes = [
        "なぜ骸骨たちはケンカしないの？ 根性（内臓）がないからさ。",
        "昔は耳でピアノを弾いてたけど、今はちゃんと手で弾いてるよ。",
        "偽物のスパゲッティって何て呼ぶか知ってる？ インパスタだよ！",
        "なんでカカシは賞をもらったの？ 畑で“抜群”の働きをしてたからさ。",
        "エレベーターのジョークを言おうかと思ったけど…持ち上がる話だからね。",
    ]
    return random.choice(jokes)


root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="Dad joke agent",
    instruction="""You are a helpful assistant that tell dad jokes.""",
    tools=[get_dad_joke],
)
