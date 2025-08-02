from dataclasses import dataclass
from typing import Any


@dataclass
class Tool:
    name: str
    arguments: dict["str", Any]
