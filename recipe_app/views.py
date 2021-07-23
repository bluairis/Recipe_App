from django.shortcuts import render
from django.http import Http404
from django.template import loader

# Create your views here.

from django.http import HttpResponse
from .models import Recipe

def index(request):
    latest_recipe_list = Recipe.objects.order_by('-pub_date')[:5]
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
    return HttpResponse("You're looking at the recipe for %s." % our_recipe.recipe_name)

def delete_recipe(request, recipe_id):
    our_recipe = Recipe.objects.get(pk=recipe_id)
    our_recipe.delete()
    template = loader.get_template('recipe_app/delete_recipe.html')
    context = {}
    return HttpResponse("The recipe has been deleted. <br> <br>" + template.render(context, request))
