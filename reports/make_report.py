COL_WIDTH_HANDLER = 30
COL_WIDTH_TIME = 10


def make_report(records: list[dict]) -> None:
    """Prints a table with handler and time from each record."""
    col_width_index = len(str(len(records))) + 1

    total_width = col_width_index + COL_WIDTH_HANDLER + COL_WIDTH_TIME - 2
    title_text = "Default report"
    title = (
        title_text
        if len(title_text) >= total_width
        else title_text.center(total_width)
    )

    header = (
        f"{'':<{col_width_index}} "
        f"{'handler':<{COL_WIDTH_HANDLER}} "
        f"{'time':<{COL_WIDTH_TIME}}"
    )
    separator = "-" * total_width

    row_format = (
        f"{{:<{col_width_index}}} "
        f"{{:<{COL_WIDTH_HANDLER}}} "
        f"{{:<{COL_WIDTH_TIME}}}"
    )

    lines: list[str] = ["", title, header, separator]
    for index, rec in enumerate(records):
        url = rec.get("url", "")
        response_time = rec.get("response_time", 0)
        lines.append(row_format.format(index, url, response_time))

    print("\n".join(lines))
