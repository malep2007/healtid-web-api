import graphene
from graphql_jwt.decorators import login_required
from graphql import GraphQLError


from healthid.apps.sales.sales_velocity import SalesVelocity
from healthid.apps.sales.schema.types.velocity import Velocity

from healthid.apps.sales.models import (
    Sale, SalesPrompt)
from healthid.utils.app_utils.database import get_model_object
from healthid.utils.app_utils.pagination import pagination_query
from healthid.utils.app_utils.pagination_defaults import PAGINATION_DEFAULT
from healthid.utils.auth_utils.decorator import user_permission
from healthid.utils.messages.sales_responses import SALES_ERROR_RESPONSES
from healthid.apps.sales.schema.types.sale import (  # noqa
    SalesPromptType, SaleDetailType, SaleType,
    SalesPromptType, SaleReturnDetailType
)


class Query(graphene.ObjectType):
    """
    Queries Sales
    Args:
        product_id (int) the product id
        outlet_id (int) the outlet id
    returns:
        Two float values for the calculated sales velocity
            and the default sales velocity
    """

    sales_velocity = graphene.Field(
        Velocity,
        product_id=graphene.Int(),
        outlet_id=graphene.Int())
    sales_prompts = graphene.List(SalesPromptType)
    sales_prompt = graphene.Field(SalesPromptType, id=graphene.Int())

    outlet_sales_history = graphene.List(SaleType,
                                         outlet_id=graphene.Int(required=True),
                                         search=graphene.String(),
                                         page_count=graphene.Int(),
                                         page_number=graphene.Int())
    all_sales_history = graphene.List(SaleType,
                                      page_count=graphene.Int(),
                                      page_number=graphene.Int())

    sale_history = graphene.Field(
        SaleType, sale_id=graphene.Int(required=True))

    @login_required
    def resolve_sales_velocity(self, info, **kwargs):
        product_id = kwargs.get('product_id')
        outlet_id = kwargs.get('outlet_id')

        return SalesVelocity(
            product_id=product_id,
            outlet_id=outlet_id).velocity_calculator()

    @login_required
    @user_permission('Manager')
    def resolve_sales_prompts(self, info, **kwargs):
        return SalesPrompt.objects.all()

    @login_required
    @user_permission('Manager')
    def resolve_sales_prompt(self, info, **kwargs):
        id = kwargs.get('id')
        sales_prompt = get_model_object(SalesPrompt, 'id', id)
        return sales_prompt

    @login_required
    def resolve_outlet_sales_history(self, info, **kwargs):
        page_count = kwargs.get('page_count')
        page_number = kwargs.get('page_number')
        search = kwargs.get('search')
        outlet_id = kwargs.get('outlet_id')

        sale = Sale()
        resolved_value = sale.sales_history(
            outlet_id=outlet_id, search=search)

        if page_count or page_number:
            sales = pagination_query(
                resolved_value, page_count, page_number)
            Query.pagination_result = sales
            return sales[0]
        if resolved_value:
            paginated_response = pagination_query(resolved_value,
                                                  PAGINATION_DEFAULT[
                                                      "page_count"],
                                                  PAGINATION_DEFAULT[
                                                      "page_number"])

            Query.pagination_result = paginated_response
            return paginated_response[0]
        return GraphQLError(SALES_ERROR_RESPONSES["no_sales_error"])

    @login_required
    def resolve_sale_history(self, info, sale_id):
        sale = get_model_object(Sale, 'id', sale_id)
        return sale

    @login_required
    @user_permission('Manager')
    def resolve_all_sales_history(self, info, **kwargs):
        page_count = kwargs.get('page_count')
        page_number = kwargs.get('page_number')

        resolved_value = Sale.objects.all()

        if page_count or page_number:
            sales = pagination_query(
                resolved_value, page_count, page_number)
            Query.pagination_result = sales
            return sales[0]
        if resolved_value:
            paginated_response = pagination_query(resolved_value,
                                                  PAGINATION_DEFAULT[
                                                      "page_count"],
                                                  PAGINATION_DEFAULT[
                                                      "page_number"])

            Query.pagination_result = paginated_response
            return paginated_response[0]
        return GraphQLError(SALES_ERROR_RESPONSES["no_sales_error"])
