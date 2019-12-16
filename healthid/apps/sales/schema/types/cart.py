import graphene
from graphene_django import DjangoObjectType

from healthid.apps.sales.models import Cart, CartItem


class CartType(DjangoObjectType):
    total = graphene.Float()

    class Meta:
        model = Cart

    def resolve_total(self, info, **kwargs):
        return self.total


class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
