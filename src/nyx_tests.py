import pytest
import sys
from src.nyx import Nyx


# helper function to simulate command-line arguments
def set_sys_argv(args):
    sys.argv = ["script.py"] + args


def test_add_arg():
    cli = Nyx()
    cli.add_arg("test", "t", "Test argument")
    assert "test" in cli._arguments
    assert cli._arguments["test"]["description"] == "Test argument"


def test_parse_args():
    cli = Nyx()
    cli.add_arg("test", "t", "Test argument")
    set_sys_argv(["--test", "value"])
    cli.parse_args()
    assert cli.test == "value"


def test_short_argument():
    cli = Nyx()
    cli.add_arg("test", "t", "Test argument")
    set_sys_argv(["-t", "value"])
    cli.parse_args()
    assert cli.test == "value"


def test_required_argument_missing():
    cli = Nyx()
    cli.add_arg("test", "t", "Test argument", required=True)
    set_sys_argv([])
    with pytest.raises(SystemExit):
        cli.parse_args()


def test_argument_without_value():
    cli = Nyx()
    cli.add_arg("flag", "f", "Boolean flag")
    set_sys_argv(["--flag"])
    cli.parse_args()
    assert cli.flag is True


def test_config():
    cli = Nyx()
    cli.config("Test Program", "--test example", True)
    assert cli._program_description == "Test Program"
    assert cli._example_usage == "--test example"
    assert cli._colored_text is True


def test_logging():
    cli = Nyx()
    cli.success("Success message")
    cli.error("Error message")
    cli.warning("Warning message")
    cli.info("Info message")


def test_help_message(capsys):
    cli = Nyx()
    cli.add_arg("test", "t", "Test argument")
    set_sys_argv(["--help"])
    with pytest.raises(SystemExit):
        cli.parse_args()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "--test" in captured.out


def test_init_function(capsys):
    def mock_function():
        print("Initialized")

    _ = Nyx(mock_function)
    captured = capsys.readouterr()
    assert "Initialized" in captured.out
