"""
This module containers helper functions.

"""

import main
from main.models import User





def check_db_status(username):
    """
    Check's whether django can connect to db

    :param username:  username string
    :return: boolean ( 0 = can connect, 1 = can't).
    """
    try:
        User.objects.get(username=username)
        return 0
    except main.models.User.DoesNotExist:
        return 1
