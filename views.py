from django.shortcuts import render, redirect

from django.http import HttpResponse, Http404
from django.template import loader
from .models import Category, Ingredient, Recipe, CalendarEntry, ShoppingList, GoogleCalendar
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import httplib2
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

def connect_helper(user):
    c = user.social_auth.get(provider='google-oauth2')
    access_token = c.tokens
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build(serviceName='calendar', version='v3', http=http)
    return service

def category_index(request):
    categories = Category.objects.order_by('name')
    template = loader.get_template('kitchen/category_index.html')
    context = { 'categories' : categories }
    return HttpResponse(template.render(context, request))

class CategoryCreate(CreateView):
    model = Category
    fields = ['category_type','name']

class CategoryUpdate(UpdateView):
    model = Category
    fields = ['category_type','name']

def ingredients_index(request):
    ingredients = Ingredient.objects.order_by('name')
    template = loader.get_template('kitchen/ingredients_index.html')
    context = { 'ingredients' : ingredients }
    return HttpResponse(template.render(context, request))

class IngredientAdd(CreateView):
    model = Ingredient
    fields = ['name','generic_name','barcode','estimated_cost','quantity_on_hand']

class IngredientUpdate(UpdateView):
    model = Ingredient
    fields = ['name','generic_name','barcode','estimated_cost','quantity_on_hand']

def recipes_index(request):
    recipes = Recipe.objects.order_by('name')
    template = loader.get_template('kitchen/recipes_index.html')
    context = { 'recipes' : recipes }
    return HttpResponse(template.render(context, request))


class RecipeAdd(CreateView):
    model = Recipe
    fields = ['name','description','preparation_time','preparation_time_units','cooking_time','cooking_time_units','category']

class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['name','description','preparation_time','preparation_time_units','cooking_time','cooking_time_units','category','ingredients']


def google_calendar_index(request):
    user = request.user
    service = connect_helper(user)

    [google_calendar.delete() for google_calendar in GoogleCalendar.objects.filter(user__exact=user).all()]

    calendar_list = service.calendarList().list().execute()
    for calendar_list_entry in calendar_list['items']:
        google_calendar = GoogleCalendar(user=request.user, calendar_name=calendar_list_entry['summary'], calendar_id=calendar_list_entry['id'])
        google_calendar.save()
         
    google_calendars = GoogleCalendar.objects.order_by('id')
    template = loader.get_template('kitchen/google_calendar_index.html')
    context = { 'google_calendars' : google_calendars}
    return HttpResponse(template.render(context, request))

def calendar_entry_index(request):
    calendar_entries = CalendarEntry.objects.order_by('date_planned')
    template = loader.get_template('kitchen/calendar_entry_index.html')
    context = { 'calendar_entries' : calendar_entries}
    return HttpResponse(template.render(context, request))

def calendar_entry_gs(request, calendar_entry_id):
    CalendarEntry.set_calendar_date(request, CalendarEntry.objects.get(pk=calendar_entry_id))
    return redirect('kitchen:calendarEntry-index')

class CalendarEntryAdd(CreateView):
    model = CalendarEntry
    fields = ['date_planned', 'recipes', 'google_calendar']

class CalendarEntryUpdate(UpdateView):
    model = CalendarEntry
    fields = ['date_planned', 'recipes', 'google_calendar']



def shopping_list_index(request):
    return HttpResponse(template.render(context, request))

class ShoppingListAdd(CreateView):
    model = ShoppingList
    fields = ['date_planned', 'ingredients']

class ShoppingListUpdate(UpdateView):
    model = ShoppingList
    fields = ['date_planned', 'ingredients']



def home(request):
    return render(request, 'home.html')
