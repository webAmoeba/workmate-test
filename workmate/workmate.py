import argparse
import sys
from pathlib import Path

from workmate.core.read_file import read_file
from workmate.core.utils import log_traceback, parse_date_arg
from workmate.reports import discover_reports


def main() -> None:
    report_funcs = discover_reports()
    parser = argparse.ArgumentParser(
        prog="workmate",
        description="Process JSON log files and generate a report",
        epilog=(
            "Examples:\n"
            "workmate --file e1.log e2.log\n"
            "workmate --file e1.log e2.log --report average\n"
            "workmate --file e1.log e2.log --report average --date 2025-06-22"
        ),
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
        choices=sorted(report_funcs.keys()),
        help="Report type (default if omitted)",
    )
    parser.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        help="Filter records by date (YYYY-MM-DD). Also accepts YYYY-DD-MM.",
    )
    args = parser.parse_args()
    all_records: list[dict] = []

    for file_name in args.file:
        path = Path(file_name)
        try:
            all_records.extend(read_file(path))
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

    if args.date:
        date_prefix = parse_date_arg(args.date)
        all_records = [
            record for record in all_records
            if isinstance(record.get("@timestamp"), str)
            and record["@timestamp"].startswith(date_prefix)
        ]

    report_name = args.report or "default"
    report_funcs[report_name](all_records, args.date if args.date else None)


if __name__ == "__main__":
    main()
