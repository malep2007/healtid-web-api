from django.core.exceptions import ObjectDoesNotExist
from graphql import GraphQLError
from healthid.apps.authentication.models import Role


class ModelQuery:
    """
    this class create queries for the role
    """

    def query_role_id(self, id):
        try:
            role = Role.objects.get(id=id)
            return role
        except ObjectDoesNotExist as e:
            raise GraphQLError("Something went wrong: {}".format(e))

    def query_role_name(self, name):
        try:
            role = Role.objects.get(name=name)
            return role
        except ObjectDoesNotExist as e:
            raise GraphQLError("Something went wrong: {}".format(e))
