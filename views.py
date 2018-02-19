from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Category, Ingredient, Recipe, CalendarEntry, ShoppingList, GoogleCalendar, RecipeIngredient, Unit
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage

from .Recipes import RecipeForm, RecipeIngredientForm, ShoppingListForm, IngredientForm, CategoryForm, UnitForm

import httplib2
import pdb
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

from .google_sheets import BackupSheet

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
    form_class = CategoryForm
    template_name = 'kitchen/category_form.html'
    
class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'kitchen/category_form.html'

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
    form_class = IngredientForm
    template_name = 'kitchen/ingredient_form.html'


class IngredientDelete(DeleteView):
    model = Ingredient
    success_url = reverse_lazy('kitchen:ingredients-index')


def recipes_index(request):
    recipes = Recipe.objects.order_by('name')
    template = loader.get_template('kitchen/recipes_index.html')
    context = { 'recipes' : recipes }
    return HttpResponse(template.render(context, request))

def recipe_review(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe.id)
    template = loader.get_template('kitchen/recipe_review.html')
    context = { 'recipe' : recipe, 'ingredients' : ingredients }
    return HttpResponse(template.render(context, request))

class RecipeAdd(CreateView):
    model = Recipe
    fields = ['name','description','preparation_time','preparation_time_units','cooking_time','cooking_time_units','category','directions','recipe_url']

class RecipeUpdate(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'kitchen/edit_recipe.html'

class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('kitchen:recipes-index')

def add_recipe_ingredient(request, recipe_id):
    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/kitchen/recipe/" + str(recipe_id) + "/review")
    else:
        recipe = Recipe.objects.get(pk=recipe_id)
        form = RecipeIngredientForm(initial={'recipe':recipe}, instance=RecipeIngredient)
    return render(request,'kitchen/add_recipe_ingredient.html',{'form':form,'recipe':recipe})

def edit_recipe_ingredient(request, id):
    if request.method == 'POST':
        ri = RecipeIngredient.objects.get(pk=id)
        form = RecipeIngredientForm(request.POST, instance=ri)
        if form.is_valid():
            form.save()
            return redirect("/kitchen/recipe/" + str(ri.recipe_id) + "/review")
    else:
        ri = RecipeIngredient.objects.get(pk=id)
        form = RecipeIngredientForm(instance=ri)
    return render(request,'kitchen/add_recipe_ingredient.html',{'form':form,'recipe':ri.recipe})

class RecipeIngredientDelete(DeleteView):
    model = RecipeIngredient
    success_url = reverse_lazy('kitchen:recipes-index')

class RecipeIngredientCreate(CreateView):
    model = RecipeIngredient
    form_class = RecipeIngredientForm

    def get_form_kwargs(self):
        kwargs = super(RecipeIngredientCreate, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs

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

class CalendarEntryDelete(DeleteView):
    model = CalendarEntry
    success_url = reverse_lazy('kitchen:calendarEntry-index')


def shopping_list_index(request):
    shopping_lists = ShoppingList.objects.order_by('name')
    template = loader.get_template('kitchen/shopping_list_index.html')
    context = { 'shopping_lists' : shopping_lists }
    return HttpResponse(template.render(context, request))

def shopping_list_print(request, id):
    shopping_list = ShoppingList.objects.get(pk=id)
    ingredients = []
    for ce in shopping_list.calendar_entries.all():
      for recipe in ce.recipes.all():
          for ringredient in RecipeIngredient.objects.filter(recipe_id=recipe.id):
            ingredients.append(ringredient.ingredient.name)
    template = loader.get_template('kitchen/shopping_list_print.html')
    context = { 'shopping_list' : shopping_list, 'ingredients':ingredients }
    return HttpResponse(template.render(context, request))


class ShoppingListAdd(CreateView):
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'kitchen/shopping_list.html'

class ShoppingListUpdate(UpdateView):
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'kitchen/shopping_list.html'

def home(request):
    return redirect('kitchen:recipes-index')

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })

def backupDatabase(request):
    b = BackupSheet()
    user = request.user
    b.backupDatabase(user)
    return redirect('home')

def syncToSheets(request):
    b = BackupSheet()
    user = request.user
    b.syncToSheets(user)
    return redirect('home')



class UnitCreate(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'kitchen/unit_form.html'

class UnitUpdate(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'kitchen/unit_form.html'

def unit_index(request):
    units = Unit.objects.order_by('name')
    template = loader.get_template('kitchen/unit_index.html')
    context = { 'units' : units }
    return HttpResponse(template.render(context, request))



def uploadRecipe(request):
    b = BackupSheet()
    user = request.user
    b.UploadRecipe(user)
    return redirect('kitchen:recipes-index')

def maintenance(request):
    template = loader.get_template('kitchen/maintenance.html')
    context = {}
    return HttpResponse(template.render(context, request))
