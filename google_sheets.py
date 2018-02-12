
from .models import Ingredient, Category, Recipe, RecipeIngredient, Unit
import pygsheets
import datetime

import httplib2
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

class BackupSheet():

    def backupDatabase(self, user):
        print("backup in progress...")

        c = user.social_auth.get(provider='google-oauth2')
        access_token = c.tokens
        credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')

        gc = pygsheets.authorize(credentials=credentials)
        sh = gc.create("SmartKitchenBackup-" + datetime.datetime.today().strftime('%Y-%m-%d-%H%M'))

        ### Ingredients
        sh.add_worksheet("Ingredients")
        wks = sh.worksheet_by_title("Ingredients")

        ingredients = Ingredient.objects.order_by("name")
        wks.update_cell('A1','Ingredient Name')
        wks.update_cell('B1','ID')
        a = []
        b = []
        for i in range(0, ingredients.count()):
          a.append([ingredients[i].name])
          b.append([ingredients[i].id])
        wks.update_cells("A2:A", a)
        wks.update_cells("B2:B", b)


        ### Categories
        sh.add_worksheet("Categories")
        wks = sh.worksheet_by_title("Categories")
        categories = Category.objects.order_by("name")
        wks.update_cell("A1",'Category Name')
        wks.update_cell("B1",'Category Type')
        wks.update_cell("C1",'ID')
        c1 = []
        c2 = []
        c3 = []
        for i in range(0, categories.count()):
            c1.append([categories[i].name])
            c2.append([categories[i].category_type])
            c3.append([categories[i].id])

        cellrange = "A2"
        wks.update_cells(cellrange,c1)
        cellrange = "B2"
        wks.update_cells(cellrange,c2)
        cellrange = "C2"
        wks.update_cells(cellrange,c3)


        ### Recipes
        sh.add_worksheet("Recipes")
        wks= sh.worksheet_by_title("Recipes")

        c1 = [['Name']]
        c2 = [['Description']]
        c3 = [['Prep Time']]
        c4 = [['Units']]
        c5 = [['Cook Time']]
        c6 = [['Units']]
        c7 = [['Category ID']]
        c8 = [['Directions']]
        c9 = [['Photo URL']]
        c10 = [['Recipe ID']]

        recipes = Recipe.objects.order_by("name")
        for i in range(0, recipes.count()):
            c1.append([recipes[i].name])
            c2.append([recipes[i].description])
            c3.append([recipes[i].preparation_time])
            c4.append([recipes[i].preparation_time_units])
            c5.append([recipes[i].cooking_time])
            c6.append([recipes[i].cooking_time_units])
            c7.append([recipes[i].category_id])
            c8.append([recipes[i].directions])
            c9.append([''])
            c10.append([recipes[i].id])

        cellrange = "A1:A"
        wks.update_cells(cellrange,c1)
        cellrange = "B1:B"
        wks.update_cells(cellrange,c2)
        cellrange = "C1:C"
        wks.update_cells(cellrange,c3)
        cellrange = "D1:D"
        wks.update_cells(cellrange,c4)
        cellrange = "E1:E"
        wks.update_cells(cellrange,c5)
        cellrange = "F1:F"
        wks.update_cells(cellrange,c6)
        cellrange = "G1:G"
        wks.update_cells(cellrange,c7)
        cellrange = "H1:H"
        wks.update_cells(cellrange,c8)
        cellrange = "I1:I"
        wks.update_cells(cellrange,c9)
        cellrange = "J1:J"
        wks.update_cells(cellrange,c10)

        ### Maintenance
        wks = sh.worksheet_by_title("Sheet1")
        sh.del_worksheet(wks)

    def syncToSheets(self, user):
        c = user.social_auth.get(provider='google-oauth2')
        access_token = c.tokens
        credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')

        gc = pygsheets.authorize(credentials=credentials)
        sh = gc.open("RestoreKitchen")

        ## Ingredients
        wks = sh.worksheet_by_title("Ingredients")
        rowcount = 1
        while True:
          row = wks.get_row(rowcount)
          if len(row[0]) == 0:
              break
          rowcount = rowcount + 1
          print(row[0])
          if rowcount > 2:
            if len(row) > 1:
              id = row[1]
              ingredient = Ingredient.objects.get(pk=id)
            else:
              ingredient = Ingredient()
            ingredient.name = row[0]
            ingredient.save()

        ## Recipes
        wks = sh.worksheet_by_title("Recipes")
        rowcount = 1
        while True:
          row = wks.get_row(rowcount)
          if len(row[0]) == 0:
              break
          rowcount = rowcount + 1
          print(row[0])
          if rowcount > 2:
            if len(row) > 8:
              id = row[9]
              recipe = Recipe.objects.get(pk=id)
            else:
              recipe = Recipe()
            recipe.name = row[0]
            recipe.description = row[1]
            recipe.preparation_time = row[2]
            recipe.preparation_time_units = row[3]
            recipe.cooking_time = row[4]
            recipe.cooking_time_units = row[5]
            recipe.category_id = row[6]
            recipe.directions = row[7]
            recipe.save()

    def UploadRecipe(self, user):
        c = user.social_auth.get(provider='google-oauth2')
        access_token = c.tokens
        credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')

        gc = pygsheets.authorize(credentials=credentials)
        sh = gc.open("SmartKitchen-RecipeUploader")

        wks = sh.worksheet_by_title("Recipes")

        row = wks.get_row(2)
        recipe = Recipe()
        recipe.name = row[0]
        recipe.description = row[1]
        recipe.preparation_time = row[2]
        recipe.preparation_time_units = Unit.objects.get(name=row[3])
        recipe.cooking_time = row[4]
        recipe.cooking_time_units = Unit.objects.get(name=row[5])
        recipe.category = Category.objects.get(name='Dinner')
        recipe.directions = row[6]
        recipe.save()

        rowcount = 7
        while True:
          row = wks.get_row(rowcount)
          print(row)
          if len(row[0]) == 0:
              break
          rowcount = rowcount + 1

          unit = Unit.objects.get(name=row[1])
          ingredient = Ingredient.objects.get(name=row[2])

          ri = RecipeIngredient()
          ri.recipe_id = recipe.id
          ri.ingredient_id = ingredient.id
          ri.unit_id = unit.id
          ri.amount = row[0]
          ri.save()

          recipe.ingredients.add(ri)
