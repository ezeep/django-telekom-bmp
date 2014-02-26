from xml.dom import minidom

from django.db import models

from django_extensions.db.fields import CreationDateTimeField

from flufl.enum import Enum


class EventTypes(Enum):
    UNKNOWN = 0
    SUBSCRIPTION_ORDER = 1
    SUBSCRIPTION_CANCEL = 2
    SUBSCRIPTION_CHANGE = 3
    SUBSCRIPTION_NOTICE = 4
    USER_ASSIGNMENT = 5
    USER_UNASSIGNMENT = 6


class Event(models.Model):
    SUBSCRIPTION = 'subscription'
    ACCESS_MANAGEMENT = 'access_management'

    EVENTS = [(int(e), e.name) for e in EventTypes]

    created = CreationDateTimeField(null=False)
    status = models.IntegerField(default=0)
    raw = models.TextField(null=True, blank=True)
    type = models.IntegerField(max_length=255, choices=EVENTS, default=0)

    @property
    def pretty_xml(self):
        xml = minidom.parseString(self.raw)
        return xml.toprettyxml()

    def __unicode__(self):
        return 'Event: %s' % EventTypes(self.type).name
