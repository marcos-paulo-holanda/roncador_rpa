import psycopg2
import pyodbc

class PostgreConnector:
    def __init__(self):
        self.server = "mrndatamarts02.mrnptr.com.br"
        self.database = "db_supply"
        self.username = "sa_robotrom_ro"
        self.password = "5p0Ka4BF%7&2RGh3*KK"
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            host = self.server,
            port = 5432,
            database = self.database,
            user = self.username,
            password = self.password
    )

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

class SqlServerConnector:
    """
    A class representing a connection to a SQL Server database.
    """

    def __init__(self):
        # Server configuration
        self.server = "mrnsqlserver01.mrnptr.com.br"
        self.database = "db_dwh"
        self.username = "sa_rhspot_ro"
        self.password = "JViHGF!ZL!0%&v7h"
        self.connection = None

    def connect(self):
        connection_str = (
            f"DRIVER={{SQL Server}};SERVER={self.server};"
            f"DATABASE={self.database};UID={self.username};PWD={self.password}"
        )
        self.connection = pyodbc.connect(connection_str)
        return self.connection
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
