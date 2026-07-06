from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ModelConfig:
    name: str = "friday-mini"
    max_context_length: int = 4096
    temperature: float = 0.7
    top_p: float = 0.95
    max_new_tokens: int = 512


class LLMBackend:
    """Abstract interface for any LLM backend used by Friday Core."""

    def __init__(self, config: Optional[ModelConfig] = None) -> None:
        self.config = config or ModelConfig()

    def generate(self, prompt: str, **kwargs: Any) -> str:
        raise NotImplementedError

    def stream_generate(self, prompt: str, **kwargs: Any):
        raise NotImplementedError


class FridayLLM:
    """High-level wrapper that will connect the runtime to models, memory, and tools."""

    def __init__(self, backend: LLMBackend) -> None:
        self.backend = backend

    def chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        prompt = self._build_prompt(message, history or [])
        return self.backend.generate(prompt)

    def _build_prompt(self, message: str, history: List[Dict[str, str]]) -> str:
        conversation = "\n".join(
            f"{entry['role']}: {entry['content']}" for entry in history
        )
        return f"system: You are Friday, an assistant for The Stark Project.\n{conversation}\nuser: {message}\nassistant:"
