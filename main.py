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

    # nyx.get_themes()
    # nyx.get_types()
    nyx.parse_args()
    nyx.success(f"running a scan on {nyx.website}", color_text=True)


def print_asci():
    print("ascii")


if __name__ == "__main__":
    main()
