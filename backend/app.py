from flask import Flask, request,jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
import os
from dotenv import load_dotenv
from datetime import datetime,timedelta

load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = db = client['social-media']  
users_collection = db.users

@app.route('/')
def home():
    return jsonify(message="Welcome to the social media website API!")



@app.route('/singin')
def signin():
    data = request.get_json()
    
    email = data.get("email")
    passowrd = data.get("password")
    
    user = db.users.find_one({'email':email})
    if not user:
        return jsonify({"msg":'User not found'}),404
    
    if bcrypt.checkpw(passowrd.encoded('utf-8'),user['password']):
        token = jwt.encode({
            'user_id':str(user['_id']),
            'exp':datetime.utcnow()+timedelta(hours=1)
        },os.getenv('JWT_SECRET_KEY'),algorithm= 'HS256')
        
        return jsonify({'token':token}),200
    return jsonify({'message':'Invalid password'}),400


@app.route("/signup" , methods = ["POST"])
def signup():
    data = request.get_json()
    
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return jsonify({"msg":"Missing fields"}),400
    
    if users_collectiont.find_one({"email":email}):
        return jsonify({"msg":"Email already exists"}),400
    
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    new_user = {
        "username":username,
        "email":email,
        "password":hashed_password
    }
    
    users_collection.insert_one(new_user)
    
    access_token = create_access_token(identity = email)
    
    return jsonify({
        "msg":"User Created successfully",
        "access_token":access_token
    }),201
    
@app.route('/logout',methods=['POST'])
def logout():
    return jsonify({'message':'Logged out successfully'}),200

if __name__ == "__main__":
    app.run(debug = True)