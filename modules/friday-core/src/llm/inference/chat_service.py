from typing import List, Dict

from ..core.model_interface import FridayLLM, LLMBackend


class ChatService:
    """Minimal service wrapper for a Friday-style chat interface."""

    def __init__(self, backend: LLMBackend) -> None:
        self.llm = FridayLLM(backend)
        self.history: List[Dict[str, str]] = []

    def respond(self, message: str) -> str:
        response = self.llm.chat(message, self.history)
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": response})
        return response
