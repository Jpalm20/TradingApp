import os
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import src.handlers.userHandler as userHandler
import src.handlers.tradeHandler as tradeHandler
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET', 'sample key')
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
#Creating a Token 

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)



@app.route('/token', methods=['POST'])
def handle_hello():
    
    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }



@app.route('/')
def hello_geek():
    return 'Health Check'

@app.route('/user/register',methods = ['POST'])
def register_user():
    if request.method == 'POST':
        return userHandler.registerUser(request.json)

@app.route('/user/login',methods = ['POST'])
def validate_user():
    if request.method == 'POST':
        return userHandler.validateUser(request.json)     

@app.route('/user/trades/<int:user_id>',methods = ['GET'])
def user_trades(user_id):
    if request.method == 'GET':
        return userHandler.getUserTrades(user_id)   

@app.route('/user/pnlbyYear/<int:user_id>/<int:date_year>',methods = ['GET'])
def pnl_year(user_id, date_year):
    if request.method == 'GET':
        return userHandler.getPnLbyYear(user_id, date_year)  

@app.route('/trade/create',methods= ['POST'])
def log_trade():
    if request.method == 'POST':
        return tradeHandler.logTrade(request.json) 

@app.route('/user/<int:user_id>',methods = ['GET','POST','DELETE'])
def existing_user(user_id):
    if request.method == 'GET':
        return userHandler.getExistingUser(user_id)
    elif request.method == 'POST':
        return userHandler.editExistingUser(user_id,request.json)
    if request.method == 'DELETE':
        return userHandler.deleteExistingUser(user_id)

@app.route('/trade/<int:trade_id>',methods = ['GET','POST','DELETE'])
def existing_trade(trade_id):
    if request.method == 'GET':
        return tradeHandler.getExistingTrade(trade_id)
    elif request.method == 'POST':
        return tradeHandler.editExistingTrade(trade_id,request.json)
    if request.method == 'DELETE':
        return tradeHandler.deleteExistingTrade(trade_id)

if __name__ == "__main__":
    app.run(debug=True)