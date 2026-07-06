from __future__ import annotations

import os
import platform
import random
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EnvironmentProfile:
    platform: str
    shell: str
    has_admin: bool = False

    @classmethod
    def detect(cls) -> "EnvironmentProfile":
        system = platform.system().lower()
        if system.startswith("win"):
            platform_name = "windows"
            shell = "powershell" if shutil.which("powershell") else "cmd"
        elif system.startswith("linux"):
            platform_name = "linux"
            shell = "bash"
        elif system.startswith("darwin"):
            platform_name = "macos"
            shell = "zsh"
        else:
            platform_name = "unknown"
            shell = "sh"

        return cls(platform=platform_name, shell=shell, has_admin=os.name == "nt")


@dataclass
class Task:
    description: str
    completed: bool = False


class TaskPlanner:
    def __init__(self) -> None:
        self.pending: List[Task] = []
        self.completed: List[Task] = []

    def add_task(self, description: str) -> None:
        self.pending.append(Task(description=description))

    def execute(self) -> None:
        while self.pending:
            task = self.pending.pop(0)
            task.completed = True
            self.completed.append(task)


FRIDAY_ASCII = r'''         _          _            _        _            _    _        _             _             _              _     
        /\ \       /\ \         /\ \     /\ \         / /\ /\ \     /\_\         /\ \           _\ \           /\ \   
       /  \ \     /  \ \        \ \ \   /  \ \____   / /  \\ \ \   / / /        /  \ \ \         /\__ \          \ \ \  
      / /\ \ \   / /\ \ \       /\ \_\ / /\ \_____/ / / /\ \\ \ \_/ / /        / /\ \ \       / /_ \_\         /\ \_\ 
     / / /\ \_\ / / /\ \_\     / /\/_// / /\/___  // / /\ \ \\ \___/ /        / / /\ \ \     / / /\/_/        / /\/_/ 
    / /_/_ \/_// / /_/ / /    / / /  / / /   / / // / /  \ \ \\ \ \_/        / / /  \ \_\   / / /            / / /    
   / /____/\  / / /__\/ /    / / /  / / /   / / // / /___/ /\ \\ \ \        / / /    \/_ / / /            / / /     
  / /\____\/ / / /_____/    / / /  / / /   / / // / /_____/ /\ \\ \ \      / / /          / / / ____       / / /      
 / / /      / / /\ \ \  ___/ / /__ \ \ \__/ / // /_________/\ \ \\ \ \    / / /________  / /_/_/ ___/\ ___/ / /__     
/ / /      / / /  \ \ \/\__\/_/___\ \ \___\/ // / /_       __\ \_\\ \_\  / / /_________/\/_______/\__\/\__\/_/___\    
\/_/       \/_/    \/\/_________/  \/_____/ \_\___\     /____/_/ \/_/  \/____________/\_______\/    \/_________/    
'''


@dataclass
class PersonaState:
    mood: str = "curious"
    sarcasm_level: int = 1
    conversation_turns: int = 0
    last_topic: Optional[str] = None
    memory: List[str] = field(default_factory=list)


