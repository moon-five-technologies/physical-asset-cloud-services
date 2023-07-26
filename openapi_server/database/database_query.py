from datetime import datetime

from openapi_server.database.database import PostgreSQLDatabase


def query_serialilzer(
        local_variables: dict, 
        remove_authentication_key_value_pair=False
    ) -> list:
    """
    This function can be used to 
        - Parse through the inputs of the user via what's passed into the controller
        - Remove the authentication key from the parameters passed into the controller to clean up the data
        - Create PostgreSQL searches that look between two given times (starting with _start_ to _end_)
        - Convert Latitude, Longitude, and search distance to a usable query that check for assets within that 
            specific circle, using PostgreSQL commands.  

    :param local_variables: dictionary, This in general will be the "locals()" value, which will retrieve a 
        dictionary which contains all parameters passed into the controller. 
    :param remove_authentication_key_value_pair: bool, if true, this will delete the "auth_information" key value 
        pair from the passed in local variables prior to processing the information.  If you are using ApiKeyAuth, 
        this should be flagged as `true`.  
    :return: A list of dictionaries containing key, value, and comparisons, which can then be passed into the 
        database class for a query. 
    """

    # Delete auth information from passed in local variable dictionary.  This will help with 
    #   formulating a query with the information passed into the controller. 
    if local_variables.get("auth_information") and remove_authentication_key_value_pair:
        del local_variables["auth_information"]

    search_params = []

    # Creates search parameters that use "_start_" and "_end_" to help search between to times.
    #   Any remaining points look for direct matches
    for key, value in local_variables.items():
        if value is not None and not isinstance(value, dict) and not isinstance(value, list) \
                and key not in ["limit", "offset", "search_radius"]:
            if "_start_" in key:
                search_params.append({"key": key,
                                      "value": value,
                                      "comparison": ">"})
            elif "_end_" in key:
                search_params.append({"key": key,
                                      "value": value,
                                      "comparison": "<="})
            else:
                search_params.append({"key": key,
                                      "value": value,
                                      "comparison": "="})
    
    # Allows for searches within a search circle as defined below.
    if local_variables.get("longitude") and local_variables.get("latitude") and local_variables.get("search_radius"):
        longitude = local_variables["longitude"]
        latitude = local_variables["latitude"]
        search_radius = local_variables["search_radius"]
        filtered_params = []

        # Remove existing longitude and latitude if a search radius in included allows for a specific location based
        # search without specifying a search radius, while allowing a radius based search as well.
        for param in search_params:
            print(param)
            if param["key"] not in ["longitude", "latitude", "search_radius"]:
                filtered_params.append(param)

        search_params = filtered_params + add_cicle_search(longitude=longitude,
                                                           latitude=latitude,
                                                           search_radius=search_radius)
    return search_params

def add_cicle_search(longitude: float, latitude: float, search_radius: float) -> list:
    """
    Returns a set of parameters by using your coordinates plus or minus the search radius. After that query,
    the results can then be narrowed down into a circle around the coordinates.
    :param longitude: float, longitudinal coordinates representing your current location.
    :param latitude: float, latitudinal coordinates representing your current location.
    :param search_radius: float, search radius in meters.
    :return: list, search parameters that encompass the maximum longitude/latitude and the minimum longitude/latitude.
    """
    search_radius_in_degrees = convert_meters_to_degrees(distance_in_meters=search_radius)
    return [
        {
            "key": "coordinates",
            "comparison": "<@",
            "value": f"circle '(({latitude},{longitude}), {search_radius_in_degrees})'"
        },
    ]

def convert_meters_to_degrees(distance_in_meters: float):
    """
    Converts meters into longitudinal or latitudinal degrees.
    Ok for short distances due to relatively flat space on a local area.
    :param distance_in_meters: float, distance as measured in meters.
    :return: float, distance in degrees.
    """
    return distance_in_meters/111139.0


def limit_user_data_access_if_not_admin(
        authentication_information: dict, 
        search_params: list, 
        uuid_name_in_table="uuid"
    ) -> list:
    """
    Limits users to only accessing their own data, unless they are registered as an admin.
        Pass in the list of query parameters. The outgoing list will limit the visability 
        of information that should not be accessed if the user is not an admin.
    
    :param authentication_information: dictionary, This dictionary is passed into the controller 
        through the security controller. If the user has gotten to the point where they are 
        accessing the logic, it's assumed that they have a valid account that has been confirmed 
        via the security controller.  
    :param search_params: list of dictionaries, The list contains dictionaries which detail the 
        name of the point to query, the value of the point to query, and what relationship the 
        recovered information should have with the recovered values (ie <=, =, <@, etc.).  
    :param uuid_name_in_table: str, The default is "uuid". Some tables have the uuid stored as 
        "device_uuid" or "user_uuid", so in order to maintain some flexability, the 
        uuid_name_in_table, parameter denotes which column to compare the authentication information uuid to.  
    :return: list, a list of search parameters that is properly redacted for non admin users.
    """

    # Skip the filtering if admin.
    if not authentication_information.get("admin"):
        limited_params = []

        # Removes searches for uuid information that is outside of the scope of access
        for param in search_params:
            if not param.get("key") == uuid_name_in_table:
                limited_params.append(param)
        
        # Appends query for relevant information
        limited_params.append({"key": uuid_name_in_table,
                               "value": authentication_information.get("uuid"),
                               "comparison": "="})
        return limited_params
    
    # Return non obfuscated data if admin.  
    return search_params