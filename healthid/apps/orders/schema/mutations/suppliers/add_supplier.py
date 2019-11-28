import graphene
from graphql_jwt.decorators import login_required

from healthid.apps.orders.schema.suppliers_query import (
    SuppliersType)
from healthid.apps.orders.models import Suppliers
from healthid.utils.app_utils.get_user_business import (
    get_user_business
)
from healthid.utils.app_utils.database import (SaveContextManager)
from healthid.utils.app_utils.validator import validator
from healthid.apps.orders.schema.mutations.suppliers.add_supplier_contacts \
    import AddSupplierContacts
from healthid.apps.orders.schema.mutations.suppliers.add_supplier_meta \
    import AddSupplierMeta


class SuppliersInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    tier_id = graphene.Int()


class SuppliersInputContacts(graphene.InputObjectType):
    email = graphene.String()
    mobile_number = graphene.String()
    address_line_1 = graphene.String()
    address_line_2 = graphene.String()
    lga = graphene.String()
    city_id = graphene.Int()
    country_id = graphene.Int()


class SuppliersInputMeta(graphene.InputObjectType):
    display_name = graphene.String()
    credit_days = graphene.Int()
    logo = graphene.String()
    payment_terms = graphene.String(required=True)
    commentary = graphene.String()


class AddSupplier(graphene.Mutation):
    """
    Add a new supplier to the database

    args:
        name(str): supplier name
        tier_id(int): id of the supplier's category

    returns:
        supplier(obj): 'Suppliers' model object detailing the created supplier.
    """

    class Arguments:
        input = SuppliersInput(required=True)
        contacts_input = SuppliersInputContacts()
        meta_input = SuppliersInputMeta()

    supplier = graphene.Field(SuppliersType)

    @classmethod
    def validate_fields(cls, input):
        fields = input
        fields['name'] = validator.special_character_validation(
            input['name'], 'supplier name')
        return fields

    @classmethod
    @login_required
    def mutate(cls, root, info, input=None,
               contacts_input=None, meta_input=None):
        user = info.context.user
        supplier = Suppliers()

        business = get_user_business(user)
        fields = cls.validate_fields(input)
        # contacts input
        contacts_fields = AddSupplierContacts.validate_fields(
            contacts_input) if contacts_input else None
        # meta input
        meta_fields = AddSupplierMeta.validate_fields(
            meta_input) if meta_input else None

        for (key, value) in fields.items():
            setattr(supplier, key, value)

        supplier.user = user
        supplier.business = business

        with SaveContextManager(supplier, model=Suppliers) as supplier:
            data = supplier
            if contacts_fields:
                contacts_fields['supplier_id'] = supplier.id
                data.supplier_contacts = AddSupplierContacts.mutate(
                    root, info, contacts_fields)

            if meta_fields:
                meta_fields['supplier_id'] = supplier.id
                meta_fields['display_name'] = meta_fields.get('display_name') \
                    or f'{supplier.name} ({supplier.supplier_id})'
                data.supplier_meta = AddSupplierMeta.mutate(
                    root, info, meta_fields)

            return cls(supplier=data)
