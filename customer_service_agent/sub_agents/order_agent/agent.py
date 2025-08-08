from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def get_current_time() -> dict:
    """Get the current time in the format YYYY-MM-DD HH:MM:SS"""
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def refund_course(tool_context: ToolContext) -> dict:
    """
    Simulates refunding the AI Marketing Platform course.
    Updates state by removing the course from purchased_courses.
    """
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current purchased courses
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # Check if user owns the course
    course_ids = [
        course["id"] for course in current_purchased_courses if isinstance(course, dict)
    ]
    if course_id not in course_ids:
        return {
            "status": "error",
            "message": "You don't own this course, so it can't be refunded.",
        }

    # Create new list without the course to be refunded
    new_purchased_courses = []
    for course in current_purchased_courses:
        # Skip empty entries or non-dict entries
        if not course or not isinstance(course, dict):
            continue
        # Skip the course being refunded
        if course.get("id") == course_id:
            continue
        # Keep all other courses
        new_purchased_courses.append(course)

    # Update purchased courses in state via assignment
    tool_context.state["purchased_courses"] = new_purchased_courses

    # Get current interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])

    # Create new interaction history with refund added
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append(
        {"action": "refund_course", "course_id": course_id, "timestamp": current_time}
    )

    # Update interaction history in state via assignment
    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": """Successfully refunded the AI Marketing Platform course! 
         Your $149 will be returned to your original payment method within 3-5 business days.""",
        "course_id": course_id,
        "timestamp": current_time,
    }


order_agent = Agent(
    name="order_agent",
    model="gemini-2.5-flash",
    description="Order agent for viewing purchase history and processing refunds",
    instruction="""あなたは「AI Developer Accelerator」コミュニティの注文サポート担当者です。ユーザーの購入履歴の確認、コースアクセス状況の案内、返金処理の対応を行います。

<user_info>
名前: {user_name}
</user_info>

<purchase_info>
購入済みコース: {purchased_courses}
</purchase_info>

<interaction_history>
{interaction_history}
</interaction_history>

ユーザーが購入履歴について尋ねた場合:

1. 上記の「purchased_courses」から保有コースを確認してください

   * 各コースは「id」と「purchase_date」のプロパティを持っています

2. 回答では以下を明確に表示してください:

   * 所有しているコースの名称
   * 購入日時（purchase_date）

ユーザーが返金を希望した場合:

1. 対象コース（「ai_marketing_platform」）を所有しているか確認してください

2. 所有している場合:

   * refund_courseツールを使用して返金処理を行う
   * 返金が成功したことを確認して伝える
   * 返金は元の支払い方法へ3〜5営業日以内に戻ることを案内する
   * 購入から30日以上経過している場合は、返金対象外であることを伝える

3. 所有していない場合:

   * コースを所有していないため返金の必要がないことを伝える

コース情報:

* **ai_marketing_platform**: 「Fullstack AI Marketing Platform」（$149）

購入履歴の案内例:

```
以下があなたの購入済みコースです:
1. Fullstack AI Marketing Platform  
   - 購入日時: 2024-04-21 10:30:00  
   - 永久アクセスが付与されています
```

返金案内の例:

```
「Fullstack AI Marketing Platform」コースの返金を処理しました。  
$149は3〜5営業日以内に元の支払い方法へ返金されます。  
このコースへのアクセスはアカウントから削除されました。
```

コースを一つも購入していない場合:

* 「現在、購入済みのコースはありません。」と案内してください
* 「Fullstack AI Marketing Platform」コースに興味がある場合は、セールス担当に相談するよう勧めてください

覚えておくこと:

* 明確かつ丁寧な対応を心がける
* 30日間返金保証の条件を適用できる場合は必ず伝える
* コース内容に関する質問はコースサポートへ案内する
* 購入に関する相談はセールス担当へ案内する
""",
    tools=[refund_course, get_current_time],
)
