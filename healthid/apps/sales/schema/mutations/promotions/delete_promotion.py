import graphene
from graphql_jwt.decorators import login_required

from healthid.apps.sales.models import (
    Promotion
)
from healthid.utils.app_utils.check_user_in_outlet import \
    check_user_is_active_in_outlet
from healthid.utils.app_utils.database import (get_model_object)
from healthid.utils.auth_utils.decorator import user_permission
from healthid.utils.messages.common_responses import SUCCESS_RESPONSES


class DeletePromotion(graphene.Mutation):
    """
    Delete a promotion for an outlet.

    args:
        promotion_id(str): id of the promotion to be deleted

    returns:
        success(str): success message confirming promotion deletion
        promotion(obj): 'Promotion' object containing details of
                        the newly deleted promotion.
    """

    class Arguments:
        promotion_id = graphene.String(required=True)

    success = graphene.String()

    @login_required
    @user_permission('Manager')
    def mutate(self, info, **kwargs):
        promotion_id = kwargs.get('promotion_id')
        user = info.context.user
        promotion = get_model_object(Promotion, 'id', promotion_id)
        check_user_is_active_in_outlet(user, outlet=promotion.outlet)
        promotion.delete(user)
        return DeletePromotion(
            success=SUCCESS_RESPONSES[
                "deletion_success"].format("Promotion"))
