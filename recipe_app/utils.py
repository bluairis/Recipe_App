from .models import Recipe, Ingredient, Direction

from django.http import Http404

""" USED IN VIEWS.INDEX """

## using a query string to sort the recipes
## by ABC, reverse ABC, pub_date, and
## reverse pub_date ... also confirms that
## the inputed query string is acceptable
## otherwise throws a 404

def sorting_by_query(query_string):
    
    try:
            sort_order = query_string["sort_order"]
            
    except KeyError:
        
        raise Http404("sort order not present")

    if sort_order not in ['-pub_date', 'pub_date', '-recipe_name', 'recipe_name']:
        raise Http404("entered sort order does not exist")
            
    latest_recipe_list = Recipe.objects.order_by(sort_order)

    return latest_recipe_list

## numbers all of the recipes so that
## the template can number each recipe
## in the table on the opening index page

def numbering_recipes(latest_recipe_list):
    
    recipe_num = 1
    my_tuple_list = []
        
    for recipe in latest_recipe_list:
        my_tuple = (recipe_num, recipe)
        my_tuple_list.append(my_tuple)
        recipe_num += 1

    return my_tuple_list


""" USED IN VIEWS.ADD_RECIPE and VIEWS.EDIT_RECIPE """

## takes in an ingredient list of strings
## separated by new lines and creates
## a list of ingredient names

def make_ingredient_list(newline_separated_str):
    if (len(newline_separated_str) == 0):
        return []

    myIngredientNameList = newline_separated_str.strip().split("\n")
    returnList = []

    for ingredient in myIngredientNameList:
        if ingredient.strip() not in returnList and ingredient.strip()!="":
            returnList.append(ingredient.strip())
        
    return returnList

## takes in an direction list of strings
## separated by new lines and creates
## a list of direction steps

def make_direction_list(newline_separated_str):
    if (len(newline_separated_str) == 0):
        return []

    myDirectionNameList = newline_separated_str.strip().split("\n")
    returnList = []

    for direction in myDirectionNameList:
        if direction.strip() not in returnList and direction.strip()!="":
            returnList.append(direction.strip())
        
    return returnList

## adding all of the
## ingredients and directions
## to a recipe

def ingredient_and_direction_add(query_string, recipe_id):

        #grabbing the recipe
        our_recipe = Recipe.objects.get(pk=recipe_id)
        
        #deleting all old ingredients
        for ingredient in our_recipe.ingredient_set.all():

            ingredient.delete()

        #deleting all old directions
        for direction in our_recipe.direction_set.all():
            
            direction.delete()

        #grabbing newly inputted data
        ingredient_list = query_string["ingredient_list"]

        direction_list = query_string["direction_list"]

        #adding new ingredients
        myIngredientNameList = make_ingredient_list(ingredient_list)
        for i in myIngredientNameList:
            ingredient = our_recipe.ingredient_set.create(ingredient_name = i)
            ingredient.save()

        #adding new directions
        myDirectionNameList = make_direction_list(direction_list)
        for i in myDirectionNameList:
            direction = our_recipe.direction_set.create(step = i)
            direction.save()

""" USED IN VIEWS.EDIT_RECIPE """

## gets recipe information
## including name, ingredients
## and directions from the database

def get_recipe_contents(recipe_id):
    
    our_recipe = Recipe.objects.get(pk=recipe_id)
    my_ingredient_string = ""
    
    for ingredient in our_recipe.ingredient_set.all():
        my_ingredient_string += ingredient.ingredient_name.strip() + "\n\n"

    my_direction_string = ""
    
    for direction in our_recipe.direction_set.all():
        my_direction_string += direction.step.strip() + "\n\n"

    context = {'recipe': our_recipe, 'ingredient_list': my_ingredient_string.strip(), 'direction_list': my_direction_string.strip()}

    return context
    
