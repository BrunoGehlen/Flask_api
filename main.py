from flask import Flask, request
from csv_handler import CsvHandler
from http import HTTPStatus
import csv
import json
import os


class User:

    def __init__(self):
        self.csv_handler = CsvHandler('users.csv', ['id','name','email','password','age'])

    def create_app(self):

        app = Flask(__name__)
        
        @app.route('/signup', methods=['POST'])
        def signup():
            if request.method == 'POST':
                data = request.get_json()

                if None in [ 
                    data.get('age'), 
                    data.get('password'), 
                    data.get('email'), 
                    data.get('name')
                ]:

                    return json.dumps({ 
                        "status" : 400,  
                        "error_code" : "400 - Bad Request", 
                        "more_info" : "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400" 
                    }), 400

                print(self.csv_handler.next_avaliable_id())
                data.update({"id": self.csv_handler.next_avaliable_id()})
                self.csv_handler.create_user(data)

            return json.dumps(data), HTTPStatus.CREATED

                # Check this out tomorow
        @app.route('/login', methods=['POST'])
        def login():
            if request.method == 'POST':
                data = request.get_json()
                with open('users.csv', 'r') as reading:
                    reader = csv.DictReader(reading, delimiter=',')
                    users = [ user for user in reader if user['email'] == data['email'] and user['password'] == data['password']]
                    if users:
                        return json.dumps({
                            "name": users[0]['name'],
                            "email": users[0]['email'],
                            "age": users[0]['age']
                        })

        @app.route('/profile/<int:user_id>', methods=['PATCH'])
        def update_user(user_id):

            # ID que não existe da erro

            if request.method == 'PATCH':
                valid_data = {}
                data = request.get_json()
                if data == {} or data.get('id'):
                    return json.dumps({ 
                        "status" : 400,  
                        "error_code" : "400 - Bad Request", 
                        "more_info" : "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400" 
                    }), HTTPStatus.BAD_REQUEST

                if data.get('age'):
                    valid_data.update({"age": data['age']})

                if data.get('email'):
                    valid_data.update({"email": data['email']})

                if data.get('password'):
                    valid_data.update({"password": data['password']})

                if data.get('name'):
                    valid_data.update({"name": data['name']})

                user = self.csv_handler.get_user_by_id(user_id)

                self.csv_handler.delete_user(user_id)
                user.update(valid_data)
                self.csv_handler.create_user(user)

                return json.dumps({
                    "name": user['name'],
                    "email": user['email'],
                    "age": user['age']
                })

        @app.route('/profile/<int:user_id>', methods=['DELETE'])
        def delete_user(user_id):
            if request.method == 'DELETE':

                self.csv_handler.delete_user(user_id)

                return HTTPStatus.GONE


        @app.route('/users', methods=['GET'])
        def all_users():

            users = self.csv_handler.get_users()

            for user in users:
                if 'password' in user:
                    del user['password']

            return json.dumps(users), 200

        return app



flask_api = User()
app = flask_api.create_app()