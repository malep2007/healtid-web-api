import graphene
from django.forms.models import model_to_dict
from graphql.error import GraphQLError
from graphql_jwt.decorators import login_required

from healthid.apps.orders.models import Suppliers, SupplierNote
from healthid.apps.outlets.models import Outlet
from healthid.apps.orders.schema.suppliers_query import (SuppliersType,
                                                         SupplierNoteType)
from healthid.utils.app_utils.database import (SaveContextManager,
                                               get_model_object)
from healthid.utils.auth_utils.decorator import user_permission
from healthid.utils.app_utils.validators import special_cahracter_validation
from healthid.utils.orders_utils.add_supplier import add_supplier


class SuppliersInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String()
    mobile_number = graphene.String()
    address_line_1 = graphene.String()
    address_line_2 = graphene.String()
    lga = graphene.String()
    city_id = graphene.Int()
    tier_id = graphene.Int()
    rating = graphene.Int()
    credit_days = graphene.Int()
    logo = graphene.String()
    payment_terms_id = graphene.Int()
    commentary = graphene.String()


class AddSupplier(graphene.Mutation):
    class Arguments:
        input = SuppliersInput(required=True)

    supplier = graphene.Field(SuppliersType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input=None):
        supplier = Suppliers()
        user = info.context.user
        outlet = get_model_object(Outlet, 'user', user)
        add_supplier.create_supplier(user, outlet, supplier, input)
        return cls(supplier=supplier)


