"""Legacy UX tests updated for new structure."""

from musicli.core.lastfm import get_artist_albums


def test_album_list_count(mock_lastfm: object, capsys: object) -> None:
    """get_artist_albums returns 2 real albums (null filtered)."""
    albums = get_artist_albums("Radiohead")
    assert len(albums) == 2  # (null) filtered out
