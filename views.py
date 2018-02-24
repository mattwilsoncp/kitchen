from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Category, Ingredient, Recipe, CalendarEntry, ShoppingList, GoogleCalendar, RecipeIngredient, Unit, Store
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage

from .Recipes import RecipeForm, RecipeIngredientForm, ShoppingListForm, IngredientForm, CategoryForm, UnitForm, CalendarEntryForm, StoreForm, ScanForm, IngredientScanForm, IngredientPickerForm

import httplib2
import pdb
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

from .google_sheets import BackupSheet

def logout(request):
    return redirect('/login')


def connect_helper(user):
    c = user.social_auth.get(provider='google-oauth2')
    access_token = c.tokens
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build(serviceName='calendar', version='v3', http=http)

    #Build list of calendars
    [google_calendar.delete() for google_calendar in GoogleCalendar.objects.filter(user__exact=user).all()]
    calendar_list = service.calendarList().list().execute()
    for calendar_list_entry in calendar_list['items']:
      google_calendar = GoogleCalendar(user=request.user, calendar_name=calendar_list_entry['summary'], calendar_id=calendar_list_entry['id'])
      google_calendar.save()

    return service

def category_index(request):
    categories = Category.objects.order_by('name')
    template = loader.get_template('kitchen/category_index.html')
    context = { 'categories' : categories }
    return HttpResponse(template.render(context, request))

class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'kitchen/form_template.html'

class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'kitchen/form_template.html'

def store_index(request):
    stores = Store.objects.order_by('name')
    template = loader.get_template('kitchen/store_index.html')
    context = { 'stores' : stores }
    return HttpResponse(template.render(context, request))

class StoreCreate(CreateView):
    model = Store
    form_class = StoreForm
    template_name = 'kitchen/form_template.html'

class StoreUpdate(UpdateView):
    model = Store
    form_class = StoreForm
    template_name = 'kitchen/form_template.html'


def ingredients_index(request):
    ingredients = Ingredient.objects.order_by('name')
    template = loader.get_template('kitchen/ingredients_index.html')
    context = { 'ingredients' : ingredients }
    return HttpResponse(template.render(context, request))

class IngredientAdd(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'kitchen/form_template.html'

class IngredientUpdate(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'kitchen/form_template.html'

class IngredientDelete(DeleteView):
    model = Ingredient
    success_url = reverse_lazy('kitchen:ingredients-index')
    template_name = 'kitchen/confirm_delete.html'

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
    form_class = RecipeForm
    template_name = 'kitchen/edit_recipe.html'

class RecipeUpdate(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'kitchen/edit_recipe.html'

class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('kitchen:recipes-index')
    template_name = 'kitchen/confirm_delete.html'

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
    template_name = 'kitchen/confirm_delete.html'

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

    google_calendars = GoogleCalendar.objects.filter(user__exact=user).order_by('id')
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
    form_class = CalendarEntryForm
    template_name = "kitchen/form_template.html"
    user = None
    title = None

    def get_form_kwargs(self):
        kwargs = super(CalendarEntryAdd, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['title'] = 'Edit Calendar'
        return kwargs

class CalendarEntryUpdate(UpdateView):
    model = CalendarEntry
    form_class = CalendarEntryForm
    template_name = "kitchen/form_template.html"
    user = None
    title = None

    def get_form_kwargs(self):
        kwargs = super(CalendarEntryUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['title'] = 'Edit Calendar'
        return kwargs

class CalendarEntryDelete(DeleteView):
    model = CalendarEntry
    success_url = reverse_lazy('kitchen:calendarEntry-index')
    template_name = 'kitchen/confirm_delete.html'


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
    template_name = 'kitchen/form_template.html'

class UnitUpdate(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'kitchen/form_template.html'

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

def exportShoppingList(request, id):
    b = BackupSheet()
    user = request.user
    b.exportShoppingList(user, id)
    return redirect('kitchen:recipes-index')

def maintenance(request):
    template = loader.get_template('kitchen/maintenance.html')
    context = {}
    return HttpResponse(template.render(context, request))

def scan_in(request):
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data['scan_item']
            if Ingredient.objects.filter(barcode__exact=barcode).count() > 0:
                return redirect('kitchen:scan-in2', barcode=barcode)
            else:
                #Create form here that displays list of ingredients to choose where barcode came from
                template = loader.get_template('kitchen/scan-in3.html')
                form = IngredientPickerForm()
                return render(request, 'kitchen/scan-in3.html', {'form':form, 'barcode': barcode})
    else:
        form = ScanForm()
    return render(request, 'kitchen/scan-in1.html', {'form':form})

def scan_in2(request, barcode):
    if request.method == 'POST':
        form = IngredientScanForm(request.POST)
        if form.is_valid():
            ingredient = Ingredient.objects.filter(barcode__exact=form.cleaned_data['barcode']).first()
            ingredient.name = form.cleaned_data['name']
            ingredient.estimated_cost = form.cleaned_data['estimated_cost']
            ingredient.quantity_on_hand = form.cleaned_data['quantity_on_hand']
            ingredient.store = form.cleaned_data['store']
            ingredient.save()
    else:
        template = loader.get_template('kitchen/scan-in2.html')
        print(barcode)
        ingredient = Ingredient.objects.filter(barcode__exact=barcode).first()
        print(ingredient)
        form = IngredientScanForm()
        return render(request, 'kitchen/scan-in2.html', {'form':form, 'ingredient':ingredient})
    return redirect('kitchen:scan-in')

def scan_in3(request):
    form = IngredientPickerForm(request.POST)
    if form.is_valid():
        ingredient = Ingredient.objects.get(pk=form.cleaned_data['ingredient'].id)
        ingredient.barcode = form.cleaned_data['barcode']
        ingredient.save()
    return redirect('kitchen:scan-in2', barcode=ingredient.barcode)
