import psycopg2
import pyodbc
import mysql.connector
from decouple import config

class DBConnection:
    def __init__(self, db_type):
        self.db_type = db_type.lower()
        self.credentials = {
            "host": config("DATABASE_HOST"),
            "database": config("DATABASE_NAME"),
            "user": config("DATABASE_USER"),
            "password": config("DATABASE_PASSWORD"),
        }

    def _connect_postgres(self):
        return psycopg2.connect(**self.credentials)

    def _connect_sqlserver(self):
        return pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.credentials['host']};"
            f"DATABASE={self.credentials['database']};"
            f"UID={self.credentials['user']};"
            f"PWD={self.credentials['password']}"
        )

    def _connect_mysql(self):
        return mysql.connector.connect(**self.credentials)

    def get(self):
        db_connectors = {
            "postgres": self._connect_postgres,
            "sqlserver": self._connect_sqlserver,
            "mysql": self._connect_mysql,
            "mariadb": self._connect_mysql,
        }

        if self.db_type not in db_connectors:
            raise ValueError(f"Tipo de base de datos no soportado: {self.db_type}")

        return db_connectors[self.db_type]()
