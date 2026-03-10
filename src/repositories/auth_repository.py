from src.repositories.base.mysqldatabase import MySQLDatabase
from src.model.user_model import User


class AuthRepository:

    def __init__(self):
        self.db = MySQLDatabase()

    def authenticate(self, email: str, password_hash: str) -> User | None:

        sql = """
        SELECT 
            u.*, c.Name AS company_name
        FROM
            users u
                INNER JOIN
            companies c ON u.id = u.company_id
        WHERE u.email = %s AND u.password_hash = %s
        LIMIT 1
        """

        result = self.db.query(sql, (email, password_hash))

        if not result:
            return None

        return User(**result[0])