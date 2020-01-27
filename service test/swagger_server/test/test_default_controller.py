# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.blueprint import Blueprint  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_calculate_du(self):
        """Test case for calculate_du

        returns the blueprint with associated the updated data utility values
        """
        Blueprint = Blueprint()
        response = self.client.open(
            '/ditas-project/DataUtilityEvaluator/1.0/datautility',
            method='POST',
            data=json.dumps(Blueprint),
            content_type='application/json; charset=utf-8')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
