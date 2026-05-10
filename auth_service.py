from dataclasses import dataclass

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from database import db
from models import User


@dataclass(frozen=True)
class AuthUser:
    id: int
    username: str
    email: str

    @classmethod
    def from_model(cls, user):
        return cls(id=user.id, username=user.username, email=user.email)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


class UserRepository:
    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def find_by_id(self, user_id):
        if not user_id:
            return None
        return db.session.get(User, user_id)

    def create(self, username, email, password_hash):
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user


class PasswordHasher:
    def hash(self, password):
        return generate_password_hash(password, method="pbkdf2:sha256")

    def verify(self, password_hash, password):
        return check_password_hash(password_hash, password)


class SessionManager:
    def login(self, user):
        session.clear()
        session["user_id"] = user.id
        session.permanent = True

    def logout(self):
        session.clear()

    def current_user_id(self):
        return session.get("user_id")


class AuthService:
    def __init__(self, users=None, passwords=None, sessions=None):
        self.users = users or UserRepository()
        self.passwords = passwords or PasswordHasher()
        self.sessions = sessions or SessionManager()

    def register(self, username, email, password):
        if self.users.find_by_email(email):
            raise ValueError("Email already exists")

        user = self.users.create(
            username=username,
            email=email,
            password_hash=self.passwords.hash(password),
        )
        self.sessions.login(user)
        return AuthUser.from_model(user)

    def login(self, email, password):
        user = self.users.find_by_email(email)
        if not user or not self.passwords.verify(user.password_hash, password):
            raise ValueError("Invalid email or password")

        self.sessions.login(user)
        return AuthUser.from_model(user)

    def logout(self):
        self.sessions.logout()

    def current_user(self):
        user = self.users.find_by_id(self.sessions.current_user_id())
        return AuthUser.from_model(user) if user else None
