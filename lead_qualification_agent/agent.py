from google.adk.agents import SequentialAgent

from .subagents.recommender import action_recommender_agent
from .subagents.scorer import lead_scorer_agent
from .subagents.validator import lead_validator_agent

root_agent = SequentialAgent(
    name="LeadQualificationPipeline",
    # ここで指定した順番にサブエージェントを呼び出す
    # エージェント間の情報共有はメッセージ履歴や状態を介して行われる
    sub_agents=[lead_validator_agent, lead_scorer_agent, action_recommender_agent],
    description="A pipeline that validates, scores, and recommends actions for sales leads",
)
