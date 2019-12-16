import graphene
from graphql_jwt.decorators import login_required

from healthid.apps.sales.models import (SaleReturn)
from healthid.apps.sales.schema.sales_schema import (SaleReturnType)
from healthid.utils.messages.sales_responses import (SALES_SUCCESS_RESPONSES)
from healthid.apps.sales.schema.types.returned_products import ReturnedProducts


class PayEnum(graphene.Enum):
    """
    This class defines choices for refund compensation type
    """
    Cash = 'cash'
    StoreCredit = 'store credit'


class InitiateSaleReturn(graphene.Mutation):
    """
    initiate a sales return by user(Cashier, manager or accountant)
    """
    message = graphene.String()
    sales_return_initiated = graphene.Field(SaleReturnType)
    error = graphene.String()

    class Arguments:
        sale_id = graphene.Int(required=True)
        returned_batches = graphene.List(ReturnedProducts, required=True)
        outlet_id = graphene.Int(required=True)
        return_amount = graphene.Float(required=True)
        return_note = graphene.String()
        refund_compensation_type = graphene.Argument(PayEnum, required=True)

    @login_required
    def mutate(self, info, **kwargs):
        new_return = SaleReturn()
        return_initiated = new_return.create_return(
            user=info.context.user, **kwargs)
        return InitiateSaleReturn(
            message=SALES_SUCCESS_RESPONSES["sale_intiate_success"],
            sales_return_initiated=return_initiated)
