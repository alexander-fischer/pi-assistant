import json
import openai
from loguru import logger
from pia.config import (
    ANSWER_MODEL_TEMPERATURE,
    LLM_API_KEY,
    LLM_API_URL,
    LLM_KEEP_ALIVE,
    TOOL_MODEL_TEMPERATURE,
)
from pia.nlp.prompts import SYSTEM_PROMPT
from pia.nlp.tools.main import Tool

client = openai.OpenAI(base_url=LLM_API_URL, api_key=LLM_API_KEY)


def stream_llm(instruction: str, model_id: str):
    return client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": instruction},
        ],
        temperature=ANSWER_MODEL_TEMPERATURE,
        extra_body={"keep_alive": LLM_KEEP_ALIVE},
        stream=True,
    )


def call_llm(instruction: str, model_id: str):
    resp = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": instruction},
        ],
        extra_body={"keep_alive": LLM_KEEP_ALIVE, "options": {"num_ctx": 8192}},
        temperature=ANSWER_MODEL_TEMPERATURE,
    )
    return resp.choices[0].message.content


def call_llm_function(instruction: str, model_id: str, tools: list) -> Tool | None:
    TASK_PROMPT = """
    You are a helpful assistant.
    """.strip()

    TOOL_PROMPT = """
    # Tools

    You may call one or more functions to assist with the user query.

    You are provided with function signatures within <tools></tools> XML tags:
    <tools>
    {tool_text}
    </tools>
    """.strip()

    FORMAT_PROMPT = """
    For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
    <tool_call>
    {"name": <function-name>, "arguments": <args-json-object>}
    </tool_call>
    """.strip()

    tool_list_as_text = "\n".join([json.dumps(tool) for tool in tools])
    system_prompt = (
        TASK_PROMPT
        + "\n\n"
        + TOOL_PROMPT.format(tool_text=tool_list_as_text)
        + "\n\n"
        + FORMAT_PROMPT
        + "\n"
    )

    resp = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction},
        ],
        temperature=TOOL_MODEL_TEMPERATURE,
        extra_body={"keep_alive": LLM_KEEP_ALIVE},
    )

    content = resp.choices[0].message.content
    logger.info(content)
    if not content or not content.startswith("<tool_call>"):
        return None

    try:
        payload = content.replace("<tool_call>", "").replace("</tool_call>", "").strip()
        call_data = json.loads(payload)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse function call JSON: %s", e)
        return None

    return Tool(name=call_data["name"], arguments=call_data["arguments"])
