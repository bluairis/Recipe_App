from django.shortcuts import render
from django.http import Http404
from django.template import loader
from django.utils import timezone

# Create your views here.

from django.http import HttpResponse
from .models import Recipe, Ingredient, Direction
from . import utils

def index(request):
    query_string = request.GET
    
    if query_string:

        try:
            sort_order = query_string["sort_order"]
            
        except KeyError:
            raise Http404("sort order not present")

        if sort_order not in ['-pub_date', 'pub_date', '-recipe_name', 'recipe_name']:
            raise Http404("entered sort order does not exist")
            
        latest_recipe_list = Recipe.objects.order_by(sort_order)


    else:
        latest_recipe_list = Recipe.objects.order_by('-pub_date')

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

def delete_ingredient(request, recipe_id, ingredient_id):
    our_recipe = Recipe.objects.get(pk=recipe_id)
    our_ingredient = our_recipe.ingredient_set.filter(pk=ingredient_id)
    our_ingredient.delete()
    template = loader.get_template('recipe_app/delete_ingredient.html')
    context = {'recipe': our_recipe}
    return HttpResponse("The ingredient has been deleted. <br> <br>" + template.render(context, request))

def delete_direction(request, recipe_id, direction_id):
    our_recipe = Recipe.objects.get(pk=recipe_id)
    our_direction = our_recipe.direction_set.filter(pk=direction_id)
    our_direction.delete()
    template = loader.get_template('recipe_app/delete_direction.html')
    context = {'recipe': our_recipe}
    return HttpResponse("The direction has been deleted. <br> <br>" + template.render(context, request))

def add_recipe(request):
    template_path = "recipe_app/add_recipe.html"
    query_string = request.GET
    
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

    if query_string: #query part of the process
        
        #editting the recipe
        our_recipe = Recipe.objects.get(pk=recipe_id)
        our_recipe.recipe_name = query_string["recipe_name"]
        our_recipe.save()

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
        myIngredientNameList = utils.make_ingredient_list(ingredient_list)
        for i in myIngredientNameList:
            ingredient = our_recipe.ingredient_set.create(ingredient_name = i)
            ingredient.save()

        #adding new directions
        myDirectionNameList = utils.make_direction_list(direction_list)
        for i in myDirectionNameList:
            direction = our_recipe.direction_set.create(step = i)
            direction.save()

        return render(request, 'recipe_app/recipe_page.html', {'recipe': our_recipe})

    else: #getting recipe information from the database
        our_recipe = Recipe.objects.get(pk=recipe_id)
        my_ingredient_string = ""
    
        for ingredient in our_recipe.ingredient_set.all():
            my_ingredient_string += ingredient.ingredient_name.strip() + "\n\n"

        my_direction_string = ""
    
        for direction in our_recipe.direction_set.all():
            my_direction_string += direction.step.strip() + "\n\n"

        context = {'recipe': our_recipe, 'ingredient_list': my_ingredient_string, 'direction_list': my_direction_string}

        return render(request, template_path, context)

