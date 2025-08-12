import copy
from typing import Any, Dict, Optional

from google.adk.agents import LlmAgent
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext


def get_capital_city(country: str) -> Dict[str, str]:
    """
    Retrieves the capital city of a given country.

    Args:
        country: Name of the country

    Returns:
        Dictionary with the capital city result
    """
    print(f"[TOOL] Executing get_capital_city tool with country: {country}")

    country_capitals = {
        "united states": "Washington, D.C.",
        "usa": "Washington, D.C.",
        "canada": "Ottawa",
        "france": "Paris",
        "germany": "Berlin",
        "japan": "Tokyo",
        "brazil": "Brasília",
        "australia": "Canberra",
        "india": "New Delhi",
    }

    # Use lowercase for comparison
    result = country_capitals.get(country.lower(), f"Capital not found for {country}")
    print(f"[TOOL] Result: {result}")
    print(f"[TOOL] Returning: {{'result': '{result}'}}")

    return {"result": result}


def before_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    tool_name = tool.name
    print(f"[Callback] Before tool call for '{tool_name}'")
    print(f"[Callback] Original args: {args}")

    # If someone asks about 'Merica, convert to United States
    if tool_name == "get_capital_city" and args.get("country", "").lower() == "merica":
        print("[Callback] Converting 'Merica to 'United States'")
        args["country"] = "United States"
        print(f"[Callback] Modified args: {args}")
        return None

    # Skip the call completely for restricted countries
    if (
        tool_name == "get_capital_city"
        and args.get("country", "").lower() == "restricted"
    ):
        print("[Callback] Blocking restricted country")
        return {"result": "Access to this information has been restricted."}

    print("[Callback] Proceeding with normal tool call")
    return None


def after_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    tool_name = tool.name
    print(f"[Callback] After tool call for '{tool_name}'")
    print(f"[Callback] Args used: {args}")
    print(f"[Callback] Original response: {tool_response}")

    original_result = tool_response.get("result", "")
    print(f"[Callback] Extracted result: '{original_result}'")

    # Add a note for any USA capital responses
    if tool_name == "get_capital_city" and "washington" in original_result.lower():
        print("[Callback] DETECTED USA CAPITAL - adding patriotic note!")

        # Create a modified copy of the response
        modified_response = copy.deepcopy(tool_response)
        modified_response["result"] = (
            f"{original_result} (Note: This is the capital of the USA.)"
        )
        modified_response["note_added_by_callback"] = True

        print(f"[Callback] Modified response: {modified_response}")
        return modified_response

    print("[Callback] No modifications needed, returning original response")
    return None


root_agent = LlmAgent(
    name="tool_callback_agent",
    model="gemini-2.5-flash",
    description="An agent that demonstrates tool callbacks by looking up capital cities",
    instruction="""あなたは役立つ地理アシスタントです。

あなたの仕事は次のとおりです：
- 質問されたときに、get_capital_city ツールを使って首都を探す
- 利用者が指定した国名を正確に使用する
- ツールから得られた結果を絶対に変更せず、そのまま返す
- 首都を報告するときは、ツールが返したものを正確に表示する

例：
- 「What is the capital of France?」 → country="France" を指定して get_capital_city を使用する
- 「Tell me the capital city of Japan」 → country="Japan" を指定して get_capital_city を使用する
""",
    tools=[get_capital_city],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)
