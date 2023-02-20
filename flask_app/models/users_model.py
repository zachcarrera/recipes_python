import re

from flask import flash

from flask_app import DATABASE, BCRYPT
from flask_app.config.mysqlconnection import connectToMySQL

# constant instance of email regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # ------ READ ------
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"

        results = connectToMySQL(DATABASE).query_db(query,data)
        return cls(results[0])


    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"

        results = connectToMySQL(DATABASE).query_db(query,data)

        if results:
            return cls(results[0])
        
        return False



    # ------ CREATE ------
    @classmethod
    def create(cls, form):
        query = """INSERT INTO users (first_name, last_name, email, password)
                    VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s)"""

        # hash pw for db
        hashed_pw = BCRYPT.generate_password_hash(form["password"])

        data = {
            **form,
            "password": hashed_pw
        }


        return connectToMySQL(DATABASE).query_db(query, data)




    # ------ VALIDATIONS ------
    @classmethod
    def validate_login(cls, data):
        found_user = cls.get_one_by_email(data)

        if not found_user:
            flash("Email/Password not valid", "login")
            return False
        
        if not BCRYPT.check_password_hash(found_user.password, data["password"]):
            flash("Email/Password not valid", "login")
            return False
        
        return found_user



    @staticmethod
    def validate_new(data):
        # take in a form submission and return false if any requirements are not met
        is_valid = True

        if len(data["first_name"]) < 2:
            flash("First name must be at least 3 characters.", "register")
            is_valid = False
        
        if len(data["last_name"]) < 2:
            flash("Last name must be at least 3 characters.", "register")
            is_valid = False

        if not EMAIL_REGEX.match(data["email"]):
            flash("Email must be valid.", "register")
            is_valid = False

        if User.get_one_by_email(data):
            flash("This email is already taken.", "register")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("Passwords must match.", "register")
            is_valid = False

        return is_valid