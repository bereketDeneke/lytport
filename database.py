from sqlalchemy import create_engine, Table, Column, MetaData, String, Integer
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        """
        Initialize by loading environment variables and establishing the connection.
        """
        load_dotenv()
        self.server = os.getenv('SERVER')
        self.database = os.getenv('DATABASE')
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.port = os.getenv('PORT')
        self.connection = None
        self.engine = None
        print(self.database)

    def connect(self):
        """
        Establish connection to the MySQL database using SQLAlchemy.
        """
        try:
            connection_string = f"mysql+pymysql://{self.username}:{self.password}@{self.server}:{self.port}/{self.database}"
            print(connection_string)
            self.engine = create_engine(connection_string)
            self.connection = self.engine.connect()
            print("Connection successful!")
        except SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            exit(0)

    def execute_query(self, query, params=None):
        """
        Execute a query that does not return a result set (INSERT, UPDATE, DELETE).
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(query, params)
        except SQLAlchemyError as e:
            print(f"Error executing query: {e}")

    def fetch_query(self, query, params=None):
        """
        Execute a query that returns a result set (SELECT).
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(query, params)
                return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Error fetching query: {e}")
            return None

    def insert(self, table, columns, values):
        """
        Insert a new row into a table.
        """
        placeholders = ', '.join([':{}'.format(col) for col in columns])
        column_string = ', '.join(columns)
        query = f"INSERT INTO {table} ({column_string}) VALUES ({placeholders})"
        param_dict = dict(zip(columns, values))
        self.execute_query(query, param_dict)

    def update(self, table, set_columns, set_values, condition_column, condition_value):
        """
        Update an existing row in a table.
        """
        set_string = ', '.join([f"{col} = :{col}" for col in set_columns])
        query = f"UPDATE {table} SET {set_string} WHERE {condition_column} = :{condition_column}"
        params = {**dict(zip(set_columns, set_values)), condition_column: condition_value}
        self.execute_query(query, params)

    def delete(self, table, condition_column, condition_value):
        """
        Delete a row from a table.
        """
        query = f"DELETE FROM {table} WHERE {condition_column} = :{condition_column}"
        params = {condition_column: condition_value}
        self.execute_query(query, params)

    def select(self, table, columns, condition_column=None, condition_value=None):
        """
        Select rows from a table with an optional condition.
        """
        column_string = ', '.join(columns)
        query = f"SELECT {column_string} FROM {table}"
        if condition_column:
            query += f" WHERE {condition_column} = :{condition_column}"
            return self.fetch_query(query, {condition_column: condition_value})
        else:
            return self.fetch_query(query)

    def create_table(self, table_name, columns):
        """
        Create a table with the given columns.
        columns should be a dictionary where the keys are column names and the values are data types.
        Example: 
        columns = {'id': 'INT PRIMARY KEY', 'name': 'VARCHAR(100)', 'age': 'INT'}
        """
        metadata = MetaData()
        column_definitions = [Column(col, self._get_sqlalchemy_type(dtype)) for col, dtype in columns.items()]
        table = Table(table_name, metadata, *column_definitions)
        try:
            metadata.create_all(self.engine)
            print(f"Table '{table_name}' created successfully!")
        except SQLAlchemyError as e:
            print(f"Error creating table: {e}")

    def _get_sqlalchemy_type(self, dtype):
        """
        Helper function to convert string-based data types to SQLAlchemy types.
        """
        if dtype.lower() == 'int':
            return Integer
        elif 'varchar' in dtype.lower():
            return String
        else:
            raise ValueError(f"Unsupported data type: {dtype}")

    def drop_table(self, table_name):
        """
        Drop the specified table if it exists.
        """
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.execute_query(query)
        print(f"Table '{table_name}' dropped successfully!")

    def close(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()
            print("Connection closed.")
