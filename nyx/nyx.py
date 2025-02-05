import sys


class Nyx:
    def __init__(self):
        self._arguments = {}

    def add_argument(self, long: str, short: str, desc: str):
        self._arguments[long.lstrip("-")] = None

    def parse_args(self, namespace=None):
        if namespace is None:
            namespace = self

        args = sys.argv[1:]
        i = 0

        while i < len(args):
            arg = args[i]

            if arg.startswith("--"):
                arg_name = arg.lstrip("-")

                if arg_name in self._arguments:
                    value = True
                    if i + 1 < len(args) and not args[i + 1].startswith("--"):
                        value = args[i + 1]
                        i += 1

                    setattr(namespace, arg_name, value)
                    self._arguments[arg_name] = value

            i += 1

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
