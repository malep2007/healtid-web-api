import graphene
from graphql_jwt.decorators import login_required

from healthid.apps.sales.schema.types.sale import (SaleType)
from healthid.apps.receipts.schema.receipt_schema import ReceiptType
from healthid.apps.receipts.models import Receipt
from healthid.apps.sales.models import (Sale)
from healthid.apps.sales.schema.types.batch_type import Batch
from healthid.utils.messages.sales_responses import (SALES_SUCCESS_RESPONSES)


class CreateSale(graphene.Mutation):
    """
    Create a sale
    """
    sale = graphene.Field(SaleType)
    message = graphene.String()
    error = graphene.String()
    receipt = graphene.Field(ReceiptType)

    class Arguments:
        customer_id = graphene.String()
        outlet_id = graphene.Int(required=True)
        batches = graphene.List(Batch, required=True)
        discount_total = graphene.Float(graphene.Float, required=True)
        sub_total = graphene.Float(graphene.Float, required=True)
        amount_to_pay = graphene.Float(graphene.Float, required=True)
        paid_amount = graphene.Float(graphene.Float, required=True)
        change_due = graphene.Float(graphene.Float, required=True)
        payment_method = graphene.String(graphene.String, required=True)
        notes = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        new_sale = Sale()
        new_receipt = Receipt()
        sale = new_sale.create_sale(info=info, **kwargs)
        receipt = new_receipt.create_receipt(sale, kwargs.get('outlet_id'))
        return CreateSale(sale=sale,
                          receipt=receipt,
                          message=SALES_SUCCESS_RESPONSES[
                              "create_sales_success"])
