# Nyx - CLI Library for Rapid Cybersecurity & Ethical Hacking Tool Development

**Nyx** is a zero-dependency, minimal-boilerplate Python library designed to simplify the development of CLI tools. It provides colorful and customizable output, custom argument types, and themes for enhanced user experience.

## Installation

To install **Nyx**, run:

```bash
pip install nyx-cli
```

## Table of Contents

- [Installation](#installation)
- [Examples](#examples)
  - [Basic Usage](#basic-usage)
  - [Custom Logging](#custom-logging)
  - [Interactive Mode](#interactive-mode)
  - [Custom ASCII Art](#custom-ascii-art)
- [Features](#features)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Examples

### Basic Usage

To use **Nyx**, first import it:

```python
from nyx.nyx import Nyx

# Create a Nyx instance
nyx = Nyx()

nyx.add_arg(
    long="example",
    short="e",
    description="Custom example message",
    required=True,  # Ensures this argument is mandatory
    arg_type="str",  # Optional: Define expected type
)

# Configure Nyx (Displayed in help `-h` or `--help`)
nyx.config(
    description="This is a test tool",
    example_input="--example 'hi mum'",
)

# Parse command-line arguments
nyx.parse_args()

# Access argument values as object attributes
print(nyx.example)
```

### Custom Logging

Nyx provides functions for structured and color-coded logging:

```python
nyx = Nyx()
nyx.config(theme="default")  # Default theme if not explicitly set, but this is optional

nyx.success("Hello world", color_text=False)  # Default: Green
nyx.error("Something bad happened")  # Red
nyx.warning("Watch out!")  # Yellow
nyx.info("Random information")  # Blue
```

#### Output:

```zsh
  [✔] SUCCESS: Hello world
  [✖] ERROR: Something bad happened
  [!] WARNING: Watch out!
  [*] INFO: Random information
```

### Interactive Mode

Nyx supports an interactive mode, prompting users for arguments:

```python
nyx = Nyx()

nyx.add_arg(
    long="website",
    short="w",
    description="Website URL",
    required=True,
    arg_type="url",
)

nyx.interactive()  # Prompts user for input
```

It's worth mentioning that optional arguments will be type checked if there weren't empty!

You can also customize the input symbol and its color:

```python
nyx.interactive(symbol="&", color="red")  # Available colors: red, green, blue, yellow (default: white)
```

### Custom ASCII Art

If you want to display ASCII art before program execution, Nyx allows you to set a startup function:

```python
def print_ascii():
    print("Some ASCII art here")

# Two ways to set a startup function:
nyx = Nyx(starting_function=print_ascii)  # Option 1
nyx.init(print_ascii)  # Option 2
```

## Argument Handling

Nyx helps users by reminding them if they miss a required argument. If an argument is mandatory and not provided, Nyx will display an error message indicating which argument was missing. For example:

```zsh
Error: Argument '--website' requires a value but none was provided.
```

Example implementation:

```python
nyx.add_arg(
    long="website",
    short="w",
    description="Website URL",
    required=True,
    arg_type="url",
)

nyx.parse_args()
```

## Features

- **Zero dependency**: No external dependencies required
- **Minimal boilerplate**: Easy-to-use API for rapid development
- **Custom argument types**: Supports validation of argument types
- **Interactive mode**: Automatically prompts for required arguments
- **Theming support**: Customizable logging themes
- **Colorized output**: Enables clear and structured CLI feedback

## Documentation

To view supported argument types and available themes, use:

```python
nyx.get_types()
nyx.get_themes()
```

## Contributing

We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

Please ensure your code follows best practices and includes documentation where necessary.

## License

**Nyx** is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Notes

- **Argument Type Handling**: When using `arg_type` like `int`, `float`, etc., Nyx validates the input but returns it as a string. You must convert it back to the expected type.
- **Async Support**: The `run_async` method is currently broken. Avoid using it in production.


