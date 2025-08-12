import sys
from pathlib import Path

import pytest

from workmate.workmate import main


def test_missing_file_exits_1(monkeypatch, capsys, tmp_path):
    # no path
    missing = tmp_path / "nope.log"

    monkeypatch.setattr(sys, "argv", ["workmate", "--file", str(missing)])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 1

    err = capsys.readouterr().err.lower()
    assert "file not found" in err


def test_bad_date_format_exits_2(monkeypatch, capsys):
    base = Path(__file__).parent
    e1 = base / "e1.log"

    # no format
    monkeypatch.setattr(
        sys, "argv", ["workmate", "--file", str(e1), "--date", "2025/06/22"]
    )
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 2

    err = capsys.readouterr().err.lower()
    assert "must be in yyyy-mm-dd" in err  # message from parse_date_arg
