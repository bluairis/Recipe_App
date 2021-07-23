import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    pub_date= models.DateTimeField('date published')
    def __str__(self):
        return self.recipe_name
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    def __str__(self):
        return self.ingredient_name

class Direction(models.Model):
    step = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
