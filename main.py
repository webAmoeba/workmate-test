import argparse
import sys
from pathlib import Path

from core.read_file import read_file
from core.utils import log_traceback
from reports.average import make_average_report
from reports.default import make_report


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="workmate",
        description="Process JSON log files and generate a report",
        epilog=("Example:\nworkmate --file e1.log e2.log"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--file",
        required=True,
        nargs="+",
        metavar="LOG_PATH",
        help="Path to log file(s)",
    )
    parser.add_argument(
        "--report",
        nargs="?",
        choices=["average", "avg"],
        help="Report type (default if omitted)",
    )
    args = parser.parse_args()
    all_records: list[dict] = []

    for file_name in args.file:
        path = Path(file_name)
        try:
            file_records = read_file(path)
            all_records.extend(file_records)
        except FileNotFoundError:
            print(f"Error: file not found: {path}", file=sys.stderr)
            log_traceback()
            sys.exit(1)
        except PermissionError:
            print(f"Error: permission denied: {path}", file=sys.stderr)
            log_traceback()
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Error: file is not UTF-8 text: {path}", file=sys.stderr)
            log_traceback()
            sys.exit(1)
        except Exception as e:
            print(
                f"Unexpected error while reading {path}: {e}", file=sys.stderr
            )
            log_traceback()
            sys.exit(1)

    if not args.report:
        make_report(all_records)
    elif args.report in ("avg", "average"):
        make_average_report(all_records)


if __name__ == "__main__":
    main()
