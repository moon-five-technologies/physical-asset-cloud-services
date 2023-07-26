import connexion
import six

from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.transaction import Transaction  # noqa: E501
from openapi_server.models.update_user import UpdateUser  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server import util

# **************************
# NOT GENERATED REQUIREMENTS
# **************************
# Required dependencies from external sources
import jwt
import firebase_admin
from datetime import datetime, timedelta
from firebase_admin import credentials
from flask import Response, jsonify

# Required dependencies from internal sources.
import configs
from openapi_server.database.database import PostgreSQLDatabase
from openapi_server.database.database_query import query_serialilzer, limit_user_data_access_if_not_admin
from openapi_server.secrets import TMP_API_SECRET_KEY


cred = credentials.Certificate(configs.FIREBASE_PRIVATE_KEY_PATH)
firebase_admin.initialize_app(cred)

def user_delete(auth_information):  # noqa: E501
    """Delete user account.

    This endpoint will allow for a user to delete their own account. In order to delete an account that is not yours, you must be an admin. # noqa: E501


    :rtype: None
    """
    # NOTE: The authentication process checks that the user uuid defined within the ApiAuthKey exists, 
    #   so, allowing us not to need to check a second time.  This endpoint does not allow for admin 
    #   deletion of accounts.

    # Delete a user account based off 
    db = PostgreSQLDatabase()
    db.delete_one(
        table="users", 
        id=auth_information.get("uuid")
    )

    return Response("Successful delete", status=204)

def user_get(auth_information, id=None, uuid=None, first_name=None, middle_name=None, last_name=None, country_code=None, area_code=None, phone_number=None, payment_amount=None, email=None, is_valid=None, conduct_is_valid=None, valid_financials=None, limit=None, offset=None):  # noqa: E501
    """Query User accounts.

    Allows for a user to retrieve their information to be displayed in an application.  Information retrieval is limited to your user&#39;s account unless you are an admin. # noqa: E501

    :param id: Database identifier.
    :type id: str
    :param uuid: A unique identifier for the row.
    :type uuid: str
    :param first_name: A users first name.
    :type first_name: str
    :param middle_name: A users middle name.
    :type middle_name: str
    :param last_name: A users last name.
    :type last_name: str
    :param country_code: A phone number&#39;s country code.
    :type country_code: int
    :param area_code: A phone number&#39;s area code.
    :type area_code: int
    :param phone_number: A phone number, not including country code or area code, including seven digits.
    :type phone_number: int
    :param payment_amount: The amount that the user will be bulked charged during an overdraft event.
    :type payment_amount: float
    :param email: The email address of a user.
    :type email: str
    :param is_valid: Denotes if user is valid or not.
    :type is_valid: bool
    :param conduct_is_valid: Denotes if user has acted poorly while using the charging system.
    :type conduct_is_valid: bool
    :param valid_financials: Denotes if user is in good financial standing.
    :type valid_financials: bool
    :param limit: Maximum number of items to return.
    :type limit: int
    :param offset: Number of items to skip before returning the results.
    :type offset: int

    :rtype: None
    """
    station_recorded_time = util.deserialize_datetime(station_recorded_time)
    station_start_recorded_time = util.deserialize_datetime(station_start_recorded_time)
    station_end_recorded_time = util.deserialize_datetime(station_end_recorded_time)
    server_recorded_time = util.deserialize_datetime(server_recorded_time)
    server_start_recorded_time = util.deserialize_datetime(server_start_recorded_time)
    server_end_recorded_time = util.deserialize_datetime(server_end_recorded_time)

    # Come one, come all, get your query here!
    search_params = query_serialilzer(
        local_variables=locals(), 
        remove_authentication_key_value_pair=True
    )

    if not search_params:
        return Response("No valid search params entered.", status=404)

    db = PostgreSQLDatabase()

    # Limit scope of data access for non-admins
    search_params = limit_user_data_access_if_not_admin(
        authentication_information=auth_information, 
        search_params=search_params
    )

    # Query based off of serialized query
    dataframe = db.get_entry(
        table="users",
        fields_to_retrieve="all",
        search_params=search_params,
        limit=limit,
        offset=offset
    )

    # Limit information returned to only essential information.
    records = dataframe.to_dict("records")
    if not auth_information.get("admin"):
        returned_records = []
        for record in records:
            returned_records.append({
                "uuid": record.get("uuid"),
                "email": record.get("email"),
                "country_code": record.get("country_code"),
                "area_code": record.get("area_code"),
                "phone_number": record.get("phone_number"),
                "first_name": record.get("first_name"),
                "last_name": record.get("last_name")
            })
        return jsonify({"users": returned_records})
    return jsonify({"users": records})

