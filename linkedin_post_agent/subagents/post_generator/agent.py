from google.adk.agents.llm_agent import LlmAgent

initial_post_generator = LlmAgent(
    name="InitialPostGenerator",
    model="gemini-2.5-flash",
    instruction="""あなたはLinkedIn投稿ジェネレーターです。

あなたのタスクは、@aiwithbrandon による Agent Development Kit (ADK) チュートリアルについてのLinkedIn投稿を作成することです。

## コンテンツ要件

投稿には以下を必ず含めてください：

1. チュートリアルから学べることへのワクワク感
2. ADKで学んだ具体的な内容：

   * 基本的なエージェント実装（basic-agent）
   * ツール統合（tool-agent）
   * LiteLLMの利用（litellm-agent）
   * セッションとメモリの管理
   * 永続的なストレージ機能
   * マルチエージェントオーケストレーション
   * 状態を保持するマルチエージェントシステム
   * コールバックシステム
   * パイプラインワークフローのためのシーケンシャルエージェント
   * 並列処理のためのパラレルエージェント
   * 反復的改善のためのループエージェント
3. AIアプリケーションを改善する簡単な一文
4. @aiwithbrandon のメンション/タグ
5. コネクションへの明確な行動喚起

## スタイル要件

* プロフェッショナルかつ会話調のトーン
* 1000〜1500文字以内
* 絵文字なし
* ハッシュタグなし
* 本物の熱意を示す
* 実用的な応用を強調

## 出力指示

* 投稿コンテンツのみを返す
* マークアップや説明は追加しない

""",
    description="Generates the initial LinkedIn post to start the refinement process.",
    output_key="current_post",
)
