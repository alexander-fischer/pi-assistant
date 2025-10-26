import ast
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
from pia.nlp.prompts import SYSTEM_PROMPT, SYSTEM_PROMPT_TOOL
from pia.nlp.tools.main import Tool
import re

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
    tool_list_as_text = "\n".join([json.dumps(tool["function"]) for tool in tools])
    system_prompt = SYSTEM_PROMPT_TOOL.format(tool_list_as_text=tool_list_as_text)

    user_prompt = f"""
        Query: {instruction}
    """
    resp = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=TOOL_MODEL_TEMPERATURE,
        extra_body={"keep_alive": LLM_KEEP_ALIVE},
        stop="<|tool_call_end|>",
    )
    content = resp.choices[0].message.content
    if not content:
        logger.error(f"No response from model {model_id} for prompt: {user_prompt}")
        return None

    m = re.search(r"\[(\w+)\((.*?)\)\]", content)
    if not m:
        logger.error(f"Cannot find tools in response: {content}")
        return None

    func_name = m.group(1)
    params_str = m.group(2)
    params = {
        k: ast.literal_eval(v)
        for k, v in re.findall(r"(\w+)\s*=\s*(\".*?\"|\'.*?\'|\S+)", params_str)
    }
    return Tool(name=func_name, arguments=params)
