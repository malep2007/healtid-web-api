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
from healthid.utils.app_utils.database import (SaveContextManager,
                                               get_model_object)
from healthid.utils.auth_utils.decorator import user_permission
from healthid.utils.messages.common_responses import SUCCESS_RESPONSES
from healthid.utils.sales_utils.validators import (
    validate_fields, add_products_to_promotion
)


class UpdatePromotion(graphene.Mutation):
    """
    Create a new promotion for an outlet.

    args:
        title(str): title of the promotion to be created
        promotion_type_id(str): id of the related promotion type that the
                                promotion will fall under
        description(str): description of the promotion to be created
        product_ids(list): list of ids for the products that the promotion will
                           be applied to
        discount(float): the value of the discount for the promotion
        outlet_id(int): the id of the outlets that will apply the promotion
                        and discounts

    returns:
        success(str): success message confirming promotion update
        promotion(obj): 'Promotion' object containing details of
                        the newly created promotion.
    """

    class Arguments:
        promotion_id = graphene.String(required=True)
        title = graphene.String()
        promotion_type_id = graphene.String()
        description = graphene.String()
        product_ids = graphene.List(graphene.Int)
        discount = graphene.Float()

    success = graphene.String()
    promotion = graphene.Field(PromotionType)

    @login_required
    @user_permission('Manager')
    def mutate(self, info, **kwargs):
        promotion_id = kwargs.pop('promotion_id')
        user = info.context.user
        promotion = get_model_object(Promotion, 'id', promotion_id)
        check_user_is_active_in_outlet(user, outlet=promotion.outlet)
        product_ids = kwargs.pop('product_ids') if kwargs.get(
            'product_ids') else []
        validate_fields(Promotion(), **kwargs)
        for (key, value) in kwargs.items():
            setattr(promotion, key, value)
        with SaveContextManager(promotion, model=Promotion) as promotion:
            promotion = add_products_to_promotion(promotion, product_ids)
            return UpdatePromotion(success=SUCCESS_RESPONSES[
                "update_success"].format("Promotion"),
                promotion=promotion)
