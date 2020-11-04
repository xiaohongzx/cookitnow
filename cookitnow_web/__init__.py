from app import app
from flask import render_template
from cookitnow_web.blueprints.users.views import users_blueprint
from cookitnow_web.blueprints.recipe.views import recipe_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(recipe_blueprint, url_prefix="/recipe")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')
