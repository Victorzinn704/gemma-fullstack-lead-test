import secrets
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": secrets.token_hex(32),
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "DEMO_PASSWORD": None,
    })

    with app.app_context():
        db.create_all()
        # Create demo user
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

def test_login_success(client):
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    assert b'Welcome to the Dashboard' in response.data
    assert b'testuser' in response.data

def test_login_failure(client):
    response = client.post('/login', data={'username': 'testuser', 'password': 'wrongpass'}, follow_redirects=True)
    assert b'Invalid username or password.' in response.data
    assert b'Welcome to the Dashboard' not in response.data

def test_dashboard_protection(client):
    # Try to access dashboard without login
    response = client.get('/dashboard', follow_redirects=True)
    assert b'Login' in response.data
    assert b'Welcome to the Dashboard' not in response.data

def test_logout(client):
    # Login first
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    # Logout
    response = client.post('/logout', follow_redirects=True)
    assert b'Login' in response.data
    assert b'Welcome to the Dashboard' not in response.data


def test_logout_requires_post(client):
    response = client.get('/logout')
    assert response.status_code == 405


def test_password_is_hashed(app):
    with app.app_context():
        user = User.query.filter_by(username="testuser").one()
        assert user.password_hash != "testpass"
        assert user.password_hash.startswith("pbkdf2:sha256:600000$")
