"""
This is the user module and supports all the ReST actions for the
USER collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
USER = {
    "Farrell": {
        "fname": "Doug",
        "lname": "Farrell",
        "timestamp": get_timestamp(),
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp(),
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp(),
    },
}


def read_all():
    """
    This function responds to a request for /api/user
    with the complete lists of user
    :return:        json string of list of user
    """
    # Create the list of user from our data
    return [USER[key] for key in sorted(USER.keys())]


def read_one(lname):
    """
    This function responds to a request for /api/user/{lname}
    with one matching user from user
    :param lname:   last name of user to find
    :return:        user matching last name
    """
    # Does the user exist in user?
    if lname in USER:
        user = USER.get(lname)

    # otherwise, nope, not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )

    return user


def create(user):
    """
    This function creates a new user in the user structure
    based on the passed in user data
    :param user:  user to create in user structure
    :return:        201 on success, 406 on user exists
    """
    lname = user.get("lname", None)
    fname = user.get("fname", None)

    # Does the user exist already?
    if lname not in USER and lname is not None:
        USER[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }
        return make_response(
            "{lname} successfully created".format(lname=lname), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Person with last name {lname} already exists".format(lname=lname),
        )


def update(lname, user):
    """
    This function updates an existing user in the user structure
    :param lname:   last name of user to update in the user structure
    :param user:  user to update
    :return:        updated user structure
    """
    # Does the user exist in user?
    if lname in USER:
        USER[lname]["fname"] = user.get("fname")
        USER[lname]["timestamp"] = get_timestamp()

        return USER[lname]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )


def delete(lname):
    """
    This function deletes a user from the user structure
    :param lname:   last name of user to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the user to delete exist?
    if lname in USER:
        del USER[lname]
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )

    # Otherwise, nope, user to delete not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )

