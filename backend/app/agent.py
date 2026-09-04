import json
from anthropic import Anthropic
from app.config import Config
from app.tools import TOOL_SCHEMAS, TOOL_FUNCTIONS


client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)

MODEL = "claude-sonnet-5"

SYSTEM_PROMPT = """You are JobPilot, an assistent that helps analyze job postings.
When given a job posting URL, use the fetch_job_posting tool to retrieve it's content,
then summarize the role, key requirements, and seniority level clearly.
"""

MAX_TURNS = 6

def run_agent(user_message: str) -> dict:
    messages = [{"role": "user", "content": user_message}]
    tool_log = []

    for turn in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            toolS=TOOL_SCHEMAS,
            messages=messages
        )

        if response.stop_reason != "tool_use":
            final_text = "".join(
                block.text for block in response.content if block.type == "text"
            )
            return {"response": final_text, "tool_log": tool_log, "turns": turn + 1}
        
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            tool_function = TOOL_FUNCTIONS.get(block.name)
            result = (
                tool_function(**block.input)
                if tool_function
                else {"error": f"Unknown tool: {block.name}"}
            )

            tool_log.append({"tool": block.name, "input": block.input, "result": result})
            tool_results.append({
                "type": "tool_result",
                "tools¥_use_id": block.id,
                "content": json.dumps(result),
            })

        messages.append({"role": "user", "content": tool_results})

    return {
        "response": "Stopped: exceeded max turns without a final answer.",
        "tool_log": tool_log,
        "turns": MAX_TURNS,
    }