import connexion
import six
import traceback
import sys

from swagger_server.models.blueprint import Blueprint  # noqa: E501
from swagger_server import util

import start
import WriteDim


def calculate_du(Blueprint):  # noqa: E501
    """returns the blueprint with associated the updated data utility values

    By passing the blueprint, the method returns the updated blueprint # noqa: E501

    :param Blueprint: file json containing the abstract blueprint to be updated with the data utility values
    :type Blueprint: dict | bytes

    :rtype: Blueprint
    """
    try:
        #if connexion.request.is_json:
        #Blueprint = Blueprint.from_dict(connexion.request.get_json())  # noqa: E501
        BP = Blueprint
        dimensions = start.start(Blueprint)
        BP = WriteDim.writedim(Blueprint, dimensions)
        #BP = writedim.writedim(Blueprint, dimensions)
    except Exception:
        traceback.print_exc(file=sys.stderr)
    return BP
