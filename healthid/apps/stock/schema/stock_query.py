import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from healthid.apps.stock.models import StockCount
from healthid.utils.app_utils.database import get_model_object
from healthid.apps.stock.models import StockCountTemplate


class StockCountTemplateType(DjangoObjectType):
    class Meta:
        model = StockCountTemplate


class StockTemplateQuery(graphene.ObjectType):
    stock_templates = graphene.List(
        StockCountTemplateType,
        outlet_id=graphene.Int(required=True))
    stock_template = graphene.Field(
        StockCountTemplateType,
        template_id=graphene.Int(required=True),
        outlet_id=graphene.Int(required=True)
    )

    @login_required
    def resolve_stock_templates(self, info, **kwargs):
        outlet_id = kwargs.get('outlet_id')
        return StockCountTemplate.objects.filter(outlet_id=outlet_id)

    @login_required
    def resolve_stock_template(self, info, **kwargs):
        template_id = kwargs.get('template_id')
        outlet_id = kwargs.get('outlet_id')
        return StockCountTemplate.objects.filter(
            outlet_id=outlet_id, id=template_id).first()


class StockCountType(DjangoObjectType):
    class Meta:
        model = StockCount


class StockCountQuery(graphene.AbstractType):
    stock_counts = graphene.List(StockCountType)
    stock_count = graphene.Field(
        StockCountType,
        id=graphene.String(required=True))

    @login_required
    def resolve_stock_counts(self, info):
        all_stock_counts = StockCount.objects.all()
        return all_stock_counts

    @login_required
    def resolve_stock_count(self, info, **kwargs):
        stock_count_id = kwargs.get('id')
        return get_model_object(StockCount, 'id', stock_count_id)


class Query(
    StockTemplateQuery,
    StockCountQuery,
    graphene.ObjectType


):
    pass
