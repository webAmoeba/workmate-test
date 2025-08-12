COL_WIDTH_HANDLER = 30
COL_WIDTH_TIME = 10


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
