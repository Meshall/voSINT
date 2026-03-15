from vosint.core.normalize import normalize_hits
from vosint.models import Hit


def test_normalize_merges_duplicates():
    hits = [
        Hit(engine="pinterest", frame_id="f1", url="HTTPS://Example.com/path/", title="a"),
        Hit(engine="bing_visual", frame_id="f2", url="https://example.com/path", title="b"),
    ]
    merged = normalize_hits(hits)
    assert len(merged) == 1
    assert merged[0].domain == "example.com"
    assert merged[0].support_engines == {"pinterest", "bing_visual"}
