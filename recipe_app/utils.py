from .models import Recipe, Ingredient, Direction

def make_ingredient_list(newline_separated_str):
    if (len(newline_separated_str) == 0):
        return []

    myIngredientNameList = newline_separated_str.strip().split("\n")
    returnList = []

    for ingredient in myIngredientNameList:
        if ingredient.strip() not in returnList and ingredient.strip()!="":
            returnList.append(ingredient.strip())
        
    return returnList

def make_direction_list(newline_separated_str):
    if (len(newline_separated_str) == 0):
        return []

    myDirectionNameList = newline_separated_str.strip().split("\n")
    returnList = []

    for direction in myDirectionNameList:
        if direction.strip() not in returnList and direction.strip()!="":
            returnList.append(direction.strip())
        
    return returnList
