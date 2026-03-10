from src.repositories.auth_repository import AuthRepository
from src.model.user_model import User


class AuthService:

    def __init__(self):
        self.auth_repository = AuthRepository()

    def login(self, email: str, password: str) -> User | None:

        try:

            user = self.auth_repository.authenticate(email, password)

            if not user:
                return None

            return user

        except Exception as e:

            print("Erro no login:", e)
            return None