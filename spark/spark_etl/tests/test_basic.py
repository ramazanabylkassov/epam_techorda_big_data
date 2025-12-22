import geohash2

def test_geohash_length():
    assert len(geohash2.encode(52.52, 13.405, 4)) == 4

def test_geohash_is_deterministic():
    assert geohash2.encode(52.52, 13.405, 4) == geohash2.encode(52.52, 13.405, 4)
