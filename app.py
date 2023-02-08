from flask import Flask
from flask import request
from flask_cors import CORS
import src.handlers.userHandler as userHandler
import src.handlers.tradeHandler as tradeHandler

app = Flask(__name__)
CORS(app)

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