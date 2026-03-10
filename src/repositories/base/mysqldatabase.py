import mysql.connector


class MySQLDatabase:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self):

        if self._initialized:
            return

        self.config = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "root123",
            "database": "weia"
        }

        self.connection = None
        self.cursor = None

        self.connect()

        self._initialized = True

    def connect(self):

        try:

            if self.connection and self.connection.is_connected():
                return

            self.connection = mysql.connector.connect(**self.config)

            self.cursor = self.connection.cursor(dictionary=True)

            print("✅ Conectado ao MySQL")

        except Exception as e:

            print("❌ Erro ao conectar:", e)

    def query(self, sql, params=None):

        try:

            self.cursor.execute(sql, params or ())
            return self.cursor.fetchall()

        except Exception as e:

            print("❌ Erro na query:", e)

    def execute(self, sql, params=None):

        try:

            cursor = self.connection.cursor()

            cursor.execute(sql, params or ())

            self.connection.commit()

            last_id = cursor.lastrowid

            cursor.close()

            return last_id

        except Exception as e:

            print("❌ Erro ao executar:", e)

    def close(self):

        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()
            print("🔌 Conexão fechada")