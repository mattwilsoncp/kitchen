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

class Store(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
      return reverse('kitchen:store-index')

    def __str__(self):
      return self.name




class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    estimated_cost = models.FloatField(default=1.00)
    quantity_on_hand = models.IntegerField(default=1)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)

    def __str__(self):
      return self.name

    def get_absolute_url(self):
        return reverse('kitchen:ingredients-index')

    class Meta:
        ordering = ["name"]

class StoreReceipt(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=1)
    receipt_total = models.FloatField(default=1.00)
    receipt_identifier = models.CharField(max_length=100)

    def __str__(self):
      return self.receipt_identifier

class StoreReceiptDetails(models.Model):
    store_receipt = models.ForeignKey(StoreReceipt, on_delete=models.CASCADE, default=1)
    item_description = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=1.00)



class Unit(models.Model):
    name = models.TextField(max_length=20, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kitchen:recipes-index')

    class Meta:
        ordering = ["name"]

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    #leftover_worthy = models.BooleanField
    preparation_time = models.IntegerField(default=1)
    preparation_time_units = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="preparation_time_unit")
    cooking_time = models.IntegerField(default=1)
    cooking_time_units = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="cooking_time_unit")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #ingredients = models.ManyToManyField(RecipeIngredient)
    directions = models.TextField(default="")
    recipe_photo = models.FileField(upload_to='recipe_photos/', blank=True)
    recipe_url = models.TextField(blank=True, max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kitchen:recipe-update', kwargs={'pk': self.pk})

    class Meta:
        ordering = ["name"]

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount) + " " + self.unit.name + ":  " + self.ingredient.name

    def get_absolute_url(self):
        return reverse('kitchen:recipes-index')


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

    class Meta:
        ordering = ["-date_planned"]

    def __str__(self):
        return str(self.date_planned)

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
    name = models.CharField(max_length=200)
    calendar_entries = models.ManyToManyField(CalendarEntry)

    def get_absolute_url(self):
        return reverse('kitchen:shoppingList-update', kwargs={'pk': self.pk})

#### User Profile ################################################

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.TextField(max_length=500, blank=True)
    site_permission = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
