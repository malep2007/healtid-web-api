import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from healthid.apps.register.models import Register


class RegisterType(DjangoObjectType):
    class Meta:
        model = Register


class Query(graphene.ObjectType):
    """
    Return a list of registers.
    Or return a single register specified.
    """

    registers = graphene.List(RegisterType)
    register = graphene.Field(RegisterType, id=graphene.Int())

    @login_required
    def resolve_registers(self, info, **kwargs):
        return Register.objects.all()

    @login_required
    def resolve_register(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Register.objects.get(pk=id)

        return None
