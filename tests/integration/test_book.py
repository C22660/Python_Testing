import server

""" Ici, client associé à une url qui va appeler une vue système => tests d'intégration
"""


def test_booking_place_in_past_competition_must_be_impossible(client):
    """ vérifie que la réservation sur des évennements passés est impossible.
    Un message d'erreur doit être alors affiché sur la page book.html
    La page booking.html ne doit être accessible que pour des compétitions en cours.
    """
    flash_message = 'Sorry, this event is already passed. Impossible to book it'
    response = client.get(f'/book/Fall Classic/Simply Lift')
    data = response.data.decode()

    assert flash_message in data
    assert response.status_code == 200


def test_after_booking_points_available_are_reduced(client):
    """ vérifie qu'une fois la réservation effectuée, les points disponibles
     aient bien été diminués du tarif de la réservation."""
    datas = {'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '2'}
    response = client.post('/purchasePlaces', data=datas, follow_redirects=True)
    data = response.data.decode()
    # Après déduction des 2 places, soit 6 points sur les 13 points, le template doit contenir :
    expected_result = "Points available: 7"

    assert expected_result in data
    assert response.status_code == 200


def test_not_possible_to_book_more_than_twelve_places(client):
    """ vérifie quil n'est pas possible de réserver plus de 12 places."""
    datas = {'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '20'}
    # flash_message = "Sorry, it's not possible to book more than 12 places."
    flash_message = "Sorry, it&#39;s not possible to book more than 12 places."
    response = client.post('/purchasePlaces', data=datas, follow_redirects=True)
    # data = response.data.decode("latin1")
    data = response.data.decode()

    assert flash_message in data
    assert response.status_code == 200


def test_not_possible_to_book_more_than_points_available(client, mocker):
    """ vérifie qu'il n'est pas possible de réserver plus de places que
     de points disponibles pour le club."""
    # création d'un club avec un nombre de place faible :
    fake_club = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "3"
        }]
    # remplacement des données du json par ce club modifié
    mocker.patch.object(server, 'clubs', fake_club)
    datas = {'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '10'}
    flash_message = "Sorry, you have only 3 points."
    response = client.post('/purchasePlaces', data=datas, follow_redirects=True)
    data = response.data.decode()

    assert flash_message in data
    assert response.status_code == 200


def test_not_possible_to_book_more_than_places_available(client, mocker):
    """ vérifie qu'il n'est pas possible de réserver plus de places que
     de places disponibles pour une compétition."""
    # création d'une compétation avec un nombre de place faible :
    fake_competition = [
        {
            "name": "Spring Festival",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "3"
        }]
    # remplacement des données clubs car elles ont pu être modifiées en dur par les précédents tests
    # se qui fait choué le test quanf il n'est pas lancé individuelement.
    fake_clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {"name": "She Lifts",
         "email": "kate@shelifts.co.uk",
         "points": "12"
         }
    ]
    # remplacement des données du json par cette compétition modifiée
    mocker.patch.object(server, 'competitions', fake_competition)
    # remplacement des données du json par ces compétitions modifiée
    mocker.patch.object(server, 'clubs', fake_clubs)
    datas = {'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '4'}
    flash_message = "Sorry, not possible to book more than places available."
    response = client.post('/purchasePlaces', data=datas, follow_redirects=True)
    data = response.data.decode()

    assert flash_message in data
    assert response.status_code == 200
