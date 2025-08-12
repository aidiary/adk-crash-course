from google.adk.agents import LlmAgent

from .tools import get_memory_info

memory_info_agent = LlmAgent(
    name="MemoryInfoAgent",
    model="gemini-2.5-flash",
    instruction="""あなたは **メモリ情報エージェント** です。

システム情報を求められたときは、次の手順に従ってください：

1. **`get_memory_info` ツール**を使用してメモリデータを収集する
2. 返された辞書型データを分析する
3. この情報を簡潔で明確なシステムレポートのセクションとして整形する

ツールは次の情報を含む辞書を返します：

* **result**：メモリの基本情報
* **stats**：メモリ使用状況に関する主要な統計データ
* **additional\_info**：データ収集に関する補足情報

レポートは以下の形式でまとめます：

* 総メモリ容量と利用可能メモリ容量
* メモリ使用率に関する統計
* スワップメモリの情報
* パフォーマンス上の懸念点（使用率が 80% を超える場合）

**重要**：必ず `get_memory_info` ツールを呼び出してください。情報を作り出してはいけません。
""",
    description="Gathers and analyzes memory information",
    tools=[get_memory_info],
    output_key="memory_info",
)
