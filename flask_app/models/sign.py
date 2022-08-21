from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

#INFORMATION OF EACH SIGN WILL BE HARD CODED INTO THE DATABASE
#THAT'S WHY WE DO NOT HAVE VALIDATIONS IN THIS MODEL NEITHER A SAVE METHOD

class Sign:
    db = 'horoscopesRUs'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.element = data['element']
        self.polarity = data['polarity']
        self.quality = data['quality']
        self.rulling_planet = data['rulling_planet']
        self.rulling_house = data['rulling_house']
        self.spirit_color = data['spirit_color']
        self.lucky_gem = data["lucky_gem"]
        self.flower = data["flower"]
        self.top_love = data['top_love']
        self.start_day = data['start_day']
        self.start_month = data['start_month']
        self.end_day = data['end_year']
        self.end_month = data['end_month']

    # @classmethod
    # def save(cls, data):
    #     query = "INSERT into users (email, first_name, last_name, birthday, birthmonth, birthyear, password) VALUES (%(email)s,%(first_name)s,%(last_name)s, %(birthday)s, %(birthmonth)s, %(birthyear)s, %(password)s);"
    #     return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM astrologicalSigns WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_all_signs(cls):
        query = 'SELECT * FROM astrologicalSigns;'
        results = connectToMySQL(cls.db).query_db(query)
        signs = []
        for sign in results:
            signs.append(cls(sign))
        return signs
