from django.shortcuts import render
from django.http import Http404
from django.template import loader
from django.utils import timezone

# Create your views here.

from django.http import HttpResponse
from .models import Recipe, Ingredient, Direction

def index(request):
    latest_recipe_list = Recipe.objects.order_by('-pub_date')
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

def add_recipe(request):
    recipe = Recipe(recipe_name = input("Enter the name of the recipe: "), pub_date = timezone.now())
    recipe.save()
    name = recipe.recipe_name.lower()

    ingredient_confirmation = input("Would you like to add ingredients? Type yes or no. ")
    while ingredient_confirmation != "yes" and ingredient_confirmation != "no":
        ingredient_confirmation = input("Please respond with yes or no. ")

    if ingredient_confirmation == "yes":
        quantity_of_ingredients = int(input("How many ingredients would you like to add? "))
        for x in range(quantity_of_ingredients):
            ingredient = recipe.ingredient_set.create(ingredient_name = input("Enter the name and quantity of the ingredient. Type \"stop\" if you have no more ingredients. "))
            if ingredient.ingredient_name == "stop":
                ingredient.delete()
                break

    direction_confirmation = input("Would you like to add directions? Type yes or no. ")
    while direction_confirmation != "yes" and direction_confirmation != "no":
        direction_confirmation = input("Please respond with yes or no. ")

    if direction_confirmation == "yes":
        quantity_of_directions = int(input("How many directions would you like to add? "))
        for x in range(quantity_of_directions):
            direction = recipe.direction_set.create(step = input("Enter your step. Type \"stop\" if you have no more ingredients. "))
            if direction.step == "stop":
                direction.delete()
                break
    
    template = loader.get_template('recipe_app/add_recipe.html')
    context = {}
    return HttpResponse("Congratulations! The recipe for %s has been added. <br> <br>" %name + template.render(context, request))

def user_add_recipe(request):
    template_path = 'recipe_app/user_add_recipe.html'
    query_string = request.GET
    if query_string:
        recipe_name = query_string["recipe_name"]
    else:
        recipe_name = ""
    context = { 'recipe_name' : recipe_name }
    recipe = Recipe(recipe_name, pub_date = timezone.now())
    #recipe.save()
    return render(request, template_path, context)

