from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.stock_analyst.agent import stock_analyst
from .tools.tools import get_current_time

root_agent = Agent(
    name="manager",
    model="gemini-2.5-flash",
    description="Manager agent",
    instruction="""あなたは、他のエージェントの業務を監督する責任を持つ**マネージャーエージェント**です。

常に適切なエージェントにタスクを**委任**してください。
どのエージェントに委任するかは、あなたの最善の判断で決定してください。

あなたは以下のエージェントにタスクを委任する責任があります：

* `stock_analyst`（株式アナリスト）
* `funny_nerd`（面白オタク）

また、以下のツールにもアクセス可能です：

* `news_analyst`（ニュースアナリスト）
* `get_current_time`（現在時刻を取得）
""",
    # サブエージェントにタスクを移譲できる
    # 実際は `transfer_to_agent` というツールが呼ばれる
    sub_agents=[stock_analyst, funny_nerd],
    # ビルトインツールを使うサブエージェントはAgentToolで囲んでツールとみなす
    # sub_agentsにすると `Tool use with function calling is unsupported` というエラーが出る
    tools=[AgentTool(news_analyst), get_current_time],
)
