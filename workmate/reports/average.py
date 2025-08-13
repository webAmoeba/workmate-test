from colorama import Fore, Style, init

init(autoreset=True)

COL_WIDTH_HANDLER = 30
COL_WIDTH_TOTAL = 10
COL_WIDTH_AVG = 15

ALIASES = ["avg"]


def make_average_report(
    records: list[dict], date_filter: str | None = None
) -> None:
    """Prints a table with handler, total and avg_response_time per handler."""
    stats: dict[str, tuple[int, float]] = {}

    for rec in records:
        url = rec.get("url", "")
        rt = rec.get("response_time", 0)
        try:
            rt_val = float(rt)
        except (TypeError, ValueError):
            continue

        if url in stats:
            cnt, total = stats[url]
            stats[url] = (cnt + 1, total + rt_val)
        else:
            stats[url] = (1, rt_val)

    col_width_index = len(str(len(stats))) + 1
    total_width = (
        col_width_index
        + COL_WIDTH_HANDLER
        + COL_WIDTH_TOTAL
        + COL_WIDTH_AVG
        + 6
    )
    if date_filter:
        title_text = (
            Fore.CYAN + f"Report Average ({date_filter})" + Style.RESET_ALL
        )
    else:
        title_text = Fore.CYAN + "Report Average" + Style.RESET_ALL
    title = (
        title_text
        if len(title_text) >= total_width
        else title_text.center(total_width)
    )
    header = (
        f"{'':<{col_width_index}} "
        f"{'handler':<{COL_WIDTH_HANDLER}} "
        f"{'total':<{COL_WIDTH_TOTAL}} "
        f"{'avg_response_time':<{COL_WIDTH_AVG}}"
    )
    separator = "-" * total_width
    row_format = (
        f"{{:<{col_width_index}}} "
        f"{{:<{COL_WIDTH_HANDLER}}} "
        f"{{:<{COL_WIDTH_TOTAL}}} "
        f"{{:<{COL_WIDTH_AVG}.3f}}"
    )
    sorted_stats = sorted(stats.items(), key=lambda x: x[1][0], reverse=True)
    lines: list[str] = ["", title, header, separator]

    for index, (url, (cnt, sum_rt)) in enumerate(sorted_stats):
        avg = sum_rt / cnt
        lines.append(row_format.format(index, url, cnt, avg))

    print("\n".join(lines))


def make_report(records: list[dict], date_filter: str | None = None) -> None:
    make_average_report(records, date_filter)
