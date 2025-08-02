from dataclasses import dataclass


@dataclass
class ToolResponse:
    message: str
    needs_rephrasing: bool
