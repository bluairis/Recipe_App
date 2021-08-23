from django.urls import path

from . import views

app_name = 'recipe_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:recipe_id>/', views.recipe_page, name='recipe_page'),
    path('<int:recipe_id>/delete', views.delete_recipe, name='delete_recipe'),
    path('add', views.add_recipe, name='add_recipe'),
    path('user_add', views.user_add_recipe, name='user_add_recipe')
]
