import pytest
from pydantic import ValidationError
from app.schemas import UserCreate


def test_invalid_email_raises():
    with pytest.raises(ValidationError):
        UserCreate(username="user1", email="not-an-email", password="abcdef")
