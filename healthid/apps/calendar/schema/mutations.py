from os import environ, getenv

import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from healthid.apps.calendar.models import Calendar
from healthid.apps.outlets.models import Outlet
from healthid.apps.authentication.models import User
from graphql_jwt.decorators import login_required
from healthid.apps.authentication.utils.decorator import master_admin_required


class CalendarType(DjangoObjectType):
    class Meta:
        model = Calendar


class CreateCalendar(graphene.Mutation):
    """This class creates a calendar
    """
    calendar = graphene.Field(CalendarType)
    success = graphene.List(graphene.String)
    errors = graphene.List(graphene.String)

    class Arguments:
        name = graphene.String(required=True)

    @staticmethod
    @login_required
    @master_admin_required
    def mutate(root, info, **kwargs):
        calendar_name = kwargs.get('calender_name', '')
        outlet_id = kwargs.get('outlet_id', '')
        outlet = Outlet.objects.get(id=outlet_id)
        calendar = Calendar.objects.create(calendar_name)
        calendar.create_relation(outlet)
        message = 'callender for outlet{str(outlet.name)} has been created successfuly'
        return CreateCalendar(
            calendar=calendar, message=message
        )
