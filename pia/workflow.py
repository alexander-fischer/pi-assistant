from loguru import logger
from pia.nlp.prompts import CREATE_ANSWER_PROMPT
from pia.config import ASSISTANT_NAME, TOOL_MODEL, ANSWER_MODEL
from pia.nlp.llm import (
    call_llm,
    call_llm_function,
    stream_llm,
)
from pia.nlp.tools.main import ToolResponse, ToolSpecs


def _get_tool_from_llm(instruction: str, tools: ToolSpecs):
    tool_to_call = call_llm_function(
        instruction=instruction,
        model_id=TOOL_MODEL,
        tools=tools.get_tools(),
    )
    return tool_to_call


def _run_audio_mode(instruction: str, tools: ToolSpecs):
    logger.info("Get tool to call")
    tool_to_call = _get_tool_from_llm(instruction=instruction, tools=tools)

    logger.info("Call tool")
    if tool_to_call:
        tool_response = tools.call_tool(tool_to_call)
    else:
        tool_response = ToolResponse(message="No tool to call.", needs_rephrasing=True)

    if tool_response.needs_rephrasing:
        logger.info("Generate answer")

        answer_prompt = CREATE_ANSWER_PROMPT.format(
            instruction=instruction,
            tool_response=tool_response.message,
            assistant_name=ASSISTANT_NAME,
        )
        answer = call_llm(
            instruction=answer_prompt,
            model_id=ANSWER_MODEL,
        )
        if answer:
            answer = answer.replace("*", "")
        else:
            answer = "No answer."
        logger.info(f"Answer: {answer}")
    else:
        answer = tool_response.message

    return answer


def _run_terminal_mode(instruction: str, tools: ToolSpecs):
    logger.info("Get tool to call")
    tool_to_call = _get_tool_from_llm(instruction=instruction, tools=tools)

    logger.info("Call tool")
    if tool_to_call:
        tool_response = tools.call_tool(tool_to_call)
    else:
        tool_response = ToolResponse(message="No tool to call.", needs_rephrasing=True)

    logger.info("Generate answer")
    answer_prompt = CREATE_ANSWER_PROMPT.format(
        instruction=instruction,
        tool_response=tool_response.message,
        assistant_name=ASSISTANT_NAME,
    )
    answer_stream = stream_llm(instruction=answer_prompt, model_id=ANSWER_MODEL)
    return answer_stream


def call_assistant(
    instruction: str,
    audio_mode: bool = False,
):
    tools = ToolSpecs()

    if audio_mode:
        return _run_audio_mode(instruction=instruction, tools=tools)
    else:
        return _run_terminal_mode(instruction=instruction, tools=tools)
