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
    return HttpResponse("Welcome to my recipe site! Below is a list of recipes! <br> <br>" + template.render(context, request))

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
    our_ingredient = our_recipe.ingredient_set.filter(ingredient_name__startswith=ingredient_name)
    our_ingredient.delete()
    template = loader.get_template('recipe_app/delete_ingredient.html')
    context = {'recipe': our_recipe}
    return HttpResponse("The ingredient %s has been deleted. <br> <br>" %name + template.render(context, request))

def delete_direction(request, recipe_id, step):
    our_recipe = Recipe.objects.get(pk=recipe_id)
    our_direction = our_recipe.direction_set.filter(step__startswith=step)
    our_direction.delete()
    template = loader.get_template('recipe_app/delete_direction.html')
    context = {'recipe': our_recipe}
    return HttpResponse("The direction has been deleted. <br> <br>" + template.render(context, request))

def add_recipe(request):
    template_path = "recipe_app/add_recipe.html"
    query_string = request.GET
    if query_string:
        recipe_name = query_string["recipe_name"]
        ingredient_list = query_string["ingredient_list"]
        direction_list = query_string["direction_list"]
        recipe = Recipe(recipe_name = recipe_name, pub_date = timezone.now())
        recipe.save()
        myIngredientNameList = utils.make_ingredient_list(ingredient_list)
        for i in myIngredientNameList:
            ingredient = recipe.ingredient_set.create(ingredient_name = i)
            ingredient.save()
        myDirectionNameList = utils.make_direction_list(direction_list)
        for i in myDirectionNameList:
            direction = recipe.direction_set.create(step = i)
            direction.save()
        return render(request, 'recipe_app/recipe_page.html', {'recipe': recipe})
    return render(request, template_path)

def edit_recipe(request, recipe_id):
    template_path = "recipe_app/edit_recipe.html"
    query_string = request.GET
    if query_string:
        our_recipe = Recipe.objects.get(pk=recipe_id)
        our_recipe.recipe_name = query_string["recipe_name"]
        our_recipe.save()

        ingredient_list = query_string["ingredient_list"]
        direction_list = query_string["direction_list"]

        myIngredientNameList = utils.make_ingredient_list(ingredient_list)
        for i in myIngredientNameList: 
            ingredient = our_recipe.ingredient_set.create(ingredient_name = i)
            ingredient.save()

        myDirectionNameList = utils.make_direction_list(direction_list)
        for i in myDirectionNameList:
            direction = our_recipe.direction_set.create(step = i)
            direction.save()

        return render(request, 'recipe_app/recipe_page.html', {'recipe': our_recipe})

    else:
        our_recipe = Recipe.objects.get(pk=recipe_id)
        my_ingredient_string = ""
    
        for ingredient in our_recipe.ingredient_set.all():
            my_ingredient_string += ingredient.ingredient_name.strip() + "\n"

        my_direction_string = ""
    
        for direction in our_recipe.direction_set.all():
            my_direction_string += direction.step.strip() + "\n\n"

        context = {'recipe': our_recipe, 'ingredients': my_ingredient_string, 'directions': my_direction_string}

        return render(request, template_path, context)

