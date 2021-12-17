""" Ici, client associé à une url qui va appeler une vue système => tests d'intégration
"""


def test_login_failed_because_email_user_unknown(client, mocker):
    """ vérifie que la fonction show_summary affiche bien un message lorsque
     le mail saisi est inconnu"""
    # email = "john@simplylift.co"
    email = "john_doe@exo.com"
    # !! Pour ne pas être dépendant du message qui pourrait être modifié,
    # Ici, définition du message attendu
    flash_message = "Sorry, but this email is unknown"
    # mock de la fonction qui génère le message pour y affecter le message attendu
    # ---- Solution avec monkeypatch (si utilisé, ajouter , monkeypatch dans les paramètres) :
    # def mock_flash_message_mail_unknown():
    #     return flash_message
    # monkeypatch.setattr('server.flash_message_mail_unknown', mock_flash_message_mail_unknown)
    # ----- Solution avec mocker :
    mocker.patch('server.flash_message_mail_unknown', return_value=flash_message)

    response = client.post('/showSummary', data={'email': email}, follow_redirects=True)
    data = response.data.decode()
    assert flash_message in data
    assert response.status_code == 404
