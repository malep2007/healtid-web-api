import graphene
from graphql.error import GraphQLError
from graphql_jwt.decorators import login_required

from healthid.apps.orders.models import Suppliers, SuppliersMeta
from healthid.apps.orders.schema.suppliers_query import SuppliersType
from healthid.utils.app_utils.database import (
    SaveContextManager, get_model_object)
from healthid.utils.messages.common_responses import ERROR_RESPONSES
from healthid.utils.messages.common_responses import SUCCESS_RESPONSES
from healthid.utils.messages.orders_responses import \
    ORDERS_ERROR_RESPONSES
from healthid.apps.orders.enums.suppliers import PaymentTermsType


class EditSupplierMeta(graphene.Mutation):
    """
    Edit a supplier's details

    args:
        id(str): id of the meta to be edited
        display_name(str): supplier display_name
        credit_days(int): average number of days expected to settle outstanding
                          payments to the supplier
        logo(str): image URL for the supplier logo
        payment_terms(str): preferred payment method
                            (on credit or cash on delivery )
        commentary(str): additional comments
        admin_comment(str): additional admin comments

    returns:
        supplier(obj): 'Suppliers' model object detailing the edited supplier
        message(str): success message confirming supplier edit
    """

    class Arguments:
        meta_id = graphene.String(required=True)
        display_name = graphene.String()
        credit_days = graphene.Int()
        logo = graphene.String()
        payment_terms = graphene.String()
        commentary = graphene.String()
        admin_comment = graphene.String()

    supplier = graphene.Field(SuppliersType)
    message = graphene.Field(graphene.String)

    @classmethod
    def validate_fields(cls, meta, kwargs):
        fields = kwargs

        fields['id'] = meta.id
        fields['supplier_id'] = meta.supplier_id
        fields['display_name'] = fields.get(
            'display_name') or meta.display_name
        fields['logo'] = fields.get('logo') or meta.logo
        fields['commentary'] = fields.get('commentary') or meta.commentary
        fields['admin_comment'] = fields.get(
            'admin_comment') or meta.admin_comment
        fields['payment_terms'] = fields.get(
            'payment_terms') or meta.payment_terms
        fields['credit_days'] = fields.get(
            'credit_days') or meta.credit_days

        # check payment terms
        is_payment_term_valid = False
        payment_terms = fields['payment_terms'].upper().replace(' ', '_')
        for choice in PaymentTermsType.choices():
            is_payment_term_valid = payment_terms in choice
            if is_payment_term_valid:
                break

        if not is_payment_term_valid:
            raise GraphQLError(
                ERROR_RESPONSES['payment_terms'].format(
                    fields['payment_terms']))

        if payment_terms == 'ON_CREDIT' and fields['credit_days'] <= 0:
            raise GraphQLError(ERROR_RESPONSES['payment_terms_on_credit'])

        if payment_terms == 'CASH_ON_DELIVERY' and fields['credit_days'] > 0:
            raise GraphQLError(
                ERROR_RESPONSES['payment_terms_cash_on_deliver'])

        del fields['meta_id']
        return fields

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        supplier_meta = SuppliersMeta()
        meta_id = kwargs.get('meta_id')
        meta = get_model_object(SuppliersMeta, 'id', meta_id)
        supplier = get_model_object(Suppliers, 'id', meta.supplier_id)

        if not supplier.is_approved:
            msg = ORDERS_ERROR_RESPONSES['supplier_edit_validation_error']
            raise GraphQLError(msg)

        fields = cls.validate_fields(meta, kwargs)

        for (key, value) in fields.items():
            if key is not None:
                setattr(supplier_meta, key, value)

        with SaveContextManager(supplier_meta,
                                model=SuppliersMeta) as supplier_meta:
            name = supplier.name
            supplier.supplier_meta = supplier_meta
            msg = SUCCESS_RESPONSES["update_success"].format(
                f"Supplier '{name}'")
            return cls(supplier, msg)