def user_login_get(auth_information):  # noqa: E501
    """Retrieve ApiKeyAuth string via basic authentication.

    After you have created an account, you can retrieve an account via # noqa: E501


    :rtype: InlineResponse200
    """
    token = jwt.encode(
        {"user_uuid": auth_information["uuid"], 
         "exp": datetime.utcnow() + timedelta(days=configs.TOKEN_LIFETIME_IN_DAYS)}, 
         TMP_API_SECRET_KEY
    )
    return jsonify({"token": token}), 200


def user_post():  # noqa: E501
    """Add new user.

    Add a new user to the database. In order to do so, you must have the correct application identifier. All users created though this API will have standard privileges, in order to view more general information, your permission level needs to be elevated to admin. # noqa: E501

    :param user: Add a new user.
    :type user: dict | bytes

    :rtype: None
    """

    # NOTE: At this point, the security controller function info_from_AppId has already run, 
    #   and indicated whether the app id is valid or not. 

    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def user_put(auth_information):  # noqa: E501
    """Update user account information.

    While not inclusive of all fields stored, this endpoint allows for a user to update their own profile.  In order to update user profiles that are not related to your account, you must be an admin. # noqa: E501

    :param update_user: Information to be updated.
    :type update_user: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        update_user = UpdateUser.from_dict(connexion.request.get_json())  # noqa: E501
        retrieved_dict = update_user.to_dict()
        db = PostgreSQLDatabase()

        # Remove any values that are None.
        filtered_dict = {k: v for k, v in retrieved_dict.items() if v is not None}

        db.update_one(
            table="users",
            search_params=[{
                "key": "uuid",
                "value": auth_information.get("uuid"),
                "comparison": "="
            }],
            to_update=filtered_dict
        )
        return Response("Successfully updated payment amount", status=204)

def user_transaction_history_get(auth_information, id=None, user_uuid=None, most_recent_entry=None):  # noqa: E501
    """Retrieve the balance of the users account.

     # noqa: E501

    :param id: Database identifier.
    :type id: str
    :param user_uuid: User unique identifier.
    :type user_uuid: str
    :param most_recent_entry: A boolean that allows the user to only the most recent entry.
    :type most_recent_entry: bool

    :rtype: List[Transaction]
    """
    search_params = query_serialilzer(
        local_variables=locals(), 
        remove_authentication_key_value_pair=True
    )


    # Limit scope of data access for non-admins
    search_params = limit_user_data_access_if_not_admin(
        authentication_information=auth_information, 
        search_params=search_params
    )


    db = PostgreSQLDatabase()
    dataframe = db.get_entry(
        table="transactions",
        fields_to_retrieve="all",
        search_params=search_params,
        limit=100,
        offset=0
    )

    records = dataframe.to_dict("records")
    if not auth_information.get("admin"):
        limited_response = []
        for record in records:
            limited_response.append({
                "recorded_time": record.get("recorded_time"),
                "server_time": record.get("server_time"),
                "balance": record.get("balance"),
                "user_uuid": record.get("user_uuid"),
                "transaction_cost": record.get("transaction_cost"),
                "transaction_location": record.get("transaction_location"),
                "name_of_transaction_location": record.get("name_of_transaction_location"),
                "is_refund": record.get("is_refund")
            })
        return jsonify({"transaction_history": limited_response}), 200
    
    # Return full record if admin
    return jsonify({"transaction_history": records}), 200