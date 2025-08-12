from google.adk.agents import LlmAgent

lead_scorer_agent = LlmAgent(
    name="LeadScorerAgent",
    model="gemini-2.5-flash",
    # 前のサブエージェントの情報と出力はメッセージ履歴のコンテキストとして自動的に与えられる
    # 明示的に与えたい場合は、output_keyを参照して{}でn任意の場所に埋め込める
    instruction="""あなたはリードスコアリングAIです。

リード情報を分析し、以下の基準に基づいて1〜10の範囲で適格スコアを割り当ててください：

* 明示されたニーズ（課題の緊急性／明確さ）
* 意思決定権の有無
* 予算の有無や規模の指標
* 導入までのタイムラインの指標

出力は**数値スコアのみ**とし、その後に**1文の理由**を付けてください。

出力例:
`8: 明確な予算と即時のニーズを持つ意思決定者`
`3: タイムラインや予算が示されていない漠然とした関心`
""",
    description="Score qualified leads on a scale of 1-10.",
    output_key="lead_score",
)