class ApproveSupplier(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
    success = graphene.Field(graphene.String)
    supplier = graphene.Field(SuppliersType)

    @classmethod
    @user_permission('Operations Admin')
    def mutate(cls, root, info, id):
        supplier = get_model_object(Suppliers, 'id', id)
        supplier.is_approved = True
        name = supplier.name
        supplier.save()
        success = f"supplier {name} has been approved!"
        return cls(success=success, supplier=supplier)


class DeleteSupplier(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
    success = graphene.Field(graphene.String)

    @classmethod
    @user_permission('Operations Admin')
    def mutate(cls, root, info, id):
        supplier = get_model_object(Suppliers, 'id', id)
        name = supplier.name
        supplier.delete()
        success = f"Supplier {name} has been deleted!"
        return cls(success=success)


class EditSupplier(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()
        email = graphene.String()
        mobile_number = graphene.String()
        address_line_1 = graphene.String()
        address_line_2 = graphene.String()
        lga = graphene.String()
        city_id = graphene.Int()
        tier_id = graphene.Int()
        rating = graphene.Int()
        credit_days = graphene.Int()
        logo = graphene.String()
        payment_terms_id = graphene.Int()
        commentary = graphene.String()
    edit_request = graphene.Field(SuppliersType)
    message = graphene.Field(graphene.String)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        id = kwargs.get('id')
        edit_request = Suppliers()
        supplier = get_model_object(Suppliers, 'id', id)
        if not supplier.is_approved:
            msg = "You can only propose an edit to an approved supplier!"
            raise GraphQLError(msg)
        if kwargs.get('email') is not None:
            email = kwargs.get('email')
        else:
            email = None

        kwargs.pop('id')
        for (key, value) in kwargs.items():
            if key is not None:
                setattr(edit_request, key, value)
        if not kwargs.get('city_id'):
            edit_request.city_id = supplier.city_id
        if not kwargs.get('payment_terms_id'):
            edit_request.payment_terms_id = \
                supplier.payment_terms_id
        if not kwargs.get('tier_id'):
            edit_request.tier_id = supplier.tier_id
        edit_request.user = info.context.user
        edit_request.parent = supplier
        edit_request.is_approved = True
        params = {
            'model_name': 'Suppliers',
            'field': 'email',
            'value': email
        }
        with SaveContextManager(edit_request, **params) as edit_request:
            name = supplier.name
            msg = f"Edit request for Supplier {name} has been sent!"
            return cls(edit_request, msg)


class EditProposal(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()
        email = graphene.String()
        mobile_number = graphene.String()
        address_line_1 = graphene.String()
        address_line_2 = graphene.String()
        lga = graphene.String()
        city_id = graphene.Int()
        tier_id = graphene.Int()
        rating = graphene.Int()
        credit_days = graphene.Int()
        logo = graphene.String()
        payment_terms_id = graphene.Int()
        commentary = graphene.String()
    edit_request = graphene.Field(SuppliersType)
    message = graphene.Field(graphene.String)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        id = kwargs.get('id')
        proposed_edit = get_model_object(Suppliers, 'id', id)
        if proposed_edit.user != info.context.user:
            msg = "You can't edit an edit request you didnot propose!"
            raise GraphQLError(msg)
        kwargs.pop('id')
        if kwargs.get('email') is not None:
            email = kwargs.get('email')
        else:
            email = proposed_edit.email
        for (key, value) in kwargs.items():
            if key is not None:
                setattr(proposed_edit, key, value)
        params = {
            'model_name': 'Suppliers',
            'field': 'email',
            'value': email
        }
        with SaveContextManager(proposed_edit, **params) as edit_request:
            name = proposed_edit.parent.name
            msg = f"Edit request for Supplier {name} has been updated!"
            return cls(edit_request, msg)


class ApproveEditRequest(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
    message = graphene.Field(graphene.String)
    supplier = graphene.Field(SuppliersType)

    @classmethod
    @user_permission('Operations Admin')
    def mutate(cls, root, info, **kwargs):
        id = kwargs.get('id')
        request_instance = get_model_object(Suppliers, 'id', id)
        dict_object = model_to_dict(request_instance)
        parent_id = dict_object.get('parent')
        pop_list = \
            ['supplier_id', 'parent', 'is_approved', 'admin_comment', 'outlet']
        [dict_object.pop(key) for key in pop_list]
        dict_object['user_id'] = dict_object.pop('user')
        dict_object['city_id'] = dict_object.pop('city')
        dict_object['tier_id'] = dict_object.pop('tier')
        dict_object['payment_terms_id'] = dict_object.pop('payment_terms')
        supplier = get_model_object(Suppliers, 'id', parent_id)
        name = supplier.name
        for (key, value) in dict_object.items():
            if value is not None:
                setattr(supplier, key, value)
        request_instance.delete()
        supplier.save()
        message = f"Supplier {name} has been successfully updated!"
        return cls(message, supplier)


class DeclineEditRequest(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        comment = graphene.String(required=True)

    message = graphene.Field(graphene.String)
    edit_request = graphene.Field(SuppliersType)

    @classmethod
    @user_permission('Operations Admin')
    def mutate(cls, root, info, **kwargs):
        id = kwargs.get('id')
        comment = kwargs.get('comment')
        edit_request = Suppliers.objects.get(id=id)
        edit_request.admin_comment = comment
        edit_request.save()
        supplier_name = edit_request.name
        msg = f"Edit request for supplier {supplier_name} has been declined!"
        return cls(msg, edit_request)


class CreateSupplierNote(graphene.Mutation):
    """ This creates a Supplier's note"""

    class Arguments:
        supplier_id = graphene.String(required=True)
        outlet_ids = graphene.List(graphene.Int, required=True)
        note = graphene.String(required=True)

    message = graphene.Field(graphene.String)
    supplier_note = graphene.Field(SupplierNoteType)
    supplier = graphene.Field(SuppliersType)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        supplier_id = kwargs.get("supplier_id")
        user = info.context.user
        outlet_ids = kwargs.get("outlet_ids")
        note = kwargs.get("note")
        special_cahracter_validation(note)
        if len(note.split()) < 2:
            raise GraphQLError("Suppliers note must be two or more words")
        supplier = get_model_object(Suppliers, "id", supplier_id)
        outlets = [get_model_object(Outlet, 'id', outlet_id)
                   for outlet_id in outlet_ids]
        supplier_note = SupplierNote(
                                      supplier=supplier,
                                      note=note,
                                      user=user
        )

        with SaveContextManager(supplier_note) as supplier_note:
            supplier_note.outlet.add(*outlets)
            supplier_note.save()
            return cls(
                       supplier_note=supplier_note,
                       supplier=supplier,
                       message="Successfully created Note")


class UpdateSupplierNote(graphene.Mutation):
    """
         This Updates a Supplier Note
    """
    class Arguments:
        id = graphene.Int(required=True)
        supplier_id = graphene.Int()
        outlet_ids = graphene.List(graphene.Int)
        note = graphene.String()
    success = graphene.Field(graphene.String)
    supplier_note = graphene.Field(SupplierNoteType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id, **kwargs):
        outlet_ids = kwargs.pop('outlet_ids')
        supplier_note = get_model_object(SupplierNote, "id", id)
        if info.context.user != supplier_note.user:
            raise GraphQLError(
                        "You can't update a note you didn't create")
        for key, value in kwargs.items():
            if key in ["note"]:
                special_cahracter_validation(value)
                if len(value.split()) < 2:
                    raise GraphQLError(
                        "Suppliers note must be two or more words")
            setattr(supplier_note, key, value)

        if outlet_ids:
            outlets = [get_model_object(Outlet, 'id', outlet_id)
                       for outlet_id in outlet_ids]
            supplier_note.outlet.clear()
            supplier_note.outlet.add(*outlets)
        with SaveContextManager(supplier_note) as supplier_note:
            return cls(
                       success="Suppliers Note was updated successfully",
                       supplier_note=supplier_note)


class DeleteSupplierNote(graphene.Mutation):
    """
    This deletes a Supplier Note
    """
    id = graphene.Int()
    success = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        supplier_note = get_model_object(SupplierNote, "id", id)
        if info.context.user != supplier_note.user:
            raise GraphQLError(
                        "You can't delete a note you didn't create")
        supplier_note.delete()
        return DeleteSupplierNote(
            success="Supplier note was deleted successfully")


class Mutation(graphene.ObjectType):
    add_supplier = AddSupplier.Field()
    approve_supplier = ApproveSupplier.Field()
    delete_supplier = DeleteSupplier.Field()
    edit_supplier = EditSupplier.Field()
    edit_proposal = EditProposal.Field()
    approve_edit_request = ApproveEditRequest.Field()
    decline_edit_request = DeclineEditRequest.Field()
    create_suppliernote = CreateSupplierNote.Field()
    update_suppliernote = UpdateSupplierNote.Field()
    delete_suppliernote = DeleteSupplierNote.Field()
