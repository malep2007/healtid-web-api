import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from healthid.apps.outlets.models import Outlet

# from dateutil import rrule
# from schedule.utils import EventListManager


class CalendarManager(models.Manager):
    """
    >>> outlet = Outlet.objects.create_outlet(*kwargs)
    >>> outlet.save()
    """

    def get_calendar_for_object(self, obj, distinction=None):
        """
        This function gets a calendar for an object.  It should only return one
        calendar.

        >>> outlet = Outlet.objects.get(*kwargs)
        >>> try:
        ...     Calendar.objects.get_calendar_for_object(outlet)
        ... except Outlet.DoesNotExist:
        ...     print "failed"
        ...
        failed

        Now if we add a calendar it should return the calendar

        >>> calendar = Calendar(name='Outlet Cal')
        >>> calendar.save()
        >>> calendar.create_relation(outlet)
        >>> Calendar.objects.get_calendar_for_object(outlet)
        <Calendar: Outlet Cal'>
        """

        calendar_list = self.get_calendars_for_object(obj, distinction)
        if len(calendar_list) == 0:
            raise Calendar.DoesNotExist("Calendar does not exist.")
        elif len(calendar_list) > 1:
            raise Exception("More than one calendars were found.")

        return calendar_list[0]

    def get_or_create_calendar_for_object(self, obj,
                                          distinction=None, name=None):

        try:
            return self.get_calendar_for_object(obj, distinction)
        except Calendar.DoesNotExist:
            if name is None:
                calendar = Calendar(name=str(obj))
            else:
                calendar = Calendar(name=name)
            calendar.save()
            calendar.create_relation(obj, distinction)
            return calendar

    def get_calendars_for_object(self, obj, distinction=None):

        ct = ContentType.objects.get_for_model(type(obj))
        if distinction:
            dist_q = Q(calendarrelation__distinction=distinction)
        else:
            dist_q = Q()
        return self.filter(
            dist_q, Q(calendarrelation__object_id=obj.id,
                      calendarrelation__content_type=ct)
        )


class Calendar(models.Model):

    name = models.CharField(_("name"), max_length=200)
    objects = CalendarManager()

    class Meta:
        verbose_name = _('calendar')
        verbose_name_plural = _('calendar')
        app_label = 'calendar'

    def __str__(self):
        return self.name

    def events(self):
        return self.event_set.all()
    events = property(events)

    def create_relation(self, obj, distinction=None, inheritable=True):

        CalendarRelation.objects.create_relation(
            self, obj, distinction, inheritable)

    def get_recent(self, amount=5, in_datetime=datetime.datetime.now):

        return self.events.order_by('-start').filter(start__lt=datetime.datetime.now())[:amount]

    # def occurrences_after(self, date=None):
    #     return EventListManager(self.events.all()).occurrences_after(date)


class CalendarRelationManager(models.Manager):
    def create_relation(self, calendar, content_object,
                        distinction=None, inheritable=True):

        ct = ContentType.objects.get_for_model(type(content_object))
        object_id = content_object.id
        cr = CalendarRelation(
            content_type=ct,
            object_id=object_id,
            calendar=calendar,
            distinction=distinction,
            content_object=content_object
        )
        cr.save()
        return cr


class CalendarRelation(models.Model):

    calendar = models.ForeignKey(
        Calendar, verbose_name=_("calendar"), on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    distinction = models.CharField(_("distinction"), max_length=20, null=True)
    inheritable = models.BooleanField(_("inheritable"), default=True)

    objects = CalendarRelationManager()

    class Meta:
        verbose_name = _('calendar relation')
        verbose_name_plural = _('calendar relations')
        app_label = 'schedule'

    def __str__(self):
        return '{} - {}'.format(self.calendar, self.content_object)
