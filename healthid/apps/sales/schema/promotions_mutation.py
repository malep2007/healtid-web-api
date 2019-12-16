import graphene

from healthid.apps.sales.schema.mutations.promotions.\
    create_promotion_type import CreatePromotionType
from healthid.apps.sales.schema.mutations.promotions.\
    create_promotion import CreatePromotion
from healthid.apps.sales.schema.mutations.promotions.\
    create_recommended_promotion import CreateRecommendedPromotion
from healthid.apps.sales.schema.mutations.promotions.\
    update_promotion import UpdatePromotion
from healthid.apps.sales.schema.mutations.promotions.\
    delete_promotion import DeletePromotion
from healthid.apps.sales.schema.mutations.promotions\
    .approve_promotion import ApprovePromotion
from healthid.apps.sales.schema.mutations.promotions.\
    create_customer_near_expire import CreateCustomNearExpirePromotion


class Mutation(graphene.ObjectType):
    create_promotion = CreatePromotion.Field()
    update_promotion = UpdatePromotion.Field()
    delete_promotion = DeletePromotion.Field()
    create_promotion_type = CreatePromotionType.Field()
    approve_promotion = ApprovePromotion.Field()
    create_recommended_promotion = CreateRecommendedPromotion.Field()
    create_custom_near_expire_promotion = \
        CreateCustomNearExpirePromotion.Field()
