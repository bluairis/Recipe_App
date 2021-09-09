from .models import Recipe, Ingredient, Direction

def make_ingredient_list(newline_separated_str):
    if (newline_separated_str == "  "):
        return []
    myIngredientNameList = newline_separated_str.split("\n")
    return myIngredientNameList

def make_direction_list(newline_separated_str):
    if (newline_separated_str == "  "):
        return []
    myDirectionNameList = newline_separated_str.split("\n")
    return myDirectionNameList
        
