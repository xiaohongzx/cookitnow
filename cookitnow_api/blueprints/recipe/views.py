from flask import Blueprint, render_template, flash, redirect, url_for, request, make_response
import requests
from app import app
import json


recipe_api_blueprint = Blueprint('recipe_api',
                            __name__,
                            template_folder='templates')

@recipe_api_blueprint.route('/', methods=['GET', 'POST'])
def recipe():
    if request.method == 'POST':
        content = requests.get(
            "https://api.spoonacular.com/recipes/findByIngredients?ingredients=" +
            (request.form['ingredient_name']) +
            "&number=10&apiKey=" + app.config.get("SPOON_API"))
        json_response = json.loads(content.text)
        return render_template("recipe/recipe_search.html", response=json_response) if json_response != [] else render_template(
            "recipe/recipe_search.html", response="")
    else:
        return render_template("recipe/recipe_search.html") 


@recipe_api_blueprint.route('/<recipe_id>', methods=['GET'])
def recipe_details(recipe_id):
    response = requests.get("https://api.spoonacular.com/recipes/"+recipe_id+"/information?includeNutrition=true&apiKey="+app.config.get("SPOON_API"))
    return make_response(render_template("recipe/recipe_details.html", recipe_id=json.loads(response.text)), 200)


