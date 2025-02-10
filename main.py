from src.nyx import Nyx


def main():
    nyx = Nyx()
    nyx.add_arg(long="arg", short="a", description="add argument", required=True)
    nyx.add_arg(long="desc", short="d", description="description", required=True)
    nyx.config(
        description="this is test tool",
        example_input="--arg test --desc 'sum text'",
        color_text=True,
    )
    nyx.parse_args()


if __name__ == "__main__":
    main()
