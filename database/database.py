from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

class Database:
    _instance = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        load_dotenv(override=True)
        self.server = os.getenv('SERVER')
        self.database = os.getenv('DATABASE')
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.port = os.getenv('PORT')
        self.connect()

    def connect(self):
        try:
            connection_string = f"mysql+pymysql://{self.username}:{self.password}@{self.server}:{self.port}/{self.database}"
            Database._engine = create_engine(connection_string)
            print("Connection successful!")
        except SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            exit(0)

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls()
        return cls._engine

    @classmethod
    def close_connection(cls):
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
            print("Connection closed.")

class BaseTable:
    def __init__(self):
        self.engine = Database.get_engine()

    def execute_query(self, query, params=None):
        try:
            with self.engine.begin() as conn:
                conn.execute(text(query), params or {})
        except SQLAlchemyError as e:
            print(f"Error executing query: {e}")

    def fetch_query(self, query, params=None):
        try:
            with self.engine.begin() as conn:
                result = conn.execute(text(query), params or {})
                return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Error fetching query: {e}")
            return None

