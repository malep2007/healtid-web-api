import graphene

from healthid.apps.sales.schema.mutations.carts.add_cart_item\
    import AddCartItem


class Mutation(graphene.ObjectType):
    add_to_cart = AddCartItem.Field()
