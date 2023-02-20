from flask import render_template, redirect, request, session, flash

from flask_app import app
from flask_app.models.recipes_model import Recipe
from flask_app.models.users_model import User


# route to show all recipes
@app.route("/recipes")
def all_recipes():

    # if there is no logged in user then redirect to login page
    if "user_id" not in session:
        flash("Login required to view this page", "secure")
        return redirect("/")

    # query db for the user in session
    user = User.get_one_by_id({"id": session["user_id"]})

    # query all recipes with a user instance attached
    recipes = Recipe.get_all_with_user()
    return render_template("recipes.html", user = user, recipes = recipes)


# route to show info of a recipe
@app.route("/recipes/<int:recipe_id>")
def show_recipe(recipe_id):

    # if there is no logged in user then redirect to login page
    if "user_id" not in session:
        flash("Login required to view this page", "secure")
        return redirect("/")

    # query db for the user in session
    user = User.get_one_by_id({"id": session["user_id"]})

    # query db for recipe with a user instance attached
    recipe = Recipe.get_one_with_user({"id": recipe_id})
    return render_template("show_recipe.html", user = user, recipe = recipe)


# route to show form to create a new recipe
@app.route("/recipes/new")
def new_recipe():

    # if there is no logged in user then redirect to login page
    if "user_id" not in session:
        flash("Login required to view this page", "secure")
        return redirect("/")

    # query db for current logged in user
    user = User.get_one_by_id({"id": session["user_id"]})
    return render_template("add_recipe.html", user = user)


# form submission to create recipe
@app.route("/create_recipe", methods=["POST"])
def create_recipe():

    # if the recipe did non pass validation then
    # redirect to "/recipes/new"
    if not Recipe.validate(request.form):
        return redirect("/recipes/new")

    # create the recipe and redirect to "/recipes"
    Recipe.create(request.form)
    return redirect("/recipes")


# route to edit a specific recipe
@app.route("/recipes/edit/<int:recipe_id>")
def edit_recipe(recipe_id):

    # if there is no logged in user then redirect to login page
    if "user_id" not in session:
        flash("Login required to view this page", "secure")
        return redirect("/")

    # query db for one recipe
    recipe = Recipe.get_one_with_user({"id": recipe_id})



    return render_template("edit_recipe.html", recipe = recipe)


# form submission to update a recipe
@app.route("/update_recipe", methods=["POST"])
def update_recipe():

    # if there is no logged in user then redirect to login page
    if not Recipe.validate(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")

    # query db to update a recipe
    Recipe.update(request.form)
    return redirect("/recipes")


# route to delete a recipe from db
@app.route("/recipes/destroy/<int:recipe_id>")
def delete_recipe(recipe_id):
    
    Recipe.delete({"id": recipe_id})
    return redirect("/recipes")