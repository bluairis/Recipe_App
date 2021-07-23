from django.urls import path

from . import views

app_name = 'recipe_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:recipe_id>/', views.recipe_page, name='recipe_page'),
    path('<int:recipe_id>/delete', views.delete_recipe, name='delete_recipe')
]
