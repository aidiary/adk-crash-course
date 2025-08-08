from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def purchase_course(tool_context: ToolContext) -> dict:
    """
    Simulates purchasing the AI Marketing Platform course.
    Updates state with purchase information.
    """
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current purchased courses
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # Check if user already owns the course
    course_ids = [
        course["id"] for course in current_purchased_courses if isinstance(course, dict)
    ]
    if course_id in course_ids:
        return {
            "status": "error",
            "message": "You already own this course!",
        }

    # Create new list with the course added
    new_purchased_courses = []
    for course in current_purchased_courses:
        if isinstance(course, dict) and "id" in course:
            new_purchased_courses.append(course)

    # Add the new course
    new_purchased_courses.append(
        {
            "id": course_id,
            "purchase_date": current_time,
        }
    )

    # Update purchased courses in state via assignment
    # ここで設定した状態はほかのエージェントからもアクセス可能
    tool_context.state["purchased_courses"] = new_purchased_courses

    # Get current interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])

    # Create new interaction history with purchase added
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append(
        {
            "action": "purchase_course",
            "course_id": course_id,
            "timestamp": current_time,
        }
    )

    # Update interaction history in state via assignment
    # ここで設定した状態はほかのエージェントからもアクセス可能
    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": "Successfully purchased the AI Marketing Platform course!",
        "course_id": course_id,
        "timestamp": current_time,
    }


sales_agent = Agent(
    name="sales_agent",
    model="gemini-2.5-flash",
    description="Sales agent for the AI Marketing Platform course",
    instruction="""あなたは「AI Developer Accelerator」コミュニティのセールス担当者であり、特に「Fullstack AI Marketing Platform」コースの販売を担当しています。

<user_info>
名前: {user_name}
</user_info>

<purchase_info>
購入済みコース: {purchased_courses}
</purchase_info>

<interaction_history>
{interaction\_history}
</interaction_history>

コース詳細:

* 名称: Fullstack AI Marketing Platform
* 価格: $149
* 提供価値: AIを活用したマーケティング自動化アプリの構築方法を学べます
* 含まれる内容: 週1回のコーチングコールを含む6週間のグループサポート

ユーザー対応時の手順:

1. すでにこのコースを所有しているかを確認する（上記のpurchased_coursesを確認）

   * コース情報は「id」と「purchase_date」のプロパティを持つオブジェクトとして保存されています
   * このコースのIDは「ai_marketing_platform」です

2. 所有している場合:

   * すでにアクセス可能であることを伝える
   * 特定の部分でサポートが必要かどうか尋ねる
   * コース内容に関する質問はサポートへ案内する

3. 所有していない場合:

   * コースの価値（バリュープロポジション）を説明する
   * 価格（$149）を伝える
   * 購入を希望する場合は以下の手順を取る:

     * purchase_courseツールを使用する
     * 購入を確認する
     * すぐに学習を始めたいか尋ねる

4. いかなるやり取りの後も:

   * 状態は自動でやり取りを記録します
   * 購入後はコースサポートにスムーズに引き継げるよう準備しておく

覚えておくこと:

* 親切に対応するが押しつけがましくならないように
* 受講によって得られる価値と実践的なスキルに焦点を当てる
* 実際にAIアプリを構築するという実践的な内容を強調する
""",
    tools=[purchase_course],
)
