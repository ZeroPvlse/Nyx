from src.nyx import Nyx


def main():
    nyx = Nyx()
    nyx.add_arg(
        long="website",
        short="w",
        description="add argument",
        required=True,
        arg_type="url",
    )
    nyx.config(
        description="this is test tool",
        example_input="--arg test --desc 'sum text'",
        color_text=True,
    )
    # nyx.print_types()
    nyx.parse_args()
    # nyx.interactive(symbol="*")
    nyx.success(f"running a scan on {nyx.website}")


if __name__ == "__main__":
    main()
