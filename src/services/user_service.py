from src.repositories.user_repository import UserRepository
from src.model.user_model import User


class UserService:

    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, company_id, name, email, password):

        try:
            user_id = self.repository.create(
                company_id,
                name,
                email,
                password
            )

            return self.repository.get_by_id(user_id)

        except Exception as e:
            print("Erro ao criar usuário:", e)
            return None

    def get_user(self, user_id: int) -> User | None:

        try:
            return self.repository.get_by_id(user_id)

        except Exception as e:
            print("Erro ao buscar usuário:", e)
            return None

    def list_company_users(self, company_id):

        try:
            return self.repository.list_by_company(company_id)

        except Exception as e:
            print("Erro ao listar usuários:", e)
            return []

    def update_user(self, user_id, name, email):

        try:
            self.repository.update(user_id, name, email)
            return True

        except Exception as e:
            print("Erro ao atualizar usuário:", e)
            return False

    def delete_user(self, user_id):

        try:
            self.repository.delete(user_id)
            return True

        except Exception as e:
            print("Erro ao deletar usuário:", e)
            return False