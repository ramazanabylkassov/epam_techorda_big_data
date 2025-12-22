import geohash2

def test_geohash_length_is_four():
    geohash = geohash2.encode(52.52, 13.405, precision=4)
    assert len(geohash) == 4

def test_geohash_is_deterministic():
    h1 = geohash2.encode(52.52, 13.405, precision=4)
    h2 = geohash2.encode(52.52, 13.405, precision=4)
    assert h1 == h2
