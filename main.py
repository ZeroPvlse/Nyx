from nyx.nyx import Nyx


def main():
    nyx = Nyx()

    nyx.add_argument("--arg", short="-a", desc="add argument")
    nyx.add_argument("--desc", short="-d", desc="description")

    nyx.parse_args(namespace=nyx)
    print(nyx.arg)


if __name__ == "__main__":
    main()
