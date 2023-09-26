from ftplib import error_reply
import os
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
import base64
import src.handlers.userHandler as userHandler
import src.handlers.tradeHandler as tradeHandler
import src.handlers.sessionHandler as sessionHandler
import src.handlers.journalentryHandler as journalentryHandler
import src.models.accountvalue as accountValue
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET')
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
jwt = JWTManager(app)

app.config['SMTP_USERNAME'] = os.environ.get('SMTP_USERNAME')
app.config['SMTP_PASSWORD'] = os.environ.get('SMTP_PASSWORD')


@app.route('/')
def hello_geek():
    logger.info("Health Check")
    return 'Health Check'


@app.route('/user/register',methods = ['POST'])
def register_user():
    logger.info("Entering Register User - " + str(request.method) + ": " + str(request.json))
    try:
        if request.method == 'POST':
            response = userHandler.registerUser(request.json)
            logger.info("Leaving Register User: " + str(response))
            return response
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Register User: " + error_message)
        return {
            "result": error_message
        }, 400


@app.route('/user/login',methods = ['POST'])
def validate_user():
    logger.info("Entering Validate User - " + str(request.method) + ": " + str(request.json))
    try:
        if request.method == 'POST':
            response = userHandler.validateUser(request.json)
            logger.info("Leaving Validate User: " + str(response))
            return response
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Validate User: " + error_message)
        return {
            "result": error_message
        }, 400
    
