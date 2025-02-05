from nyx.nyx import Nyx


def main():
    nyx = Nyx()

    nyx.add_argument("--arg")

    nyx.parse_args(namespace=Nyx)


if __name__ == "__main__":
    main()
