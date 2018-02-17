from django import forms
from .models import Recipe, Unit, Category, RecipeIngredient, Ingredient, ShoppingList, CalendarEntry

class RecipeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    recipe_url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    preparation_time = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    preparation_time_units = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    cooking_time = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    cooking_time_units = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    directions = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    recipe_photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}))

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
    calendar_entries = forms.ModelMultipleChoiceField(queryset=CalendarEntry.objects.all(), widget=forms.SelectMultiple(attrs={'class':'form-control', 'size':'14'}))
    class Meta:
        model = ShoppingList
        fields = '__all__'
