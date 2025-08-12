from workmate.reports.average import make_report


def test_average_skips_invalid_response_time(capsys):
    records = [
        {"url": "/a", "response_time": "oops"},
        {"url": "/a", "response_time": 0.2},
        {"url": "/b", "response_time": None},
    ]
    make_report(records)
    out = capsys.readouterr().out

    # total=1 avg=0.200
    assert "/a" in out
    assert "1" in out
    assert "0.200" in out

    # continue
    assert "/b" not in out


# empty report
def test_average_empty_input(capsys):
    make_report([])
    out = capsys.readouterr().out
    assert "Report Average" in out
    assert not any(line and line[0].isdigit() for line in out.splitlines())
