from flask import Blueprint, render_template, flash, redirect, url_for, request, make_response
import requests
from app import app
from models.upload_recipe import UploadRecipe
import json
import os
from werkzeug import secure_filename


UPLOAD_FOLDER = 'cookitnow_web/static/images/uploaded_img/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@recipe_blueprint.route('/show_customize_recipe', methods=['GET'])
def show_customize_recipe():
    all_recipe = UploadRecipe.select()
    return render_template("recipe/show_customize_recipe.html", all_recipe = all_recipe) 


@recipe_blueprint.route('/upload_recipe', methods=['GET'])
def upload_recipe():
    return render_template("recipe/upload_recipe.html") 


@recipe_blueprint.route('/upload', methods=['POST'])
def create_recipe():
    data = request.form

    if "recipeimage" not in request.files:
        flash("Please select an image for the recipe!")
        return redirect(url_for("recipe.upload_recipe"))
    file = request.files['recipeimage']
    if file.filename == "":
        flash("Please select an image for the recipe!")
        return redirect(url_for("recipe.upload_recipe"))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    else:
        flash("Could not upload image, please go back and try again")
        return redirect(url_for("recipe.upload_recipe"))
        
    url = file.filename
    create_new_recipe = UploadRecipe(
        r_title = data.get('recipetitle'), 
        r_cookingtime = data.get('recipetime'),
        r_image_url = url,
        r_serving = data.get('recipeserve'), 
        r_ingredient = data.get('recipeingredient'), 
        r_step = data.get('recipestep'), 
        r_about = data.get('recipeabout')
    )

    if create_new_recipe.save():   
        return redirect(url_for("recipe.show_recipe"))
    else:
        return redirect(url_for("recipe.upload_recipe"))



@recipe_blueprint.route('/customize/<id>', methods=["GET"])
def show_recipe(id):
    c_recipe = UploadRecipe.get_or_none(UploadRecipe.id == id)
    return render_template("recipe/show_recipe.html", c_recipe = c_recipe)    



@recipe_blueprint.route('/customize/<id>/edit', methods=["GET"])
def edit_recipe(id):
    edit_recipe = UploadRecipe.get_or_none(UploadRecipe.id == id)
    return render_template("recipe/edit_recipe.html", edit_recipe = edit_recipe, id = id) 



@recipe_blueprint.route('/<id>/edit', methods=["POST"])
def update_recipe(id):
    update_recipe = UploadRecipe.get_or_none(UploadRecipe.id == id)
    data = request.form

    if update_recipe:
        if "recipeimage" not in request.files:
            flash("Please select an image for the recipe!")
            return redirect(url_for("recipe.edit_recipe",id = id))
        file = request.files['recipeimage']
        if file.filename == "":
            flash("Please select an image for the recipe!")
            return redirect(url_for("recipe.edit_recipe",id = id))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        else:
            flash("Could not upload image, please go back and try again")
            return redirect(url_for("recipe.edit_recipe",id = id))
            
        url = file.filename

        update_recipe.r_title = data.get('recipetitle')
        update_recipe.r_cookingtime = data.get('recipetime')
        update_recipe.r_image_url = url
        update_recipe.r_serving = data.get('recipeserve')
        update_recipe.r_ingredient = data.get('recipeingredient')
        update_recipe.r_step = data.get('recipestep')
        update_recipe.r_about = data.get('recipeabout')
        
        

        if update_recipe.save():   
            return redirect(url_for("recipe.show_recipe", id=id))
        else:
            return redirect(url_for("recipe.edit_recipe", id=id))
    
    return render_template("recipe/edit_recipe.html", update_recipe = update_recipe, id = id)          