from __future__ import unicode_literals

import uuid
import datetime
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import Distance

# Create your models here.


# Datenfelder fuer Import CSV: Anrede (Herr, Frau, Keine Angabe), Vornamen (Textfeld),
# Nachname (Textfeld), E-Mail Adresse, PLZ (4-digit), Strasse, Hausnummer

#Land, PLZ, Ort, Strasse, Hausnummer, Tuernummer, Anrede, Vorname, Nachname,
# E-Mail Adresse, Produktbedarf (Paket mit 500 Flyern)
from rest_framework.exceptions import ValidationError

from anthill import geo
from anthill.models import *


class Activist(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    # Anrede (Herr, Frau, Keine Angabe)
    anrede = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=300, null=True, blank=True)
    last_name = models.CharField(max_length=300, null=True, blank=True)
    facebook_id = models.CharField(max_length=32, null=True, blank=True)
    facebook_bot_id = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    postalcode = models.IntegerField(null=True, blank=True)  # PLZ (4-digit)
    municipal = models.CharField(max_length=500, null=True, blank=True)  # Ort
    street = models.CharField(max_length=500, null=True, blank=True)
    house_number = models.CharField(max_length=100, null=True, blank=True)
    coordinate = models.PointField(null=True, blank=True)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = 'uuid'

    @classmethod
    def create(cls, email, postalcode):
        activist = cls(email=email, postalcode=postalcode)
        coordinate = geo.get_coordinates(activist.postalcode)
        activist.coordinate = GEOSGeometry('POINT(%f %f)' % (coordinate[1], coordinate[0]), srid=4326)
        return activist

    @property
    def is_authenticated(self):
        return True

    def clean(self):
        if self.postalcode is None and self.municipal is None:
            raise ValidationError(_('Either postalcode or municipal are required.'))

        if self.email is None and self.facebook_id is None and self.facebook_bot_id is None:
            raise ValidationError(_('Either email or facebook_id or facebook_bot_id are required.'))

        # if self.postalcode is not None:
        #   coordinate = geo.get_coordinates(self.postalcode)
        #    self.coordinate = GEOSGeometry('POINT(%f %f)' % (coordinate[1], coordinate[0]), srid=4326)

        # todo: email, facebook_id and facebook_bot_id need to be unique when set.

    def find_meetups_nearby(self):
        try:
            DISTANCE_LIMIT_METERS = 100000  # todo: check if this is really meters
            data = Meetup.objects.filter(coordinate__distance_lt=(self.coordinate, Distance(m=DISTANCE_LIMIT_METERS)))
            #data = Meetup.objects.filter(coordinate__distance_lt=(self.coordinate, Distance(m=DISTANCE_LIMIT_METERS)))\
            #    .annotate(distance=Distance('coordinate', self.coordinate))\
            #    .order_by('distance')
            return data
        except ValueError as e:
            return []

    def __str__(self):
        return '{} ({}) - {}'.format(self.email, self.postalcode, self.uuid)


class Meetup(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1000)
    datetime = models.DateTimeField()
    postalcode = models.IntegerField()  # PLZ (4-digit)
    municipal = models.CharField(max_length=500)  # Ort
    street = models.CharField(max_length=500)
    house_number = models.CharField(max_length=100)
    coordinate = models.PointField()
    activist = models.ManyToManyField(
        Activist, null=True, blank=True, related_name='meetups')

    @classmethod
    def create(cls, title, postalcode, municipal, street, house_number, coordinate=None):
        meetup = cls(title=title, postalcode=postalcode, municipal=municipal, street=street, house_number=house_number)
        if coordinate is None:
            coordinate = geo.get_coordinates(postalcode)
        meetup.coordinate = GEOSGeometry('POINT(%f %f)' % (coordinate[1], coordinate[0]), srid=4326)
        return meetup

    def __str__(self):
        return '{} - {}'.format(self.title, self.uuid)

    @staticmethod
    def find_meetups_near_activist(activist_uuid):
        activist = Activist.objects.filter(uuid=activist_uuid).first()
        return activist.find_meetups_nearby()

    @staticmethod
    def proposed_times():
        """returns an array of porposed datetimes that new events may be created at"""
        today = datetime.date.today()
        # find the next saturday that's at least 7 days away from today
        saturday = today + datetime.timedelta(days=(5-today.weekday()), weeks=1)
        # events on saturday start at 11:00
        saturday = datetime.datetime.combine(saturday, datetime.time(11, 00))
        # find the sunday after this saturday, using the same time as saturday
        sunday = saturday + datetime.timedelta(days=1)
        # find the next workday that's at least 5 days away from today
        workday = today + datetime.timedelta(days=5)
        # events on a workday start at 18:00
        workday = datetime.datetime.combine(workday, datetime.time(18, 00))
        if workday.weekday() == 5:
            workday = workday + datetime.timedelta(days=2)
        elif workday.weekday() == 6:
            workday = workday + datetime.timedelta(days=1)
        return map(lambda t: (t, t + datetime.timedelta(hours=2)), sorted([saturday, sunday, workday]))

class InterestingPlaces(models.Model):
    title = models.CharField(max_length=1000)
    postalcode = models.IntegerField()  # PLZ (4-digit)
    municipal = models.CharField(max_length=500)  # Ort
    coordinate = models.PointField()

    def __str__(self):
        return '{} {}: {}'.format(self.postalcode, self.municipal, self.title)
