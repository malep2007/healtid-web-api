import graphene

from healthid.apps.sales.schema.mutations.sales_mutations\
    .create_sales_prompts import CreateSalesPrompts
from healthid.apps.sales.schema.mutations.sales_mutations\
    .update_sales_prompt import UpdateSalesPrompt
from healthid.apps.sales.schema.mutations.sales_mutations\
    .delete_sales_prompt import DeleteSalesPrompt
from healthid.apps.sales.schema.mutations.sales_mutations\
    .create_sale import CreateSale
from healthid.apps.sales.schema.mutations.sales_mutations\
    .consultation_payment import ConsultationPayment
from healthid.apps.sales.schema.mutations.sales_mutations\
    .initiate_sale_return import InitiateSaleReturn
from healthid.apps.sales.schema.mutations.sales_mutations\
    .approve_sale_return import ApproveSalesReturn
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
    .approve import ApprovePromotion
from healthid.apps.sales.schema.mutations.promotions.\
    create_customer_near_expire import CreateCustomNearExpirePromotion
from healthid.apps.sales.schema.mutations.carts.add_cart_item\
    import AddCartItem


class Mutation(graphene.ObjectType):
    # sale
    create_salesprompts = CreateSalesPrompts.Field()
    delete_salesprompt = DeleteSalesPrompt.Field()
    update_salesprompt = UpdateSalesPrompt.Field()
    create_sale = CreateSale.Field()
    consultation_payment = ConsultationPayment.Field()
    initiate_sales_return = InitiateSaleReturn.Field()
    approve_sales_return = ApproveSalesReturn.Field()
    # promotion
    create_promotion = CreatePromotion.Field()
    update_promotion = UpdatePromotion.Field()
    delete_promotion = DeletePromotion.Field()
    create_promotion_type = CreatePromotionType.Field()
    approve_promotion = ApprovePromotion.Field()
    create_recommended_promotion = CreateRecommendedPromotion.Field()
    create_custom_near_expire_promotion = \
        CreateCustomNearExpirePromotion.Field()

    # cart
    add_to_cart = AddCartItem.Field()
