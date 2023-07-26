import logging
import configs
from psycopg2.extensions import AsIs

from openapi_server.database import PostgreSQLDatabase
from openapi_server.secrets import POSTGRESQL_PASSWORD

logger = logging.getLogger(__name__)

class PostgreSQLDatabaseSetup(PostgreSQLDatabase):
    def __init__(self):
        super().__init__()

    def create_table(
            self, 
            table: str, 
            columns_and_types: dict
        ) -> None:
        """
        Creates a table based off of offered columns and types.  This should
            only be used during a database setup operation, since there is no reason for a user
            to create a database during nominal operations.

        :param table: The name of the table that you would like to create.
        :param columns_and_types: A dictionary that contains all of the columns, data types, and requirements 
            (ie Unique or not, required or not, etc.).  This dictionary can also contain a constraints, which 
            allow for references between tables.  
        :return:
        """
        if self.db_connection is None or self.db_connection.closed:
            self.psycopg_connect()

        # Remove the table constraints from values that are going to be added to the database.
        keys = []
        values = []
        for key, value in columns_and_types.items():
            if "table_constraints" != key:
                keys.append(key)
                values.append(value)

        formatted_columns_and_types = ", ".join([f"{key} {values[i]}" for i, key in enumerate(keys)])

        # Parses out the "table_constraints" key within the dictionary, The corresponding value 
        #   shows which table and column a specific entry will be referencing.  Ie if you have a 
        #   column that contains the user_uuid within a transaction, there will be a reference to the
        #   user table and the uuid column. This can be used as a check to make sure that that user exists
        #   prior to initiating thigns like a charge session. 
        if "table_constraints" in columns_and_types.keys():
            for constraint in columns_and_types["table_constraints"]:
                formatted_columns_and_types += f", CONSTRAINT {constraint['name']} " \
                                               f"FOREIGN KEY ({constraint['key']}) " \
                                               f"REFERENCES {constraint['reference']}"

        # Writing to the database to create a table
        with self.db_connection.cursor() as cursor:
            cursor.execute(
                'CREATE TABLE %s (%s)', 
                (AsIs(table),
                 AsIs(formatted_columns_and_types))
            )

        self.db_connection.commit()
        self.close()
        logger.info(f"Created a new table: {table}")