@app.route('/user/preferences',methods = ['GET'])
def get_user_preferences():
    logger.info("Entering User Preferences - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.method == 'GET':
                    response = userHandler.getUserPreferences(user_id)
                    logger.info("Leaving User Preferences: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving User Preferences: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving User Preferences: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving User Preferences: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving User Preferences: " + error_message)
        return {
            "result": error_message
        }, 400
        

@app.route('/user/preferences/toggleav',methods = ['POST'])
def toggle_account_value_tracking():
    logger.info("Entering Toggle Account Value Tracking - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.method == 'POST':
                    response = userHandler.toggleAvTracking(user_id)
                    logger.info("Leaving Toggle Account Value Tracking: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving Toggle Account Value Tracking: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving Toggle Account Value Tracking: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Toggle Account Value Tracking: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Toggle Account Value Tracking: " + error_message)
        return {
            "result": error_message
        }, 400
        
        
@app.route('/user/preferences/toggleeoi',methods = ['POST'])
def toggle_email_optin_flag():
    logger.info("Entering Toggle Email Alerts - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.method == 'POST':
                    response = userHandler.toggleEmailOptInHandler(user_id)
                    logger.info("Leaving Toggle Email Alerts: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving Toggle Email Alerts: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving Toggle Email Alerts: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Toggle Email Alerts: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Toggle Email Alerts: " + error_message)
        return {
            "result": error_message
        }, 400


@app.route('/user/getUserFromSession',methods= ['GET'])
def user_from_session():
    logger.info("Entering Get User From Session - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            if eval:
                if request.method == 'GET':
                    response = userHandler.getUserFromSession(auth_token)
                    logger.info("Leaving Get User From Session: " + str(response))
                    return response
            else:
                logger.warning("Leaving Get User From Session: " + str(message))
                return {
                    "result": message
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Get User From Session: " + response)
            return {
                "result": response
            }, 401    
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Get User From Session: " + error_message)
        return {
            "result": error_message
        }, 400


@app.route('/user/trades',methods = ['GET'])
def user_trades():
    logger.info("Entering User Trades - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.args:
                    if request.method == 'GET':
                        response = userHandler.getUserTrades(user_id, request.args) 
                        logger.info("Leaving User Trades with Filters: " + str(response))
                        return response
                else: 
                    if request.method == 'GET':
                        response = userHandler.getUserTrades(user_id) 
                        logger.info("Leaving User Trades without Filters: " + str(response))
                        return response
            elif not eval:
                logger.warning("Leaving User Trades: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving User Trades: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving User Trades: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving User Trades: " + error_message)
        return {
            "result": error_message
        }, 400
        

@app.route('/user/trades/stats',methods = ['GET'])
def user_trades_stats():
    logger.info("Entering User Trade Stats - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.args:
                    if request.method == 'GET':
                        response = userHandler.getUserTradesStats(user_id, request.args) 
                        logger.info("Leaving User Trade Stats with Filters: " + str(response))
                        return response
                else: 
                    if request.method == 'GET':
                        response = userHandler.getUserTradesStats(user_id) 
                        logger.info("Leaving User Trade Stats without Filters: " + str(response))
                        return response
            elif not eval:
                logger.warning("Leaving User Trade Stats: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving User Trade Stats: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving User Trade Stats: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving User Trade Stats: " + error_message)
        return {
            "result": error_message
        }, 400
        
        
@app.route('/user/accountValue',methods = ['GET', 'POST'])
def user_account_value():
    logger.info("Entering User Account Value - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.method == 'GET':
                    if request.args:
                        user_id = message2
                        response = userHandler.getAccountValue(user_id, request.args)
                        logger.info("Leaving User Account Value: " + str(response))
                        return response
                    else: 
                        response = "Please include filter parameter 'date'"
                        logger.warning("Leaving User Account Value: " + response)
                        return {
                            "result": response
                        }, 400
                if request.method == 'POST':
                    response = userHandler.setAccountValue(user_id,request.json)
                    logger.info("Leaving User Account Value: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving User Account Value: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving User Account Value: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving User Account Value: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving User Account Value: " + error_message)
        return {
            "result": error_message
        }, 400
        
        
@app.route('/accountValueJob',methods = ['POST'])
def account_value_job():
    logger.info("Account Value Job Triggered - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_parts = auth_header.split()
            if len(auth_parts) == 2 and auth_parts[0].lower() == 'basic':
                credentials = auth_parts[1]
                username, password = base64.b64decode(credentials).decode('utf-8').split(':')
                if username == app.config['SMTP_USERNAME'] and password == app.config['SMTP_PASSWORD']:
                    if request.method == 'POST':
                        response = accountValue.Accountvalue.accountValueJob()
                        logger.info("Leaving Account Value Job: " + str(response))
                        return {
                            "result": response
                        }, 200
                else:
                    response = "Invalid Credentials"
                    logger.warning("Leaving Account Value Job: " + response)
                    return {
                        "result": response
                    }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Account Value Job: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Account Value Job: " + error_message)
        return {
            "result": error_message
        }, 400
        
        
@app.route('/user/trades/page',methods = ['GET'])
def user_trades_page():
    logger.info("Entering User Trade Pagination - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                if request.args:
                    if request.method == 'GET':
                        user_id = message2
                        response = userHandler.getUserTradesPage(user_id, request.args) 
                        logger.info("Leaving User Trade Pagination: " + str(response))
                        return response
                else: 
                    reponse = "Please include Page Number and Rows per Page"
                    logger.warning("Leaving User Trade Pagination: " + response)
                    return {
                        "result": response
                    }, 400
            elif not eval:
                logger.warning("Leaving User Trade Pagination: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving User Trade Pagination: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving User Trade Pagination: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving User Trade Pagination: " + error_message)
        return {
            "result": error_message
        }, 400
        

@app.route('/trade/searchTicker',methods = ['GET'])
def search_user_ticker():
    logger.info("Entering Search User Ticker - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                if request.args:
                    if request.method == 'GET':
                        user_id = message2
                        response = tradeHandler.searchUserTicker(user_id, request.args)
                        logger.info("Leaving Search User Ticker with Filters: " + str(response))
                        return response
                else: 
                    if request.method == 'GET':
                        user_id = message2
                        response = tradeHandler.searchUserTicker(user_id)
                        logger.info("Leaving Search User Ticker without Filters: " + str(response))
                        return response
            elif not eval:
                logger.warning("Leaving Search User Ticker: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving Search User Ticker: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Search User Ticker: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Search User Ticker: " + error_message)
        return {
            "result": error_message
        }, 400
  

@app.route('/user/pnlbyYear/<int:date_year>',methods = ['GET'])
def pnl_year(date_year):
    logger.info("Entering PnL by Year - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.args:
                    if request.method == 'GET':
                        response = userHandler.getPnLbyYear(user_id, date_year, request.args) 
                        logger.info("Leaving PnL by Year with Filters: " + str(response))
                        return response
                else:
                    if request.method == 'GET':
                        response = userHandler.getPnLbyYear(user_id, date_year)
                        logger.info("Leaving PnL by Year without Filters: " + str(response))
                        return response
            elif not eval:
                logger.warning("Leaving PnL by Year: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving PnL by Year: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving PnL by Year: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving PnL by Year: " + error_message)
        return {
            "result": error_message
        }, 400
     

@app.route('/trade/create',methods= ['POST'])
def log_trade():
    logger.info("Entering Log Trade - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                if request.method == 'POST':
                    user_id = message2
                    response = tradeHandler.logTrade(user_id, request.json) 
                    logger.info("Leaving Log Trade: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving Log Trade: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving Log Trade: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Log Trade: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Log Trade: " + error_message)
        return {
            "result": error_message
        }, 400
        

@app.route('/trade/importCsv',methods= ['POST'])
def import_csv():
    logger.info("Entering Import CSV - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                if request.method == 'POST':
                    file = request.files["csv_file"]
                    user_id = message2
                    response = tradeHandler.importCsv(file, user_id) 
                    logger.info("Leaving Import CSV: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving Import CSV: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving Import CSV: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Import CSV: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Import CSV: " + error_message)
        return {
            "result": error_message
        }, 400
  

@app.route('/user/reportBug',methods= ['POST'])
def report_bug():
    logger.info("Entering Report Bug - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getEmailFromToken(auth_token)
            if eval and eval2:
                if request.method == 'POST':
                    email = message2
                    response = userHandler.reportBug(request.json, email) 
                    logger.info("Leaving Report Bug: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving Report Bug: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving Report Bug: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Report Bug: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Report Bug: " + error_message)
        return {
            "result": error_message
        }, 400
              
        
@app.route('/user/changePassword',methods= ['POST'])
def change_Password():
    logger.info("Entering Change Password - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                if request.method == 'POST':
                    user_id = message2
                    response = userHandler.changePassword(user_id, request.json) 
                    logger.info("Leaving Change Password: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving Change Password: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving Change Password: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Change Password: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Change Password: " + error_message)
        return {
            "result": error_message
        }, 400
    
        
@app.route('/user/logout',methods= ['POST'])
def logout_session():
    logger.info("Entering Logout Session - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            if eval:
                if request.method == 'POST':
                    response = sessionHandler.logoutSession(auth_token) 
                    logger.info("Leaving Logout Session: " + str(response))
                    return response
            else:
                logger.warning("Leaving Logout Session: " + str(message))
                return {
                    "result": message
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Logout Session: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Logout Session: " + error_message)
        return {
            "result": error_message
        }, 400


@app.route('/user',methods = ['GET','POST','DELETE'])
def existing_user():
    logger.info("Entering Existing User - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.method == 'GET':
                    response = userHandler.getExistingUser(user_id)
                    logger.info("Leaving Existing User: " + str(response))
                    return response
                elif request.method == 'POST':
                    response = userHandler.editExistingUser(user_id,request.json)
                    logger.info("Leaving Existing User: " + str(response))
                    return response
                if request.method == 'DELETE':
                    response = userHandler.deleteExistingUser(user_id)
                    logger.info("Leaving Existing User: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving Existing User: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving Existing User: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Existing User: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Existing User: " + error_message)
        return {
            "result": error_message
        }, 400


@app.route('/trade/<int:trade_id>',methods = ['GET','POST','DELETE'])
def existing_trade(trade_id):
    logger.info("Entering Existing Trade - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            if eval:
                if request.method == 'GET':
                    response = tradeHandler.getExistingTrade(trade_id)
                    logger.info("Leaving Existing Trade: " + str(response))
                    return response
                elif request.method == 'POST':
                    response = tradeHandler.editExistingTrade(trade_id,request.json)
                    logger.info("Leaving Existing Trade: " + str(response))
                    return response
                if request.method == 'DELETE':
                    response = tradeHandler.deleteExistingTrade(trade_id)
                    logger.info("Leaving Existing Trade: " + str(response))
                    return response
            else:
                logger.warning("Leaving Existing Trade: " + str(message))
                return {
                    "result": message
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Existing Trade: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Existing Trade: " + error_message)
        return {
            "result": error_message
        }, 400
        
@app.route('/trade/deleteTrades',methods = ['DELETE'])
def delete_trades():
    logger.info("Entering Delete Trades - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            if eval:
                if request.method == 'DELETE':
                    response = tradeHandler.deleteTrades(request.json)
                    logger.info("Leaving Delete Trades: " + str(response))
                    return response
            else:
                logger.warning("Leaving Delete Trades: " + str(message))
                return {
                    "result": message
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Delete Trades: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Delete Trades: " + error_message)
        return {
            "result": error_message
        }, 400
        

@app.route('/trade/exportCsv',methods = ['POST'])
def export_csv():
    logger.info("Entering Export CSV - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            if eval:
                if request.method == 'POST':
                    response = tradeHandler.exportCsv(request.json)
                    logger.info("Leaving Export CSV: " + str(response))
                    return response
            else:
                logger.warning("Leaving Export CSV: " + str(message))
                return {
                    "result": message
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Export CSV: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Export CSV: " + error_message)
        return {
            "result": error_message
        }, 400
        

@app.route('/user/generateResetCode',methods = ['POST'])
def generate_reset_code():
    logger.info("Entering Generate Reset Code - " + str(request.method) + ": " + str(request.json))
    try:
        if request.method == 'POST':
            response = userHandler.generateResetCode(request.json)
            logger.info("Leaving Generate Reset Code: " + str(response))
            return response
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Generate Reset Code: " + error_message)
        return {
            "result": error_message
        }, 400
    
    
@app.route('/user/confirmResetCode',methods = ['POST'])
def validate_reset_code():
    logger.info("Entering Validate Reset Code - " + str(request.method) + ": " + str(request.json))
    try:
        if request.method == 'POST':
            response = userHandler.validateResetCode(request.json)
            logger.info("Leaving Validate Reset Code: " + str(response))
            return response
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Validate Reset Code: " + error_message)
        return {
            "result": error_message
        }, 400
    

@app.route('/user/resetPassword',methods = ['POST'])
def reset_password():
    logger.info("Entering Reset Password - " + str(request.method) + ": " + str(request.json))
    try:
        if request.method == 'POST':
            response = userHandler.resetPassword(request.json)
            logger.info("Leaving Reset Password: " + str(response))
            return response
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Reset Password: " + error_message)
        return {
            "result": error_message
        }, 400
        

@app.route('/journal/<string:date>',methods = ['GET','POST','DELETE'])
def existing_journalentry(date):
    logger.info("Entering Existing Journal Entry - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.method == 'GET':
                    response = journalentryHandler.getJournalEntries(user_id, date)
                    logger.info("Leaving Existing Journal Entry: " + str(response))
                    return response
                elif request.method == 'POST':
                    response = journalentryHandler.postJournalEntry(user_id, date, request.json)
                    logger.info("Leaving Existing Journal Entry: " + str(response))
                    return response
                if request.method == 'DELETE':
                    response = journalentryHandler.deleteJournalEntry(user_id, date)
                    logger.info("Leaving Existing Journal Entry: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving Existing Journal Entry: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving Existing Journal Entry: " + str(message2))
                return {
                    "result": message2
                }, 401
        else:
            response = "Authorization Header is Missing"
            logger.warning("Leaving Existing Journal Entry: " + response)
            return {
                "result": response
            }, 401
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        logger.error("Leaving Existing Journal Entry: " + error_message)
        return {
            "result": error_message
        }, 400


if __name__ == "__main__":
    app.run(debug=True)