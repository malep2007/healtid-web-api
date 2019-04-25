import graphene
from graphql.error import GraphQLError
from graphql_jwt.decorators import login_required

from healthid.apps.preference.models import Currency, Preference, Timezone
from healthid.apps.preference.schema.preference_schema import (CurrencyType,
                                                               TimezoneType,
                                                               VatType)
from healthid.utils.app_utils.database import get_model_object
from healthid.utils.auth_utils.decorator import master_admin_required
from healthid.utils.preference_utils.update_currency import update_vate


def get_currency_from_file(name):
    # filters currency by name from the ist of currencies
    currencies = Currency.get_currency_formats()

    currency = Currency()
    default_currency = list(
        filter(lambda money: money['name'] == name, currencies))
    if default_currency:
        for(key, value) in default_currency[0].items():
            if key is not None:
                setattr(currency, key, value)
        return currency
    raise GraphQLError(
        'Currency with name {} does not exist'.format(name))


def get_currency(currency_name, **kwargs):
    # checks for currency in models before updating it.
    currencies = Currency.objects.filter(name=currency_name)
    if not currencies.exists():
        currency = get_currency_from_file(currency_name)
        for(key, value) in kwargs.items():
            if key is not None:
                setattr(currency, key, value)
        currency.save()
        return currency
    return currencies.first()


class UpdatePreference(graphene.Mutation):
    """
    Updates a timezone
    """
    outlet_currency = graphene.Field(CurrencyType)
    outlet_timezone = graphene.Field(TimezoneType)
    outlet_vat = graphene.Field(VatType)
    success = graphene.String()

    class Arguments:
        outlet_timezone = graphene.String()
        preference_id = graphene.String(required=True)
        outlet_currency = graphene.String()
        outlet_vat = graphene.Float()

    @login_required
    @master_admin_required
    def mutate(self, info, **kwargs):
        outlet_timezone_id = kwargs.get('outlet_timezone')
        outlet_currency = kwargs.get('outlet_currency')
        outlet_vat_rate = kwargs.get('outlet_vat')
        preference_id = kwargs.get('preference_id')
        preference = get_model_object(Preference, 'id', preference_id)
        if outlet_vat_rate:
            outlet_vat = update_vate(outlet_vat_rate, preference)
            preference.vat_rate.rate = outlet_vat

        if outlet_timezone_id:
            outlet_timezone = get_model_object(
                Timezone, 'id', outlet_timezone_id)
            preference.outlet_timezone = outlet_timezone
        if outlet_currency:
            currency = get_currency(outlet_currency, **kwargs)
            preference.outlet_currency_id = currency.id
        preference.save()

        return UpdatePreference(
            outlet_timezone=preference.outlet_timezone,
            outlet_currency=preference.outlet_currency,
            outlet_vat=preference.vat_rate,
            success=("Preference updated successfully")
        )


class Mutation(graphene.ObjectType):
    update_preference = UpdatePreference.Field()
