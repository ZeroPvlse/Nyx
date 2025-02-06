import sys


class Nyx:
    def __init__(self):
        self._arguments = {}
        self._short_to_long = {}

    def add_argument(self, long: str, short: str, desc: str):
        self._arguments[long.lstrip("-")] = {"description": desc, "value": None}
        self._short_to_long[short.lstrip("-")] = long.lstrip("-")

    def parse_args(self, namespace=None):
        if namespace is None:
            namespace = self

        arg_name = ""
        arg_value = ""
        for i, arg in enumerate(sys.argv[1:]):
            if arg.startswith("-"):
                if arg.startswith("--"):
                    arg_name = arg.lstrip("-")
                    arg_value = sys.argv[i + 2] if i + 1 < len(sys.argv) else None
                elif arg.startswith("-") and len(arg) == 2:
                    short = arg.lstrip("-")
                    arg_name = self._short_to_long.get(short)
                    arg_value = sys.argv[i + 2] if i + 1 < len(sys.argv) else None

                if arg_name and arg_name in self._arguments:
                    if arg_value:
                        self._arguments[arg_name]["value"] = arg_value
                        setattr(namespace, arg_name, arg_value)

        return namespace

    def __getattr__(self, name):
        if name in self._arguments:
            return self._arguments[name]
        raise AttributeError(f"'Nyx' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._arguments[name] = value
