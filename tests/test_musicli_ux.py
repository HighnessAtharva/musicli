import pytest
from musicli import musicli

def test_album_list_count(monkeypatch, capsys):
    class DummyArtist:
        def get_top_albums(self):
            class DummyAlbum:
                def __init__(self, name):
                    self.item = name
            return [DummyAlbum("A - Album1"), DummyAlbum("A - Album2")]
    monkeypatch.setattr(musicli.network, "get_artist", lambda name: DummyArtist())
    albums = musicli.get_album_list("A")
    out = capsys.readouterr().out
    assert "Found 2 albums" in out
    assert len(albums) == 3  # includes EXIT
