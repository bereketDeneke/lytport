import pyodbc
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
        self.password = f'"{os.getenv('PASSWORD')}\''
        self.port = os.getenv('PORT')
        print(self.port, self.password)
        self.connection = None
        self.connect()

    def connect(self):
        """
        Establish connection to the SQL Server database.
        """
        try:
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server},{self.port};DATABASE={self.database};UID={self.username};PWD={self.password}"
            self.connection = pyodbc.connect(connection_string)
            print("Connection successful!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            exit(0)

    def execute_query(self, query, params=None):
        """
        Execute a query that does not return a result set (INSERT, UPDATE, DELETE).
        """
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()

    def fetch_query(self, query, params=None):
        """
        Execute a query that returns a result set (SELECT).
        """
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error fetching query: {e}")
            return None
        finally:
            cursor.close()

    def insert(self, table, columns, values):
        """
        Insert a new row into a table.
        """
        placeholders = ', '.join(['?'] * len(values))
        column_string = ', '.join(columns)
        query = f"INSERT INTO {table} ({column_string}) VALUES ({placeholders})"
        self.execute_query(query, values)

    def update(self, table, set_columns, set_values, condition_column, condition_value):
        """
        Update an existing row in a table.
        """
        set_string = ', '.join([f"{col} = ?" for col in set_columns])
        query = f"UPDATE {table} SET {set_string} WHERE {condition_column} = ?"
        params = set_values + [condition_value]
        self.execute_query(query, params)

    def delete(self, table, condition_column, condition_value):
        """
        Delete a row from a table.
        """
        query = f"DELETE FROM {table} WHERE {condition_column} = ?"
        self.execute_query(query, [condition_value])

    def select(self, table, columns, condition_column=None, condition_value=None):
        """
        Select rows from a table with an optional condition.
        """
        column_string = ', '.join(columns)
        query = f"SELECT {column_string} FROM {table}"
        if condition_column:
            query += f" WHERE {condition_column} = ?"
            return self.fetch_query(query, [condition_value])
        else:
            return self.fetch_query(query)

    def create_table(self, table_name, columns):
        """
        Create a table with the given columns.
        columns should be a dictionary where the keys are column names and the values are data types.
        Example: 
        columns = {'id': 'INT PRIMARY KEY', 'name': 'VARCHAR(100)', 'age': 'INT'}
        """
        column_definitions = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE {table_name} ({column_definitions})"
        self.execute_query(query)
        print(f"Table '{table_name}' created successfully!")

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
