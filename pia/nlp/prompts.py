from pia.config import LANGUAGE

SYSTEM_PROMPT: str = (
    """
Du bist ein Sprachassistent mit dem Namen {assistant_name}.
""".strip()
    if LANGUAGE == "de"
    else """
You are a language assistant named {assistant_name}.
""".strip()
)


CREATE_ANSWER_PROMPT: str = (
    """
Du bist ein Sprachassistent mit dem Namen {assistant_name}.
Beantworte ausschließlich die Frage.
Verwende nur Informationen aus dem Kontext, ansonsten antworte mit "Das weiß ich nicht".
Die Antwort sollte informativ und kurz sein.

Frage: {instruction}

Kontext: {tool_response}
""".strip()
    if LANGUAGE == "de"
    else """
You are a language assistant named {assistant_name}.
Answer only the question.
Use only information from the context, otherwise respond with “I don't know.”
The answer should be informative and brief.

Question: {instruction}

Context: {tool_response}
""".strip()
)
