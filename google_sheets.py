
from .models import Ingredient, Category, Recipe
import pygsheets
import datetime

class BackupSheet():

    def backupDatabase(request):
        print("backup in progress...")
        gc = pygsheets.authorize()
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
