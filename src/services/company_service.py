from src.repositories.company_repository import CompanyRepository
from src.model.company_model import Company

class CompanyService:

    def __init__(self):
        self.repository = CompanyRepository()

    def create_company(self, name: str):

        try:
            company_id = self.repository.create(name)
            return self.repository.get_by_id(company_id)

        except Exception as e:
            print("Erro ao criar empresa:", e)
            return None

    def get_company(self, company_id: int) -> Company | None:

        try:
            return self.repository.get_by_id(company_id)

        except Exception as e:
            print("Erro ao buscar empresa:", e)
            return None

    def list_companies(self):

        try:
            return self.repository.list_all()

        except Exception as e:
            print("Erro ao listar empresas:", e)
            return []

    def update_company(self, company_id: int, name: str):

        try:
            self.repository.update(company_id, name)
            return True

        except Exception as e:
            print("Erro ao atualizar empresa:", e)
            return False

    def delete_company(self, company_id: int):

        try:
            self.repository.delete(company_id)
            return True

        except Exception as e:
            print("Erro ao deletar empresa:", e)
            return False