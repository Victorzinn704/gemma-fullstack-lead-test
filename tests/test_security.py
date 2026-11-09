import re
import secrets
import pytest
from app import create_app, db
from app.models import User

def settings():
    return {"TESTING": True, "SECRET_KEY": secrets.token_hex(32),
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}

def test_weak_or_missing_secret_refuses_startup():
    for secret in (None, "short"):
        with pytest.raises(RuntimeError):
            create_app(settings() | {"SECRET_KEY": secret})

def test_csrf_required_and_valid_form_can_login_and_logout():
    app = create_app(settings())
    with app.app_context():
        db.create_all()
        user = User(username="testuser")
        password = secrets.token_urlsafe(24)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    client = app.test_client()
    assert client.post("/login", data={"username": "testuser", "password": password}).status_code == 400
    page = client.get("/login").get_data(as_text=True)
    token = re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)
    assert client.post("/login", data={"username": "testuser", "password": password, "csrf_token": token}).status_code == 302
    assert client.get("/dashboard").status_code == 200
    assert client.post("/logout").status_code == 400
    assert client.post("/logout", data={"csrf_token": token}).status_code == 302
    assert client.get("/dashboard").status_code == 302

def test_database_creation_is_explicit_and_security_headers_present():
    app = create_app(settings())
    with app.app_context():
        from sqlalchemy import inspect
        assert inspect(db.engine).get_table_names() == []
    response = app.test_client().get("/login")
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
    assert response.headers["Cache-Control"] == "no-store"
