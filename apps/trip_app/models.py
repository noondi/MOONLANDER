from __future__ import unicode_literals
from django.db import models
from ..user_app.models import User
# from django.utils import timezone
import datetime

def check_dates(now, travel_from, travel_to):
    now_time = []
    for val in now:
        if val == '-':
            continue
        if val == ' ':
            break
        now_time.append(val)
    travel_from_time = []
    for val in travel_from:
        if val == '-':
            continue
        travel_from_time.append(val)
    travel_to_time = []
    for val in travel_to:
        if val == '-':
            continue
        travel_to_time.append(val)
    now_string = ''.join(now_time)
    from_string = ''.join(travel_from_time)
    to_string = ''.join(travel_to_time)
    if int(from_string) > int(now_string):
        return [from_string, to_string]
    else:
        return False

# Create your models here.
class TripManager(models.Manager):
    def create_trip(self, data):
        errors = {}
        if not data['destination'] or not data['description']:
            errors['field'] = ['No empty fields']

        result = check_dates(datetime.datetime.now().strftime('%Y-%m-%d'), data['travel_from'], data['travel_to'])        
        if result == False:
            errors['from_date'] = 'Your travel-from date  must be in the future and not in the past'
        else:
            if int(result[1]) < int(result[0]):
                errors['to_date'] = 'Your travel-to date  must be after your travel-from date'
        if len(errors):
            return errors
        else:
            return self.create(destination=data['destination'], description=data['description'],
                        travel_from=data['travel_from'], travel_to=data['travel_to']) 
class TravelManager(models.Manager):
    def create_travel(self, data, user):
        entry = Trip.objects.create_trip(data)
        if type(entry) is dict:
            return Trip.objects.create_trip(data)
        else:
            if self.filter(trip=entry, user=user):
                return False
            else:
                return self.create(trip=entry, user=user)

    def add_user(self, trip_id, user):
        trip = Trip.objects.get(id=trip_id)
        if self.filter(trip=trip, user=user):
            return False
        else:
            return self.create(trip=trip, user=user)
class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    travel_from= models.DateTimeField(default=datetime.datetime.now())
    travel_to= models.DateTimeField(default=datetime.datetime.now())
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = TripManager()
    def __repr__(self):
       return "<Trip object: {} {}>".format(self.destination, self.description, self.travel_from, self.travel_to)
    def user_trip(self):
        users = []
        travels = Travel.objects.filter(trip=self)
        for travel in travels:
            users.append(travel.user)
        return users
class Travel(models.Model):
    trip = models.ForeignKey(Trip, related_name='travel_trips')
    user = models.ForeignKey(User, related_name='travel_users')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = TravelManager()
    def __repr__(self):
       return "<Travel object: {} {}>".format(self.trip, self.user)
   

