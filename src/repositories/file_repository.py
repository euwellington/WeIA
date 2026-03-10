from src.repositories.base.mysqldatabase import MySQLDatabase


class FileRepository:

    def __init__(self):

        self.db = MySQLDatabase()


    def create(
        self,
        company_id,
        user_id,
        folder_id,
        name,
        original_name,
        file_size,
        mime_type,
        ftp_path,
        file_hash
    ):

        sql = """
        INSERT INTO files (
            company_id,
            user_id,
            folder_id,
            name,
            original_name,
            file_size,
            mime_type,
            ftp_path,
            file_hash
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        return self.db.execute(
            sql,
            (
                company_id,
                user_id,
                folder_id,
                name,
                original_name,
                file_size,
                mime_type,
                ftp_path,
                file_hash
            )
        )


    def get_by_hash(self, file_hash):

        sql = """
        SELECT id, ftp_path
        FROM files
        WHERE file_hash=%s
        LIMIT 1
        """

        result = self.db.query(sql, (file_hash,))

        if not result:
            return None

        return result[0]


    def list_by_folder(self, folder_id):

        sql = "SELECT * FROM files WHERE folder_id=%s"

        return self.db.query(sql, (folder_id,))


    def get_by_id(self, file_id):

        sql = "SELECT * FROM files WHERE id=%s"

        result = self.db.query(sql, (file_id,))

        if not result:
            return None

        return result[0]


    def delete(self, file_id):

        sql = "DELETE FROM files WHERE id=%s"

        return self.db.execute(sql, (file_id,))