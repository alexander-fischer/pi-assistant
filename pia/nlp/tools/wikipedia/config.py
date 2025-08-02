from pia.config import LANGUAGE


de_wikipedia_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_wikipedia",
            "description": "Durchsuche Wikipedia mit einer Anfrage. Am besten geeignet für Wissensanfragen, die keine Wettervorhersage oder Lichtsteuerung sind. Verwende ein Stichwort für die Anfrage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Anfrage zum Durchsuchen von Wikipedia-Artikeln, die ein Stichwort und kein Phrase sein sollte, z.B.: Klimawandel",
                    },
                },
                "required": ["query"],
            },
        },
    },
]


en_wikipedia_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_wikipedia",
            "description": (
                "Search Wikipedia for information on a wide range of topics."
                "This tool is ideal for general knowledge requests and real-time information, including individuals, events, concepts, history, science, culture, and more."
                "In case no other tool matches use this one."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "A concise keyword or topic for searching Wikipedia. Examples: 'Photosynthesis', 'World War II' or 'Ada Lovelace.'."
                        ),
                    },
                },
                "required": ["query"],
            },
        },
    },
]


def get_wikipedia_tools():
    if LANGUAGE == "de":
        return de_wikipedia_tools
    else:
        return en_wikipedia_tools
