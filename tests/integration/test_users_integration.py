import os
import time
import pytest
from fastapi.testclient import TestClient

from main import app
from app.db import init_db


@pytest.fixture(autouse=True)
def setup_db():
    # Ensure tables exist for the configured DATABASE_URL
    # If using the default sqlite file, remove it to start fresh between runs
    try:
        from app.db import DATABASE_URL, engine
        if DATABASE_URL.startswith("sqlite") and "test_db.sqlite" in DATABASE_URL:
            # Close all connections before removing file
            engine.dispose()
            import os
            if os.path.exists("./test_db.sqlite"):
                os.remove("./test_db.sqlite")
    except Exception:
        pass
    init_db()
    yield
    # Clean up after each test
    try:
        from app.db import engine
        engine.dispose()
    except Exception:
        pass


def test_register_user_success():
    """Test successful user registration."""
    client = TestClient(app)
    payload = {"username": "testuser1", "email": "testuser1@example.com", "password": "password123"}
    r = client.post("/users/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    # Now returns JWT token instead of user data
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_register_duplicate_user():
    """Test registration with duplicate username/email returns 400."""
    client = TestClient(app)
    payload = {"username": "testuser2", "email": "testuser2@example.com", "password": "password123"}
    r1 = client.post("/users/register", json=payload)
    assert r1.status_code == 200
    
    # Attempt duplicate
    r2 = client.post("/users/register", json=payload)
    assert r2.status_code == 400
    response_data = r2.json()
    assert "error" in response_data and "already exists" in response_data["error"].lower()


def test_register_invalid_email():
    """Test registration with invalid email format returns 400."""
    client = TestClient(app)
    payload = {"username": "testuser3", "email": "not-an-email", "password": "password123"}
    r = client.post("/users/register", json=payload)
    assert r.status_code == 400


def test_login_user_success():
    """Test successful user login."""
    client = TestClient(app)
    # First register a user
    register_payload = {"username": "loginuser1", "email": "loginuser1@example.com", "password": "mypassword"}
    client.post("/users/register", json=register_payload)
    
    # Now login
    login_payload = {"username": "loginuser1", "password": "mypassword"}
    r = client.post("/users/login", json=login_payload)
    assert r.status_code == 200
    data = r.json()
    # Now returns JWT token instead of user data
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_login_invalid_username():
    """Test login with non-existent username returns 401."""
    client = TestClient(app)
    login_payload = {"username": "nonexistent", "password": "anypassword"}
    r = client.post("/users/login", json=login_payload)
    assert r.status_code == 401
    response_data = r.json()
    # May return error as string or in detail field depending on exception handler
    assert "invalid" in str(response_data).lower() or "detail" in response_data


def test_login_invalid_password():
    """Test login with wrong password returns 401."""
    client = TestClient(app)
    # Register a user
    register_payload = {"username": "loginuser2", "email": "loginuser2@example.com", "password": "correctpassword"}
    client.post("/users/register", json=register_payload)
    
    # Try to login with wrong password
    login_payload = {"username": "loginuser2", "password": "wrongpassword"}
    r = client.post("/users/login", json=login_payload)
    assert r.status_code == 401
    response_data = r.json()
    assert "error" in response_data and "invalid" in response_data["error"].lower()


def test_register_and_uniqueness():
    """Legacy test for backward compatibility."""
    client = TestClient(app)
    payload = {"username": "tester1", "email": "tester1@example.com", "password": "pass123"}
    r = client.post("/users/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    # Now returns JWT token instead of user data
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

    # Attempt duplicate
    r2 = client.post("/users/register", json=payload)
    assert r2.status_code == 400


def test_invalid_email_via_endpoint():
    """Legacy test for backward compatibility."""
    client = TestClient(app)
    payload = {"username": "tester2", "email": "not-an-email", "password": "pass123"}
    r = client.post("/users/register", json=payload)
    # This application maps validation errors to HTTP 400 in the handler
    assert r.status_code == 400
