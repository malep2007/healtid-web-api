import graphene
from graphql_jwt.decorators import login_required

from healthid.apps.sales.models import Cart
from healthid.apps.sales.schema.types.cart import CartType


class Query(graphene.AbstractType):
    cart = graphene.Field(CartType)

    @login_required
    def resolve_cart(self, info, **kwargs):
        '''
        Method that returns a cart of a logged in user.
        '''
        cart, _ = Cart.objects.get_or_create(user=info.context.user)
        return cart
