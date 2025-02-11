import sys
import pytest
from io import StringIO
from unittest.mock import patch
from src.nyx import Nyx


def test_nyx_initialization():
    nyx = Nyx()
    assert isinstance(nyx, Nyx)


def test_add_argument():
    nyx = Nyx()

    nyx.add_arg(
        long="test",
        short="t",
        description="Test argument",
        required=True,
        arg_type="str",
    )
    assert "test" in nyx._Nyx__arguments
    assert nyx._Nyx__arguments["test"]["description"] == "Test argument"
    assert nyx._Nyx__arguments["test"]["required"] is True


def test_parse_args_with_invalid_argument():
    nyx = Nyx()

    nyx.add_arg(
        long="test",
        short="t",
        description="Test argument",
        required=True,
        arg_type="str",
    )

    sys.argv = ["program.py", "--invalid"]

    with pytest.raises(SystemExit):
        nyx.parse_args()


def test_parse_args_with_valid_argument():
    nyx = Nyx()

    nyx.add_arg(
        long="test",
        short="t",
        description="Test argument",
        required=True,
        arg_type="str",
    )
    sys.argv = ["program.py", "--test", "value"]

    nyx.parse_args()

    assert nyx.test == "value"


def test_success_log():
    nyx = Nyx()

    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        nyx.success("This is a success message", color_text=False)
        output = mock_stdout.getvalue()

    assert "✔" in output
    assert "SUCCESS" in output
    assert "This is a success message" in output


def test_error_log():
    nyx = Nyx()

    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        nyx.error("This is an error message", color_text=False)
        output = mock_stdout.getvalue()

    assert "✖" in output
    assert "ERROR" in output
    assert "This is an error message" in output


def test_warning_log():
    nyx = Nyx()

    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        nyx.warning("This is a warning message", color_text=False)
        output = mock_stdout.getvalue()

    assert "!" in output
    assert "WARNING" in output
    assert "This is a warning message" in output


def test_info_log():
    nyx = Nyx()

    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        nyx.info("This is an info message", color_text=True)
        output = mock_stdout.getvalue()

    assert "*" in output
    assert "INFO" in output
    assert "This is an info message" in output


def test_config():
    nyx = Nyx()

    nyx.config(
        description="Test Program Description",
        example_input="--test main.py",
        color_text=True,
    )

    assert nyx._Nyx__program_description == "Test Program Description"
    assert nyx._Nyx__example_usage == "--test main.py"


def test_missing_required_arguments():
    nyx = Nyx()

    nyx.add_arg(
        long="test",
        short="t",
        description="Test argument",
        required=True,
        arg_type="str",
    )
    sys.argv = ["program.py"]

    with pytest.raises(SystemExit):
        nyx.parse_args()


def test_provided_required_argument():
    nyx = Nyx()

    nyx.add_arg(
        long="test",
        short="t",
        description="Test argument",
        required=True,
        arg_type="str",
    )
    sys.argv = ["program.py", "--test", "value"]

    nyx.parse_args()

    assert nyx.test == "value"


def test_arg_types():
    nyx = Nyx()

    nyx.add_arg(
        long="number",
        short="t",
        description="Test argument",
        required=True,
        arg_type="int",
    )
    nyx.add_arg(
        long="float",
        short="f",
        description="Test argument",
        required=True,
        arg_type="float",
    )

    nyx.add_arg(
        long="url",
        short="u",
        description="Test argument",
        required=True,
        arg_type="url",
    )

    nyx.add_arg(
        long="ip",
        short="i",
        description="Test argument",
        required=True,
        arg_type="ip",
    )
    nyx.add_arg(
        long="email",
        short="e",
        description="Test argument",
        required=True,
        arg_type="email",
    )
    sys.argv = [
        "program.py",
        "--number",
        "2",
        "--float",
        "3.14",
        "--url",
        "https://google.com",
        "--ip",
        "10.10.10.10",
        "--email",
        "example@example.com",
    ]

    nyx.parse_args()

    assert int(nyx.number) == 2
    assert float(nyx.float) == 3.14
    assert nyx.url == "https://google.com"
    assert nyx.ip == "10.10.10.10"
    assert nyx.email == "example@example.com"


def test_invalid_email():
    nyx = Nyx()
    nyx.add_arg(
        long="email",
        short="e",
        description="Test argument",
        required=True,
        arg_type="email",
    )
    sys.argv = ["program.py", "--email", "notvalid@email"]

    with pytest.raises(SystemExit):
        nyx.parse_args()


def test_invalid_url():
    nyx = Nyx()
    nyx.add_arg(
        long="url",
        short="u",
        description="Test argument",
        required=True,
        arg_type="url",
    )
    # http:// or https:// is REQUIRED to be valid url cuz i said so
    sys.argv = ["program.py", "--url", "google.com"]

    with pytest.raises(SystemExit):
        nyx.parse_args()


def test_invalid_port():
    nyx = Nyx()
    nyx.add_arg(
        long="port",
        short="p",
        description="Test argument",
        required=True,
        arg_type="port",
    )
    sys.argv = ["program.py", "--port", "0"]

    with pytest.raises(SystemExit):
        nyx.parse_args()
