from datetime import datetime

import graphene
from dateutil.relativedelta import relativedelta
from graphql_jwt.decorators import login_required

from healthid.apps.products.schema.product_query import (
    Product
)
from healthid.apps.sales.models import (
    Promotion
)
from healthid.utils.app_utils.check_user_in_outlet import \
    check_user_is_active_in_outlet
from healthid.utils.auth_utils.decorator import user_permission
from healthid.utils.sales_utils.validators import (
    set_recommended_promotion
)


class CreateRecommendedPromotion(graphene.Mutation):
    """
    Create a recommended promotion for an outlet.

    args:
        outlet_id(int): the id of the outlets that will apply the promotion
                        and discounts

    returns:
        success(str): success message confirming promotion creation
        promotion(obj): 'Promotion' object containing details of
                        the newly created promotion.
    """

    class Arguments:
        outlet_id = graphene.Int(required=True)

    success = graphene.String()

    @login_required
    @user_permission('Manager')
    def mutate(self, info, **kwargs):
        outlet_id = kwargs.get('outlet_id')
        user = info.context.user
        check_user_is_active_in_outlet(user, outlet_id=outlet_id)
        today_date = datetime.now()
        twelve_month = today_date + relativedelta(months=+12)
        near_expired_products = Product.objects \
            .for_outlet(outlet_id) \
            .filter(nearest_expiry_date__range=(today_date, twelve_month))
        promotion_set = set_recommended_promotion(Promotion,
                                                  near_expired_products)
        return CreateRecommendedPromotion(
            success='Promotion set on {} product(s)'.format(promotion_set))
