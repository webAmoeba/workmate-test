import traceback
from datetime import datetime


def log_traceback() -> None:
    with open("workmate_error.log", "a", encoding="utf-8") as lf:
        lf.write("\n" + "=" * 160 + "\n")
        lf.write(f"[{datetime.now().isoformat()}]\n")
        traceback.print_exc(file=lf)
