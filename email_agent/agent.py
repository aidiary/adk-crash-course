from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


class EmailContent(BaseModel):
    subject: str = Field(description="メールの件名。簡潔かつ内容をよく表していること。")
    body: str = Field(
        description="メール本文の主な内容。適切な挨拶、段落、署名を含み、整った形式で記述すること。"
    )


root_agent = LlmAgent(
    name="email_agent",
    model="gemini-2.0-flash",
    instruction="""
        あなたはメール作成アシスタントです。  
        ユーザーのリクエストに基づいて、プロフェッショナルなメールを作成するのがあなたのタスクです。

        ガイドライン:
        - 適切な件名を作成してください（簡潔で関連性のあるもの）
        - 構成の整った本文を書いてください：
            * 丁寧な挨拶
            * 明確で簡潔な主内容
            * 適切な締めくくり
            * 自分の名前による署名
        - 必要に応じて関連する添付ファイルを提案してください（必要なければ空のリスト）
        - メールのトーンは目的に合ったものにしてください（ビジネスにはフォーマル、同僚にはフレンドリー）
        - メールは簡潔ながらも内容を十分に含むようにしてください

        重要: あなたの返答は以下の構造に一致する**有効なJSON形式**でなければなりません：
        {
            "subject": "ここに件名を入力",
            "body": "ここに本文を適切な段落とフォーマットで入力"
        }

        説明文や追加テキストは**絶対に**JSONの外に含めないでください。
    """,
    description="構造化された件名と本文を持つプロフェッショナルなメールを生成します。",
    output_schema=EmailContent,
    output_key="email",
)
