import re

from graphql import GraphQLError


def validate_email(email):
    email = email.strip()

    if re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]{2,5}$',
                email) is None:
        raise GraphQLError('Please input a valid email'.format(email))
    return email


def special_cahracter_validation(string):
    string_regex = re.search(r'[^a-zA-Z0-9.,\-\s]+', string)
    if string_regex is not None:
        raise GraphQLError("special characters not allowed")


def validate_empty_field(field, value):
    """
    Utility method to check if a field value is blank
    and return an error message if it is so.
    """
    if value.strip() == "":
        message = "{} field cannot be blank!".format(field)
        raise GraphQLError(message)
