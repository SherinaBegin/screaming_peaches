from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

#INFORMATION OF EACH SIGN WILL BE HARD CODED INTO THE DATABASE
#THAT'S WHY WE DO NOT HAVE VALIDATIONS IN THIS MODEL NEITHER A SAVE METHOD

class Comment:
    db = 'horoscopesRUs'

    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.likes = data['likes']
        self.user_id = data['user_id']


    @classmethod
    def save(cls, data):
        query = "INSERT into comments (comment, likes, user_id ) VALUES (%(comment)s,%(likes)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM comments WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_all_comments(cls):
        query = 'SELECT * FROM comments;'
        results = connectToMySQL(cls.db).query_db(query)
        comments = []
        for comment in results:
            comments.append(cls(comment))
        return comments
    
    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['comment']) < 3:
            is_valid = False
        flash("Comment must have at least 3 characters")
        return is_valid

