from django.shortcuts import render
from django.http import Http404
from django.template import loader
from django.utils import timezone

# Create your views here.

from django.http import HttpResponse
from .models import Recipe, Ingredient, Direction
from . import utils

def index(request):
    template = loader.get_template('recipe_app/index.html')
    
    query_string = request.GET
    
    if query_string:

        latest_recipe_list = utils.sorting_by_query(query_string)

    else:
        latest_recipe_list = Recipe.objects.order_by('-pub_date')

    my_tuple_list = utils.numbering_recipes(latest_recipe_list)
    
    context = {
        'latest_recipe_list': my_tuple_list,
        }
    
    return HttpResponse(template.render(context, request))

def recipe_page(request, recipe_id):
    our_recipe = Recipe.objects.get(pk=recipe_id)
    try:
        our_recipe
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    latest_recipe_list = Recipe.objects.order_by('-pub_date')
    
    return render(request, 'recipe_app/recipe_page.html', {'latest_recipe_list': latest_recipe_list, 'recipe': our_recipe})

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

        #grabbing the recipe
        recipe_name = query_string["recipe_name"]
        
        #creating the recipe
        recipe = Recipe(recipe_name = recipe_name, pub_date = timezone.now())
        recipe.save()

        utils.ingredient_and_direction_add(query_string, recipe.id)
        
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

        utils.ingredient_and_direction_add(query_string, recipe_id)

        return render(request, 'recipe_app/recipe_page.html', {'recipe': our_recipe})

    else: #getting recipe information from the database
        
        context = utils.get_recipe_contents(recipe_id)

        return render(request, template_path, context)

def about(request):
    template_path = "recipe_app/about.html"
    return render(request, template_path)
