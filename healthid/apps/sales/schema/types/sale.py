import graphene
from graphene_django import DjangoObjectType
from graphene.utils.resolve_only_args import resolve_only_args

from healthid.apps.sales.models import Sale, SaleDetail, SalesPrompt


class SaleDetailType(DjangoObjectType):
    class Meta:
        model = SaleDetail


class SaleType(DjangoObjectType):
    register_id = graphene.Int(source='get_default_register')

    class Meta:
        model = Sale
        interfaces = (graphene.relay.Node,)

    id = graphene.ID(required=True)

    @resolve_only_args
    def resolve_id(self):
        return self.id


class SalesPromptType(DjangoObjectType):
    class Meta:
        model = SalesPrompt
