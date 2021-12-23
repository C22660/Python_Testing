
def test_logout_redirection_on_index_page(client):
    response = client.get('/logout')

    assert response.status_code == 302
