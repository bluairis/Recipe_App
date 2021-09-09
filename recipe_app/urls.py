from django.urls import path

from . import views

app_name = 'recipe_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:recipe_id>/', views.recipe_page, name='recipe_page'),
    path('<int:recipe_id>/delete', views.delete_recipe, name='delete_recipe'),
    path('<int:recipe_id>/<str:ingredient_name>/delete', views.delete_ingredient, name='delete_ingredient'),
    path('<int:recipe_id>/<str:direction_name>/delete', views.delete_direction, name='delete_direction'),
    path('add', views.add_recipe, name='add_recipe'),
]
