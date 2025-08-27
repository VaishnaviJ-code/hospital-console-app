# mysql connection class

import configparser
import pymysql
import os
from pymysql.err import MySQLError


class DBConnection:
    """
    Establish a singleton connection with the database using PyMySQL.
    This ensures only one instance of DBConnection is ever created.
    """

    __instance = None  # to store the singleton instance

    def __new__(cls):
        """
        Override __new__ to implement singleton.
        Ensures only one instance of DBConnection is ever created.
        """
        if cls.__instance is None:
            cls.__instance = super(DBConnection, cls).__new__(cls)
            cls.__instance.__initialize()  # initialize only once
        return cls.__instance

    def __initialize(self):
        """
        Initialize the database connection using properties
        from db_config.ini
        """
        try:
            # load the configuration file
            config = configparser.ConfigParser()
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(project_root, 'config', 'db_config.ini')
            config.read(config_path)

            # establish the MySQL connection via pymysql
            self.connection = pymysql.connect(
                host=config.get("pymysql", "host"),
                user=config.get("pymysql", "user"),
                password=config.get("pymysql", "password"),
                database=config.get("pymysql", "database"),
                port=config.getint("pymysql", "port", fallback=3306),
                cursorclass=pymysql.cursors.DictCursor  # return results as dict
            )

            if self.connection.open:
                print("Connected to MySQL database using PyMySQL...")

        except MySQLError as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None

    def get_connection(self):
        """
        Returns the active database connection object.
        """
        return self.connection
