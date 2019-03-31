import graphene
from graphql_jwt.decorators import login_required
from healthid.apps.authentication.utils.decorator import master_admin_required
from healthid.apps.outlets.models import Register
from healthid.apps.outlets.schema.register_schema import RegisterType


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
        name = kwargs.get('name')
        if name:
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
        return "Enter Name field"



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
        if id is None:
            errors = ["id", "Register Id is empty"]
            return UpdateRegister(success, errors=errors)

        register_instance = Register.objects.get(pk=id)

        if register_instance is None:
            errors = ["Register", "Register does not exist"]
            return UpdateRegister(success, errors=errors)

        if input.name != "":
            try:
                success = True
                register_instance.name = input.name
                if register_instance:
                   register_instance.save()
                   message = [
                        f"Successfully updated {register_instance} to {input.name}"
                    ]
                   return UpdateRegister(
                        success=success, register=register_instance, message=message
                    )
                return UpdateRegister(success=success, register=None)
            except Exception as e:
                errors = ["Something went wrong: {}".format(e)]
                return UpdateRegister(success=False, errors=errors)

        errors = ["name", "Name Field is empty"]
        return UpdateRegister(success=False, errors=errors)


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
        if register:
            register.delete()
            return DeleteRegister(
            success="Register was deleted successfully")

        return DeleteRegister(success="Error No register by that ID")


class Mutation(graphene.ObjectType):
    create_register = CreateRegister.Field()
    delete_register = DeleteRegister.Field()
    update_register = UpdateRegister.Field()






