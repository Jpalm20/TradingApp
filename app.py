import os
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
import src.handlers.userHandler as userHandler
import src.handlers.tradeHandler as tradeHandler
import src.handlers.sessionHandler as sessionHandler
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET')
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
jwt = JWTManager(app)


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

@app.route('/user/getUserFromSession',methods= ['GET'])
def user_from_session():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.method == 'GET':
                return userHandler.getUserFromSession(auth_token)
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401    

@app.route('/user/trades/<int:user_id>',methods = ['GET'])
def user_trades(user_id):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.args is not None:
                if request.method == 'GET':
                    return userHandler.getUserTrades(user_id, request.args) 
            else: 
                if request.method == 'GET':
                    return userHandler.getUserTrades(user_id) 
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401
  

@app.route('/user/pnlbyYear/<int:user_id>/<int:date_year>',methods = ['GET'])
def pnl_year(user_id, date_year):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.args is not None:
                if request.method == 'GET':
                    return userHandler.getPnLbyYear(user_id, date_year, request.args) 
                else:
                    return userHandler.getPnLbyYear(user_id, date_year)
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401
     

@app.route('/trade/create',methods= ['POST'])
def log_trade():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.method == 'POST':
                return tradeHandler.logTrade(request.json) 
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401
        

@app.route('/trade/importCsv',methods= ['POST'])
def import_csv():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            if request.method == 'POST':
                file = request.files["csv_file"]
                user_id = message2
                return tradeHandler.importCsv(file, user_id) 
        elif not eval:
            return {
                "result": message
            }, 401
        else:
            return {
                "result": message2
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401
        
        
@app.route('/user/changePassword/<int:user_id>',methods= ['POST'])
def change_Password(user_id):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.method == 'POST':
                return userHandler.changePassword(user_id, request.json) 
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401
        

@app.route('/user/reportBug',methods= ['POST'])
def report_bug():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.method == 'POST':
                return userHandler.reportBug(request.json) 
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401
        
@app.route('/user/logout',methods= ['POST'])
def logout_session():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.method == 'POST':
                return sessionHandler.logoutSession(auth_token) 
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401


@app.route('/user/<int:user_id>',methods = ['GET','POST','DELETE'])
def existing_user(user_id):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.method == 'GET':
                return userHandler.getExistingUser(user_id)
            elif request.method == 'POST':
                return userHandler.editExistingUser(user_id,request.json)
            if request.method == 'DELETE':
                return userHandler.deleteExistingUser(user_id)
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401


@app.route('/trade/<int:trade_id>',methods = ['GET','POST','DELETE'])
def existing_trade(trade_id):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.method == 'GET':
                return tradeHandler.getExistingTrade(trade_id)
            elif request.method == 'POST':
                return tradeHandler.editExistingTrade(trade_id,request.json)
            if request.method == 'DELETE':
                return tradeHandler.deleteExistingTrade(trade_id)
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401
        
@app.route('/trade/deleteTrades',methods = ['DELETE'])
def delete_trades():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.method == 'DELETE':
                return tradeHandler.deleteTrades(request.json)
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401


if __name__ == "__main__":
    app.run(debug=True)