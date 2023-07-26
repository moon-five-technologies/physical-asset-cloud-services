# ****************************************************
# 
# General exceptions
# 
# ****************************************************


class MultipleEntriesFoundToUpdate(Exception):
    """There should only be one entry to update, but multiple were found."""
    pass

class UnableToFindEntryToUpdate(Exception):
    """Unable to get entry based off of search parameters give."""
    pass

class CannotUpdateId(Exception):
    """You cannot update the database identifier."""
    pass


# ****************************************************
# 
# Station related exceptions
# 
# ****************************************************

class UnableToFindStationStatus(Exception):
    """No station status entries found with given UUID."""
    pass

class UnableToFindStation(Exception):
    """There are no stations listed under the searched parameters."""
    pass

class StationIsOffline(Exception):
    """Cannot implement this action since the station is offline."""
    pass

class StationInUse(Exception):
    """Cannot implement this action since the station is in use."""
    pass

class StationNotInUse(Exception):
    """This action expected the station to be in use. It is currently not."""
    pass

class MoreThanOneStationActiveUnderUse(Exception):
    """There is more than one station active under the user."""
    pass

# ****************************************************
# 
# User related exceptions
# 
# ************************** **************************


class MultipleUsersFound(Exception):
    """Multiple users found when only one should be returned."""
    pass

class NoUsersFound(Exception):
    """No users found when only one should be returned."""
    pass

class UserMismatch(Exception):
    """The user logged into the station is not the same as the user attempting to log out."""
    pass

class MissingUser(Exception):
    """A user uuid was expected, but not recieved."""
    pass
