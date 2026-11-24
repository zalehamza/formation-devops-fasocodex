from portal import calculate_fee


def test_fee():
    assert calculate_fee(100) == 2.0


def test_zero_amount():
    assert calculate_fee(0) == 0.0


def test_large_amount():
    assert calculate_fee(5000) == 100.0
