from src.repositories.base.mysqldatabase import MySQLDatabase
from src.model.company_model import Company


class CompanyRepository:

    def __init__(self):
        self.db = MySQLDatabase()

    def create(self, name: str):
        sql = "INSERT INTO companies (name) VALUES (%s)"
        return self.db.execute(sql, (name,))

    def get_by_id(self, company_id: int):

        sql = "SELECT * FROM companies WHERE id=%s"
        result = self.db.query(sql, (company_id,))

        if not result:
            return None

        return Company(**result[0])

    def list_all(self):

        sql = "SELECT * FROM companies"
        results = self.db.query(sql)

        return [Company(**row) for row in results]