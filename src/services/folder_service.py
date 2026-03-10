from src.repositories.folder_repository import FolderRepository
from src.model.folder_model import Folder


class FolderService:

    def __init__(self):
        self.repository = FolderRepository()

    def create_folder(self, company_id, user_id, name, description: str, parent_id=None):

        try:

            folder_id = self.repository.create(
                company_id,
                user_id,
                name,
                description,
                parent_id
            )

            return self.repository.get_by_id(folder_id)

        except Exception as e:
            print("Erro ao criar pasta:", e)
            return None

    def get_folder(self, folder_id) -> Folder | None:

        try:
            return self.repository.get_by_id(folder_id)

        except Exception as e:
            print("Erro ao buscar pasta:", e)
            return None
        
    def list_by_company(self, folder_id) -> Folder | None:

        try:
            return self.repository.list_by_company(folder_id)

        except Exception as e:
            print("Erro ao buscar pasta:", e)
            return None

    def list_user_folders(self, user_id):

        try:
            return self.repository.list_by_user(user_id)

        except Exception as e:
            print("Erro ao listar pastas:", e)
            return []

    def list_subfolders(self, parent_id):

        try:
            return self.repository.list_subfolders(parent_id)

        except Exception as e:
            print("Erro ao listar subpastas:", e)
            return []

    def update_folder(self, folder_id, name):

        try:
            self.repository.update(folder_id, name)
            return True

        except Exception as e:
            print("Erro ao atualizar pasta:", e)
            return False

    def delete_folder(self, folder_id):

        try:
            self.repository.delete(folder_id)
            return True

        except Exception as e:
            print("Erro ao deletar pasta:", e)
            return False