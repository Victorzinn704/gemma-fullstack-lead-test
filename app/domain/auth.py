from typing import Protocol

class Account(Protocol):
    def check_password(self, password: str) -> bool: ...

class Users(Protocol):
    def find_by_username(self, username: str) -> Account | None: ...

class Authentication:
    def __init__(self, users: Users):
        self.users = users

    def authenticate(self, username: str, password: str):
        user = self.users.find_by_username(username)
        return user if user and user.check_password(password) else None
