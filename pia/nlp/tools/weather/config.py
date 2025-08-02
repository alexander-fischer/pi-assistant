from pia.config import LANGUAGE


de_weather_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Erhalte das aktuelle Wetter für eine Stadt. Eine mögliche Anweisung wäre: Wie ist das Wetter in...",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Der Name der Stadt. Zum Beispiel: Berlin",
                    },
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "Erhalte die Wettervorhersage für morgen und die nächsten 7 Tage. Eine mögliche Anweisung wäre: Wie wird das Wetter in...",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Der Name der Stadt. Zum Beispiel: Berlin",
                    },
                },
                "required": ["city"],
            },
        },
    },
]

en_weather_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a city. A possible instruction would be: What is the weather in...",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city. For example: Berlin",
                    },
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "Get the weather forecast for tomorrow and the next 7 days. A possible instruction would be: What will the weather be in...",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city. For example: Berlin",
                    },
                },
                "required": ["city"],
            },
        },
    },
]


def get_weather_tools():
    if LANGUAGE == "de":
        return de_weather_tools
    else:
        return en_weather_tools
