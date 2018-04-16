import connexion
import six

from swagger_server.models.data_utility import DataUtility  # noqa: E501
from swagger_server.models.filter import Filter  # noqa: E501
from swagger_server import util

import DQEvaluator
import json
import pandas as pd
import os


def calculate_du(method, attributes=None, filter=None):  # noqa: E501
    """returns the data utility related to the data exposed through a CAF method

    By passing one of the URL exposed by a CAF, the method returns the data utility # noqa: E501

    :param method: URL of the method exposed by a data source
    :type method: str
    :param attributes: list of attributes relevant for the user
    :type attributes: List[str]
    :param filter: list of pairs attributes, value (needs to be compatible with Filter)
    :type filter: dict | bytes

    :rtype: DataUtility
    """

    dimensions = DQEvaluator.DQEvaluator(method, attribute_list=attributes, filter=filter)
    dimensions["URL"] = method

    return dimensions

    
