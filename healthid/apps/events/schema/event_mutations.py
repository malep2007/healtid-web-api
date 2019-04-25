import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from healthid.apps.events.models import Event
from healthid.apps.events.models import EventType as EventTypeModel
from healthid.apps.outlets.models import Outlet
from healthid.utils.app_utils.database import (SaveContextManager,
                                               get_model_object)
from healthid.utils.auth_utils.decorator import master_admin_required
from healthid.utils.events_utils.validate_role import ValidateAdmin


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class EventsTypeType(DjangoObjectType):
    class Meta:
        model = EventTypeModel


class CreateEvent(graphene.Mutation):
    """Mutation creates an event on a calendar.
    """
    event = graphene.Field(EventType)
    success = graphene.List(graphene.String)
    error = graphene.List(graphene.String)

    class Arguments:
        event_type_id = graphene.String(required=True)
        start = graphene.Date(required=True)
        end = graphene.Date(required=True)
        event_title = graphene.String(required=True)
        description = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        msg = "Sorry, calendar is only used by outlet staff!"

        outlet = get_model_object(Outlet, 'user', user, message=msg)
        event_type = kwargs.get('event_type')
        event_type_id = kwargs.get('event_type_id')
        event_type = get_model_object(EventTypeModel, 'id', event_type_id)
        ValidateAdmin().validate_master_admin(user, event_type.name)
        event = Event(
            event_type_id=kwargs.get('event_type_id'),
            start=kwargs.get('start'),
            end=kwargs.get('end'),
            event_title=kwargs.get('event_title'),
            description=kwargs.get('description')
        )
        with SaveContextManager(event) as event:
            event.user.add(user)
            event.outlet.add(outlet)
            event.save()
            success = ["Event created successfully!"]
            return CreateEvent(event=event, success=success)


class UpdateEvent(graphene.Mutation):
    """Mutation updates an event on a calendar.
    """
    event = graphene.Field(EventType)
    success = graphene.List(graphene.String)
    error = graphene.List(graphene.String)

    class Arguments:
        id = graphene.String(required=True)
        event_type_id = graphene.String(required=True)
        start = graphene.Date(required=True)
        end = graphene.Date(required=True)
        event_title = graphene.String(required=True)
        description = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        request_user = info.context.user
        _id = kwargs['id']
        event = get_model_object(Event, 'id', _id)
        event_creator = event.user.first()
        if str(request_user.email) != str(event_creator.email):
            raise GraphQLError("Can't update events that don't belong to you!")
        new_event = kwargs.items()

        for key, value in new_event:
            if key is not None:
                setattr(event, key, value)
        event.save()
        success = ["Event updated successfully!"]
        return UpdateEvent(event=event, success=success)


class DeleteEvent(graphene.Mutation):
    """Deletes an event
    """
    event = graphene.Field(EventType)
    success = graphene.List(graphene.String)
    error = graphene.List(graphene.String)

    class Arguments:
        id = graphene.String()

    @login_required
    def mutate(self, info, id):
        request_user = info.context.user
        event = get_model_object(Event, 'id', id)
        event_creator = event.user.first()
        if request_user != event_creator:
            raise GraphQLError(
                "You can't delete events that don't belong to you!"
            )
        event.delete()
        success = ["Event deleted successfully!"]
        return DeleteEvent(success=success)


class CreateEventType(graphene.Mutation):
    '''Mutation to create an event type
    '''
    event_type = graphene.Field(EventsTypeType)
    success = graphene.List(graphene.String)
    error = graphene.List(graphene.String)

    class Arguments:
        name = graphene.String(required=True)

    @login_required
    @master_admin_required
    def mutate(self, info, name):
        params = {'model_name': 'EventType', 'value': name}
        event_type = EventTypeModel(name=name)
        with SaveContextManager(event_type, **params) as event_type:
            success = ['Event Type created successfully!']
            return CreateEventType(
                success=success, event_type=event_type
            )


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    delete_event = DeleteEvent.Field()
    update_event = UpdateEvent.Field()
    create_event_type = CreateEventType.Field()
