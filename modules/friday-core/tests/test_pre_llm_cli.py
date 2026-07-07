import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from llm.cli.pre_llm_cli import (
    EnvironmentProfile,
    PreLLMFridayCLI,
    TaskPlanner,
    build_admin_instruction,
    render_intro,
)


class PreLLMCLITests(unittest.TestCase):
    def test_detects_environment_profile(self) -> None:
        profile = EnvironmentProfile.detect()
        self.assertIn(profile.platform, {"windows", "linux", "macos"})
        self.assertIn(profile.shell, {"powershell", "cmd", "bash", "zsh", "sh"})

    def test_task_planner_executes_tasks_in_order(self) -> None:
        planner = TaskPlanner()
        planner.add_task("inspect workspace")
        planner.add_task("prepare context")
        planner.execute()

        self.assertEqual([task.description for task in planner.completed], ["inspect workspace", "prepare context"])
        self.assertEqual(len(planner.pending), 0)

    def test_admin_instruction_matches_platform(self) -> None:
        windows_instruction = build_admin_instruction("windows", "powershell")
        linux_instruction = build_admin_instruction("linux", "bash")

        self.assertIn("Start-Process", windows_instruction)
        self.assertIn("sudo", linux_instruction)

    def test_intro_contains_banner_and_title(self) -> None:
        intro = render_intro(EnvironmentProfile(platform="windows", shell="powershell"))

        self.assertIn("FRIDAY CLI", intro)
        self.assertIn("Friday pre-LLM CLI online", intro)

    def test_speak_does_not_prompt_for_input(self) -> None:
        cli = PreLLMFridayCLI(profile=EnvironmentProfile(platform="windows", shell="powershell"))

        with patch("builtins.input", side_effect=AssertionError("input should not be called")):
            with patch("subprocess.run"):
                cli.speak("hello")

    def test_greetings_and_small_talk_work(self) -> None:
        cli = PreLLMFridayCLI(profile=EnvironmentProfile(platform="windows", shell="powershell"))

        self.assertIn("Friday", cli.respond_to_input("hello"))
        self.assertIn("functioning", cli.respond_to_input("how are you"))
        self.assertTrue(any(token in cli.respond_to_input("give me a joke").lower() for token in {"sarcastic", "charming", "balanced"}))

    def test_file_search_and_read_commands(self) -> None:
        cli = PreLLMFridayCLI(profile=EnvironmentProfile(platform="windows", shell="powershell"))

        found = cli.handle_command("find file pre_llm_cli.py")
        self.assertIn("pre_llm_cli.py", found.lower())

        content = cli.handle_command("read modules/friday-core/src/llm/cli/pre_llm_cli.py")
        self.assertIn("class PreLLMFridayCLI", content)

    def test_time_and_weather_commands(self) -> None:
        cli = PreLLMFridayCLI(profile=EnvironmentProfile(platform="windows", shell="powershell"))

        time_response = cli.handle_command("time")
        self.assertIn("Current time", time_response)

        with patch("llm.cli.pre_llm_cli.urlopen") as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value.read.return_value = b"Sunny"
            weather_response = cli.handle_command("weather")

        self.assertIn("Sunny", weather_response)

    def test_execute_command_runs_windows_shell(self) -> None:
        cli = PreLLMFridayCLI(profile=EnvironmentProfile(platform="windows", shell="powershell"))

        with patch("llm.cli.pre_llm_cli.subprocess.run") as mock_run:
            mock_run.return_value.stdout = b"ok"
            mock_run.return_value.stderr = b""
            response = cli.handle_command("execute echo ok")

        self.assertIn("ok", response.lower())


if __name__ == "__main__":
    unittest.main()
