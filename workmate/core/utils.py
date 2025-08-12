import sys
import traceback
from datetime import datetime


def log_traceback() -> None:
    with open("workmate_error.log", "a", encoding="utf-8") as lf:
        lf.write("\n" + "=" * 160 + "\n")
        lf.write(f"[{datetime.now().isoformat()}]\n")
        traceback.print_exc(file=lf)


def parse_date_arg(date_str: str) -> str:
    """
    Accepts 'YYYY-MM-DD' or 'YYYY-DD-MM' and
    returns normalized 'YYYY-MM-DD'.
    If the format is incorrect, prints an error and terminates the program.
    """
    parts = date_str.split("-")
    if len(parts) != 3:
        print(
            "Error: --date must be in YYYY-MM-DD (or YYYY-DD-MM) format.",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        y = int(parts[0])
        a = int(parts[1])
        b = int(parts[2])
    except ValueError:
        print("Error: --date contains non-numeric parts.", file=sys.stderr)
        sys.exit(2)

    if 1 <= a <= 12 and 1 <= b <= 31:  # expected
        m, d = a, b
    elif 1 <= a <= 31 and 1 <= b <= 12:  # USA format
        m, d = b, a
    else:
        print("Error: --date values are out of range.", file=sys.stderr)
        sys.exit(2)

    return f"{y:04d}-{m:02d}-{d:02d}"
