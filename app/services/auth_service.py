from app.domain.auth import Authentication
from app.infrastructure.users import SqlAlchemyUsers

def authenticate(username, password):
    return Authentication(SqlAlchemyUsers()).authenticate(username, password)
