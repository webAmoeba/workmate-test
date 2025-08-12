import pytest

from workmate.core.utils import parse_date_arg


@pytest.mark.parametrize(
    "inp,expected",
    [
        ("2025-06-22", "2025-06-22"),
        ("2025-22-06", "2025-06-22"),  # USA format
        ("1999-1-2", "1999-01-02"),
    ],
)
def test_parse_date_arg_ok(inp, expected):
    assert parse_date_arg(inp) == expected


@pytest.mark.parametrize(
    "bad",
    [
        "2025/06/22",
        "2025-06",
        "abcd-06-22",
        "2025-99-99",
    ],
)
def test_parse_date_arg_bad(bad):
    with pytest.raises(SystemExit) as e:
        parse_date_arg(bad)
    assert e.value.code == 2
