import csv
import os

class CsvHandler():

    def __init__(self, filename, fieldnames):
        self.fieldnames = fieldnames
        self.filename = filename

    def write_list(self, dict_list):

        with open(self.filename, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)

            if os.stat(self.filename).st_size == 0:
                writer.writeheader()

            if dict_list:
                for dict_ in dict_list:
                    writer.writerow(dict_)

    def create_user(self, user):

        with open(self.filename, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)

            if os.stat(self.filename).st_size == 0:
                writer.writeheader()

            writer.writerow(user)

    def delete_user(self, user_id):
        
        users = []

        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file, delimiter=',')
            users = [ user for user in reader if int(user['id']) != user_id ]

        open(self.filename, 'w').truncate(0)

        self.write_list(users)

    def get_users(self):
        
        users = []

        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file, delimiter=',')
            users = [ user for user in reader ]
        
        return users

    def next_avaliable_id(self):

        next_id = 0
        users = []

        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file, delimiter=',')
            ids = [ user['id'] for user in reader ]

        if ids:
            ids.sort(key=lambda id: int(id))
            next_id = int(ids[-1])

        return next_id + 1

    def get_user_by_id(self, user_id):

        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file, delimiter=',')
            user = [ user for user in reader if int(user['id']) == user_id ]
        
        if user:
            return user[0]
        
        else:
            return "Not Found"
