import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from healthid.utils.auth_utils.decorator import user_permission

from healthid.apps.business.models import Business
from healthid.apps.outlets.models import City, Country, Outlet, OutletKind
from healthid.utils.app_utils.database import get_model_object
from healthid.utils.messages.outlet_responses import OUTLET_ERROR_RESPONSES


class OutletType(DjangoObjectType):
    class Meta:
        model = Outlet


class CityType(DjangoObjectType):
    class Meta:
        model = City


class CountryType(DjangoObjectType):
    class Meta:
        model = Country


class OutletKindType(DjangoObjectType):
    class Meta:
        model = OutletKind


class OutletQuery(graphene.ObjectType):
    """
    Return a list of outlets.
    Or return a single outlet specified.
    """
    errors = graphene.Field(graphene.String)
    outlets = graphene.List(OutletType)
    outlet = graphene.Field(
        OutletType,
        id=graphene.Int(),
        name=graphene.String(),
        kind_id=graphene.Int(),
        phone_number=graphene.String(),
        address_line1=graphene.String(),
        address_line2=graphene.String(),
        lga=graphene.String(),
        city_id=graphene.Int(),
        date_launched=graphene.String(),
        prefix_id=graphene.String()
    )

    @login_required
    @user_permission('Manager')
    def resolve_outlets(self, info, **kwargs):
        user_id = info.context.user.id
        business_id = (Business.user
                       .through
                       .objects
                       .filter(user_id=user_id)[0]
                       .business_id
                       )
        return Outlet.objects.filter(
            business_id=business_id
        )

    @login_required
    def resolve_outlet(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return get_model_object(Outlet, 'id', id)

        return None


class CityQuery(graphene.ObjectType):
    errors = graphene.Field(graphene.String)
    cities = graphene.List(CityType)
    city = graphene.Field(
        CityType,
        id=graphene.Int(),
        name=graphene.String(),
    )

    @login_required
    def resolve_cities(self, info, **kwargs):
        return City.objects.all()

    @login_required
    def resolve_city(self, info, **kwargs):
        city_id = kwargs.get('id')
        city_name = kwargs.get('name', ' ').title()
        if (city_id or city_name) is not None:
            city = City.objects.filter(
                Q(id=city_id) | Q(name=city_name)
            ).first()
            if city is None:
                raise GraphQLError(
                      OUTLET_ERROR_RESPONSES["inexistent_city_error"])
            return city
        raise GraphQLError(
              OUTLET_ERROR_RESPONSES["city_query_invalid_input_error"])


class CountryQuery(graphene.ObjectType):
    errors = graphene.Field(graphene.String)
    countries = graphene.List(CountryType)
    country = graphene.Field(
        CountryType,
        id=graphene.Int(),
        name=graphene.String()
    )

    @login_required
    def resolve_countries(self, info, **kwargs):
        return Country.objects.all()

    @login_required
    def resolve_country(self, info, **kwargs):
        ctry_id = kwargs.get('id')
        ctry_name = kwargs.get('name', '').title()
        if (ctry_id or ctry_name) is not None:
            ctry = Country.objects.filter(
                Q(id=ctry_id) | Q(name=ctry_name)
            ).first()
            if ctry is None:
                raise GraphQLError(
                      OUTLET_ERROR_RESPONSES["inexistent_country_error"])
            return ctry
        raise GraphQLError(
              OUTLET_ERROR_RESPONSES["city_query_invalid_input_error"])


class Query(
    OutletQuery,
    CityQuery,
    CountryQuery,
    graphene.ObjectType
):
    pass
