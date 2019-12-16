import graphene


class SalesReturnEnum(graphene.Enum):
    CustomerError = 'wrong product bought'
    RetailerError = 'Returned to Distributor'
    DamagedProduct = 'Damaged Product'
    ExpiredProduct = 'Expired Product'
    Others = 'Others'


class ReturnedProducts(graphene.InputObjectType):
    """
    This class defines necessary fields of a product to be returned
    """
    batch_id = graphene.ID(required=True)
    quantity = graphene.Int(required=True)
    price = graphene.Float(required=True)
    resellable = graphene.Boolean(required=True)
    return_reason = graphene.Argument(SalesReturnEnum, required=True)
