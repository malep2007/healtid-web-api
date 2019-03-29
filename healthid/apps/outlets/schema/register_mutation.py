import graphene
from graphql_jwt.decorators import login_required
from healthid.apps.authentication.utils.decorator import master_admin_required
from healthid.apps.outlets.models import Register
from healthid.apps.outlets.schema.register_schema import RegisterType


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
    register = graphene.Field(RegisterType)

    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    ok = graphene.Boolean()

    @login_required
    @master_admin_required
    def mutate(self, info, name, **kwargs):
        ok=False
        id = kwargs.get('id')
        register = Register.objects.get(pk=id)
        if register:
            ok = True
            register.name = name
            register.save()
            return UpdateRegister(ok=ok, register=register)
        return UpdateRegister(ok=ok, register=None)



class DeleteRegister(graphene.Mutation):
    """
    This Deletes a register
    """
    id = graphene.Int()


    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    @login_required
    @master_admin_required
    def mutate(self, info, id):
        ok = False
        register = Register.objects.get(pk=id)
        if register:
            register.delete()
            return DeleteRegister(
            ok=True)

        return DeleteRegister(ok=ok)


class Mutation(graphene.ObjectType):
    create_register = CreateRegister.Field()
    delete_register = DeleteRegister.Field()
    update_register = UpdateRegister.Field()

