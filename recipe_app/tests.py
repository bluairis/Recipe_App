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
    
    # tests for views.add_recipe/views.edit_recipe
    
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

    def test_ingredient_and_direction_add_nothing(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        
        query_string =  {'recipe_name': 'r1', 'ingredient_list': '', 'direction_list': ''}

        utils.ingredient_and_direction_add(query_string, r1.id)

        self.assertEquals(len(r1.ingredient_set.all()), 0)

        self.assertEquals(len(r1.direction_set.all()), 0)

    def test_ingredient_and_direction_adding_ingredients(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        
        query_string =  {'recipe_name': 'r1', 'ingredient_list': 'Chicken\nBeans', 'direction_list': ''}

        utils.ingredient_and_direction_add(query_string, r1.id)

        self.assertEquals(len(r1.ingredient_set.all()), 2)

        self.assertEquals(len(r1.direction_set.all()), 0)

    def test_ingredient_and_direction_adding_directions(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()
        
        query_string =  {'recipe_name': 'r1', 'ingredient_list': 'Chicken\nBeans', 'direction_list': 'Bake\nClean\nEat'}

        utils.ingredient_and_direction_add(query_string, r1.id)

        self.assertEquals(len(r1.ingredient_set.all()), 2)

        self.assertEquals(len(r1.direction_set.all()), 3)

    def test_ingredient_and_direction_removing_ingredients(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()

        i1 = r1.ingredient_set.create(ingredient_name = "i1")
        i1.save()

        i2 = r1.ingredient_set.create(ingredient_name = "i2")
        i2.save()

        i3 = r1.ingredient_set.create(ingredient_name = "i3")
        i3.save()
        
        query_string =  {'recipe_name': 'r1', 'ingredient_list': 'Chicken\nBeans', 'direction_list': ''}

        utils.ingredient_and_direction_add(query_string, r1.id)

        self.assertEquals(len(r1.ingredient_set.all()), 2)

        self.assertEquals(len(r1.direction_set.all()), 0)

    def test_ingredient_and_direction_removing_directions(self):
        r1 = Recipe(recipe_name = "r1", pub_date = timezone.now())
        r1.save()

        i1 = r1.ingredient_set.create(ingredient_name = "i1")
        i1.save()

        i2 = r1.ingredient_set.create(ingredient_name = "i2")
        i2.save()

        i3 = r1.ingredient_set.create(ingredient_name = "i3")
        i3.save()

        d1 = r1.direction_set.create(step = "d1")
        d1.save()

        d2 = r1.direction_set.create(step = "d2")
        d2.save()

        d3 = r1.direction_set.create(step = "d3")
        d3.save()

        d4 = r1.direction_set.create(step = "d4")
        d4.save()
        
        query_string =  {'recipe_name': 'r1', 'ingredient_list': 'Chicken\nBeans\ni1', 'direction_list': 'Clean\nd1\nd2'}

        utils.ingredient_and_direction_add(query_string, r1.id)

        self.assertEquals(len(r1.ingredient_set.all()), 3)

        self.assertEquals(len(r1.direction_set.all()), 3)
        
    # tests for views.edit_recipe

    def test_grabbing_recipe_content(self):

        # creating recipe
        avocado_toast = Recipe(recipe_name = "Avocado Toast ...", pub_date = timezone.now())
        avocado_toast.save()

        # adding ingredients
        bread = avocado_toast.ingredient_set.create(ingredient_name = "1 slice of bread (I like thick-sliced whole-grain bread best)")
        bread.save()

        avocado = avocado_toast.ingredient_set.create(ingredient_name = "1/2 ripe avocado")
        avocado.save()

        salt = avocado_toast.ingredient_set.create(ingredient_name = "pinch of salt")
        salt.save()

        toppings = avocado_toast.ingredient_set.create(ingredient_name = "Optional: Any of the extra toppings suggested in this post")
        toppings.save()

        #adding directions
        toasting = avocado_toast.direction_set.create(step = "Toast your slice of bread until golden and firm.")
        toasting.save()

        removing = avocado_toast.direction_set.create(step = "Remove the pit from your avocado. Use a big spoon to scoop out the flesh. Put it in a bowl and mash it up with a fork until it’s as smooth as you like it. Mix in a pinch of salt (about 1/8 teaspoon) and add more to taste, if desired.")
        removing.save()

        spreading = avocado_toast.direction_set.create(step = "Spread avocado on top of your toast. Enjoy as-is or top with any extras offered in this post (I highly recommend a light sprinkle of flaky sea salt, if you have it).")
        spreading.save()

        #running function

        context = utils.get_recipe_contents(avocado_toast.id)

        self.assertEquals(context,{'recipe': avocado_toast,
                                   'ingredient_list': bread.ingredient_name + "\n\n" +
                                                      avocado.ingredient_name + "\n\n" +
                                                      salt.ingredient_name + "\n\n" +
                                                      toppings.ingredient_name,
                                   'direction_list': toasting.step + "\n\n" +
                                                     removing.step + "\n\n" +
                                                     spreading.step})

        

        
        


        

    


