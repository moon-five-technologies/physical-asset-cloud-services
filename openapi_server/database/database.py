import logging
import psycopg2
import pandas

from datetime import datetime
from sqlalchemy import create_engine
from psycopg2.extensions import AsIs
from typing import Union
from uuid import uuid4
from getpass import getpass, getuser

import configs

from openapi_server.secrets import POSTGRESQL_PASSWORD
from openapi_server.exceptions import CannotUpdateId, MultipleEntriesFoundToUpdate, UnableToFindEntryToUpdate

logger = logging.getLogger(__name__)


class PostgreSQLDatabase:
    def __init__(self, 
                 host=configs.DATABASE_DEFAULT_HOST, 
                 port=configs.DATABASE_DEFAULT_PORT, 
                 database=configs.DATABASE_NAME, 
                 user=configs.DATABASE_USER, 
                 password=POSTGRESQL_PASSWORD):
        
        self.host = host
        self.port = port
        self.database = database
        self._user = user
        self._password = password
        self.db_connection = None
        self.sqlalchemy_engine = None

    @property
    def server_time(self) -> str:
        return f"'{datetime.utcnow()}'"

    @property
    def user(self) -> str:
        if self._user is None:
            self._user = getuser()
        return self._user

    @property
    def password(self) -> str:
        if self._password is None:
            self._password = getpass(
                prompt=f"Enter password for user {self.user}: "
            )
        return self._password

    def close(self) -> None:
        if self.db_connection:
            self.db_connection.close()

    def psycopg_connect(self) -> None:
        """
        Connects with database and logs message.
        :return:
        """
        self.db_connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        logger.info(f"Opened connection to "
                    f"{self.user}@{self.host}:{self.port}/{self.database} "
                    f"successfully.")

    def sqlalchemy_connect(self) -> None:
        """
        Connect to the remote postgresql instance via SQLAlchemy. 
        """
        self.sqlalchemy_engine = create_engine(
            f'postgresql://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.database}'
        )
        logger.info(f"Opened connection to sqlalchemy engine at "
                    f"{self.user}@{self.host}:{self.port}/{self.database} "
                    f"successfully.")


    def insert_one(
            self, 
            table: str, 
            entry: dict
        ) -> None:
        """
        Inserts an entry into a POSTGRESQL database via psycopg.
        :param table:
        :param entry:
        :return:
        """
        if self.db_connection is None or self.db_connection.closed:
            self.psycopg_connect()

        keys, values = [], []
        for key, value in entry.items():
            if value is None:
                continue
            keys.append(key)
            values.append(str(query_parameter_formatting(query_parameter=value)))

        keys = ",".join(keys + ["server_time"])
        values = ",".join(values + [self.server_time])

        # print(f"INSERT INTO {table} ({keys}) VALUES ({values})")
        with self.db_connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO %s (%s) VALUES (%s)", 
                (AsIs(table), 
                 AsIs(keys), 
                 AsIs(values))
            )
        self.db_connection.commit()
        self.close()
        logger.info("Record created successfully.")

    def insert_many(
            self, 
            table: str, 
            entries: list
        ) -> None:
        """
        Inserts multiple entries into a POSTGRESQL database via psycopg.
        :param table: string,
        :param entries: list of dictionaries.
        :return:
        """
        for entry in entries:
            self.insert_one(table=table, entry=entry)
        self.close()

    def delete_one(
            self, 
            table: str, 
            id: int
        ) -> None:
        """
        Delete a single entry
        """
        if self.db_connection is None or self.db_connection.closed:
            self.psycopg_connect()
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM %s WHERE id = %s", 
                (AsIs(table), 
                 AsIs(id))
            )
        
        self.db_connection.commit()
        self.close()
        logger.info("Delete entry.")

    def update(
            self, 
            table, 
            search_params: dict, 
            to_update: dict
        ) -> None:
        """
        Update entries in POSTGRESQL database via psycopg.
        :param table:
        :param search_params:
        :param to_update:
        :return:
        """
        pass

    def update_one(
            self, 
            table, 
            search_params: list, 
            to_update: dict
        ) -> None:
        """
        Update one entry in POSTGRESQL database via psycopg.
        :param table:
        :param search_params:
        :param to_update:
        :return:
        """
        entries = self.get_entry(
            table=table, 
            fields_to_retrieve="all", 
            search_params=search_params
        )
        
        # Check to make sure that there is only a single entry to update.
        entry_count = len(entries.index) 
        if entry_count > 1:
            raise MultipleEntriesFoundToUpdate()
        elif len(entries.index) == 0:
            raise UnableToFindEntryToUpdate()
        
        # Construct fields to update.
        update_list = [] 
        for key, value in to_update.items():
            if key == "id":
                raise CannotUpdateId()
            if isinstance(value, str):
                update_list.append(f"{key} = '{value}'")
            else:
                update_list.append(f"{key} = {value}")

        if self.db_connection is None or self.db_connection.closed:
            self.psycopg_connect()

        # print("\n\n\n", entries, "\n\n\n")
        with self.db_connection.cursor() as cursor:
            cursor.execute('UPDATE %s SET %s WHERE id = %s', (
                AsIs(table), 
                AsIs(", ".join(update_list)),
                AsIs(entries.iloc[0]["id"])
            ))

        self.db_connection.commit()
        self.close()
        logger.info("Updated table.")



    def get_entry(
            self, 
            table: str, 
            fields_to_retrieve: Union[list, str], 
            search_params: list, 
            join_params=[], 
            fields_to_retrieve_from_join=[], 
            and_or_search="AND", 
            limit=20, 
            offset=0, 
            order_by=("server_time", "DESC")
        ) -> None:
        """
        Searches via search parameters for entries in a POSTGRESQL database via sqlalchemy.
        :param table: string,
        :param fields_to_retrieve: list or string,
        :param search_params: list of dictionaries,
        :param join_params: list of dictionaries,
        :param fields_to_retrieve_from_join: 
        :param limit: int,
        :param offset: int,
        :param order_by: (str, str) order by first param either DESC or ASC in the second param.
        :return: pandas.DataFrame, A pandas dataframe containing all queried information will be returned.
        """
        fields_to_retrieve = "*" if isinstance(fields_to_retrieve, str) else ",".join(fields_to_retrieve)
        search_array = []
        join_array = []
        # print(search_params)
        for parameter in search_params:
            search_array.append(f"{parameter['key']} {parameter['comparison']} "
                                f"{query_parameter_formatting(query_parameter=parameter['value'])}")
        

        self.sqlalchemy_connect()

        if join_params:
            if not fields_to_retrieve_from_join:
                raise ValueError("You need to add values to fields_to_retrieve_from_join.")

            # Append names to make sure that the properfields are retrieved from the joined tables.
            fields_to_retrieve = [f"{table}.{field}" for field in fields_to_retrieve]
            fields_to_retrieve += fields_to_retrieve_from_join
            fields_to_retrieve = ", ".join(fields_to_retrieve)

            search_array = [f"{table}.{field}" for field in search_array]

            for parameter in join_params:
                join_array.append(f"LEFT JOIN {parameter['table_name']} ON "
                                  f"{table}.{parameter['value']} = {parameter['table_name']}.{parameter['table_location']}")

            self.close()
            return pandas.read_sql_query(
                "SELECT %s FROM %s %s WHERE %s ORDER BY %s %s LIMIT %s OFFSET %s",
                con=self.sqlalchemy_engine,
                params=(
                    AsIs(fields_to_retrieve),
                    AsIs(table),
                    AsIs(' '.join(join_array)),
                    AsIs(f' {and_or_search} '.join(search_array)),
                    AsIs(order_by[0]),
                    AsIs(order_by[1]),
                    AsIs(str(limit)),
                    AsIs(str(offset))
                )
            )
        self.close()
        return pandas.read_sql_query(
            "SELECT %s FROM %s WHERE %s ORDER BY %s %s LIMIT %s OFFSET %s",
            con=self.sqlalchemy_engine,
            params=(
                AsIs(fields_to_retrieve),
                AsIs(table),
                AsIs(' AND '.join(search_array)),
                AsIs(order_by[0]),
                AsIs(order_by[1]),
                AsIs(str(limit)),
                AsIs(str(offset))
            )
        )

    def get_telemetry(self, telemetry_points: list, station_uuid: str, start_window: str, end_window=None, order_by=("server_time", "ASC")):
        """
        Searches via search parameters for entries in a POSTGRESQL database via sqlalchemy.
        :param table: string, 
        :param telemetry_points: 
        :param station_uuid: 
        :param order_by: (str, str) order by first param either DESC or ASC in the second param.
        :return: pandas.DataFrame, A pandas dataframe containing all queried information will be returned.
        """
        search_array = []
        for telemetry_point_name in telemetry_points:
            if not isinstance(telemetry_point_name, str):
                raise TypeError("Unexpected type retrieved from list of telemetry values")
            print(telemetry_point_name)
            search_array.append(f"name = {query_parameter_formatting(telemetry_point_name)}")

        self.sqlalchemy_connect()

        if end_window:
            self.close()
            return pandas.read_sql_query(
                'SELECT * FROM "telemetry" WHERE %s AND %s AND %s AND %s ORDER BY %s %s LIMIT %s OFFSET %s',
                con=self.sqlalchemy_engine,
                params=(
                    AsIs(' OR '.join(search_array)),
                    AsIs(f"station_uuid = {query_parameter_formatting(station_uuid)}"),
                    AsIs(f"server_time >= {query_parameter_formatting(start_window)}"),
                    AsIs(f"server_time <= {query_parameter_formatting(end_window)}"),
                    AsIs(order_by[0]),
                    AsIs(order_by[1]),
                    AsIs(str(100000)),
                    AsIs(str(0))
                )
            )
        else:
            self.close()
            return pandas.read_sql_query(
                'SELECT * FROM "telemetry" WHERE %s AND %s AND %s ORDER BY %s %s LIMIT %s OFFSET %s',
                con=self.sqlalchemy_engine,
                params=(
                    AsIs(' OR '.join(search_array)),
                    AsIs(f"station_uuid = {query_parameter_formatting(station_uuid)}"),
                    AsIs(f"server_time >= {query_parameter_formatting(start_window)}"),
                    AsIs(order_by[0]),
                    AsIs(order_by[1]),
                    AsIs(str(100000)),
                    AsIs(str(0))
                )
            )



