from flask import Flask 
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
import os 


app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

class User:
    def __init__(self,email,password):
        self.email = email
        self.password = password
    
    def save(self):
        hashed_password = generate_password_hash(self.password,method="sha256")
        user_data={
            "email":self.email,
            "password":hashed_password
        }
        mongo.db.users.insert_one(user_data)
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email':email})