from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
   db = 'horoscopesRUs'

   def __init__(self, data):
      self.id = data['id']
      self.email = data['email']
      self.first_name = data['first_name']
      self.last_name = data['last_name']
      self.birthday = data['birthday']
      self.birthmonth = data['birthmonth']
      self.birthyear = data['birthyear']
      self.password = data['password']
      self.astrologicalSign_id = data['astrologicalSign_id']


   @classmethod
   def save(cls, data):
      query = "INSERT into users (email, first_name, last_name, birthday, birthmonth, birthyear, password, astrologicalSign_id, created_at, updated_at) VALUES (%(email)s,%(first_name)s,%(last_name)s, %(birthday)s, %(birthmonth)s, %(birthyear)s, %(password)s, %(astrologicalSign_id)s, NOW(), NOW() );"
      return connectToMySQL(User.db).query_db(query, data)

   @classmethod
   def get_user_by_id(cls, data):
      query = "SELECT * FROM users WHERE id = %(id)s;"
      results = connectToMySQL(User.db).query_db(query, data)
      if len(results) < 1:
         return False
      return cls(results[0])

   @classmethod
   def get_user_by_email(cls, data):
      query = "SELECT * FROM users WHERE email = %(email)s;"
      results = connectToMySQL(User.db).query_db(query, data)
      if len(results) < 1:
         return False
      return cls(results[0])

   @classmethod
   def get_all_users(cls):
      query = 'SELECT * FROM users;'
      results = connectToMySQL(User.db).query_db(query)
      users = []
      for user in results:
         users.append(cls(user))
      return users

   @staticmethod
   def validate_user(user):
      is_valid = True
      query = 'SELECT * FROM users WHERE email = %(email)s;'
      results = connectToMySQL(User.db).query_db(query, user)
      if len(results) >= 1:
         flash('email is already taken')
         is_valid = False
      if not EMAIL_REGEX.match(user['email']):
         flash("Invalid email address.")
         is_valid = False
      if len(user['first_name']) < 1:
         is_valid = False
         flash("First name cannot be blank.")
      if len(user['last_name']) < 1:
         is_valid = False
         flash("Last name cannot be blank.")
      if ( int(user['birthday']) < 1):
         is_valid = False
         flash("Birth day cannot be blank.")
      if ( int(user['birthmonth']) < 1 or int(user['birthmonth']) > 12 ) :
         is_valid = False
         flash("Birt month cannot be blank.")
      if (int(user['birthyear']) < 1):
         is_valid = False
         flash("Birt year cannot be blank.")
      if len(user['password']) < 8:
         is_valid = False
         flash("Password must be atleast 8 characters long.")
      if user['password'] != user['confirm_password']:
         is_valid = False
         flash('Passwords do no match.')
      return is_valid
