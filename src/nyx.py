from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
import sys
import os
import socket
import re


class Nyx:
    __GREEN = "\033[92m"
    __RED = "\033[5;31m"
    __YELLOW = "\033[93m"
    __BLUE = "\033[96m"
    __WHITE = "\033[0;37m"

    def __init__(self, starting_function: Callable | None = None) -> None:
        """
        Initializes the Nyx class and sets up the argument parser.

        Parameters:
        starting_function (Callable | None):
            A function to be executed at the start of the program.
            It cannot take input or return any values.
            Default is None.
        """
        self._arguments = {}
        self._short_to_long = {}
        if starting_function is not None:
            self.init(starting_function)

        self._example_usage = ""
        self._help_options = [{}]
        self._program_description = ""

        self._colored_text = False

    def add_arg(
        self,
        long: str,
        short: str,
        description: str,
        required: bool = False,
        arg_type: str = None,  # pyright: ignore[reportArgumentType]
    ) -> None:
        """
        Adds an argument to the CLI application.

        Parameters:
        long (str): Full parameter name (e.g., --test, --run).
        short (str): Short parameter name (e.g., -t, -r).
        description (str): A brief description of the parameter (e.g., "test currently running code").
        required (bool): Whether the parameter is mandatory. Default is False.
        arg_type (str): Custom type like url, json, ip, file etc. Go to docs for more types.

        Returns:
        None
        """
        self._arguments[long] = {
            "description": description,
            "value": None,
            "required": required,
            "type": arg_type,
        }
        self._short_to_long[short] = long
        self._help_options.append(
            {
                "long": long,
                "short": short,
                "description": description,
                "required": required,
                "type": arg_type,
            }
        )

    #
    def parse_args(self, namespace=None) -> "Nyx | object":
        """
        Parses the command-line arguments from sys.argv.

        Parameters:
        namespace (object | None): The class or object where arguments should be assigned as attributes.
                                   If None, the current Nyx object will be used.

        Returns:
        Nyx | object: Returns the namespace object (Nyx or any passed object).
        """
        if namespace is None:
            namespace = self

        arg_name = None
        provided_args = set()

        for i, arg in enumerate(sys.argv[1:]):
            self._handle_help(arg)
            arg_name = self._get_arg_name(arg)
            self._process_argument(arg_name, i + 1, namespace, provided_args)  # pyright: ignore[reportArgumentType]

        self._check_missing_args(provided_args)
        return namespace

    def _print_error(self, message: str):
        if self._colored_text:
            print(f"{self.__RED}Error: {message}{self.__WHITE}")
        else:
            print(f"Error: {message}")
        sys.exit(1)

    def _handle_help(self, arg: str):
        if arg in ("--help", "-h"):
            self._print_help()
            sys.exit(0)

    def _get_arg_name(self, arg: str):
        if arg.startswith("--"):
            return arg.lstrip("-")
        elif len(arg) == 2:
            return self._short_to_long.get(arg.lstrip("-"))
        return None

    def _process_argument(
        self, arg_name: str, next_arg_index: int, namespace, provided_args: set
    ):
        if arg_name and arg_name in self._arguments:
            provided_args.add(arg_name)
            has_next_value = next_arg_index < len(sys.argv) - 1 and not sys.argv[
                next_arg_index + 1
            ].startswith("-")

            if has_next_value:
                arg_value = sys.argv[next_arg_index + 1]
                self._arguments[arg_name]["value"] = arg_value
                setattr(namespace, arg_name, arg_value)
                self.validate_type(arg_name, arg_value)
            else:
                if self._arguments[arg_name]["required"]:
                    self._print_error(
                        f"Argument '--{arg_name}' requires a value but none was provided."
                    )
                else:
                    self._arguments[arg_name]["value"] = True
                    setattr(namespace, arg_name, True)

    def _check_missing_args(self, provided_args: set):
        missing_args = [
            arg
            for arg, details in self._arguments.items()
            if details.get("required") and arg not in provided_args
        ]
        if missing_args:
            self._print_error(
                f"The following required arguments are missing: {', '.join(missing_args)}"
            )

    #
    def config(
        self,
        description: str = "",
        example_input: str = "",
        color_text: bool = False,
    ):
        """
        Sets the program description, example usage, and color settings for output.

        Parameters:
        description (str): A description of the program, shown at the start of the help screen.
        example_input (str): Example program usage, excluding the filename.
                             Format: '--test main.py --time True'.
        color_text (bool): Whether to print colored text in logs. Default is False.

        Returns:
        None
        """
        try:
            self._example_usage = str(example_input)
        except ValueError:
            print(
                f"Example program usage must be a string, but got {type(example_input)}"
            )

        try:
            self._program_description = str(description)
        except ValueError:
            print(f"Program description must be a string, but got {type(description)}")

        self._colored_text = color_text

    def _print_help(self):
        """
        Prints the help message with program description, usage, and available options.

        Returns:
        None
        """
        script_name = os.path.basename(sys.argv[0])
        print(
            f"""{self._program_description}

Usage: {script_name} {self._example_usage}

Options:"""
        )
        for i in self._help_options:
            if i:
                print(
                    f"\t--{i['long']},\t-{i['short']}\trequired: {i['required']}\t {i['description']}"
                )

    #
    def init(self, func: Callable) -> None:
        """
        Executes the provided function at the start of the program.

        Parameters:
        func (Callable): The function to be run at the beginning.
                          It should not accept any input or return anything.

        Returns:
        None
        """
        func()

    def __getattr__(self, name):
        if name in self._arguments:
            return self._arguments[name]["value"]
        raise AttributeError(f"'Nyx' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        elif name in self._arguments:
            self._arguments[name]["value"] = value
        else:
            super().__setattr__(name, value)

    # the "cool ui part etc"
    def _print_log(
        self, message: str, color: str, symbol: str, is_colored: bool
    ) -> None:
        if is_colored:
            print(
                f"{self.__WHITE}[{color}{symbol}{self.__WHITE}] {color}{message}{self.__WHITE}"
            )
        else:
            print(
                f"{self.__WHITE}[{color}{symbol}{self.__WHITE}] {self.__WHITE}{message}"
            )

    def _log_with_symbol(
        self, log: str, color: str, symbol: str, color_text: bool
    ) -> None:
        """
        A helper method to reduce repetition for success, error, warning, and info methods.
        This handles both colored and non-colored output logic.
        """
        is_colored = color_text if color_text is not None else self._colored_text
        self._print_log(message=log, color=color, symbol=symbol, is_colored=is_colored)

    def success(self, log: str, color_text=False) -> None:
        """Prints out [✔] and log in green."""
        self._log_with_symbol(log, self.__GREEN, "✔", color_text)

    def error(self, log: str, color_text=False) -> None:
        """Prints out [✖] and log in red."""
        self._log_with_symbol(log, self.__RED, "✖", color_text)

    def warning(self, log: str, color_text=False) -> None:
        """Prints out [!] and log in yellow."""
        self._log_with_symbol(log, self.__YELLOW, "!", color_text)

    def info(self, log: str, color_text=False) -> None:
        """Prints out [*] and log in blue."""
        self._log_with_symbol(log, self.__BLUE, "*", color_text)

    # this is bullshit
    def validate_type(self, arg_name: str, value: str):
        arg_type = self._arguments[arg_name].get("type")
        if arg_type == "int" and not self._is_valid_int(value):
            self._print_error(f"Invalid integer value for '{arg_name}': {value}")
        elif arg_type == "float" and not self._is_valid_float(value):
            self._print_error(f"Invalid float value for '{arg_name}': {value}")
        elif arg_type == "str" and not self._is_valid_string(value):
            self._print_error(f"Invalid string value for '{arg_name}': {value}")
        elif arg_type == "url" and not self._is_valid_url(value):
            self._print_error(f"Invalid URL provided for '{arg_name}': {value}")
        elif arg_type == "ip" and not self._is_valid_ip(value):
            self._print_error(f"Invalid IP address for '{arg_name}': {value}")
        elif arg_type == "port" and not self._is_valid_port(value):
            self._print_error(f"Invalid port for '{arg_name}': {value}")
        elif arg_type == "file" and not os.path.isfile(value):
            self._print_error(f"File does not exist or cannot be read: {value}")
        elif arg_type == "dir" and not os.path.isdir(value):
            self._print_error(f"Directory does not exist: {value}")
        elif arg_type == "email" and not self._is_valid_email(value):
            self._print_error(f"Invalid email address for '{arg_name}': {value}")

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL with simple regex."""
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]*[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ...or ipv4
            r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # or ipv6
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return re.match(regex, url) is not None

    def _is_valid_int(self, value: str) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False

    def _is_valid_float(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _is_valid_string(self, value: str) -> bool:
        return isinstance(value, str) and len(value) > 0

    def _is_valid_ip(self, ip: str) -> bool:
        """Validate if the input is valid IP address."""
        try:
            socket.inet_pton(socket.AF_INET, ip)
            return True
        except socket.error:
            try:
                socket.inet_pton(socket.AF_INET6, ip)
                return True
            except socket.error:
                return False

    def _is_valid_port(self, port: str) -> bool:
        """Ensure the port is within the valid range (1-65535)."""
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except ValueError:
            return False

    def _is_valid_email(self, email: str) -> bool:
        """Simple regex to check if email format is valid."""
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    # it would be cool to pass array of symbols
    def interactive(self, symbol: str = "", color: str = "") -> None:
        """
        Use input field instead of sys args

        params:
        Symbol: str -> symbol that will appear when prompting for input

        returns -> None
        """
        type_map = {
            "int": "integer (e.g., 123)",
            "float": "floating point number (e.g., 12.34)",
            "string": "a string of text",
            "url": "a valid URL (e.g., https://example.com)",
            "ip": "a valid IP address (e.g., 192.168.1.1)",
            "port": "a valid port number (1-65535)",
            "file": "a valid file path (e.g., /path/to/file)",
            "dir": "a valid directory path (e.g., /path/to/directory)",
            "email": "a valid email address (e.g., user@example.com)",
        }

        if color is not None:
            match color:
                case "red":
                    color = self.__RED
                case "green":
                    color = self.__GREEN
                case "blue":
                    color = self.__BLUE
                case "yellow":
                    color = self.__YELLOW
                case _:
                    color = ""

        color = color if color != "" else self.__GREEN
        symbol = symbol if symbol != "" else "?"

        for arg, details in self._arguments.items():
            if details["required"] and details["value"] is None:
                while True:
                    expected_type = details.get("type", "string")
                    type_message = type_map.get(expected_type, "a string of text")

                    if self._colored_text:
                        user_input = input(
                            f"[{color}{symbol}{self.__WHITE}] {self.__WHITE}Enter {arg} ({type_message}): "
                        )
                    else:
                        user_input = input(f"[{symbol}] Enter {arg} ({type_message}): ")

                    try:
                        self.validate_type(arg, user_input)
                        self._arguments[arg]["value"] = user_input
                        setattr(self, arg, user_input)
                        break
                    except Exception as e:
                        self._print_error(f"Error {str(e)}")

    #
    def run_async(self, func, *args, **kwargs):
        """Run a function asynchronously with multiple threads."""
        threads = kwargs.get("threads", 10)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future = executor.submit(func, *args, **kwargs)
            return future.result()

    #
    def print_types(self):
        """
        Display supported types by arg_type argument
        """
        print("""
int -> integer (e.g., 123)
float -> floating point number (e.g., 12.34)
string -> a string of text
url -> a valid URL (e.g., https://example.com)
ip -> a valid IP address (e.g., 192.168.1.1)
port -> a valid port number (1-65535)
file -> a valid file path (e.g., /path/to/file)
dir -> a valid directory path (e.g., /path/to/directory)
email -> a valid email address (e.g., user@example.com)""")
