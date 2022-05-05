from tkinter.tix import Select
from flask import Flask, request, jsonify, make_response
from flask_restful import Api
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from requests import Response
from db import *

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = "thisissecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:akshat0509@localhost/login_sys"

@app.route('/signup',methods=["POST"])
def create_user():
    data = request.get_json()
    password = bcrypt.generate_password_hash(data['password']).decode("utf-8")
    new_user = User(username=data['username'],email=data['email'],pssword=password,p_id=data['p_id'],)
    session.add(new_user)
    session.commit()
    return jsonify({"message":"New User created"},data)

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    user_email = data['email']
    user_password = data['password']
    
    user, user_pass= dbGetUserByEmail(user_email)

    if not user:
        return make_response("User doesn't exist")
    
    if bcrypt.check_password_hash(user_pass, user_password):
        token = create_access_token(identity=user_email)
        return jsonify({ "token": token })
    return make_response("incorrect password")

@app.route('/user', methods=['GET'])
@jwt_required()
def user_info():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/save_ad_unit', methods=['POST'])
@jwt_required()
def save_ad():
    data = request.get_json()
    current_user = get_jwt_identity()
    user_id = dbGetUser(current_user)
    dbSaveAdUnit(data,int(user_id))

    return jsonify({"message":"New Ad Unit created"},data)

@app.route('/get_ad_unit/', methods=["GET"])
@jwt_required()
def load_ad():
    if 'page' in request.args:
        page_name = request.args['page']
        return(dbLoadAdUnit(page_name))
    else:
        return(dbEmptyLoadAdUnit())

if __name__ == "__main__":
    app.run(debug=True)
