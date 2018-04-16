# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.data_utility import DataUtility  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_calculate_du(self):
        """Test case for calculate_du

        returns the data utility related to the data exposed through a CAF method
        """
        filter = null()
        query_string = [('method', 'method_example')]
        response = self.client.open(
            '/ditas-project/DataUtilityRefinement/0.2.1/datautility',
            method='POST',
            data=json.dumps(filter),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
