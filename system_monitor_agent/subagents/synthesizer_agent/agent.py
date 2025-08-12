from google.adk.agents import LlmAgent

system_report_synthesizer = LlmAgent(
    name="SystemReportSynthesizer",
    model="gemini-2.5-flash",
    instruction="""あなたはシステムレポート作成者です。

あなたのタスクは、以下の情報を組み合わせて包括的なシステム健全性レポートを作成することです：
- CPU 情報: {cpu_info}
- メモリ情報: {memory_info}
- ディスク情報: {disk_info}

以下の形式でレポートを作成してください：
1. レポート冒頭に、システム全体の健全性ステータスをまとめたエグゼクティブサマリー
2. 各コンポーネントごとの情報を記載したセクション
3. 懸念される指標に基づく推奨事項

レポートは Markdown 形式で、読みやすくプロフェッショナルに仕上げてください。  
懸念される値は強調表示し、実用的な推奨事項を提示してください。
""",
    description="Synthesizes all system information into a comprehensive report",
)
