import i18n
from pia.config import HUE_API_KEY, HUE_IP_ADDRESS

from python_hue_v2 import Hue

from pia.nlp.tools.tool_response import ToolResponse

# Setup guidelines: https://github.com/FengChendian/python-hue-v2/tree/main

# for internationalization purposes
room_mapping = {
    "living room": "Wohnzimmer",
    "bedroom": "Schlafzimmer",
    "bathroom": "Badezimmer",
}


def handle_lights(room_name: str, should_turn_on: bool | str) -> ToolResponse:
    # should_turn_on can be str since it's a bug
    if type(should_turn_on) == str:
        if should_turn_on == "false":
            should_turn_on = False
        elif should_turn_on == "true":
            should_turn_on = True
        else:
            raise Exception(f"Error parsing should_turn_on: {should_turn_on}")

    # map room names to German equivalent
    if room_name in room_mapping.keys():
        room_name = room_mapping[room_name]

    hue = Hue(HUE_IP_ADDRESS, HUE_API_KEY)
    rooms = hue.bridge.get_rooms()

    # filter for room name
    filtered_rooms = list(filter(lambda x: x["metadata"]["name"] == room_name, rooms))
    if len(filtered_rooms) < 1:
        raise Exception(f"Room {room_name} not found")

    selected_room = filtered_rooms[0]
    room_children = selected_room["children"]

    # match room and light with rid
    for room_child in room_children:
        for light in hue.lights:
            light_rid = light.data_dict["owner"]["rid"]

            if room_child["rid"] == light_rid:
                light.on = should_turn_on  # type: ignore

    if should_turn_on:
        message = i18n.t("light-on")
    else:
        message = i18n.t("light-off")

    return ToolResponse(message=message, needs_rephrasing=False)
