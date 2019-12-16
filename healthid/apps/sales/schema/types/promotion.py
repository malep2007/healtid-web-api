from graphene_django import DjangoObjectType

from healthid.apps.sales.models import Promotion, PromotionType as PromotionTypeModel


class PromotionType(DjangoObjectType):
    class Meta:
        model = Promotion


class PromotionTypeModelType(DjangoObjectType):
    class Meta:
        model = PromotionTypeModel
