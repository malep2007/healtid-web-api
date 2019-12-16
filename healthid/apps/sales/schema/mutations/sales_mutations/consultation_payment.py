import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from healthid.apps.consultation.models import CustomerConsultation
from healthid.apps.sales.models import (Sale)
from healthid.apps.sales.schema.sales_schema import (
    ConsultationPaymentType)
from healthid.utils.app_utils.database import (SaveContextManager,
                                               get_model_object)
from healthid.apps.receipts.models import Receipt
from healthid.apps.receipts.schema.receipt_schema import ReceiptType
from healthid.utils.messages.sales_responses import (SALES_ERROR_RESPONSES)


class ConsultationPayment(graphene.Mutation):
    """
    Make payment for a consultation
    Args:
        customer_consultation_id (id) id of the consultation item
        discount_total (float) discount given if any
        sub_total (float) sale subtotal
        paid_amount (float) amount client has given
        change_due (float) change due to client
        payment_method (str) payment option chosen
        notes (str) Narrative for the sale
    returns:
         sale object for the consultation,
         otherwise a GraphqlError is raised
    """
    sale = graphene.Field(ConsultationPaymentType)
    message = graphene.String()
    receipt = graphene.Field(ReceiptType)

    class Arguments:
        customer_consultation_id = graphene.Int(required=True)
        discount_total = graphene.Float(graphene.Float, required=True)
        sub_total = graphene.Float(graphene.Float, required=True)
        paid_amount = graphene.Float(graphene.Float, required=True)
        change_due = graphene.Float(graphene.Float, required=True)
        payment_method = graphene.String(graphene.String, required=True)
        notes = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        customer_consultation_id = kwargs.get('customer_consultation_id')
        customer_consultation = get_model_object(
            CustomerConsultation, 'id', customer_consultation_id)
        outlet = customer_consultation.outlet

        if customer_consultation.paid:
            raise GraphQLError(SALES_ERROR_RESPONSES["already_marked_as_paid"])

        price = customer_consultation.consultation_type.price_per_session
        new_sale = Sale(
            sales_person=user, customer=customer_consultation.customer,
            outlet=outlet,
            amount_to_pay=price)

        del kwargs['customer_consultation_id']
        for (key, value) in kwargs.items():
            setattr(new_sale, key, value)

        with SaveContextManager(new_sale, model=Sale) as new_sale:
            pass

        customer_consultation.paid = True
        customer_consultation.sale_record = new_sale
        customer_consultation.save()

        new_receipt = Receipt()
        receipt = new_receipt.create_receipt(new_sale, outlet.id)

        return ConsultationPayment(
            sale=new_sale, receipt=receipt, message='message')
