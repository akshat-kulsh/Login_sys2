from flask import Flask, request, jsonify, make_response
from flask_login import current_user
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = "thisissecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:akshat0509@localhost/login_sys"

db = SQLAlchemy(app)
db1 = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user_table'
    idusers = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(30))
    pssword = db.Column(db.String(100))
    p_id = db.Column(db.Integer)

class adUnit(db1.Model):
    __tablename__ = 'ad_Unit'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.idusers))
    user_table = db.relationship("User", backref=db.backref("user_table", uselist=False))
    page_name = db.Column(db.String(30))
    adUnitSize = db.Column(db.String(40))
    adLink = db.Column(db.String(100))

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

@app.route('/login', methods=["POST"])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response("Need more arguments")
    
    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response("User doesn't exist")
    
    if bcrypt.check_password_hash(user.pssword, auth.password):
        token = create_access_token(identity=auth.username)
        #token = jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({ "token": token })
    return make_response("incorrect password")

@app.route('/user', methods=['GET'])
@jwt_required()
def user_info():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/save_ad_unit', methods=['POST'])
@login_manager.user_loader
def save_ad():
    data = request.get_json()
    query = "SELECT idusers FROM user_table WHERE email = '%s'" %(current_user,)
    user_id = db.engine.execute(query)
    print(user_id, type(user_id))
    save_ad = adUnit(page_name=data['page_name'], adUnitSize=data['adUnitSize'], adLink=data['adLink'], user_id= user_id )
    db1.session.add(save_ad)
    db1.session.commit()
    return jsonify({"message":"New Ad Unit created"},data)


@app.route('/load_ad_unit', methods=["GET"])
def load_ad():
    return jsonify()

if __name__ == "__main__":
    app.run(debug=True)
