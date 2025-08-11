import argparse
import sys
import traceback
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        prog="workmate",
        description="Process JSON log files and generate a report",
        epilog="""Example:
workmate --file e1.log e2.log""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--file",
        required=True,
        nargs="+",
        metavar="LOG_PATH",
        help="Path to log file(s)",
    )
    args = parser.parse_args()

    for file_name in args.file:
        path = Path(file_name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    print(line, end="")
        except FileNotFoundError:
            print(f"Error: file not found: {path}", file=sys.stderr)
            _log_traceback()
            sys.exit(1)
        except PermissionError:
            print(f"Error: permission denied: {path}", file=sys.stderr)
            _log_traceback()
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Error: file is not UTF-8 text: {path}", file=sys.stderr)
            _log_traceback()
            sys.exit(1)
        except Exception as e:
            print(
                f"Unexpected error while reading {path}: {e}", file=sys.stderr
            )
            _log_traceback()
            sys.exit(1)


def _log_traceback():
    with open("workmate_error.log", "a", encoding="utf-8") as lf:
        lf.write("\n" + "=" * 160 + "\n")
        lf.write(f"[{datetime.now().isoformat()}]\n")
        traceback.print_exc(file=lf)


if __name__ == "__main__":
    main()
