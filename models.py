from django.db import models
from django.urls import reverse

import httplib2
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

import gspread
import pdb

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#### OAuth2 Functions #####################################################################

def connect_helper(user):
    c = user.social_auth.get(provider='google-oauth2')
    access_token = c.tokens
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build(serviceName='calendar', version='v3', http=http)
    return service

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


class Unit(models.Model):
    name = models.TextField(max_length=20, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kitchen:recipes-index')

class RecipeIngredient(models.Model):
    amount = models.TextField(max_length=50, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount) + " " + self.unit.name + ":  " + self.ingredient.name

    def get_absolute_url(self):
        return reverse('kitchen:recipes-index')

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    #leftover_worthy = models.BooleanField
    preparation_time = models.IntegerField(default=1)
    preparation_time_units = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="preparation_time_unit")
    cooking_time = models.IntegerField(default=1)
    cooking_time_units = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="cooking_time_unit")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(RecipeIngredient)
    directions = models.TextField(default="")
    recipe_photo = models.FileField(upload_to='recipe_photos/', default="")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kitchen:recipe-update', kwargs={'pk': self.pk})


#### Google Calendar Functions ######################################################

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

#### Shopping Lists #############################################

class ShoppingList(models.Model):
    date_planned = models.DateField(auto_now=False, auto_now_add=False, editable=True)
    ingredients = models.ManyToManyField(Ingredient)

    def get_absolute_url(self):
        return reverse('kitchen:shoppingList-update', kwargs={'pk': self.pk})

#### User Profile ################################################

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.TextField(max_length=500, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
