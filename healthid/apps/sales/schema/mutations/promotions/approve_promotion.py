import graphene
from graphql_jwt.decorators import login_required

from healthid.apps.sales.models import (
    Promotion
)
from healthid.apps.sales.schema.types.promotion import (
    PromotionType
)
from healthid.utils.app_utils.check_user_in_outlet import \
    check_user_is_active_in_outlet
from healthid.utils.app_utils.database import (get_model_object)
from healthid.utils.auth_utils.decorator import user_permission
from healthid.utils.messages.sales_responses import SALES_SUCCESS_RESPONSES


class ApprovePromotion(graphene.Mutation):
    """
    Approve a promotion for an outlet.

    args:
        promotion_id(str): id of the promotion to be deleted

    returns:
        success(str): success message confirming promotion approval
        promotion(obj): 'Promotion' object containing details of
                        the newly approved promotion.
    """

    class Arguments:
        promotion_id = graphene.String(required=True)

    success = graphene.String()
    promotion = graphene.Field(PromotionType)

    @login_required
    @user_permission('Manager')
    def mutate(self, info, **kwargs):
        promotion_id = kwargs.get('promotion_id')
        user = info.context.user
        promotion = get_model_object(Promotion, 'id', promotion_id)
        check_user_is_active_in_outlet(user, outlet=promotion.outlet)
        promotion.is_approved = True
        promotion.save()
        return ApprovePromotion(
            success=SALES_SUCCESS_RESPONSES["promotion_approval_success"],
            promotion=promotion)
