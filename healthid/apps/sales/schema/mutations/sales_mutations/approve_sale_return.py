import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from healthid.apps.sales.models import (SaleReturn)
from healthid.apps.sales.schema.sales_schema import (SaleReturnType)
from healthid.utils.app_utils.database import (get_model_object)
from healthid.utils.auth_utils.decorator import user_permission
from healthid.apps.receipts.models import Receipt
from healthid.utils.messages.sales_responses import (SALES_ERROR_RESPONSES,
                                                     SALES_SUCCESS_RESPONSES)


class ApproveSalesReturn(graphene.Mutation):
    sales_return = graphene.Field(SaleReturnType)
    message = graphene.String()

    class Arguments:
        sales_return_id = graphene.Int(required=True)
        sales_id = graphene.Int(required=True)
        returned_sales = graphene.List(graphene.Int, required=True)

    @login_required
    @user_permission('Manager')
    def mutate(self, info, **kwargs):
        sales_id = kwargs.get('sales_id')
        returned_sales = kwargs.get('returned_sales')

        if not returned_sales:
            raise GraphQLError(SALES_ERROR_RESPONSES["empty_sales_return"])

        receipt = get_model_object(Receipt, 'sale_id', sales_id)

        new_return = SaleReturn()
        sales_return = new_return.approve_sales_return(
            user=info.context.user, receipt=receipt, **kwargs)

        return ApproveSalesReturn(
            sales_return=sales_return,
            message=SALES_SUCCESS_RESPONSES["sales_return_approved"])
