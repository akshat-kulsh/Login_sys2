from flask import Flask, request, jsonify, make_response
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = "thisissecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:akshat0509@localhost/login_sys"

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user_table'
    idusers = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(30))
    pssword = db.Column(db.String(100))
    p_id = db.Column(db.Integer)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'token is missing!!'})
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(p_id = data['p_id']).first()
        except:
            return jsonify({"message": "token is invalid!!"})

        return f(current_user,*args, **kwargs)
    return decorated


@app.route('/signup',methods=["POST"])
def create_user():
    data = request.get_json()
    password = bcrypt.generate_password_hash(data['pssword']).decode("utf-8")
    new_user = User(username=data['username'],email=data['email'],pssword=password,p_id=data['p_id'],)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"New User created"},data)

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response("Need more arguments")
    
    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response("User doesn't exist")
    
    if bcrypt.check_password_hash(user.pssword, auth.password):
        token = jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({ "token": token })
    return make_response("incorrect password")

@app.route('/user', methods=['GET'])
@token_required
def user_info(current_user):
    user = User.query.all()
    output = []
    if not user:
        return jsonify({'message':"User not found"})
    
    for i in user:
        user_data = {}
        user_data['p_id'] = user.p_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['pssword'] = user.pssword
        output.append(user_data)

    return jsonify({'user':output})

if __name__ == "__main__":
    app.run(debug=True)
