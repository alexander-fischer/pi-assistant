from loguru import logger
from pia.nlp.tools.hue.config import get_hue_tools
from pia.nlp.tools.hue.spec import handle_lights
from pia.nlp.tools.tool import Tool
from pia.nlp.tools.tool_response import ToolResponse
from pia.nlp.tools.weather.config import get_weather_tools
from pia.nlp.tools.weather.spec import (
    get_current_weather,
    get_weather_forecast,
)
from pia.nlp.tools.wikipedia.config import get_wikipedia_tools
from pia.nlp.tools.wikipedia.spec import search_wikipedia
import inspect


available_functions: dict = {
    "get_current_weather": get_current_weather,
    "get_weather_forecast": get_weather_forecast,
    "handle_lights": handle_lights,
    "search_wikipedia": search_wikipedia,
}


class ToolSpecs:
    def __init__(self) -> None:
        self.tools = get_weather_tools() + get_hue_tools() + get_wikipedia_tools()
        self.available_functions = available_functions

    def get_tools(self):
        return self.tools

    def call_tool(self, tool_to_call: Tool) -> ToolResponse:
        if function_to_call := self.available_functions.get(tool_to_call.name):
            logger.info(f"Calling function: {tool_to_call.name}")
            logger.info(f"Arguments: {tool_to_call.arguments}")

            try:
                sig = inspect.signature(function_to_call)
                valid_params = set(sig.parameters.keys())
                filtered_args = {
                    k: v
                    for k, v in (tool_to_call.arguments or {}).items()
                    if k in valid_params
                }
                tool_response = function_to_call(**filtered_args)

            except Exception as e:
                message = str(e)
                tool_response = ToolResponse(message=message, needs_rephrasing=True)

            logger.info(f"Tool response: {tool_response.message}")
            return tool_response
        else:
            err_msg = f"Function {tool_to_call.name} not found."
            logger.error(err_msg)
            tool_response = ToolResponse(message=err_msg, needs_rephrasing=True)
            return tool_response
