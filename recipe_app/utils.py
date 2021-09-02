from .models import Recipe, Ingredient, Direction

def make_ingredient_list(newline_separated_str):
    for i in newline_separated_str:
        myIngredientList = []
        myIngredient = ""
        if (i == "\n"):
            myIngredientList.append(myIngredient)
            myIngredient = ""
        else:
            myIngredient += newline_separated_str[i]
    return myIngredientList

def make_direction_list(newline_separated_str):
    for i in newline_separated_str:
        myDirectionList = []
        myDirection = ""
        if (i == "\n"):
            myDirectionList.append(myDirection)
            myDirection = ""
        else:
            myDirection += newline_separated_str[i]
    return myDirectionList
        
