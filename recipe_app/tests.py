from django.http import Http404

from django.utils import timezone

from django.test import TestCase, SimpleTestCase

from .models import Recipe, Ingredient, Direction

from . import views, utils

# Create your tests here.

class AllMyTests(TestCase):

    # basic model based tests
    
    def test_recipe_name(self):
        r1 = Recipe(recipe_name = "my_recipe", pub_date = timezone.now())
        self.assertEquals(r1.recipe_name, "my_recipe")

    def test_recipe_date(self):
        the_time = timezone.now()
        r1 = Recipe(recipe_name = "my_recipe", pub_date = the_time)
        self.assertEquals(r1.pub_date, the_time)

    def test_recipe_saving(self):
        r1 = Recipe(recipe_name = "my_recipe", pub_date = timezone.now())
        r1.save()

    def test_ingredient_name(self):
        r1 = Recipe(recipe_name = "my_recipe", pub_date = timezone.now())
        r1.save()
        i1 = r1.ingredient_set.create(ingredient_name = "i1")
        self.assertEquals(i1.ingredient_name, "i1")

    def test_direction_saving(self):
        r1 = Recipe(recipe_name = "my_recipe", pub_date = timezone.now())
        r1.save()
        d1 = r1.direction_set.create(step = "d1")
        self.assertEquals(d1.step, "d1")

    def test_ingredient_saving(self):
        r1 = Recipe(recipe_name = "my_recipe", pub_date = timezone.now())
        r1.save()
        i1 = r1.ingredient_set.create(ingredient_name = "i1")
        i1.save()

    def test_direction_saving(self):
        r1 = Recipe(recipe_name = "my_recipe", pub_date = timezone.now())
        r1.save()
        d1 = r1.direction_set.create(step = "d1")
        d1.save()
        
    # tests for views.index
    
    def test_abc_sorting(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        r3 = Recipe(recipe_name = "r3", pub_date = timezone.now())
        r3.save()
        r2 = Recipe(recipe_name = "r2", pub_date = timezone.now())
        r2.save()

        latest_recipe_list = utils.sorting_by_query({"sort_order" : "recipe_name"})

        recipe_list = list(latest_recipe_list)

        self.assertEquals(recipe_list, [r1, r2, r3])

    def test_rev_abc_sorting(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        r3 = Recipe(recipe_name = "r3", pub_date = timezone.now())
        r3.save()
        r2 = Recipe(recipe_name = "r2", pub_date = timezone.now())
        r2.save()

        latest_recipe_list = utils.sorting_by_query({"sort_order" : "-recipe_name"})

        recipe_list = list(latest_recipe_list)

        self.assertEquals(recipe_list, [r3, r2, r1])

    def test_pub_date_sorting(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        r3 = Recipe(recipe_name = "r3", pub_date = timezone.now())
        r3.save()
        r2 = Recipe(recipe_name = "r2", pub_date = timezone.now())
        r2.save()

        latest_recipe_list = utils.sorting_by_query({"sort_order" : "pub_date"})

        recipe_list = list(latest_recipe_list)

        self.assertEquals(recipe_list, [r1, r3, r2])

    def test_rev_pub_date_sorting(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        r3 = Recipe(recipe_name = "r3", pub_date = timezone.now())
        r3.save()
        r2 = Recipe(recipe_name = "r2", pub_date = timezone.now())
        r2.save()

        latest_recipe_list = utils.sorting_by_query({"sort_order" : "-pub_date"})

        recipe_list = list(latest_recipe_list)

        self.assertEquals(recipe_list, [r2, r3, r1])

    def test_bad_sort_order(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        r3 = Recipe(recipe_name = "r3", pub_date = timezone.now())
        r3.save()
        r2 = Recipe(recipe_name = "r2", pub_date = timezone.now())
        r2.save()

        with self.assertRaises(Http404):
            utils.sorting_by_query({"sort_order" : "chicken"})

    def test_bad_query(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        r3 = Recipe(recipe_name = "r3", pub_date = timezone.now())
        r3.save()
        r2 = Recipe(recipe_name = "r2", pub_date = timezone.now())
        r2.save()

        with self.assertRaises(Http404):
            utils.sorting_by_query({'chicken': 'chicken'})

    def test_numbering_recipes(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        r3 = Recipe(recipe_name = "r3", pub_date = timezone.now())
        r3.save()
        r2 = Recipe(recipe_name = "r2", pub_date = timezone.now())
        r2.save()

        latest_recipe_list = Recipe.objects.all()

        tuples = utils.numbering_recipes(latest_recipe_list)

        self.assertEquals(tuples, [(1, r1),(2, r3), (3, r2)])

    def test_numbering_sorted_recipes(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        r3 = Recipe(recipe_name = "r3", pub_date = timezone.now())
        r3.save()
        r2 = Recipe(recipe_name = "r2", pub_date = timezone.now())
        r2.save()

        latest_recipe_list = utils.sorting_by_query({"sort_order" : "-recipe_name"})

        tuples = utils.numbering_recipes(latest_recipe_list)

        self.assertEquals(tuples, [(1, r3),(2, r2), (3, r1)])

    def test_numbering_empty_list_of_recipes(self):

        latest_recipe_list = Recipe.objects.all()

        tuples = utils.numbering_recipes(latest_recipe_list)

        self.assertEquals(tuples, [])
    
    # tests for views.add_recipe
    
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
  

    


