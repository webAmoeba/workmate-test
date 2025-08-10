import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        prog="workmate",
    )
    parser.add_argument("--file", required=True, help="Path to file")
    args = parser.parse_args()

    path = Path(args.file)

    f = open(path, "r", encoding="utf-8")
    for line in f:
        print(line, end="")
    f.close()


if __name__ == "__main__":
    main()
