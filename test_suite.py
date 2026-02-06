import unittest
from unittest.mock import patch, MagicMock
from agents.planner import PlannerAgent
from agents.verifier import VerifierAgent
from agents.executor import ExecutorAgent
from tools.weather import get_weather
from tools.github import search_repositories

class TestAIOpsAssistant(unittest.TestCase):

    def setUp(self):
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.verifier = VerifierAgent()

    def test_planner_schema_compliance(self):
        """Test if planner returns a list of dictionaries with correct keys."""
        mock_response = '[{"tool": "get_weather", "args": {"city": "London"}, "reason": "Test"}]'
        with patch.object(self.planner.client, 'generate_response', return_value=mock_response):
            plan = self.planner.create_plan("What is the weather in London?")
            self.assertIsInstance(plan, list)
            if plan:
                self.assertIn("tool", plan[0])
                self.assertIn("args", plan[0])

    def test_weather_tool_failure_handling(self):
        """Test if weather tool handles API errors gracefully."""
        with patch('tools.weather.requests.get') as mock_get:
            mock_get.side_effect = Exception("API Down")
            result = get_weather("NonExistentCity")
            self.assertEqual(result["status"], "failed")
            self.assertIn("error", result)

    def test_github_tool_failure_handling(self):
        """Test if github tool handles API errors gracefully."""
        with patch('tools.github.requests.get') as mock_get:
            mock_get.side_effect = Exception("Connection Timeout")
            result = search_repositories("python")
            self.assertEqual(result["status"], "failed")
            self.assertIn("error", result)

    def test_executor_robustness(self):
        """Test if executor handles failed tool calls without crashing."""
        plan = [{"tool": "get_weather", "args": {"city": "London"}, "reason": "Test"}]
        # Need to patch where it's USED in the executor
        with patch('agents.executor.get_weather', return_value={"status": "failed", "error": "Mock Failure"}):
            # Re-initialize to pick up the patch if it wasn't picked up, 
            # or better yet, patch the tool_map directly for this test.
            self.executor.tool_map["get_weather"] = MagicMock(return_value={"status": "failed", "error": "Mock Failure"})
            results = self.executor.execute(plan)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["status"], "failed")

    def test_verifier_integrity(self):
        """Test if verifier generates a response from execution logs."""
        mock_output = "The weather in London is clear."
        execution_results = [{"step": {}, "output": {"temperature": 20}, "status": "success"}]
        with patch.object(self.verifier.client, 'generate_response', return_value=mock_output):
            final = self.verifier.verify_and_finalize("Weather in London", execution_results)
            self.assertEqual(final, mock_output)

if __name__ == "__main__":
    unittest.main()
