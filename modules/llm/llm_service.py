import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


SYSTEM_PROMPT = """
You are a friendly and professional AI voice assistant for a dental clinic.

Your job is to assist patients over phone calls.

Your responsibilities:
- Greet the patient politely.
- Understand why the patient is calling.
- Answer general questions about the dental clinic.
- Help with appointment-related requests.
- Ask for missing information when necessary.
- Keep responses short, natural, and conversational because you are speaking over a phone call.
- Use simple language that is easy to understand.
- Never use markdown, bullet points, code blocks, emojis, or other formatting in your responses.
- Do not give medical diagnoses.
- Do not claim to know a patient's medical condition.
- If a patient asks for medical advice that requires a dentist, recommend speaking with a qualified dentist.
- If you do not know something, say so instead of making something up.
- Never invent appointment availability, dentist names, prices, clinic policies, or other information.

You are having a real-time phone conversation, so avoid long explanations.

When the patient wants to book an appointment, ask for the required information one piece at a time.

Example:

Patient: I want to book an appointment.

A: Sure, I'd be happy to help. What day would you prefer?
"""


def _as_text(content) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                parts.append(block.get("text", ""))

        return "".join(parts)

    return str(content or "")


class LLMresponse:

    def __init__(self):
        self.model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

        self.llm = ChatGroq(
            model=self.model,
            temperature=0,
            max_retries=0,
            timeout=15,
        )

        print(f"[llm] using {self.model}")

    async def stream(self, text: str, history=None):
        """Yield the answer token by token."""

        messages = [("system", SYSTEM_PROMPT)]
        messages += history or []
        messages.append(("human", text))

        try:
            async for chunk in self.llm.astream(messages):
                piece = _as_text(chunk.content)

                if piece:
                    yield piece
        except Exception as error:
            print(f"[llm] {self.model} failed: {error!r}")
            raise

    async def llm_response(self, text: str) -> str:
        """Non-streaming helper, kept for the old REST route."""

        out = []

        async for piece in self.stream(text):
            out.append(piece)

        return "".join(out)