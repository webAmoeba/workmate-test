from pathlib import Path

from workmate.core.read_file import read_file


def test_read_file_ok():
    base = Path(__file__).parent
    p = base / "e1.log"
    records = read_file(p)
    assert isinstance(records, list)
    assert len(records) > 0
    assert "url" in records[0]
    assert "response_time" in records[0]


def test_read_file_broken_warn_and_log(tmp_path, capsys, monkeypatch):
    # workmate_error.log here
    monkeypatch.chdir(tmp_path)

    base = Path(__file__).parent
    src = base / "broken.log"
    p = tmp_path / "broken.log"
    p.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    records = read_file(p)
    # test for continue
    assert len(records) == 2

    # warning
    err = capsys.readouterr().err
    assert "broken JSON line(s)" in err
    assert "details in workmate_error.log" in err

    # .log crated
    logf = tmp_path / "workmate_error.log"
    assert logf.exists()
    content = logf.read_text(encoding="utf-8")
    assert "Broken JSON in" in content
    assert "Total broken lines: 1" in content


def test_read_file_empty(tmp_path):
    p = tmp_path / "empty.log"
    p.write_text("", encoding="utf-8")
    records = read_file(p)
    assert records == []
