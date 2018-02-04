from django.db import models
from django.urls import reverse

import httplib2
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

import bson
import json

def connect_helper(user):
    c = user.social_auth.get(provider='google-oauth2')
    access_token = c.tokens
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build(serviceName='calendar', version='v3', http=http)
    return service

# Create your models here.
class Category(models.Model):
    category_type = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
      return self.name

    def get_absolute_url(self):
        return reverse('kitchen:category-index')

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    estimated_cost = models.FloatField(default=1.00)
    quantity_on_hand = models.IntegerField(default=1)

    def __str__(self):
      return self.name

    def get_absolute_url(self):
        return reverse('kitchen:ingredients-index')

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    #leftover_worthy = models.BooleanField
    preparation_time = models.IntegerField(default=1)
    preparation_time_units = models.CharField(max_length=10)
    cooking_time = models.IntegerField(default=1)
    cooking_time_units = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    directions = models.TextField(default="")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kitchen:recipe-update', kwargs={'pk': self.pk})


class GoogleCalendar(models.Model):
    user = models.CharField(max_length=200)
    calendar_name = models.CharField(max_length=200)
    calendar_id   = models.CharField(max_length=200)

    def __str__(self):
        return self.calendar_name

    
class CalendarEntry(models.Model):
    date_planned = models.DateField(auto_now=False, auto_now_add=False, editable=True)
    recipes = models.ManyToManyField(Recipe)
    google_calendar = models.ForeignKey(GoogleCalendar, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('kitchen:calendarEntry-index')

    def set_calendar_date(request,self):
        user = request.user
        service = connect_helper(user)
        start_date = self.date_planned
        event = {
            'summary': self.recipes.all()[0].name,
            'start': {
                'date': start_date.strftime("%Y-%m-%d"),
                'timeZone': 'America/New_York',
            },
            'end': {
                'date': start_date.strftime("%Y-%m-%d"),
                'timeZone': 'America/New_York',
            },
        }
        event = service.events().insert(calendarId=self.google_calendar.calendar_id, body=event).execute()

class ShoppingList(models.Model):
    date_planned = models.DateField(auto_now=False, auto_now_add=False, editable=True)
    ingredients = models.ManyToManyField(Ingredient)

    def get_absolute_url(self):
        return reverse('kitchen:shoppingList-update', kwargs={'pk': self.pk})
