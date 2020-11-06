from flask import Blueprint, render_template, flash, redirect, url_for, request, make_response
import requests
from app import app
import json


recipe_blueprint = Blueprint('recipe',
                            __name__,
                            template_folder='templates')

@recipe_blueprint.route('/', methods=['GET', 'POST'])
def recipe():
    if request.method == 'POST':
        content = requests.get(
            "https://api.spoonacular.com/recipes/findByIngredients?ingredients=" +
            (request.form['ingredient_name']) +
            "&number=30&apiKey=" + app.config.get("SPOON_API"))
        json_response = json.loads(content.text)
        return render_template("recipe/recipe_search.html", response=json_response) if json_response != [] else render_template(
            "recipe/recipe_search.html", response="")
    else:
        return render_template("recipe/recipe_search.html") 


@recipe_blueprint.route('/<recipe_id>', methods=['GET'])
def recipe_details(recipe_id):
    response = requests.get("https://api.spoonacular.com/recipes/"+recipe_id+"/information?includeNutrition=true&apiKey="+app.config.get("SPOON_API"))
    similar_recipe = requests.get("https://api.spoonacular.com/recipes/"+recipe_id+"/similar?number=7&apiKey="+app.config.get("SPOON_API"))
    return make_response(render_template("recipe/recipe_details.html", recipe_id=json.loads(response.text), recipe_similar =json.loads(similar_recipe.text)), 200)


@recipe_blueprint.route('/random_recipe', methods=['GET'])
def random_recipe():
    random_content = requests.get("https://api.spoonacular.com/recipes/random?number=30&apiKey="+app.config.get("SPOON_API"))
    json_response = json.loads(random_content.text)
    return make_response(render_template("recipe/random_recipe.html", response=json_response), 200)


@recipe_blueprint.route('/cooking_video', methods=['GET', 'POST'])
def cooking_video():
    if request.method == 'POST':
        content = requests.get(
            "https://api.spoonacular.com/food/videos/search?includeIngredients=" +
            (request.form['ingredient_name_video']) +
            "&number=20&apiKey=" + app.config.get("SPOON_API"))
        json_response = json.loads(content.text)
        return render_template("recipe/cooking_video.html", response=json_response) if json_response != [] else render_template(
            "recipe/cooking_video.html", response="")
    else:
        return render_template("recipe/cooking_video.html") 