def query_parameter_formatting(query_parameter):
    """
    Allows for strings and datetimes to be properly queried in a search.
    :param query_parameter: The search parameter used in the POSTGRESQL query.
    :return: Type Unknown, The reformatted query.
    """
    if isinstance(query_parameter, str):
        if "circle '" in query_parameter:
            return query_parameter
        else:
            return f"'{query_parameter}'"
    if isinstance(query_parameter, datetime):
        return f"'{query_parameter}'"
    return query_parameter


def query_formatting(list_of_entries: list):
    reformatted_entries = []
    for entry in list_of_entries:
        if isinstance(entry, str) or isinstance(entry, datetime):
            reformatted_entries.append(f"'{entry}'")
        else:
            reformatted_entries.append(entry)
    return reformatted_entries


def value_formatting(dictionary: dict):
    """
    Adds single quotes to denote strings for queries.
    :param dictionary: Any dictionary.
    :return: A list of values where strings have a single quote surround them to denote string type for POSTGRESQL queries.
    """
    values = list(dictionary.values())
    return query_formatting(values)

def check_for_zero_state(dictionary_entry: dict, fields_to_check: list) -> dict:
    """
    Checks that dictionaries are not violating expected state by having a zero (not a database id) as an entry. If they do, it will be removed from the entry.
    """
    for field in fields_to_check:
        if field in dictionary_entry.keys():
            if dictionary_entry[field] == 0:
                dictionary_entry.pop(field)
    return dictionary_entry