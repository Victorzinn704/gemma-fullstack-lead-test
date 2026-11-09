from app.models import User

class SqlAlchemyUsers:
    def find_by_username(self, username: str):
        return User.query.filter_by(username=username).first()
