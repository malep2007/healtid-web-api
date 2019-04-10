import graphene
from graphql_jwt.decorators import login_required
from healthid.apps.authentication.utils.decorator import master_admin_required
from healthid.apps.register.models import Register
from healthid.apps.register.schema.register_schema import RegisterType


class RegisterInput(graphene.InputObjectType):

    id = graphene.String()
    name = graphene.String()


class CreateRegister(graphene.Mutation):
    """
    This Creates a register
    """
    register = graphene.Field(RegisterType)

    class Arguments:
        name = graphene.String()
        outlet_id = graphene.Int()
        receipt_id = graphene.String()

    @login_required
    @master_admin_required
    def mutate(self, info, **kwargs):
        try:
            register = Register()
            for(k, v) in kwargs.items():
                setattr(register, k, v)
            register.save()
        except Exception as e:
            raise Exception(f'Something went wrong {e}')

        return CreateRegister(
            register=register
        )


class UpdateRegister(graphene.Mutation):
    """
    This Updates a register
    """

    class Arguments:
        id = graphene.Int()
        input = RegisterInput(required=True)

    errors = graphene.List(graphene.String)
    message = graphene.List(graphene.String)
    success = graphene.Boolean()
    register = graphene.Field(RegisterType)

    @staticmethod
    @login_required
    @master_admin_required
    def mutate(root, info, id, input=None):
        success = False
        register_instance = Register.objects.get(pk=id)
        try:
            success = True
            register_instance.name = input.name
            if register_instance:
                register_instance.save()
                return UpdateRegister(
                    success=success, register=register_instance,
                )

        except Exception as e:
            raise Exception(e)


class DeleteRegister(graphene.Mutation):
    """
    This Deletes a register
    """
    id = graphene.Int()
    success = graphene.String()

    class Arguments:
        id = graphene.Int()

    @login_required
    @master_admin_required
    def mutate(self, info, id):
        register = Register.objects.get(pk=id)
        register.delete()
        return DeleteRegister(
            success="Register was deleted successfully")


class Mutation(graphene.ObjectType):
    create_register = CreateRegister.Field()
    delete_register = DeleteRegister.Field()
    update_register = UpdateRegister.Field()
