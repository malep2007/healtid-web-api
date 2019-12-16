import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from healthid.apps.sales.models import (
    PromotionType as PromotionTypeModel
)
from healthid.apps.sales.schema.types.promotion import (
    PromotionTypeModelType
)
from healthid.utils.app_utils.database import (SaveContextManager)
from healthid.utils.auth_utils.decorator import user_permission
from healthid.utils.messages.common_responses import SUCCESS_RESPONSES
from healthid.utils.messages.sales_responses import \
    SALES_ERROR_RESPONSES


class CreatePromotionType(graphene.Mutation):
    """
    Create a new promotion type

    args:
        name(str): name of the promotion type to be created

    returns:
        success(str): success message confirming promotion type creation
        promotion_type(obj): 'PromotionType' object containing details of
                             the newly created promotion type.
    """

    class Arguments:
        name = graphene.String(required=True)

    success = graphene.String()
    promotion_type = graphene.Field(PromotionTypeModelType)

    @login_required
    @user_permission('Manager')
    def mutate(self, info, **kwargs):
        name = kwargs.get('name')
        if name.strip() == "":
            raise GraphQLError(SALES_ERROR_RESPONSES["promotion_type_error"])
        params = {'model': PromotionTypeModel}
        promotion_type = PromotionTypeModel(name=name)
        with SaveContextManager(promotion_type, **params) as promotion_type:
            success = SUCCESS_RESPONSES[
                "creation_success"].format("Promotion Type")
            return CreatePromotionType(
                success=success, promotion_type=promotion_type)
