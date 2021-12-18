from server import load_clubs, load_competitions


def test_load_clubs_is_type_list():
    result = []
    assert type(load_clubs()) == type(result)


def test_load_competitions_is_type_list():
    result = []
    assert type(load_competitions()) == type(result)
