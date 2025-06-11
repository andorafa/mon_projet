from unittest.mock import patch
from app.utils import email

@patch("smtplib.SMTP")
def test_send_email_success(mock_smtp):
    mock_instance = mock_smtp.return_value.__enter__.return_value
    email.send_email(
        to="test@example.com",
        subject="Test",
        body="Hello",
        attachment=None
    )
    assert mock_instance.send_message.called
