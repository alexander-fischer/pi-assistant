from pia.config import LANGUAGE


de_hue_tools = [
    {
        "type": "function",
        "function": {
            "name": "handle_lights",
            "description": "Schalte das Licht in Räumen zu Hause ein oder aus.",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_name": {
                        "type": "enum",
                        "description": "Name des Raumes, in dem das Licht ein- oder ausgeschaltet werden soll. Die Raumnamen sind: Wohnzimmer, Schlafzimmer und Badezimmer",
                        "enum": ["Wohnzimmer", "Schlafzimmer", "Badezimmer"],
                    },
                    "should_turn_on": {
                        "type": "bool",
                        "description": "Boolescher Wert, ob das Licht ein- oder ausgeschaltet werden soll.",
                    },
                },
                "required": ["room_name", "should_turn_on"],
            },
        },
    },
]

en_hue_tools = [
    {
        "type": "function",
        "function": {
            "name": "handle_lights",
            "description": "Turn on or turn off lights in rooms at home.",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_name": {
                        "type": "enum",
                        "description": "Name of the room where lights should be turned on or off. Room names are: living room, bedroom and bathroom.",
                        "enum": ["living room", "bedroom", "bathroom"],
                    },
                    "should_turn_on": {
                        "type": "bool",
                        "description": "Boolean, if lights should be turned on or off.",
                    },
                },
                "required": ["room_name", "should_turn_on"],
            },
        },
    },
]


def get_hue_tools():
    if LANGUAGE == "de":
        return de_hue_tools
    else:
        return en_hue_tools
