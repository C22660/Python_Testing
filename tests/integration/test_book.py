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
