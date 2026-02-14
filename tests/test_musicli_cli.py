import pytest
from musicli import musicli

def test_help_message(capsys, monkeypatch):
    import sys
    monkeypatch.setattr(sys, 'argv', ['musicli', '--help'])
    with pytest.raises(SystemExit):
        musicli.start()
    out = capsys.readouterr().out
    assert "musicli CLI Help" in out
    assert "Usage:" in out
    assert "Features:" in out
