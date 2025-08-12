import argparse
import importlib
import pkgutil
import sys
from pathlib import Path

import workmate.reports as reports_pkg
from workmate.core.read_file import read_file
from workmate.core.utils import log_traceback


def discover_reports() -> dict[str, callable]:
    """Searches all modules in workmate.reports
    with function make_report(records)."""
    discovered: dict[str, callable] = {}
    for _, module_name, _ in pkgutil.iter_modules(reports_pkg.__path__):
        mod = importlib.import_module(f"{reports_pkg.__name__}.{module_name}")
        fn = getattr(mod, "make_report", None)
        if callable(fn):
            discovered[module_name] = fn

            for alias in getattr(mod, "ALIASES", []):
                discovered.setdefault(alias, fn)
    return discovered


def main() -> None:
    report_funcs = discover_reports()
    parser = argparse.ArgumentParser(
        prog="workmate",
        description="Process JSON log files and generate a report",
        epilog="Example:\n  workmate --file e1.log e2.log [--report average]",
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

    report_name = args.report or "default"
    report_funcs[report_name](all_records)


if __name__ == "__main__":
    main()