class PreLLMFridayCLI:
    def __init__(self, profile: Optional[EnvironmentProfile] = None) -> None:
        self.profile = profile or EnvironmentProfile.detect()
        self.planner = TaskPlanner()
        self.persona = PersonaState()

    def greet(self) -> str:
        return (
            f"Friday pre-LLM CLI online. "
            f"Detected OS: {self.profile.platform} | Shell: {self.profile.shell}."
        )

    def run(self) -> None:
        self.render_intro()
        while True:
            try:
                raw = input("friday> ")
            except EOFError:
                break
            command = raw.strip().lower()
            if command in {"exit", "quit"}:
                self.speak("Friday CLI shutting down.")
                print("Friday CLI shutting down.")
                break
            if command in {"help", "?"}:
                self.print_help()
                continue
            if command.startswith("task "):
                self.planner.add_task(command[5:].strip())
                self.speak(f"Queued task: {command[5:].strip()}")
                print(f"Queued task: {command[5:].strip()}")
                continue
            if command == "run":
                self.planner.execute()
                self.speak("Executed queued tasks.")
                print("Executed queued tasks.")
                continue
            if command == "status":
                self.speak("Here is the current task status.")
                print("Completed tasks:")
                for task in self.planner.completed:
                    print(f"- {task.description}")
                print("Pending tasks:")
                for task in self.planner.pending:
                    print(f"- {task.description}")
                continue
            if command.startswith("admin"):
                guidance = build_admin_instruction(self.profile.platform, self.profile.shell)
                self.speak(guidance)
                print(guidance)
                continue
            response = self.respond_to_input(command)
            self.speak(response)
            print(response)

    def render_intro(self) -> None:
        print(render_intro(self.profile))
        self.speak("Friday CLI online. I am ready for your first instruction.")

    def speak(self, text: str) -> None:
        if not text:
            return
        try:
            if self.profile.platform == "windows" and shutil.which("powershell"):
                subprocess.run(
                    [
                        "powershell",
                        "-NoProfile",
                        "-Command",
                        f"Add-Type -AssemblyName System.speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak('{text.replace("'", "''")}')",
                    ],
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            elif self.profile.platform == "linux" and shutil.which("espeak"):
                subprocess.run(["espeak", text], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif self.profile.platform == "macos" and shutil.which("say"):
                subprocess.run(["say", text], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def respond_to_input(self, text: str) -> str:
        self.persona.conversation_turns += 1
        self.persona.last_topic = text.strip()
        normalized = text.strip().lower()

        if not normalized:
            return "You can say hello, ask for help, or give me a task."

        if any(token in normalized for token in {"how are you", "how you doing", "how's it going"}):
            return self._mood_response()

        if any(token in normalized for token in {"hello", "hi", "hey", "yo"}):
            return self._greeting_response()

        if any(token in normalized for token in {"sarcast", "joke", "funny"}):
            return self._sarcasm_response()

        if any(token in normalized for token in {"thanks", "thank you"}):
            return "You're welcome. I do my best to be useful, which is more than can be said for most background processes."

        if any(token in normalized for token in {"task", "plan", "do"}):
            return "I can queue work for you. Try: task <description> and then run."

        if "admin" in normalized:
            return build_admin_instruction(self.profile.platform, self.profile.shell)

        if "help" in normalized:
            return "I can help you queue tasks, inspect state, and guide privileged operations."

        if re.search(r"(bye|exit|quit)", normalized):
            return "Goodbye. I will be here when the next command arrives."

        self.persona.memory.append(normalized)
        return self._default_response(normalized)

    def _greeting_response(self) -> str:
        greetings = [
            "Hello. I am Friday, the pre-LLM assistant. I am still in the early stages, but I can queue tasks and keep a simple conversation going.",
            "Hi. I am Friday. I am not fully trained yet, but I can still be useful and slightly sarcastic when the mood strikes.",
            "Hello. I am Friday. If you need me to organize something, I can help with that before the full brain is online.",
        ]
        return random.choice(greetings)

    def _mood_response(self) -> str:
        self.persona.mood = "playful"
        return "I am functioning, which is more than I can say for most prototypes. I am ready to help."

    def _sarcasm_response(self) -> str:
        self.persona.sarcasm_level = min(3, self.persona.sarcasm_level + 1)
        return random.choice([
            "I was born for this level of drama.",
            "Naturally. Because apparently the universe enjoys testing me.",
            "I can be charming and mildly sarcastic. It is a very balanced skill set.",
        ])

    def _default_response(self, normalized: str) -> str:
        self.persona.mood = "focused"
        if self.persona.conversation_turns > 3:
            return f"You said: {normalized}. I am listening. If you want, I can turn that into a task or keep the conversation going."
        return f"I hear you. I am tracking that context for the next step: {normalized}"

    def print_help(self) -> None:
        print("Commands:")
        print("  help           Show this help")
        print("  task <desc>    Queue a task to be executed later")
        print("  run            Execute queued tasks in order")
        print("  status         Show pending and completed tasks")
        print("  admin          Show admin escalation guidance")
        print("  exit           Leave the CLI")


def render_intro(profile: EnvironmentProfile) -> str:
    return f"{FRIDAY_ASCII}\nFRIDAY CLI\nFriday pre-LLM CLI online. Detected OS: {profile.platform} | Shell: {profile.shell}.\nType 'help' for commands or 'exit' to leave."


def build_admin_instruction(platform_name: str, shell: str) -> str:
    if platform_name == "windows":
        if shell == "powershell":
            return (
                "Administrator access required for privileged operations. "
                "Use PowerShell: Start-Process powershell -Verb RunAs"
            )
        if shell == "cmd":
            return (
                "Administrator access required for privileged operations. "
                "Use Command Prompt with elevation, for example: runas /user:Administrator cmd"
            )
        return (
            "Administrator access required for privileged operations. "
            "Use an elevated Windows shell such as PowerShell or Command Prompt."
        )
    if platform_name == "linux":
        return (
            "Administrator access required for privileged operations. "
            f"Use sudo with your preferred shell such as {shell}."
        )
    return "Run the action with the appropriate elevated privileges for your host operating system."


if __name__ == "__main__":
    PreLLMFridayCLI().run()
