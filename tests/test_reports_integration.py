import sys
from pathlib import Path

from workmate.workmate import main


def _read_expected(name: str) -> str:
    base = Path(__file__).parent / "expected"
    return (base / name).read_text(encoding="utf-8").rstrip()


def _strip_trailing_whitespace_per_line(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.rstrip().splitlines())


def test_default_report_matches_expected(monkeypatch, capsys):
    base = Path(__file__).parent
    e1 = base / "e1.log"
    e2 = base / "e2.log"

    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    monkeypatch.setattr(sys, "argv", ["workmate", "--file", str(e1), str(e2)])
    main()
    out = capsys.readouterr().out

    expected = _read_expected("default.txt")
    assert _strip_trailing_whitespace_per_line(
        out
    ) == _strip_trailing_whitespace_per_line(expected)


def test_average_report_matches_expected(monkeypatch, capsys):
    base = Path(__file__).parent
    e1 = base / "e1.log"
    e2 = base / "e2.log"

    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    monkeypatch.setattr(
        sys, "argv", ["workmate", "--file", str(e1), str(e2), "--report", "avg"]
    )
    main()
    out = capsys.readouterr().out

    expected = _read_expected("average.txt")
    assert _strip_trailing_whitespace_per_line(
        out
    ) == _strip_trailing_whitespace_per_line(expected)


def test_default_report_with_date_matches_expected(monkeypatch, capsys):
    base = Path(__file__).parent
    e1 = base / "e1.log"
    e2 = base / "e2.log"

    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["workmate", "--file", str(e1), str(e2), "--date", "2025-06-22"],
    )
    main()
    out = capsys.readouterr().out

    expected = _read_expected("default-date.txt")
    assert _strip_trailing_whitespace_per_line(
        out
    ) == _strip_trailing_whitespace_per_line(expected)


def test_average_report_with_date_matches_expected(monkeypatch, capsys):
    base = Path(__file__).parent
    e1 = base / "e1.log"
    e2 = base / "e2.log"

    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "workmate",
            "--file",
            str(e1),
            str(e2),
            "--report",
            "avg",
            "--date",
            "2025-06-22",
        ],
    )
    main()
    out = capsys.readouterr().out

    expected = _read_expected("avg-date.txt")
    assert _strip_trailing_whitespace_per_line(
        out
    ) == _strip_trailing_whitespace_per_line(expected)
