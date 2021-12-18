from server import flash_message_mail_unknown


def test_flash_message_mail_unknown():
    flash_message = "Sorry, but this email is unknown"
    assert flash_message_mail_unknown() == flash_message
