# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.transaction import Transaction  # noqa: E501
from openapi_server.models.update_user import UpdateUser  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.test import BaseTestCase


class TestUsersController(BaseTestCase):
    """UsersController integration test stubs"""

    def test_user_delete(self):
        """Test case for user_delete

        Delete user account.
        """
        headers = { 
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/user',
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_get(self):
        """Test case for user_get

        Query User accounts.
        """
        query_string = [('id', '1'),
                        ('uuid', '1cfd7646-80e1-43a3-ba9c-f4a2c569c045'),
                        ('first_name', 'Robert'),
                        ('middle_name', 'Jingle'),
                        ('last_name', 'Smith'),
                        ('country_code', 1),
                        ('area_code', 408),
                        ('phone_number', 3143155),
                        ('payment_amount', 20.0),
                        ('email', 'user@email.com'),
                        ('is_valid', true),
                        ('conduct_is_valid', true),
                        ('valid_financials', true),
                        ('limit', 20),
                        ('offset', 0)]
        headers = { 
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/user',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_login_get(self):
        """Test case for user_login_get

        Retrieve ApiKeyAuth string via basic authentication.
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Basic Zm9vOmJhcg==',
        }
        response = self.client.open(
            '/api/v1/user/login',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_post(self):
        """Test case for user_post

        Add new user.
        """
        user = null
        headers = { 
            'Content-Type': 'application/json',
            'AppId': 'special-key',
        }
        response = self.client.open(
            '/api/v1/user',
            method='POST',
            headers=headers,
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_put(self):
        """Test case for user_put

        Update user account information.
        """
        update_user = null
        headers = { 
            'Content-Type': 'application/json',
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/user',
            method='PUT',
            headers=headers,
            data=json.dumps(update_user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_transaction_history_get(self):
        """Test case for user_transaction_history_get

        Retrieve the balance of the users account.
        """
        query_string = [('id', '1'),
                        ('user_uuid', '1cfd7646-80e1-43a3-ba9c-f4a2c569c045'),
                        ('most_recent_entry', false)]
        headers = { 
            'Accept': 'application/json',
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/user/transaction-history',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
