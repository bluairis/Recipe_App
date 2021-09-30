from django.shortcuts import render
from django.http import Http404
from django.template import loader
from django.utils import timezone

# Create your views here.

from django.http import HttpResponse
from .models import Recipe, Ingredient, Direction
from . import utils

def index(request, *args, **kwargs):
    if kwargs:
        order = kwargs["sort_order"]
    else:
        order = '-pub_date'

    if order == 'add':
        template_path = "recipe_app/add_recipe.html"
        
    if order not in ['-pub_date', 'pub_date', '-recipe_name', 'recipe_name']:
        order = '-pub_date'
        
    latest_recipe_list = Recipe.objects.order_by(order)
    template = loader.get_template('recipe_app/index.html')
    context = {
        'latest_recipe_list': latest_recipe_list,
        }
    return HttpResponse(template.render(context, request))

def recipe_page(request, recipe_id):
    our_recipe = Recipe.objects.get(pk=recipe_id)
    try:
        our_recipe
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")
    return render(request, 'recipe_app/recipe_page.html', {'recipe': our_recipe})

def delete_recipe(request, recipe_id):
    our_recipe = Recipe.objects.get(pk=recipe_id)
    name = our_recipe.recipe_name.lower()
    our_recipe.delete()
    template = loader.get_template('recipe_app/delete_recipe.html')
    context = {}
    return HttpResponse("The recipe for %s has been deleted. <br> <br>" %name + template.render(context, request))

def delete_ingredient(request, recipe_id, ingredient_name):
    our_recipe = Recipe.objects.get(pk=recipe_id)
    name = ingredient_name.lower()
    our_ingredient = our_recipe.ingredient_set.filter(ingredient_name=ingredient_name)
    our_ingredient.delete()
    template = loader.get_template('recipe_app/delete_ingredient.html')
    context = {'recipe': our_recipe}
    return HttpResponse("The ingredient %s has been deleted. <br> <br>" %name + template.render(context, request))

def delete_direction(request, recipe_id, step):
    our_recipe = Recipe.objects.get(pk=recipe_id)
    our_direction = our_recipe.direction_set.filter(step=step)
    our_direction.delete()
    template = loader.get_template('recipe_app/delete_direction.html')
    context = {'recipe': our_recipe}
    return HttpResponse("The direction has been deleted. <br> <br>" + template.render(context, request))

def add_recipe(request):
    template_path = "recipe_app/add_recipe.html"
    query_string = request.GET
    print("OG OG OG QUERY QUERY QUERY =========", query_string)
    if query_string: #query part of process
        #getting info from query_string
        recipe_name = query_string["recipe_name"]
        ingredient_list = query_string["ingredient_list"]
        direction_list = query_string["direction_list"]
        
        #creating the recipe
        recipe = Recipe(recipe_name = recipe_name, pub_date = timezone.now())
        recipe.save()

        #creating the ingredients
        myIngredientNameList = utils.make_ingredient_list(ingredient_list)
        for i in myIngredientNameList:
            ingredient = recipe.ingredient_set.create(ingredient_name = i)
            ingredient.save()

        #creating the directions
        myDirectionNameList = utils.make_direction_list(direction_list)
        for i in myDirectionNameList:
            direction = recipe.direction_set.create(step = i)
            direction.save()
        
        return render(request, 'recipe_app/recipe_page.html', {'recipe': recipe})
    
    return render(request, template_path)

def edit_recipe(request, recipe_id):
    template_path = "recipe_app/edit_recipe.html"
    query_string = request.GET

    print("QUERY QUERY QUERY =========", query_string)

    if query_string: #query part of the process
        
        #editting the recipe
        our_recipe = Recipe.objects.get(pk=recipe_id)
        our_recipe.recipe_name = query_string["recipe_name"]
        our_recipe.save()

        for ingredient in our_recipe.ingredient_set.all():
        
            #deleting ingredient if user editted to a blank
            if query_string["ingredient_" + ingredient.ingredient_name] == "":
                ingredient.delete()

            #editting the ingredient
            else:
                ingredient.ingredient_name = query_string["ingredient_" + ingredient.ingredient_name]
                ingredient.save()

        for direction in our_recipe.direction_set.all():
            
            #deleting direction if user editted to a blank
            if query_string["direction_" + direction.step] == "":
                direction.delete()

            #editting the direction
            else:
                direction.step = query_string["direction_" + direction.step]
                direction.save()

        #grabbing newly inputted data
        ingredient_list = query_string["ingredient_list"]
        direction_list = query_string["direction_list"]


        #adding new ingredients
        myIngredientNameList = utils.make_ingredient_list(ingredient_list)
        for i in myIngredientNameList:

            #checking ingredients don't yet exist
            if not our_recipe.ingredient_set.filter(ingredient_name=i):
                ingredient = our_recipe.ingredient_set.create(ingredient_name = i)
                ingredient.save()

        #adding new directions
        myDirectionNameList = utils.make_direction_list(direction_list)
        for i in myDirectionNameList:

            #checking directions don't yet exist
            if not our_recipe.direction_set.filter(step=i):
                direction = our_recipe.direction_set.create(step = i)
                direction.save()

        return render(request, 'recipe_app/recipe_page.html', {'recipe': our_recipe})

    else: #getting recipe information from the database
        our_recipe = Recipe.objects.get(pk=recipe_id)
        my_ingredient_list = []
    
        for ingredient in our_recipe.ingredient_set.all():
            my_ingredient_list.append(ingredient.ingredient_name.strip())

        my_direction_list = []
    
        for direction in our_recipe.direction_set.all():
            my_direction_list.append(direction.step.strip())

        context = {'recipe': our_recipe, 'ingredient_list': my_ingredient_list, 'direction_list': my_direction_list}

        return render(request, template_path, context)

