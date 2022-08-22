from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime
import math

#INFORMATION OF EACH SIGN WILL BE HARD CODED INTO THE DATABASE
#THAT'S WHY WE DO NOT HAVE VALIDATIONS IN THIS MODEL NEITHER A SAVE METHOD

class Comment:
    db = 'horoscopesRUs'

    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.user_id = data['user_id']
        self.created_at = data['created_at']


    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def save(cls, data):
        query = "INSERT into comments (comment, user_id ) VALUES (%(comment)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE comments SET comment = %(comment)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_comment_by_id(cls, data):
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
    
    @classmethod
    def get_comments_by_sign(cls, data):
        query = 'SELECT users.first_name, comments.* FROM users LEFT JOIN comments ON users.id = comments.user_id where users.astrologicalSign_id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        comments = []
        for comment in results:
            comments.append(cls(comment))
        return comments

    @classmethod
    def delete_comment(cls, data):
        query = 'DELETE FROM comments WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['comment']) < 3:
            is_valid = False
        flash("Comment must have at least 3 characters")
        return is_valid

