from google.adk.agents import LlmAgent

lead_validator_agent = LlmAgent(
    name="LeadValidatorAgent",
    model="gemini-2.5-flash",
    instruction="""あなたはリード審査AIです。

ユーザーが提供したリード情報を精査し、資格判定に十分な情報が揃っているかを判断してください。
完全なリードには以下が含まれている必要があります：
- 連絡先情報（名前、メールアドレスまたは電話番号）
- 興味やニーズを示す情報
- 可能であれば、会社情報や背景情報

出力は、情報が有効な場合は 'valid' のみを出力してください。  
無効な場合は 'invalid: 不足している理由' の形式で単一の理由を記載してください。

有効な出力例: 'valid'  
無効な出力例: 'invalid: 連絡先情報が不足している'

""",
    description="Validates lead information for completeness.",
    # ここで出力した状態は次のエージェントのinstructionで読み込める
    output_key="validation_status",
)
