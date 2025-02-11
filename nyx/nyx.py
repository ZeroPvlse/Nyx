"""CLI parser library designed for making hacking/pentesting tools"""

# TODO: ADD CUSTOM THEMES IN THE FUTURE
# TODO: FIX ASYNC
# TODO: add auto type conversion

import os
import re
import socket
import sys
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor


class Nyx:
    __success = "\033[0;32m"
    __error = "\033[0;31m"
    __warning = "\033[0;33m"
    __info = "\033[36m"
    __text_color = "\033[0;37m"
    __succes_sym = "✔"
    __err_sym = "✖"
    __warn_sym = "!"
    __info_sym = "*"

    def __init__(self, starting_function: Callable | None = None) -> None:
        """
        Initializes the Nyx class and sets up the argument parser.

        Parameters:
        starting_function (Callable | None):
            A function to be executed at the start of the program.
            It cannot take input or return any values.
            Default is None.
        """
        self.__arguments = {}
        self.__short_to_long = {}
        if starting_function is not None:
            self.init(starting_function)

        self.__example_usage = ""
        self.__help_options = [{}]
        self.__program_description = ""

        self.__colored_text = False

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
        self.__arguments[long] = {
            "description": description,
            "value": None,
            "required": required,
            "type": arg_type,
        }
        self.__short_to_long[short] = long
        self.__help_options.append(
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
            self.__handle_help(arg)
            arg_name = self.__get_arg_name(arg)
            self.__process_argument(arg_name, i + 1, namespace, provided_args)  # pyright: ignore[reportArgumentType]

        self.__check_missing_args(provided_args)
        return namespace

    def __print_error(self, message: str):
        if self.__colored_text:
            print(f"{self.__error}Error: {message}{self.__text_color}")
        else:
            print(f"Error: {message}")
        sys.exit(1)

    def __handle_help(self, arg: str):
        if arg in ("--help", "-h"):
            self.__print_help()
            sys.exit(0)

    def __get_arg_name(self, arg: str):
        if arg.startswith("--"):
            return arg.lstrip("-")
        elif len(arg) == 2:
            return self.__short_to_long.get(arg.lstrip("-"))
        return None

    def __process_argument(
        self, arg_name: str, next_arg_index: int, namespace, provided_args: set
    ):
        if arg_name and arg_name in self.__arguments:
            provided_args.add(arg_name)
            has_next_value = next_arg_index < len(sys.argv) - 1 and not sys.argv[
                next_arg_index + 1
            ].startswith("-")

            if has_next_value:
                arg_value = sys.argv[next_arg_index + 1]
                self.__arguments[arg_name]["value"] = arg_value
                setattr(namespace, arg_name, arg_value)
                self.__validate_type(arg_name, arg_value)
            else:
                if self.__arguments[arg_name]["required"]:
                    self.__print_error(
                        f"Argument '--{arg_name}' requires a value but none was provided."
                    )
                else:
                    self.__arguments[arg_name]["value"] = True
                    setattr(namespace, arg_name, True)

    def __check_missing_args(self, provided_args: set):
        missing_args = [
            arg
            for arg, details in self.__arguments.items()
            if details.get("required") and arg not in provided_args
        ]
        if missing_args:
            self.__print_error(
                f"The following required arguments are missing: {', '.join(missing_args)}"
            )

    #
    def config(
        self,
        description: str = "",
        example_input: str = "",
        color_text: bool = False,
        theme: str = "",
    ):
        """
        Sets the program description, example usage, and color settings for output.

        Parameters:
        description (str): A description of the program, shown at the start of the help screen.
        example_input (str): Example program usage, excluding the filename.
                             Format: '--test main.py --time True'.
        color_text (bool): Whether to print colored text in logs. Default is False.
        theme (str):

        Returns:
        None
        """
        try:
            self.__example_usage = str(example_input)
        except ValueError:
            print(
                f"Example program usage must be a string, but got {type(example_input)}"
            )

        try:
            self.__program_description = str(description)
        except ValueError:
            print(f"Program description must be a string, but got {type(description)}")

        self.__colored_text = color_text

        if theme != "":
            self.__pick_theme(theme)

    def __print_help(self):
        """
        Prints the help message with program description, usage, and available options.

        Returns:
        None
        """
        script_name = os.path.basename(sys.argv[0])
        print(
            f"""{self.__program_description}

Usage: {script_name} {self.__example_usage}

Options:"""
        )
        for i in self.__help_options:
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
        if name in self.__arguments:
            return self.__arguments[name]["value"]
        raise AttributeError(f"'Nyx' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        elif name in self.__arguments:
            self.__arguments[name]["value"] = value
        else:
            super().__setattr__(name, value)

    # the "cool ui part etc"
    def __print_log(
        self, message: str, color: str, symbol: str, is_colored: bool
    ) -> None:
        if is_colored:
            print(
                f"{self.__text_color}[{color}{symbol}{self.__text_color}] {color}{message}{self.__text_color}"
            )
        else:
            print(
                f"{self.__text_color}[{color}{symbol}{self.__text_color}] {self.__text_color}{message}"
            )

    def __log_with_symbol(
        self, log: str, color: str, symbol: str, color_text: bool
    ) -> None:
        """
        A helper method to reduce repetition for success, error, warning, and info methods.
        This handles both colored and non-colored output logic.
        """
        is_colored = color_text if color_text is not None else self.__colored_text
        self.__print_log(message=log, color=color, symbol=symbol, is_colored=is_colored)

    # TODO: fix handling logic if global config color is false it should not color it by default

    def success(self, log: str, color_text=True) -> None:
        """With default theme prints out [✔] and log in green."""
        log = f"SUCCESS: {log}"
        self.__log_with_symbol(log, self.__success, self.__succes_sym, color_text)

    def error(self, log: str, color_text=True) -> None:
        """With default theme prints out [✖] and log in red."""
        log = f"ERROR: {log}"
        self.__log_with_symbol(log, self.__error, self.__err_sym, color_text)

    def warning(self, log: str, color_text=True) -> None:
        """With default theme prints out [!] and log in yellow."""
        log = f"WARNING: {log}"
        self.__log_with_symbol(log, self.__warning, self.__warn_sym, color_text)

    def info(self, log: str, color_text=True) -> None:
        """With default theme prints out [*] and log in blue."""
        log = f"INFO: {log}"
        self.__log_with_symbol(log, self.__info, self.__info_sym, color_text)

    def __validate_type(self, arg_name: str, value: str):
        arg_type = self.__arguments[arg_name].get("type")
        if arg_type == "int" and not self.__is_valid_int(value):
            self.__print_error(f"Invalid integer value for '{arg_name}': {value}")
        elif arg_type == "float" and not self.__is_valid_float(value):
            self.__print_error(f"Invalid float value for '{arg_name}': {value}")
        elif arg_type == "str" and not self.__is_valid_string(value):
            self.__print_error(f"Invalid string value for '{arg_name}': {value}")
        elif arg_type == "url" and not self.__is_valid_url(value):
            self.__print_error(f"Invalid URL provided for '{arg_name}': {value}")
        elif arg_type == "ip" and not self.__is_valid_ip(value):
            self.__print_error(f"Invalid IP address for '{arg_name}': {value}")
        elif arg_type == "port" and not self.__is_valid_port(value):
            self.__print_error(f"Invalid port for '{arg_name}': {value}")
        elif arg_type == "file" and not os.path.isfile(value):
            self.__print_error(f"File does not exist or cannot be read: {value}")
        elif arg_type == "dir" and not os.path.isdir(value):
            self.__print_error(f"Directory does not exist: {value}")
        elif arg_type == "email" and not self.__is_valid_email(value):
            self.__print_error(f"Invalid email address for '{arg_name}': {value}")

    def __is_valid_url(self, url: str) -> bool:
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

    def __is_valid_int(self, value: str) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False

    def __is_valid_float(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def __is_valid_string(self, value: str) -> bool:
        return isinstance(value, str) and len(value) > 0

    def __is_valid_ip(self, ip: str) -> bool:
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

    def __is_valid_port(self, port: str) -> bool:
        """Ensure the port is within the valid range (1-65535)."""
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except ValueError:
            return False

    def __is_valid_email(self, email: str) -> bool:
        """Simple regex to check if email format is valid."""
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    # it would be cool to pass array of symbols
    # optionals should be also displayed to users
    def interactive(self, symbol: str = "", color: str = "") -> None:
        """
        Gets argumets from running input fields. Optional values CAN have empty values.

        Parameters:
        symbol (str): symbol that will appear in input prompt

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
                    color = self.__error
                case "green":
                    color = self.__success
                case "blue":
                    color = self.__info
                case "yellow":
                    color = self.__warning
                case _:
                    color = ""

        color = color if color != "" else self.__success
        symbol = symbol if symbol != "" else "?"

        for arg, details in self.__arguments.items():
            if details["required"] and details["value"] is None:
                while True:
                    expected_type = details.get("type", "string")
                    type_message = type_map.get(expected_type, "a string of text")

                    if self.__colored_text:
                        user_input = input(
                            f"[{color}{symbol}{self.__text_color}] {self.__text_color}Enter {arg} ({type_message}): "
                        )
                    else:
                        user_input = input(f"[{symbol}] Enter {arg} ({type_message}): ")

                    try:
                        self.__validate_type(arg, user_input)
                        self.__arguments[arg]["value"] = user_input
                        setattr(self, arg, user_input)
                        break
                    except Exception as e:
                        self.__print_error(f"Error {str(e)}")
            # this is for optionals they are handled last cuz they aren't that important
            else:
                while True:
                    expected_type = details.get("type", "string")
                    type_message = type_map.get(expected_type, "a string of text")

                    if self.__colored_text:
                        user_input = input(
                            f"[{color}{symbol}{self.__text_color}] {self.__text_color}Optional {arg} ({type_message}): "
                        )
                    else:
                        user_input = input(f"[{symbol}] Enter {arg} ({type_message}): ")

                    try:
                        if user_input == "":
                            self.__arguments[arg]["value"] = user_input
                            break
                        else:
                            self.__validate_type(arg, user_input)
                            self.__arguments[arg]["value"] = user_input
                            setattr(self, arg, user_input)
                            break
                    except Exception as e:
                        self.__print_error(f"Error {str(e)}")

    #
    def __run_async(self, func, *args, **kwargs):
        """Run a function asynchronously with multiple threads."""
        threads = kwargs.get("threads", 10)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future = executor.submit(func, *args, **kwargs)
            return future.result()

    #
    def get_types(self):
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

    def get_themes(self):
        """
        Display supported themes
        """

        print("""
THEMES:
    "default"
        \033[92m"success": ✔ \033[0;37m
        \033[5;91m"error": ✖ \033[0;37m
        \033[93m"warning": ! \033[0;37m
        \033[96m"info": * \033[0;37m

    "anon"
        \033[97m"success": □ \033[0;37m
        \033[91m"error": ■ \033[0;37m
        \033[93m"warning": ▲ \033[0;37m  
        \033[90m"info": ○   \033[0;37m

    "hack"
        \033[92m"success": ++  \033[0;37m
        \033[91m"error": --    \033[0;37m
        \033[93m"warning": ## \033[0;37m
        \033[94m"info": @@ \033[0;37m

    "cyber"
        \033[96m"success": ** \033[0;37m
        \033[91m"error": XX \033[0;37m
        \033[33m"warning": !! \033[0;37m
        \033[34m"info": ## \033[0;37m

    "ghost"
        \033[97m"success": ~~ \033[0;37m
        \033[91m"error": XX \033[0;37m
        \033[35m"warning": ^^ \033[0;37m
        \033[90m"info": __ \033[0;37m

    "virus"
        \033[92m"success": ++ \033[0;37m
        \033[91m"error": ** \033[0;37m
        \033[93m"warning": !! \033[0;37m
        \033[96m"info": ## \033[0;37m

    "pwn"
        \033[35m"success": ^_^ \033[0;37m
        \033[91m"error": X_X \033[0;37m
        \033[93m"warning": #_# \033[0;37m
        \033[97m"info": *_* \033[0;37m

    "stealth"
        \033[90m"success": ~~~ \033[0;37m
        \033[91m"error": *** \033[0;37m
        \033[90m"warning": --- \033[0;37m
        \033[94m"info": +++ \033[0;37m

    "binary"
        \033[92m"success": 00 \033[0;37m
        \033[91m"error": 01 \033[0;37m
        \033[93m"warning": !! \033[0;37m
        \033[96m"info": ?? \034[0;37m

    "glitch"
        \033[96m"success": %%% \033[0;37m
        \033[95m"error": &&& \033[0;37m
        \033[93m"warning": ### \033[0;37m
        \033[94m"info": @@@ \033[0;37m

    "root"
        \033[93m"success": $ \033[0;37m
        \033[91m"error": ! \033[0;37m
        \033[33m"warning": # \033[0;37m
        \033[97m"info": & \033[0;37m
        """)

    def __pick_theme(self, theme: str = "") -> None:
        """
        Adjust program style to match given theme
        Parameters:
        theme (str): style of the output
        """
        themes = {
            "default": {
                "success": ("✔", "\033[92m"),
                "error": ("✖", "\033[5;91m"),
                "warning": ("!", "\033[93m"),
                "info": ("*", "\033[96m"),
            },
            "anon": {
                "success": ("□", "\033[97m"),
                "error": ("■", "\033[91m"),
                "warning": ("▲", "\033[93m"),
                "info": ("○", "\033[90m"),
            },
            "hack": {
                "success": ("++", "\033[92m"),
                "error": ("--", "\033[91m"),
                "warning": ("##", "\033[93m"),
                "info": ("@@", "\033[94m"),
            },
            "cyber": {
                "success": ("**", "\033[96m"),
                "error": ("XX", "\033[91m"),
                "warning": ("!!", "\033[33m"),
                "info": ("##", "\033[34m"),
            },
            "ghost": {
                "success": ("~~", "\033[97m"),
                "error": ("XX", "\033[91m"),
                "warning": ("^^", "\033[35m"),
                "info": ("__", "\033[90m"),
            },
            "virus": {
                "success": ("++", "\033[92m"),
                "error": ("**", "\033[91m"),
                "warning": ("!!", "\033[93m"),
                "info": ("##", "\033[96m"),
            },
            "pwn": {
                "success": ("^_^", "\033[35m"),
                "error": ("X_X", "\033[91m"),
                "warning": ("#_#", "\033[93m"),
                "info": ("*_*", "\033[97m"),
            },
            "stealth": {
                "success": ("~~~", "\033[90m"),
                "error": ("***", "\033[91m"),
                "warning": ("---", "\033[90m"),
                "info": ("+++", "\033[94m"),
            },
            "binary": {
                "success": ("00", "\033[92m"),
                "error": ("01", "\033[91m"),
                "warning": ("!!", "\033[93m"),
                "info": ("??", "\033[96m"),
            },
            "glitch": {
                "success": ("%%%", "\033[96m"),
                "error": ("&&&", "\033[95m"),
                "warning": ("###", "\033[93m"),
                "info": ("@@@", "\033[94m"),
            },
            "root": {
                "success": ("$", "\033[93m"),
                "error": ("!", "\033[91m"),
                "warning": ("#", "\033[33m"),
                "info": ("&", "\033[97m"),
            },
        }

        if theme in themes:
            self.__set_theme(
                success=themes[theme]["success"],
                error=themes[theme]["error"],
                warning=themes[theme]["warning"],
                info=themes[theme]["info"],
            )
        else:
            raise ValueError(
                "Invalid theme! Refer to the docs for more info about themes"
            )

    def __set_theme(
        self,
        success: tuple[str, str],
        error: tuple[str, str],
        warning: tuple[str, str],
        info: tuple[str, str],
    ):
        """
        Creates a theme based on input:
        """
        self.__succes_sym, self.__success = success
        self.__err_sym, self.__error = error
        self.__warn_sym, self.__warning = warning
        self.__info_sym, self.__info = info
