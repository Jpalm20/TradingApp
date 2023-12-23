from ftplib import error_reply
import os
from flask import Flask, jsonify, render_template
from flask import request
from flask_cors import CORS
import redis
from datetime import datetime
import hashlib
import json
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
from urllib.parse import urlparse


app = Flask(__name__)
CORS(app)

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

if 'REDIS_PASSWORD' in os.environ:
    url = urlparse(os.environ.get('REDIS_TLS_URL'))
    redis_client = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None, decode_responses=True)
else:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True
    )

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

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
            if 'user_id' in response:
                user_id = response['user_id']
                key = f'user:{user_id}'
                redis_client.setex(key, 14400, json.dumps(response))
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
    logger.info("Entering User Preferences - " + str(request.method))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.method == 'GET':
                    key = f'preferences:{user_id}'
                    cached_data = redis_client.get(key)
                    if cached_data:
                        logger.info("Leaving User Preferences (Cache Hit): " + cached_data)
                        return json.loads(cached_data)
                    response = userHandler.getUserPreferences(user_id)
                    if 'account_value_optin' in response:
                        redis_client.setex(key, 14400, json.dumps(response))
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
                    if 'account_value_optin' in response:
                        key = f'preferences:{user_id}'
                        redis_client.setex(key, 14400, json.dumps(response))
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
                    if 'account_value_optin' in response:
                        key = f'preferences:{user_id}'
                        redis_client.setex(key, 14400, json.dumps(response))
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
    logger.info("Entering Get User From Session - " + str(request.method))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.method == 'GET':
                    key = f'user:{user_id}'
                    cached_data = redis_client.get(key)
                    if cached_data:
                        logger.info("Leaving Get User From Session (Cache Hit): " + cached_data)
                        return json.loads(cached_data)
                    response = userHandler.getUserFromSession(auth_token)
                    if 'user_id' in response:
                        redis_client.setex(key, 14400, json.dumps(response))
                    logger.info("Leaving Get User From Session: " + str(response))
                    return response
            elif not eval:
                logger.warning("Leaving Get User From Session: " + str(message))
                return {
                    "result": message
                }, 401
            else:
                logger.warning("Leaving Get User From Session: " + str(message2))
                return {
                    "result": message2
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
    logger.info("Entering User Trades - " + str(request.method))
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
                        #need to check for filters key in redis and then confirm filters are still same and havent changed otherwise need to go to db
                        filter_criteria_json = json.dumps(request.args)
                        filter_hash = hashlib.md5(filter_criteria_json.encode()).hexdigest()
                        key = f"trades:{user_id}:{filter_hash}"
                        cached_data = redis_client.get(key)
                        if cached_data:
                            logger.info("Leaving User Trades with Filters (Cache Hit): " + cached_data)
                            return json.loads(cached_data)
                        response = userHandler.getUserTrades(user_id, request.args) 
                        if 'trades' in response:
                            redis_client.setex(key, 14400, json.dumps(response))
                        #need to set filters key as well to compare next time
                        logger.info("Leaving User Trades with Filters: " + str(response))
                        return response
                else: 
                    if request.method == 'GET':
                        #need to check for filters key in redis and then confirm filters are still none and havent changed
                        key = f"trades:{user_id}:no_filter"
                        cached_data = redis_client.get(key)
                        if cached_data:
                            logger.info("Leaving User Trades without Filters (Cache Hit): " + cached_data)
                            return json.loads(cached_data)
                        response = userHandler.getUserTrades(user_id) 
                        if 'trades' in response:
                            redis_client.setex(key, 14400, json.dumps(response))
                        #need to set filters key to none as well to compare next time
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
    logger.info("Entering User Trade Stats - " + str(request.method))
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
                        #need to check for filters key in redis and then confirm filters are still same and havent changed otherwise need to go to db
                        filter_criteria_json = json.dumps(request.args)
                        filter_hash = hashlib.md5(filter_criteria_json.encode()).hexdigest()
                        key = f"stats:{user_id}:{filter_hash}"
                        cached_data = redis_client.get(key)
                        if cached_data:
                            logger.info("Leaving User Trade Stats with Filters (Cache Hit): " + cached_data)
                            return json.loads(cached_data)
                        response = userHandler.getUserTradesStats(user_id, request.args) 
                        if 'stats' in response:
                            redis_client.setex(key, 14400, json.dumps(response))
                        #need to set filters key as well to compare next time 
                        logger.info("Leaving User Trade Stats with Filters: " + str(response))
                        return response
                else: 
                    if request.method == 'GET':
                        #need to check for filters key in redis and then confirm filters are still none and havent changed
                        key = f"stats:{user_id}:no_filter"
                        cached_data = redis_client.get(key)
                        if cached_data:
                            logger.info("Leaving User Trade Stats without Filters (Cache Hit): " + cached_data)
                            return json.loads(cached_data)
                        response = userHandler.getUserTradesStats(user_id) 
                        if 'stats' in response:
                            redis_client.setex(key, 14400, json.dumps(response))
                        #need to set filters key to none as well to compare next time
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
    if request.method == 'POST':
        logger.info("Entering User Account Value - " + str(request.method) + ": " + str(request.json))
    if request.method == 'GET':
        logger.info("Entering User Account Value - " + str(request.method))
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
                        #need to check for filters key in redis and then confirm filters are still same and havent changed otherwise need to go to db
                        filter_criteria_json = json.dumps(request.args)
                        filter_hash = hashlib.md5(filter_criteria_json.encode()).hexdigest()
                        key = f"accountvalues:{user_id}:{filter_hash}"
                        cached_data = redis_client.get(key)
                        if cached_data:
                            logger.info("Leaving User Account Value (Cache Hit): " + cached_data)
                            return json.loads(cached_data)
                        response = userHandler.getAccountValue(user_id, request.args)
                        if 'accountvalues' in response:
                            redis_client.setex(key, 14400, json.dumps(response))
                        #need to set filters key as well to compare next time 
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
                    #Need to be able to update object to update this single value in the key object of multiple values
                    if 'accountvalue' in response:
                        user_keys = redis_client.keys(f'accountvalues:{user_id}:*')

                        # Iterate through the user's keys and update the JSON objects
                        for key in user_keys:
                            # Get the existing JSON object from Redis
                            existing_json = json.loads(redis_client.get(key))

                            # Search for the date_to_check within the "accountvalues" array
                            for item in existing_json.get("accountvalues", []):
                                if item.get("date") == response['date']:
                                    # Update the "accountvalue" field for the matching date
                                    item["accountvalue"] = response['accountvalue']

                                    # Save the updated JSON object back to Redis
                                    redis_client.setex(key, 3600, json.dumps(existing_json))
                                    break  # Exit the loop after the update
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
    logger.info("Entering User Trade Pagination - " + str(request.method))
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
                        #need to check for filters key in redis and then confirm filters are still same and havent changed otherwise need to go to db
                        filter_criteria_json = json.dumps(request.args)
                        filter_hash = hashlib.md5(filter_criteria_json.encode()).hexdigest()
                        key = f"tradespage:{user_id}:{filter_hash}"
                        cached_data = redis_client.get(key)
                        if cached_data:
                            logger.info("Leaving User Trade Pagination (Cache Hit): " + cached_data)
                            return json.loads(cached_data)
                        response = userHandler.getUserTradesPage(user_id, request.args) 
                        if 'page' in response:
                            redis_client.setex(key, 14400, json.dumps(response))
                        #need to set filters key as well to compare next time
                        logger.info("Leaving User Trade Pagination: " + str(response))
                        return response
                else: 
                    response = "Please include Page Number and Rows per Page"
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
    logger.info("Entering Search User Ticker - " + str(request.method))
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
                        #need to check for filters key in redis and then confirm filters are still same and havent changed otherwise need to go to db
                        filter_criteria_json = json.dumps(request.args)
                        filter_hash = hashlib.md5(filter_criteria_json.encode()).hexdigest()
                        key = f"tickersearch:{user_id}:{filter_hash}"
                        cached_data = redis_client.get(key)
                        if cached_data:
                            logger.info("Leaving Search User Ticker with Filters (Cache Hit): " + cached_data)
                            return json.loads(cached_data)
                        response = tradeHandler.searchUserTicker(user_id, request.args)
                        if 'tickers' in response:
                            redis_client.setex(key, 14400, json.dumps(response))
                        #need to set filters key as well to compare next time
                        logger.info("Leaving Search User Ticker with Filters: " + str(response))
                        return response
                else: 
                    if request.method == 'GET':
                        user_id = message2
                        #need to check for filters key in redis and then confirm filters are still none and havent changed otherwise need to go to db
                        key = f"tickersearch:{user_id}:no_filter"
                        cached_data = redis_client.get(key)
                        if cached_data:
                            logger.info("Leaving Search User Ticker without Filters (Cache Hit): " + cached_data)
                            return json.loads(cached_data)
                        response = tradeHandler.searchUserTicker(user_id)
                        if 'tickers' in response:
                            redis_client.setex(key, 14400, json.dumps(response))
                        #need to set filters key to none as well to compare next time
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
    logger.info("Entering PnL by Year - " + str(request.method))
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
                        #This cache entry will need to be basded on user_id and year
                        filter_criteria_json = json.dumps(request.args)
                        filter_hash = hashlib.md5(filter_criteria_json.encode()).hexdigest()
                        key = f"pnlyear:{user_id}:{date_year}:{filter_hash}"
                        cached_data = redis_client.get(key)
                        if cached_data:
                            logger.info("Leaving PnL by Year with Filters (Cache Hit): " + cached_data)
                            return json.loads(cached_data)
                        response = userHandler.getPnLbyYear(user_id, date_year, request.args) 
                        if 'months' in response:
                            redis_client.setex(key, 14400, json.dumps(response))
                        logger.info("Leaving PnL by Year with Filters: " + str(response))
                        return response
                else:
                    if request.method == 'GET':
                        key = f"pnlyear:{user_id}:{date_year}:no_filter"
                        cached_data = redis_client.get(key)
                        if cached_data:
                            logger.info("Leaving PnL by Year without Filters (Cache Hit): " + cached_data)
                            return json.loads(cached_data)
                        response = userHandler.getPnLbyYear(user_id, date_year)
                        if 'months' in response:
                            redis_client.setex(key, 14400, json.dumps(response))
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
                    #Need to delte all affected cache keys here (trades, stats, accountvalues, tradespage, tickersearch, pnlyear) 
                    # confirm above is all and will need to do this for all endpoints that directly edit trades, etc.
                    if 'trade_id' in response:
                        #delete all affected keys, too costly to update them
                        top_level_keys = [
                            'trades',
                            'stats',
                            'accountvalues',
                            'tradespage',
                            'tickersearch',
                            'pnlyear'
                        ]
                        for key in top_level_keys:
                            pattern = f'{key}:{user_id}:*'
                            keys_to_delete = redis_client.keys(pattern)
                            if keys_to_delete:
                                redis_client.delete(*keys_to_delete)
                        #add key for this trade id
                        trade_id = response['trade_id']
                        key = f'trade:{trade_id}'
                        redis_client.setex(key, 14400, json.dumps(response))
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
                    if 'trades' in response:
                        #delete all affected keys, too costly to update them
                        top_level_keys = [
                            'trades',
                            'stats',
                            'accountvalues',
                            'tradespage',
                            'tickersearch',
                            'pnlyear'
                        ]
                        for key in top_level_keys:
                            pattern = f'{key}:{user_id}:*'
                            keys_to_delete = redis_client.keys(pattern)
                            if keys_to_delete:
                                redis_client.delete(*keys_to_delete)
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
    if request.method == 'GET':
        logger.info("Entering Existing User - " + str(request.method))
    if request.method == 'POST' or request.method == 'DELETE':
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
                    #cache entry will be based on user_id if user_id same then no need to go to backend
                    key = f'user:{user_id}'
                    cached_data = redis_client.get(key)
                    if cached_data:
                        logger.info("Leaving Existing User (Cache Hit): " + cached_data)
                        return json.loads(cached_data)
                    response = userHandler.getExistingUser(user_id)
                    if 'user_id' in response:
                        redis_client.setex(key, 14400, json.dumps(response))
                    logger.info("Leaving Existing User: " + str(response))
                    return response
                elif request.method == 'POST':
                    response = userHandler.editExistingUser(user_id,request.json)
                    if 'user_id' in response:
                        key = f'user:{user_id}'
                        redis_client.setex(key, 14400, json.dumps(response))
                    logger.info("Leaving Existing User: " + str(response))
                    return response
                if request.method == 'DELETE':
                    response = userHandler.deleteExistingUser(user_id)
                    if 'result' in response and response['result'] == "User Successfully Deleted":
                        #delete all affected keys, too costly to update them
                        top_level_keys = [
                            'trades',
                            'stats',
                            'accountvalues',
                            'tradespage',
                            'tickersearch',
                            'pnlyear',
                            'user',
                            'journalentry',
                            'preferences'
                        ]
                        for key in top_level_keys:
                            pattern = f'{key}:{user_id}:*'
                            keys_to_delete = redis_client.keys(pattern)
                            if keys_to_delete:
                                redis_client.delete(*keys_to_delete)
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
    if request.method == 'GET':
        logger.info("Entering Existing Trade - " + str(request.method))
    if request.method == 'POST' or request.method == 'DELETE':
        logger.info("Entering Existing Trade - " + str(request.method) + ": " + str(request.json))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            if eval:
                if request.method == 'GET':
                    #cache entry will be based on trade_id from trade_id input param if trade_id is same and exists then no need to go to backend
                    key = f'trade:{trade_id}'
                    cached_data = redis_client.get(key)
                    if cached_data:
                        logger.info("Leaving Existing Trade (Cache Hit): " + cached_data)
                        return json.loads(cached_data)
                    response = tradeHandler.getExistingTrade(trade_id)
                    if 'trade_id' in response:
                        redis_client.setex(key, 14400, json.dumps(response))
                    logger.info("Leaving Existing Trade: " + str(response))
                    return response
                elif request.method == 'POST':
                    response = tradeHandler.editExistingTrade(trade_id,request.json)
                    if 'trade_id' in response:
                        #delete all affected keys, too costly to update them
                        user_id = response['user_id']
                        top_level_keys = [
                            'trades',
                            'stats',
                            'accountvalues',
                            'tradespage',
                            'tickersearch',
                            'pnlyear'
                        ]
                        for key in top_level_keys:
                            pattern = f'{key}:{user_id}:*'
                            keys_to_delete = redis_client.keys(pattern)
                            if keys_to_delete:
                                redis_client.delete(*keys_to_delete)
                        #add key for this trade id
                        key = f'trade:{trade_id}'
                        redis_client.setex(key, 14400, json.dumps(response))
                    logger.info("Leaving Existing Trade: " + str(response))
                    return response
                if request.method == 'DELETE':
                    response = tradeHandler.deleteExistingTrade(trade_id)
                    if 'result' in response and response['result'] == "Trade Successfully Deleted":
                        #delete all affected keys, too costly to update them
                        user_id = response['user_id']
                        top_level_keys = [
                            'trades',
                            'stats',
                            'accountvalues',
                            'tradespage',
                            'tickersearch',
                            'pnlyear'
                        ]
                        for key in top_level_keys:
                            pattern = f'{key}:{user_id}:*'
                            keys_to_delete = redis_client.keys(pattern)
                            if keys_to_delete:
                                redis_client.delete(*keys_to_delete)
                        #add key for this trade id
                        key = f'trade:{trade_id}'
                        redis_client.delete(key)
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
                    if 'result' in response and (response['result'] == "Trade Successfully Deleted" or response['result'] == "Trades Successfully Deleted"):
                        #delete all affected keys, too costly to update them
                        #TODO: get user_id from handler function and return to use here
                        user_id = response['user_id']
                        top_level_keys = [
                            'trades',
                            'stats',
                            'accountvalues',
                            'tradespage',
                            'tickersearch',
                            'pnlyear'
                        ]
                        for key in top_level_keys:
                            pattern = f'{key}:{user_id}:*'
                            keys_to_delete = redis_client.keys(pattern)
                            if keys_to_delete:
                                redis_client.delete(*keys_to_delete)
                        #add key for this trade id
                        for id in request.json:
                            key = f'trade:{id}'
                            redis_client.delete(key)
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
    if request.method == 'POST' or request.method == 'DELETE':
        logger.info("Entering Existing Journal Entry - " + str(request.method) + ": " + str(request.json))
    if request.method == 'GET':
        logger.info("Entering Existing Journal Entry - " + str(request.method))
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            eval,message = sessionHandler.validateToken(auth_token)
            eval2,message2 = sessionHandler.getUserFromToken(auth_token)
            if eval and eval2:
                user_id = message2
                if request.method == 'GET':
                    #cache entry will be based on user_id and (month and year) from date input param if user_id (month and year) exists in cache then no need to go to backend
                    date_obj = datetime.strptime(date, '%Y-%m-%d')
                    year = date_obj.year
                    month = date_obj.month
                    key = f'journalentry:{user_id}:{year}:{month}'
                    cached_data = redis_client.get(key)
                    if cached_data:
                        logger.info("Leaving Existing Journal Entry (Cache Hit): " + cached_data)
                        return json.loads(cached_data)
                    response = journalentryHandler.getJournalEntries(user_id, date)
                    if 'entries' in response:
                        redis_client.setex(key, 14400, json.dumps(response))
                    logger.info("Leaving Existing Journal Entry: " + str(response))
                    return response
                elif request.method == 'POST':
                    response = journalentryHandler.postJournalEntry(user_id, date, request.json)
                    #check if handler was successful in updating entry
                    logger.info("Here 1")
                    if 'entry' in response:
                        #look through user journal entries and if key exists for date, update it
                        date_obj = datetime.strptime(date, '%Y-%m-%d')
                        year = date_obj.year
                        month = date_obj.month
                        key = f'journalentry:{user_id}:{year}:{month}'
                        existing_json = json.loads(redis_client.get(key))
                        for item in existing_json.get("entries", []):
                            if item.get("date") == response['date']:
                                item["entrytext"] = response['entry']
                                redis_client.setex(key, 3600, json.dumps(existing_json))
                                break  # Exit the loop after the update
                    logger.info("Leaving Existing Journal Entry: " + str(response))
                    return response
                if request.method == 'DELETE':
                    response = journalentryHandler.deleteJournalEntry(user_id, date)
                    #check if handler was successful in deleting entry
                    if 'result' in response and response['result'] == "Journal Entry Successfully Deleted":
                        #look through user journal entries and if key exists for date, delete it
                        date_obj = datetime.strptime(date, '%Y-%m-%d')
                        year = date_obj.year
                        month = date_obj.month
                        key = f'journalentry:{user_id}:{year}:{month}'
                        existing_json = json.loads(redis_client.get(key))
                        if existing_json:
                            entries = existing_json.get("entries", [])
                            new_entries = [item for item in entries if item.get("date") != response['date']]
                            existing_json["entries"] = new_entries
                            redis_client.setex(key, 3600, json.dumps(existing_json))
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
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
