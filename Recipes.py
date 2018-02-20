from django import forms
from .models import Recipe, Unit, Category, RecipeIngredient, Ingredient, ShoppingList, CalendarEntry, GoogleCalendar
from django.contrib.auth.models import User

class RecipeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    recipe_url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    preparation_time = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    preparation_time_units = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    cooking_time = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    cooking_time_units = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    directions = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    recipe_photo = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control file'}))

    class Meta:
        model = Recipe
        fields = '__all__'

class RecipeIngredientForm(forms.ModelForm):
    amount = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    recipe = forms.ModelChoiceField(queryset=Recipe.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = RecipeIngredient
        fields = '__all__'

class ShoppingListForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    calendar_entries = forms.ModelMultipleChoiceField(queryset=CalendarEntry.objects.all(), widget=forms.SelectMultiple(attrs={'class':'form-control', 'height':'150px'}))
    class Meta:
        model = ShoppingList
        fields = '__all__'

class IngredientForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    generic_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    barcode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    estimated_cost = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    quantity_on_hand = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Ingredient
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    category_type = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Category
        fields = '__all__'

class UnitForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Unit
        fields = '__all__'

class CalendarEntryForm(forms.ModelForm):
    date_planned = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    recipes = forms.ModelMultipleChoiceField(queryset=Recipe.objects.all(), widget=forms.SelectMultiple(attrs={'class':'form-control'}))

    class Meta:
        model = CalendarEntry
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(CalendarEntryForm, self).__init__(*args, **kwargs)
        self.user = user
        google_calendar = forms.ModelChoiceField(queryset=GoogleCalendar.objects.filter(user__exact=self.user._meta.get_field('id')).all(), widget=forms.Select(attrs={'class':'form-control'}))
