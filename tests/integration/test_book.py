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
    assert response.status_code == 403


def test_after_booking_points_available_are_reduced(client):
    """ vérifie qu'une fois la réservation effectuée, les points disponibles
     aient bien été diminués du tarif de la réservation."""
    datas = {'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '5'}
    response = client.post('/purchasePlaces', data=datas, follow_redirects=True)
    data = response.data.decode()
    # Après déduction des 5 places sur les 7 points, le template doit contenir :
    expected_result = "Points available: 8"

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
    assert response.status_code == 403


def test_not_possible_to_book_more_than_points_available(client, mocker):
    """ vérifie quil n'est pas possible de réserver plus de places que
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
    assert response.status_code == 403