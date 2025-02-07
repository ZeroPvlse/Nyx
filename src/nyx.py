from collections.abc import Callable
import sys
import os


class Nyx:
    def __init__(self, starting_function: Callable | None = None) -> None:
        """
        Initialize argument parser.

        params:
        starting_function -> function that will runn at the beginning of the program
                            it can't take any input nor return any value.
                            default value is None.
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
        Add arguments to run your cli app.

        params:
        long: str -> full parameter name.       example: --test, --run
        short: str -> short parameter name.     example: -t, -r
        desc: str -> parameter description.     example: "test currently running code"
        required: bool -> is this parameter required to run.
                 default value is False.

        return -> None
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
        Check sys.argv for arguments defined using add_arg.

        params:
        namespace -> class that will have args sigined as it's attributes.
                    default value is None.
                    if default is None, Nyx will be used as namespace object

        return -> if namespace has default value, then it returns Nyx object.
                  else it will return any object that was passed to namespace
        """
        if namespace is None:
            namespace = self

        arg_name = ""
        arg_value = ""
        for i, arg in enumerate(sys.argv[1:]):
            if arg.startswith("-"):
                if arg.startswith("--"):
                    if arg == "--help":
                        self._print_help()
                        sys.exit(0)

                    arg_name = arg.lstrip("-")
                    arg_value = (
                        sys.argv[i + 2] if i + 1 < len(sys.argv) else self._print_help()
                    )

                elif arg.startswith("-") and len(arg) == 2:
                    if arg == "-help":
                        self._print_help()
                        sys.exit(0)

                    short = arg.lstrip("-")
                    arg_name = self._short_to_long.get(short)
                    arg_value = (
                        sys.argv[i + 2] if i + 1 < len(sys.argv) else self._print_help()
                    )

                if arg_name and arg_name in self._arguments:
                    if arg_value:
                        self._arguments[arg_name]["value"] = arg_value
                        setattr(namespace, arg_name, arg_value)

        return namespace

    def config(
        self,
        description: str,
        example_input: str,
        color_text: bool = False,
    ):
        """
        Specify program description with example usage. this will execute
        when -h or --help is called

        params:
        description: str -> program description that will display at the
                            very begginig of help window

        example_input: str -> example program usage.
                            inclue just parameters and example inputs, excluding filename
                            example:
                            '--test main.py --time True'
                            filename that calls this function is included by default

        colored_output: bool -> should logs have colored text when printing.

        """
        try:
            example_input = str(example_input)
            self._example_usage = example_input
        except ValueError:
            print(
                f"example program usage must be a string but got {type(example_input)}"
            )

        try:
            description = str(description)
            self._program_description = description
        except ValueError:
            print(f"program description must be a string but got {type(example_input)}")

        self._colored_text = color_text

    def _print_help(self):
        script_name = os.path.basename(sys.argv[0])
        print(
            f"""{self._program_description}

Usage: {script_name} {self._example_usage}

Options:"""
        )
        for i in self._help_options:
            if i == {}:
                pass
            else:
                print(
                    f"\t--{i['long']},\t-{i['short']}\trequired: {i['required']}\t {i['description']}"
                )

    def init(self, func: Callable) -> None:
        """
        Display starting ascii art or literally anything else that should run at the beginning
        passed in function doesn't take anything nor return anything
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
    def success(self, log: str) -> None:
        """
        Prints out [✔] and log in green.
        if nyx.config has colored_output=False then only "✔" is green
        """
        if self._colored_text:
            print("\033[97m[\033[92m✔\033[97m] \033[92m" + log + "\033[97m")
        else:
            print("\033[97m[\033[92m✔\033[97m] " + log + "\033[97m")

    def error(self, log: str) -> None:
        """
        Prints out [✖] and log in red.
        if nyx.config has colored_output=False then only "✖" is red
        """
        if self._colored_text:
            print("\033[97m[\033[5;31m✖\033[97m] \033[5;31m" + log + "\033[97m")
        else:
            print("\033[97m[\033[5;31m✖\033[97m] " + log + "\033[97m")

    def warning(self, log: str) -> None:
        """
        Prints out [!] and log in yellow.
        if nyx.config has colored_output=False then only "!" is yellow
        """
        if self._colored_text:
            print("\033[97m[\033[93m!\033[97m] \033[93m" + log + "\033[97m")
        else:
            print("\033[97m[\033[93m!\033[97m] " + log + "\033[97m")

    def info(self, log: str) -> None:
        """
        Prints out [*] and log in blue.
        if nyx.config has colored_output=False then only "*" is blue
        """
        if self._colored_text:
            print("\033[97m[\033[96m*\033[97m] \033[96m" + log + "\033[97m")
        else:
            print("\033[97m[\033[96m*\033[97m] " + log + "\033[97m")
