import graphene


class Batch(graphene.InputObjectType):
    """
    This class defines necessary fields of a product to be sold
    """
    batch_id = graphene.ID()
    quantity = graphene.Int()
    discount = graphene.Float()
    price = graphene.Float()
    note = graphene.String()
