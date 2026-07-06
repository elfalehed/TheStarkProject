from typing import Callable, Dict, List


class ToolRouter:
    """Routes tool calls from LLM outputs to plugin handlers."""

    def __init__(self) -> None:
        self.tools: Dict[str, Callable[..., str]] = {}

    def register(self, name: str, handler: Callable[..., str]) -> None:
        self.tools[name] = handler

    def route(self, tool_name: str, *args, **kwargs) -> str:
        if tool_name not in self.tools:
            raise KeyError(f"Tool '{tool_name}' is not registered")
        return self.tools[tool_name](*args, **kwargs)

    def list_tools(self) -> List[str]:
        return sorted(self.tools.keys())
