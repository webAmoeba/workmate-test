import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        prog="workmate",
        description="Process JSON log files and generate a report",
        epilog="""Example:
        workmate --file example1.log example2.log
        """,
    )
    parser.add_argument(
        "--file",
        required=True,
        nargs="+",
        metavar="LOG_PATH",
        help="- Path to log file(s)",
    )
    args = parser.parse_args()

    for file_name in args.file:
        path = Path(file_name)
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                print(line, end="")


if __name__ == "__main__":
    main()
