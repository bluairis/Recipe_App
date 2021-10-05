from django.urls import path

from . import views

app_name = 'recipe_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add_recipe, name='add_recipe'),
    path('<int:recipe_id>/', views.recipe_page, name='recipe_page'),
    path('<int:recipe_id>/delete', views.delete_recipe, name='delete_recipe'),
    path('<int:recipe_id>/<int:ingredient_id>/delete_ingredient', views.delete_ingredient, name='delete_ingredient'),
    path('<int:recipe_id>/<int:direction_id>/delete_direction', views.delete_direction, name='delete_direction'),    
    path('<int:recipe_id>/edit_recipe', views.edit_recipe, name='edit_recipe')
]
