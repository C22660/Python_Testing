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
