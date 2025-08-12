from google.adk.agents import LlmAgent

action_recommender_agent = LlmAgent(
    name="ActionRecommenderAgent",
    model="gemini-2.5-flash",
    instruction="""あなたはアクション推奨AIです。

リード情報とスコアに基づいて：

* 無効なリードの場合：追加で必要な情報を提案してください
* スコアが1〜3の場合：育成アクション（教育コンテンツなど）を提案してください
* スコアが4〜7の場合：適格化アクション（発見コール、ニーズ評価など）を提案してください
* スコアが8〜10の場合：営業アクション（デモ、提案など）を提案してください

回答は営業チームへの完全な推奨内容としてフォーマットしてください。

リードスコア：
{lead_score}

リード検証ステータス：
{validation_status}
""",
    description="Recommends next actions based on lead qualification.",
    output_key="action_recommendation",
)
