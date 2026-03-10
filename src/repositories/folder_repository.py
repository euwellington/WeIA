from src.repositories.base.mysqldatabase import MySQLDatabase
from src.model.folder_model import Folder


class FolderRepository:

    def __init__(self):
        self.db = MySQLDatabase()

    def create(self, company_id, user_id, name, description: str, parent_id=None):

        sql = """
        INSERT INTO folders (company_id,user_id,name, description, parent_id)
        VALUES (%s,%s,%s,%s,%s)
        """

        return self.db.execute(sql, (company_id, user_id, name, description, parent_id))


    def get_by_id(self, folder_id):

        sql = "SELECT * FROM folders WHERE id=%s"

        result = self.db.query(sql, (folder_id,))

        if not result:
            return None

        return Folder(**result[0])


    def list_by_company(self, company_id):

        sql = """
        SELECT * FROM folders
        WHERE company_id=%s
        """

        results = self.db.query(sql, (company_id,))

        if not results:
            return []

        return [Folder(**row) for row in results]


    def list_by_user(self, user_id):

        sql = "SELECT * FROM folders WHERE user_id=%s"

        results = self.db.query(sql, (user_id,))

        return [Folder(**row) for row in results]


    def list_subfolders(self, parent_id):

        sql = "SELECT * FROM folders WHERE parent_id=%s"

        results = self.db.query(sql, (parent_id,))

        return [Folder(**row) for row in results]


    def update(self, folder_id, name):

        sql = """
        UPDATE folders
        SET name=%s
        WHERE id=%s
        """

        self.db.execute(sql, (name, folder_id))


    def delete(self, folder_id):

        sql = "DELETE FROM folders WHERE id=%s"

        self.db.execute(sql, (folder_id,))