# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class UserUUID(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, user_uuid=None):  # noqa: E501
        """UserUUID - a model defined in OpenAPI

        :param user_uuid: The user_uuid of this UserUUID.  # noqa: E501
        :type user_uuid: str
        """
        self.openapi_types = {
            'user_uuid': str
        }

        self.attribute_map = {
            'user_uuid': 'user_uuid'
        }

        self._user_uuid = user_uuid

    @classmethod
    def from_dict(cls, dikt) -> 'UserUUID':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserUUID of this UserUUID.  # noqa: E501
        :rtype: UserUUID
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_uuid(self):
        """Gets the user_uuid of this UserUUID.


        :return: The user_uuid of this UserUUID.
        :rtype: str
        """
        return self._user_uuid

    @user_uuid.setter
    def user_uuid(self, user_uuid):
        """Sets the user_uuid of this UserUUID.


        :param user_uuid: The user_uuid of this UserUUID.
        :type user_uuid: str
        """

        self._user_uuid = user_uuid
