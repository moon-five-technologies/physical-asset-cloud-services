# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class UserAllOf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, email=None, firebase_uuid=None):  # noqa: E501
        """UserAllOf - a model defined in OpenAPI

        :param email: The email of this UserAllOf.  # noqa: E501
        :type email: str
        :param firebase_uuid: The firebase_uuid of this UserAllOf.  # noqa: E501
        :type firebase_uuid: str
        """
        self.openapi_types = {
            'email': str,
            'firebase_uuid': str
        }

        self.attribute_map = {
            'email': 'email',
            'firebase_uuid': 'firebase_uuid'
        }

        self._email = email
        self._firebase_uuid = firebase_uuid

    @classmethod
    def from_dict(cls, dikt) -> 'UserAllOf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User_allOf of this UserAllOf.  # noqa: E501
        :rtype: UserAllOf
        """
        return util.deserialize_model(dikt, cls)

    @property
    def email(self):
        """Gets the email of this UserAllOf.


        :return: The email of this UserAllOf.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UserAllOf.


        :param email: The email of this UserAllOf.
        :type email: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def firebase_uuid(self):
        """Gets the firebase_uuid of this UserAllOf.


        :return: The firebase_uuid of this UserAllOf.
        :rtype: str
        """
        return self._firebase_uuid

    @firebase_uuid.setter
    def firebase_uuid(self, firebase_uuid):
        """Sets the firebase_uuid of this UserAllOf.


        :param firebase_uuid: The firebase_uuid of this UserAllOf.
        :type firebase_uuid: str
        """
        if firebase_uuid is None:
            raise ValueError("Invalid value for `firebase_uuid`, must not be `None`")  # noqa: E501

        self._firebase_uuid = firebase_uuid
