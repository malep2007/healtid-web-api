import graphene
from graphql import GraphQLError
from django.contrib.auth import authenticate
from graphql_jwt.utils import jwt_encode, jwt_payload

from rest_framework.authtoken.models import Token

from healthid.apps.authentication.models import User
from healthid.apps.authentication.schema.auth_queries import UserType
from healthid.utils.app_utils.database import get_model_object


class LoginUser(graphene.Mutation):
    message = graphene.String()
    token = graphene.String()
    rest_token = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        mobile_number = graphene.String()
        password = graphene.String()
        email = graphene.String()

    def mutate(self, info, **kwargs):
        email = kwargs.get('email')
        mobile_number = kwargs.get('mobile_number')
        password = kwargs.get('password')
        message = "Invalid login credentials"
        if email is None:
            user = get_model_object(
                User, 'mobile_number', mobile_number, message=message)
            email = user.email
        user = get_model_object(User, 'email', email, message=message)
        if user.is_active:
            user_auth = authenticate(username=email, password=password)
            if user_auth is None:
                raise GraphQLError(message)
            message = "Login Successful"
            # Create token to access GraphQL-based views
            payload = jwt_payload(user_auth)
            token = jwt_encode(payload)
            # Create token to access REST-based views
            rest_payload = Token.objects.get_or_create(user=user_auth)
            rest_token = rest_payload[0]
            return LoginUser(message=message, token=token, user=user_auth,
                             rest_token=rest_token)
        return GraphQLError(
            "Your Email address has not been verified. "
            "Kindly check your inbox for a verification link.")
