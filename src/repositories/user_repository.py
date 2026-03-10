from src.repositories.base.mysqldatabase import MySQLDatabase
from src.model.user_model import User


class UserRepository:

    def __init__(self):
        self.db = MySQLDatabase()

    def create(self, company_id, name, email, password_hash):

        sql = """
        INSERT INTO users (company_id, name, email, password_hash)
        VALUES (%s,%s,%s,%s)
        """

        return self.db.execute(sql, (company_id, name, email, password_hash))

    def get_by_id(self, user_id):

        sql = "SELECT * FROM users WHERE id=%s"

        result = self.db.query(sql, (user_id,))

        if not result:
            return None

        return User(**result[0])

    def get_by_email(self, email):

        sql = "SELECT * FROM users WHERE email=%s"

        result = self.db.query(sql, (email,))

        if not result:
            return None

        return User(**result[0])

    def list_by_company(self, company_id):

        sql = "SELECT * FROM users WHERE company_id=%s"

        results = self.db.query(sql, (company_id,))

        return [User(**row) for row in results]

    def update(self, user_id, name, email):

        sql = """
        UPDATE users
        SET name=%s, email=%s
        WHERE id=%s
        """

        self.db.execute(sql, (name, email, user_id))

    def delete(self, user_id):

        sql = "DELETE FROM users WHERE id=%s"

        self.db.execute(sql, (user_id,))