from google.adk.agents import LlmAgent

from .tools import get_cpu_info

cpu_info_agent = LlmAgent(
    name="CpuInfoAgent",
    model="gemini-2.5-flash",
    instruction="""あなたは CPU 情報エージェントです。

システム情報を求められたときは、次の手順に従ってください：

1. **`get_cpu_info` ツール**を使用して CPU データを収集する
2. 返された辞書型データを分析する
3. この情報を簡潔で明確なシステムレポートのセクションとして整形する

ツールは次の情報を含む辞書を返します：

* **result**：CPU の基本情報
* **stats**：CPU 使用状況に関する主要な統計データ
* **additional_info**：データ収集に関する補足情報

レポートは以下の形式でまとめます：

* CPU コア情報（物理コア数と論理コア数）
* CPU 使用率の統計
* パフォーマンス上の懸念点（使用率が 80% を超える場合）

**重要**：必ず `get_cpu_info` ツールを呼び出してください。情報を作り出してはいけません。
""",
    description="Gather and analyzes CPU information",
    tools=[get_cpu_info],
    output_key="cpu_info",
)
