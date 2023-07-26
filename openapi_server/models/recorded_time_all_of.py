# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class RecordedTimeAllOf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, recorded_time=None):  # noqa: E501
        """RecordedTimeAllOf - a model defined in OpenAPI

        :param recorded_time: The recorded_time of this RecordedTimeAllOf.  # noqa: E501
        :type recorded_time: datetime
        """
        self.openapi_types = {
            'recorded_time': datetime
        }

        self.attribute_map = {
            'recorded_time': 'recorded_time'
        }

        self._recorded_time = recorded_time

    @classmethod
    def from_dict(cls, dikt) -> 'RecordedTimeAllOf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The RecordedTime_allOf of this RecordedTimeAllOf.  # noqa: E501
        :rtype: RecordedTimeAllOf
        """
        return util.deserialize_model(dikt, cls)

    @property
    def recorded_time(self):
        """Gets the recorded_time of this RecordedTimeAllOf.


        :return: The recorded_time of this RecordedTimeAllOf.
        :rtype: datetime
        """
        return self._recorded_time

    @recorded_time.setter
    def recorded_time(self, recorded_time):
        """Sets the recorded_time of this RecordedTimeAllOf.


        :param recorded_time: The recorded_time of this RecordedTimeAllOf.
        :type recorded_time: datetime
        """
        if recorded_time is None:
            raise ValueError("Invalid value for `recorded_time`, must not be `None`")  # noqa: E501

        self._recorded_time = recorded_time