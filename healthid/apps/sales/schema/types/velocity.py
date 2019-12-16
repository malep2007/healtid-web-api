import graphene


class Velocity(graphene.ObjectType):
    default_sales_velocity = graphene.Float()
    calculated_sales_velocity = graphene.Float()
    message = graphene.String()
