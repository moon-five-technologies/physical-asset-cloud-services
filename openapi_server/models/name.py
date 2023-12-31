# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Name(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, first_name=None, last_name=None):  # noqa: E501
        """Name - a model defined in OpenAPI

        :param first_name: The first_name of this Name.  # noqa: E501
        :type first_name: str
        :param last_name: The last_name of this Name.  # noqa: E501
        :type last_name: str
        """
        self.openapi_types = {
            'first_name': str,
            'last_name': str
        }

        self.attribute_map = {
            'first_name': 'first_name',
            'last_name': 'last_name'
        }

        self._first_name = first_name
        self._last_name = last_name

    @classmethod
    def from_dict(cls, dikt) -> 'Name':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Name of this Name.  # noqa: E501
        :rtype: Name
        """
        return util.deserialize_model(dikt, cls)

    @property
    def first_name(self):
        """Gets the first_name of this Name.


        :return: The first_name of this Name.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this Name.


        :param first_name: The first_name of this Name.
        :type first_name: str
        """

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this Name.


        :return: The last_name of this Name.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this Name.


        :param last_name: The last_name of this Name.
        :type last_name: str
        """

        self._last_name = last_name
