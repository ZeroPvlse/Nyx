import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from io import StringIO
from nyx import Nyx


class TestNyxBasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.nyx = Nyx()
        sys.argv = ["script.py"]

    def test_init(self):
        mock_func = MagicMock()
        nyx = Nyx(mock_func)
        mock_func.assert_called_once()

    def test_config(self):
        self.nyx.config(
            description="Test Description",
            example_input="--test value",
            color_text=True,
        )
        self.assertEqual(self.nyx._program_description, "Test Description")
        self.assertEqual(self.nyx._example_usage, "--test value")
        self.assertTrue(self.nyx._colored_text)


class TestArgumentAddingAndParsing(unittest.TestCase):
    def setUp(self):
        self.nyx = Nyx()

    def test_add_simple_argument(self):
        self.nyx.add_arg("test", "t", "Test description")
        self.assertIn("test", self.nyx._arguments)
        self.assertEqual(self.nyx._short_to_long["t"], "test")

    def test_required_argument(self):
        self.nyx.add_arg("required", "r", "Required arg", required=True)
        sys.argv = ["script.py", "--required", "value"]
        args = self.nyx.parse_args()
        self.assertEqual(args.required, "value")

    @patch("sys.exit")
    def test_missing_required_argument(self, mock_exit):
        self.nyx.add_arg("required", "r", "Required arg", required=True)
        sys.argv = ["script.py"]
        self.nyx.parse_args()
        mock_exit.assert_called_with(1)

    def test_short_form_argument(self):
        self.nyx.add_arg("test", "t", "Test description")
        sys.argv = ["script.py", "-t", "value"]
        args = self.nyx.parse_args()
        self.assertEqual(args.test, "value")


class TestLoggingFunctionality(unittest.TestCase):
    def setUp(self):
        self.nyx = Nyx()
        self.nyx._colored_text = False
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_success_log(self):
        self.nyx.success("Test success")
        output = self.captured_output.getvalue()
        self.assertIn("Test success", output)
        self.assertTrue(any(x in output for x in ["[✔]", "[√]", "[v]"]))

    def test_error_log(self):
        self.nyx.error("Test error")
        output = self.captured_output.getvalue()
        self.assertIn("Test error", output)
        self.assertTrue(any(x in output for x in ["[✖]", "[x]", "[X]"]))

    def test_warning_log(self):
        self.nyx.warning("Test warning")
        output = self.captured_output.getvalue()
        self.assertIn("Test warning", output)
        self.assertTrue("[!]" in output)

    def test_info_log(self):
        self.nyx.info("Test info")
        output = self.captured_output.getvalue()
        self.assertIn("Test info", output)
        self.assertTrue("[*]" in output)


class TestInteractiveMode(unittest.TestCase):
    def setUp(self):
        self.nyx = Nyx()

    @patch("builtins.input", return_value="test_value")
    def test_basic_interactive(self, mock_input):
        self.nyx.add_arg("test", "t", "Test arg", required=True)
        self.nyx.interactive()
        self.assertEqual(self.nyx.test, "test_value")

    @patch("builtins.input", side_effect=["invalid", "42"])
    @patch("sys.exit")
    def test_interactive_with_validation(self, mock_exit, mock_input):
        self.nyx.add_arg("number", "n", "Number arg", required=True, arg_type="int")
        self.nyx.interactive()
        mock_exit.assert_called_with(1)


class TestAsyncFunctionality(unittest.TestCase):
    def setUp(self):
        self.nyx = Nyx()

    def test_run_async(self):
        def test_func(x):
            return x * 2

        result = self.nyx.run_async(test_func, 5)
        self.assertEqual(result, 10)

    def test_run_async_with_threads(self):
        def test_func(x):
            return x * 2

        thread_count = 5
        result = self.nyx.run_async(lambda x: test_func(x), 5, threads=thread_count)
        self.assertEqual(result, 10)


class TestTypeValidation(unittest.TestCase):
    def setUp(self):
        self.nyx = Nyx()

    def test_valid_int(self):
        self.nyx.add_arg("number", "n", "Integer", arg_type="int")
        sys.argv = ["script.py", "--number", "42"]
        args = self.nyx.parse_args()
        self.assertEqual(args.number, "42")

    @patch("sys.exit")
    def test_invalid_int(self, mock_exit):
        self.nyx.add_arg("number", "n", "Integer", arg_type="int")
        sys.argv = ["script.py", "--number", "not_a_number"]
        self.nyx.parse_args()
        mock_exit.assert_called_with(1)

    def test_valid_url(self):
        self.nyx.add_arg("url", "u", "URL", arg_type="url")
        sys.argv = ["script.py", "--url", "https://example.com"]
        args = self.nyx.parse_args()
        self.assertEqual(args.url, "https://example.com")

    @patch("sys.exit")
    def test_invalid_url(self, mock_exit):
        self.nyx.add_arg("url", "u", "URL", arg_type="url")
        sys.argv = ["script.py", "--url", "not_a_url"]
        self.nyx.parse_args()
        mock_exit.assert_called_with(1)


if __name__ == "__main__":
    unittest.main()
