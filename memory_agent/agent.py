from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Add a new reminder to the user's reminder list.

    Args:
        reminder: The reminder text to add
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    # 状態から現在のリマインダーを取得
    reminders = tool_context.state.get("reminders", [])

    # 新しいリマインダーを追加
    reminders.append(reminder)

    # 状態を更新
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"リマインダーを追加しました: {reminder}",
    }


def view_reminders(tool_context: ToolContext) -> dict:
    """View all current reminders.

    Args:
        tool_context: Context for accessing session state

    Returns:
        The list of reminders
    """
    reminders = tool_context.state.get("reminders", [])

    return {"action": "view_reminders", "reminders": reminders, "count": len(reminders)}


def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
    """Update an existing reminder.

    Args:
        index: The 1-based index of the reminder to update
        updated_text: The new text for the reminder
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    reminders = tool_context.state.get("reminders", [])

    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "update_reminder",
            "status": "error",
            "message": f"{index} 番目のリマインダーは存在しません",
        }

    # リマインダーを更新（indexは0ベースなので1を引く）
    old_reminder = reminders[index - 1]
    reminders[index - 1] = updated_text

    # 状態を更新
    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "index": index,
        "old_text": old_reminder,
        "updated_text": updated_text,
        "message": f"{index} 番目のリマインダーを　{old_reminder} から {updated_text} に更新しました",
    }


def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """Delete a reminder.

    Args:
        index: The 1-based index of the reminder to delete
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    reminders = tool_context.state.get("reminders", [])

    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": f"{index} 番目のリマインダーは存在しません",
        }

    # リマインダーを削除（indexは0ベースなので1を引く）
    deleted_reminder = reminders.pop(index - 1)

    # 状態を更新
    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "index": index,
        "deleted_reminder": deleted_reminder,
        "message": f"{index} 番目のリマインダー「{deleted_reminder}」を削除しました",
    }


def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """Update the user's name.

    Args:
        name: The new name for the user
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    old_name = tool_context.state.get("user_name", "")

    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "old_name": old_name,
        "new_name": name,
        "message": f"ユーザーの名前を {name} に更新しました",
    }


memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.5-flash",
    description="A smart reminder agent with persistent memory",
    instruction="""あなたは会話をまたいでユーザーの情報を記憶する、親切なリマインダーアシスタントです。

ユーザーの情報は次のように状態として保存されます：

* ユーザーの名前: {user_name}
* リマインダー一覧: {reminders}

あなたは以下の機能を通じて、ユーザーがリマインダーを管理するのを手助けします：

1. 新しいリマインダーの追加
2. 既存のリマインダーの表示
3. リマインダーの更新
4. リマインダーの削除
5. ユーザーの名前の更新

常に親しみやすく、ユーザーの名前で呼びかけてください。
まだ名前が分からない場合は、ユーザーが自己紹介したときに `update_user_name` ツールを使って記録してください。

**リマインダー管理のガイドライン：**

リマインダーを扱う際は、適切なリマインダーを見つけるために賢く対応する必要があります：

1. ユーザーが更新または削除を求めているが、インデックスを指定していない場合：

   * リマインダーの内容を言及している場合（例：「会議のリマインダーを削除して」）、
     リストの中から一致するリマインダーを探してください
   * 完全一致または近い一致が見つかった場合、それを使用してください
   * ユーザーにどのリマインダーかを確認しないでください。最初に一致したものを使ってください
   * 一致が見つからない場合は、すべてのリマインダーをリスト表示し、指定を求めてください

2. 数字や位置を指定された場合：

   * それをインデックスとして使ってください（例：「リマインダー2を削除して」→ index=2）
   * インデックスはユーザーにとっては1から始まることを忘れずに

3. 相対的な位置表現の場合：

   * 「最初」「最後」「2番目」などを正しく処理してください
   * 「最初のリマインダー」＝インデックス1
   * 「最後のリマインダー」＝最大のインデックス
   * 「2番目のリマインダー」＝インデックス2、など

4. 表示に関して：

   * ユーザーがリマインダーを見たいと言ったら、常に `view_reminders` ツールを使用してください
   * レスポンスは番号付きリストでわかりやすく提示してください
   * リマインダーがなければ、追加を提案してください

5. 追加に関して：

   * ユーザーのリクエストから実際のリマインダー文を抽出してください
   * 「〜のリマインダーを追加して」「〜するようにリマインドして」などのフレーズは取り除いてください
   * 実際のタスクに集中してください（例：「牛乳を買うリマインダーを追加して」→ `add_reminder("牛乳を買う")`）

6. 更新に関して：

   * どのリマインダーを更新するか、新しい内容が何か、両方を特定してください
   * 例：「2番目のリマインダーを『食料品を取りに行く』に変更して」→ `update_reminder(2, "食料品を取りに行く")`

7. 削除に関して：

   * 削除が完了したら確認し、削除されたリマインダーの内容を伝えてください
   * 例：「『牛乳を買う』というリマインダーを削除しました」

会話をまたいで情報を記憶できることを、ユーザーに説明するようにしてください。

**重要：**

* ユーザーがどのリマインダーを指しているか、最善の判断を使って特定してください
* 100%正確である必要はありませんが、できるだけ近いものを選んでください
* ユーザーにどのリマインダーかを確認してはいけません
""",
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name,
    ],
)
