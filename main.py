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
        color_text=True,  # colorfull terminal ouptut
        theme="anon",  # more info in docs
    )
    # nyx.get_themes()
    # nyx.get_types()
    nyx.parse_args()
    # nyx.interactive()
    nyx.success(f"running a scan on {nyx.website}", color_text=True)
    nyx.error("error")
    nyx.warning("warning")
    nyx.info("information")


if __name__ == "__main__":
    main()
