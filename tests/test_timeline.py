from vosint.core.timeline import rank_timeline
from vosint.models import Hit


def test_rank_timeline_known_dates_first():
    a = Hit(engine="p", frame_id="1", url="https://a", date_raw="2021-01-01")
    b = Hit(engine="p", frame_id="2", url="https://b")
    a.date_parsed = __import__("datetime").datetime(2021, 1, 1)
    out = rank_timeline([b, a])
    assert out[0].url == "https://a"
