import json
import sys
from datetime import datetime
from pathlib import Path


def read_file(path: Path) -> list[dict]:
    """Reads a file in UTF-8, parses JSON strings
    and returns a list of dictionaries."""
    records: list[dict] = []
    broken_count = 0
    first_broken_line = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                broken_count += 1
                if first_broken_line is None:
                    first_broken_line = line
                continue
            records.append(obj)

    if broken_count:
        with open("workmate_error.log", "a", encoding="utf-8") as lf:
            lf.write("\n" + "=" * 160 + "\n")
            lf.write(f"[{datetime.now().isoformat()}] Broken JSON in {path}\n")
            lf.write(f"Total broken lines: {broken_count}\n")
            lf.write(f"First broken line content: {first_broken_line}\n")
        print(
            f"Warning: {broken_count} broken JSON line(s) found in {path} "
            f"(details in workmate_error.log)",
            file=sys.stderr,
        )

    return records
