import argparse
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

COL_WIDTH_HANDLER = 30
COL_WIDTH_TIME = 10


def read_file(path: Path) -> list[dict]:
    """Reads a file in UTF-8, parses JSON strings
    and returns a list of dictionaries."""
    records: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue  # skips broken lines
            records.append(obj)
    return records


def make_report(records: list[dict]) -> None:
    """Prints a table with handler and time from each record."""
    COL_WIDTH_INDEX = len(str(len(records))) + 1
    header = (
        f"{'':<{COL_WIDTH_INDEX}} "
        f"{'handler':<{COL_WIDTH_HANDLER}} "
        f"{'time':<{COL_WIDTH_TIME}}"
    )
    total_width = COL_WIDTH_INDEX + COL_WIDTH_HANDLER + COL_WIDTH_TIME - 2
    separator = "–" * total_width
    row_format = (
        f"{{:<{COL_WIDTH_INDEX}}} "
        f"{{:<{COL_WIDTH_HANDLER}}} "
        f"{{:<{COL_WIDTH_TIME}}} "
    )
    lines: list[str] = [header, separator]

    for index, rec in enumerate(records):
        url = rec.get("url", "")
        response_time = rec.get("response_time", 0)
        lines.append(row_format.format(index, url, response_time))

    print("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="workmate",
        description="Process JSON log files and generate a report",
        epilog=(
            "Example:\n"
            "workmate --file e1.log e2.log"
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
    args = parser.parse_args()

    all_records: list[dict] = []
    for file_name in args.file:
        path = Path(file_name)
        try:
            file_records = read_file(path)
            all_records.extend(file_records)
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

    make_report(all_records)


def _log_traceback() -> None:
    with open("workmate_error.log", "a", encoding="utf-8") as lf:
        lf.write("\n" + "=" * 160 + "\n")
        lf.write(f"[{datetime.now().isoformat()}]\n")
        traceback.print_exc(file=lf)


if __name__ == "__main__":
    main()
