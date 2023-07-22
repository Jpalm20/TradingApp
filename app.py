import os
from flask import Flask, jsonify, render_template
from flask import request
from flask_cors import CORS
import base64
import src.handlers.userHandler as userHandler
import src.handlers.tradeHandler as tradeHandler
import src.handlers.sessionHandler as sessionHandler
import src.models.accountvalue as accountValue
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET')
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
jwt = JWTManager(app)

app.config['SMTP_USERNAME'] = os.environ.get('SMTP_USERNAME')
app.config['SMTP_PASSWORD'] = os.environ.get('SMTP_PASSWORD')


@app.route('/')
def index():
    return 'Health Check'


@app.route('/user/register',methods = ['POST'])
def register_user():
    if request.method == 'POST':
        return userHandler.registerUser(request.json)


@app.route('/user/login',methods = ['POST'])
def validate_user():
    if request.method == 'POST':
        return userHandler.validateUser(request.json)
    
    
@app.route('/user/preferences',methods = ['GET'])
def get_user_preferences():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            user_id = message2
            if request.method == 'GET':
                return userHandler.getUserPreferences(user_id)
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
        

@app.route('/user/preferences/toggleav',methods = ['POST'])
def toggle_account_value_tracking():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            user_id = message2
            if request.method == 'POST':
                return userHandler.toggleAvTracking(user_id)
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


@app.route('/user/trades',methods = ['GET'])
def user_trades():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            user_id = message2
            if request.args:
                if request.method == 'GET':
                    return userHandler.getUserTrades(user_id, request.args) 
            else: 
                if request.method == 'GET':
                    return userHandler.getUserTrades(user_id) 
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
        

@app.route('/user/trades/stats',methods = ['GET'])
def user_trades_stats():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            user_id = message2
            if request.args:
                if request.method == 'GET':
                    return userHandler.getUserTradesStats(user_id, request.args) 
            else: 
                if request.method == 'GET':
                    return userHandler.getUserTradesStats(user_id) 
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
        
        
@app.route('/user/accountValue',methods = ['GET', 'POST'])
def user_account_value():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            user_id = message2
            if request.method == 'GET':
                return userHandler.getAccountValue(user_id)
            if request.method == 'POST':
                return userHandler.setAccountValue(user_id,request.json)
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
        
        
@app.route('/accountValueJob',methods = ['POST'])
def account_value_job():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_parts = auth_header.split()
        if len(auth_parts) == 2 and auth_parts[0].lower() == 'basic':
            credentials = auth_parts[1]
            username, password = base64.b64decode(credentials).decode('utf-8').split(':')
            if username == app.config['SMTP_USERNAME'] and password == app.config['SMTP_PASSWORD']:
                if request.method == 'POST':
                    return {
                        "result": accountValue.Accountvalue.accountValueJob()
                    }, 200
            else:
                return {
                    "result": "Invalid Credentials"
                }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401
        
        
@app.route('/user/trades/page',methods = ['GET'])
def user_trades_page():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            if request.args:
                if request.method == 'GET':
                    user_id = message2
                    return userHandler.getUserTradesPage(user_id, request.args) 
            else: 
                return {
                    "result": "Please include Page Number and Rows per Page"
                }, 400
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
        

@app.route('/trade/searchTicker',methods = ['GET'])
def search_user_ticker():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            if request.args:
                if request.method == 'GET':
                    user_id = message2
                    return tradeHandler.searchUserTicker(user_id, request.args)
            else: 
                if request.method == 'GET':
                    user_id = message2
                    return tradeHandler.searchUserTicker(user_id)
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
  

@app.route('/user/pnlbyYear/<int:date_year>',methods = ['GET'])
def pnl_year(date_year):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            user_id = message2
            if request.args:
                if request.method == 'GET':
                    return userHandler.getPnLbyYear(user_id, date_year, request.args) 
            else:
                if request.method == 'GET':
                    return userHandler.getPnLbyYear(user_id, date_year)
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
     

@app.route('/trade/create',methods= ['POST'])
def log_trade():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            if request.method == 'POST':
                user_id = message2
                return tradeHandler.logTrade(user_id, request.json) 
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
  

@app.route('/user/reportBug',methods= ['POST'])
def report_bug():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getEmailFromToken(auth_token)
        if eval and eval2:
            if request.method == 'POST':
                email = message2
                return userHandler.reportBug(request.json, email) 
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
              
        
@app.route('/user/changePassword',methods= ['POST'])
def change_Password():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            if request.method == 'POST':
                user_id = message2
                return userHandler.changePassword(user_id, request.json) 
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


@app.route('/user',methods = ['GET','POST','DELETE'])
def existing_user():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        eval2,message2 = sessionHandler.getUserFromToken(auth_token)
        if eval and eval2:
            user_id = message2
            if request.method == 'GET':
                return userHandler.getExistingUser(user_id)
            elif request.method == 'POST':
                return userHandler.editExistingUser(user_id,request.json)
            if request.method == 'DELETE':
                return userHandler.deleteExistingUser(user_id)
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
        

@app.route('/trade/exportCsv',methods = ['POST'])
def export_csv():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        eval,message = sessionHandler.validateToken(auth_token)
        if eval:
            if request.method == 'POST':
                return tradeHandler.exportCsv(request.json)
        else:
            return {
                "result": message
            }, 401
    else:
        return {
            "result": "Authorization Header is Missing"
        }, 401
        

@app.route('/user/generateResetCode',methods = ['POST'])
def generate_reset_code():
    if request.method == 'POST':
        return userHandler.generateResetCode(request.json)
    
    
@app.route('/user/confirmResetCode',methods = ['POST'])
def validate_reset_code():
    if request.method == 'POST':
        return userHandler.validateResetCode(request.json)
    

@app.route('/user/resetPassword',methods = ['POST'])
def reset_password():
    if request.method == 'POST':
        return userHandler.resetPassword(request.json)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)