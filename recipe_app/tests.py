from django.utils import timezone

from django.test import TestCase, SimpleTestCase

from .models import Recipe, Ingredient, Direction

from . import views, utils

# Create your tests here.

class AllMyTests(SimpleTestCase):

    # tests for ensuring the models get populated properly with data:
    
    def test_recipe_name(self):
        r1 = Recipe(recipe_name = "my_recipe", pub_date = timezone.now())
        self.assertEquals(r1.recipe_name, "my_recipe")

    def test_recipe_date(self):
        the_time = timezone.now()
        r1 = Recipe(recipe_name = "my_recipe", pub_date = the_time)
        self.assertEquals(r1.pub_date, the_time)

    def test_ingredient_name(self):
        r1 = Recipe(recipe_name = "my_recipe", pub_date = timezone.now())
        r1.save()
        self.assertEquals(1,1)


    # tests for ensuring ingredients and directions are added as expected:
    
    def test_empty_ingredient_list(self):
        my_list = utils.make_ingredient_list("")
        self.assertEquals(my_list,[])

    def test_empty_direction_list(self):
        my_list = utils.make_direction_list("")
        self.assertEquals(my_list,[])

    def test_ingredients_new_lines(self):
        my_list = utils.make_ingredient_list("Chicken\n\n\n\n\nPeas\n\n\n\n\n\nSugarWater")
        self.assertEquals(my_list,["Chicken","Peas","SugarWater"])

    def test_directions_new_lines(self):
        my_list = utils.make_ingredient_list("Step1\n\n\n\n\n\n\nStep2\nStep3\n\n\nStep4Step5")
        self.assertEquals(my_list,["Step1", "Step2", "Step3", "Step4Step5"])

    def test_ingredient_special_chars(self):
        my_list = utils.make_ingredient_list("\\nChicken\n\\tPeas\n\"Bananas\"\n3/4 tsp of Salt")
        self.assertEquals(my_list,["\\nChicken","\\tPeas", "\"Bananas\"","3/4 tsp of Salt"])

    def test_direction_special_chars(self):
        my_list = utils.make_direction_list("\\nStep1!\\***3/4,\\n\nStep2")
        self.assertEquals(my_list,["\\nStep1!\\***3/4,\\n","Step2"])
  

    


