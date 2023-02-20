from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_model
from flask import flash

from flask_app import DATABASE



class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.cooked_at = data["cooked_at"]
        self.under_30 = data["under_30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]


    def under_30_to_str(self):
        """turn the boolean value of under_30 into a yes or no string"""

        if self.under_30:
            return "Yes"
        
        return "No"



    # ------ READ ------
    @classmethod
    def get_all_with_user(cls):

        query = """
                SELECT * FROM recipes
                JOIN users ON recipes.user_id = users.id;"""

        results = connectToMySQL(DATABASE).query_db(query)

        recipes = []

        for row in results:
            recipe = cls(row)

            user_data = {
                **row, 
                "id" : row["users.id"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }

            recipe.user = users_model.User(user_data)

            recipes.append(recipe)

        return recipes

    
    @classmethod
    def get_one_with_user(cls, data):
        query = """
                SELECT * FROM recipes
                JOIN users ON recipes.user_id = users.id
                WHERE recipes.id = %(id)s;"""

        results = connectToMySQL(DATABASE).query_db(query, data)
        
        recipe = cls(results[0])

        user_data = {
            **results[0], 
            "id" : results[0]["users.id"],
            "created_at" : results[0]["users.created_at"],
            "updated_at" : results[0]["users.updated_at"]
        }

        recipe.user = users_model.User(user_data)

        return recipe

        
    # ------ CREATE ------
    @classmethod
    def create(cls, data):
        query = """INSERT INTO recipes (name, description, instructions, cooked_at, under_30, user_id)
                    VALUES (%(name)s, %(description)s, %(instructions)s, %(cooked_at)s, %(under_30)s, %(user_id)s)"""

        return connectToMySQL(DATABASE).query_db(query, data)


    # ------ DELETE ------
    @classmethod
    def delete(cls, data):
        query = """DELETE FROM recipes WHERE id = %(id)s"""

        return connectToMySQL(DATABASE).query_db(query, data)

    
    # ------ UPDATE ------
    @classmethod
    def update(cls, data):
        query = """
                UPDATE recipes
                SET name = %(name)s, description = %(description)s, instructions = %(instructions)s,
                cooked_at = %(cooked_at)s, under_30 = %(under_30)s, updated_at = NOW()
                WHERE id = %(id)s;"""
        
        return connectToMySQL(DATABASE).query_db(query, data)



    # ------ VALIDATIONS ------
    @staticmethod
    def validate(data):
        # validate recipe form data
        
        is_valid = True

        if len(data["name"]) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        
        if len(data["description"]) < 3:
            flash("Description must be at least 3 characters.")

            is_valid = False

        
        if len(data["instructions"]) < 3:
            flash("Instructions must be at least 3 characters.")

            is_valid = False

        
        if data["cooked_at"] == "":
            flash("Date must be filled out.")

            is_valid = False


        return is_valid