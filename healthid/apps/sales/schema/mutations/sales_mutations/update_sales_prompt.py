import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from healthid.apps.sales.models import (SalesPrompt)
from healthid.apps.sales.schema.types.sale import (SalesPromptType)
from healthid.utils.app_utils.database import (SaveContextManager,
                                               get_model_object)
from healthid.utils.auth_utils.decorator import user_permission
from healthid.utils.messages.sales_responses import (SALES_ERROR_RESPONSES)
from healthid.utils.messages.common_responses import SUCCESS_RESPONSES


class UpdateSalesPrompt(graphene.Mutation):
    """
    This Updates a Sales prompt
    """
    success = graphene.String()
    salesPrompt = graphene.Field(SalesPromptType)

    class Arguments:
        id = graphene.Int(required=True)
        prompt_title = graphene.String()
        description = graphene.String()
        product_id = graphene.Int()
        outlet_id = graphene.Int()

    @login_required
    @user_permission('Manager')
    def mutate(self, info, id, **kwargs):
        salesPrompt = get_model_object(SalesPrompt, 'id', id)
        for key, value in kwargs.items():
            if key in ["prompt_title", "description"]:
                if value.strip() == "":
                    raise GraphQLError(SALES_ERROR_RESPONSES["title_error"])
            setattr(salesPrompt, key, value)
        params = {'model': SalesPrompt}
        with SaveContextManager(salesPrompt, **params) as salesPrompt:
            return UpdateSalesPrompt(
                success=SUCCESS_RESPONSES[
                    "update_success"].format("Sales prompt"),
                salesPrompt=salesPrompt)
