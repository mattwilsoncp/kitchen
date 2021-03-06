
from django.urls import path
from . import views
from kitchen.views import CategoryUpdate, CategoryCreate, IngredientUpdate, IngredientAdd, IngredientDelete, RecipeAdd, RecipeUpdate, RecipeDelete, CalendarEntryAdd, CalendarEntryUpdate, CalendarEntryDelete, ShoppingListAdd, ShoppingListUpdate, backupDatabase, RecipeIngredientCreate, UnitCreate, RecipeIngredientDelete, UnitUpdate, StoreCreate, StoreUpdate

app_name = 'kitchen'
urlpatterns = [
    path('categories/', views.category_index, name='category-index'),
    path('category/<int:pk>/', CategoryUpdate.as_view(), name='category-update'),
    path('category/add/', CategoryCreate.as_view(), name='category-create' ),

    path('stores/', views.store_index, name='store-index'),
    path('stores/add/', StoreCreate.as_view(), name='store-add' ),
    path('stores/<int:pk>/', StoreUpdate.as_view(), name='store-update'),

    path('ingredients/', views.ingredients_index, name='ingredients-index'),
    path('ingredients/add/', IngredientAdd.as_view(), name='ingredient-add' ),
    path('ingredient/<int:pk>/', IngredientUpdate.as_view(), name='ingredient-update'),
    path('ingredient/<int:pk>/delete/', IngredientDelete.as_view(), name='ingredient-delete'),

    path('recipes/', views.recipes_index, name='recipes-index'),
    path('recipe/add/', RecipeAdd.as_view(), name='recipe-add' ),
    path('recipe/<int:pk>/', RecipeUpdate.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete', RecipeDelete.as_view(), name='recipe-delete'),
    path('recipe/<int:recipe_id>/review', views.recipe_review, name='recipe-review'),
    path('recipe_ingredient/add/<int:recipe_id>', views.add_recipe_ingredient, name='recipe-ingredient-add' ),
    path('recipe_ingredient/edit/<int:id>', views.edit_recipe_ingredient, name='recipe-ingredient-edit' ),
    path('recipe_ingredient/delete/<int:pk>', RecipeIngredientDelete.as_view(), name='recipe-ingredient-delete'),

    path('google_calendars/', views.google_calendar_index, name='google_calendar_index'),
    path('calendar_entries/', views.calendar_entry_index, name='calendarEntry-index'),
    path('calendar_entry/add/', CalendarEntryAdd.as_view(), name='calendarEntry-add' ),
    path('calendar_entry/<int:pk>/', CalendarEntryUpdate.as_view(), name='calendarEntry-update'),
    path('calendar_entry/<int:calendar_entry_id>/gs/', views.calendar_entry_gs, name='calendarEntry-gs'),
    path('calendar_entry/<int:recipe_id>/delete/', CalendarEntryDelete.as_view(), name='calendarEntry-delete'),

    path('shopping_lists/', views.shopping_list_index, name='shoppingList-index'),
    path('shopping_list/add/', ShoppingListAdd.as_view(), name='shoppingList-add' ),
    path('shopping_list/<int:pk>/', ShoppingListUpdate.as_view(), name='shoppingList-update'),
    path('shopping_list/<int:id>/print', views.exportShoppingList, name='shoppingList-print'),

    path('backupDatabase/', views.backupDatabase, name='backupDatabase'),
    path('syncToSheets/', views.syncToSheets, name="syncToSheets"),
    path('uploadRecipe/', views.uploadRecipe, name="uploadRecipe"),

    path('units/', views.unit_index, name='unit-index' ),
    path('unit/add/', UnitCreate.as_view(), name='unit-add' ),
    path('unit/edit/<int:pk>', UnitUpdate.as_view(), name='unit-update' ),

    path('maintenance/', views.maintenance, name='maintenance' ),
    path('scan-in/', views.scan_in, name='scan-in'),
    path('scan-in2/<str:barcode>/', views.scan_in2, name='scan-in2'),
    path('scan-in3/', views.scan_in3, name='scan-in3'),

]
