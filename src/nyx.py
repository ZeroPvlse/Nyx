from collections.abc import Callable
import sys
import os


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
        self, long: str, short: str, description: str, required: bool = False
    ) -> None:
        """
        Adds an argument to the CLI application.

        Parameters:
        long (str): Full parameter name (e.g., --test, --run).
        short (str): Short parameter name (e.g., -t, -r).
        description (str): A brief description of the parameter (e.g., "test currently running code").
        required (bool): Whether the parameter is mandatory. Default is False.

        Returns:
        None
        """
        self._arguments[long] = {
            "description": description,
            "value": None,
            "required": required,
        }
        self._short_to_long[short] = long
        self._help_options.append(
            {
                "long": long,
                "short": short,
                "description": description,
                "required": required,
            }
        )

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
            if arg.startswith("-"):
                if arg.startswith("--"):
                    if arg == "--help":
                        self._print_help()
                        sys.exit(0)

                    arg_name = arg.lstrip("-")
                elif len(arg) == 2:
                    if arg == "-h":
                        self._print_help()
                        sys.exit(0)

                    arg_name = self._short_to_long.get(arg.lstrip("-"))

                if arg_name and arg_name in self._arguments:
                    provided_args.add(arg_name)

                    next_arg_index = i + 1
                    has_next_value = next_arg_index < len(
                        sys.argv
                    ) - 1 and not sys.argv[next_arg_index + 1].startswith("-")

                    if has_next_value:
                        arg_value = sys.argv[next_arg_index + 1]
                        self._arguments[arg_name]["value"] = arg_value
                        setattr(namespace, arg_name, arg_value)
                    else:
                        if self._arguments[arg_name]["required"]:
                            if self._colored_text:
                                print(
                                    f"{self.__RED}Error: Argument '--{arg_name}' requires a value but none was provided.{self.__WHITE}"
                                )
                            else:
                                print(
                                    f"Error: Argument '--{arg_name}' requires a value but none was provided."
                                )
                            sys.exit(1)
                        else:
                            self._arguments[arg_name]["value"] = True
                            setattr(namespace, arg_name, True)

        missing_args = []
        for arg, details in self._arguments.items():
            if (
                isinstance(details, dict)
                and details.get("required")
                and arg not in provided_args
            ):
                missing_args.append(arg)

        if missing_args:
            if self._colored_text:
                print(
                    f"{self.__RED}Error: The following required arguments are missing: {', '.join(missing_args)}"
                )
            else:
                print(
                    f"Error: The following required arguments are missing: {', '.join(missing_args)}"
                )

            sys.exit(1)

        return namespace

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
            return self._arguments[name]
        raise AttributeError(f"'Nyx' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._arguments[name] = value

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
