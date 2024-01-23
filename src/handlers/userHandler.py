import os
import smtplib
from email.mime.text import MIMEText
import sys
from urllib import request
import numpy
from datetime import date, datetime, timedelta
import json
import requests
from flask_jwt_extended import create_access_token
import logging

logger = logging.getLogger(__name__)

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import accountvalue

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import session

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import trade

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import resetcode

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import utils

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'validators',)
sys.path.append( mymodule_dir )
import userValidator

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'transformers',)
sys.path.append( mymodule_dir )
import userTransformer

import hashlib

JIRA_URL = os.environ.get('JIRA_URL')
JIRA_EMAIL = os.environ.get('JIRA_EMAIL')
JIRA_API_KEY = os.environ.get('JIRA_API_KEY')

# Email details
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')


def registerUser(requestBody):
    logger.info("Entering Register User Handler: " + "(request: {})".format(str(requestBody)))
    response = userValidator.validateNewUser(requestBody)
    if response != True:
        logger.warning("Leaving Register User Handler: " + str(response))
        return response
    requestTransformed = userTransformer.transformNewUser(requestBody)
    newUser = user.User(None,requestTransformed['first_name'],requestTransformed['last_name'],requestTransformed['birthday'],
                        requestTransformed['email'],requestTransformed['password'],requestTransformed['street_address'],
                        requestTransformed['city'],requestTransformed['state'],requestTransformed['country'],None,None)
    response = user.User.addUser(newUser)
    if response[0]:
        logger.warning("Leaving Register User Handler: " + str(response))
        return {
            "result": response
        }, 400
    else:
        response = {
            "user_id": response[1],
            "first_name": newUser.firstName,
            "last_name": newUser.lastName,
            "birthday": newUser.birthday,
            "email": newUser.email,
            "street_address": newUser.streetAddress,
            "city": newUser.city,
            "state": newUser.state,
            "country": newUser.country,
            "result": "User Created Successfully"
        }
        logger.info("Leaving Register User Handler: " + str(response))
        return response

def validateUser(requestBody):
    logger.info("Entering Validate User Handler: " + "(request: {})".format(str(requestBody)))
    response = user.User.getUserbyEmail(requestBody['email'])
    if not response[0]:
        response = "No User Found with this Email, Please Use a Different Email or Create an Account"
        logger.warning("Leaving Validate User Handler: " + response)
        return {
            "result": response
        }, 403
    elif 'password' in response[0][0]:
        hashPass = userTransformer.hashPassword(requestBody['password'])
        if response[0][0]['password'] == hashPass:
            access_token = create_access_token(identity=response[0][0]['user_id']) 
            newSession = session.Session(None,response[0][0]['user_id'],access_token,datetime.now()+timedelta(hours=24))
            sessionResponse = session.Session.addSession(newSession)
            if sessionResponse[0]:
                logger.warning("Leaving Validate User Handler: " + str(sessionResponse))
                return sessionResponse, 400
            else:
                response = {
                    "token": access_token,
                    "user_id": response[0][0]['user_id'],
                    "first_name": response[0][0]['first_name'],
                    "last_name": response[0][0]['last_name'],
                    "birthday": response[0][0]['birthday'],
                    "email": response[0][0]['email'],
                    "street_address": response[0][0]['street_address'],
                    "city": response[0][0]['city'],
                    "state": response[0][0]['state'],
                    "country": response[0][0]['country'],
                    "created_at" : response[0][0]['created_at'].strftime("%Y-%m-%d %H:%M:%S")
                }
                logger.info("Leaving Validate User Handler: " + str(response))
                return response
        else:
            response = "Incorrect Password, Please Try Again"
            logger.warning("Leaving Validate User Handler: " + response)
            return {
                "result": response
            }, 403
            
def changePassword(user_id, requestBody):
    logger.info("Entering Change Password Handler: " + "(user_id: {}, request: {})".format(str(user_id),str(requestBody)))
    response = userValidator.validateChangePassword(requestBody)
    if response != True:
        logger.warning("Leaving Change Password Handler: " + str(response))
        return response
    response = user.User.getUserbyID(user_id)
    if not response[0]:
        response = "User Does Not Exist"
        logger.warning("Leaving Change Password Handler: " + response)
        return {
            "result": response
        }, 403
    elif 'password' in response[0][0]:
        hashPass = userTransformer.hashPassword(requestBody['curr_pass'])
        if response[0][0]['password'] == hashPass:
            hashPass = userTransformer.hashPassword(requestBody['new_pass_1'])
            response = user.User.updatePass(user_id,hashPass)
            if response[0]:
                logger.warning("Leaving Change Password Handler: " + str(response))
                return {
                    "result": response
                }, 400
            else:
                response = "Password Successfully Changed"
                logger.info("Leaving Change Password Handler: " + response)
                return {
                    "result": response
                }
        else:
            response = "Incorrect Current Password, Please Try Again"
            logger.warning("Leaving Change Password Handler: " + response)
            return {
                "result": response
            }, 403
        
        
def getExistingUser(user_id):
    logger.info("Entering Get User Handler: " + "(user_id: {})".format(str(user_id)))
    response = user.User.getUserbyID(user_id)
    if 'user_id' in response[0][0]:
        response = {
            "user_id": response[0][0]['user_id'],
            "first_name": response[0][0]['first_name'],
            "last_name": response[0][0]['last_name'],
            "birthday": response[0][0]['birthday'],
            "email": response[0][0]['email'],
            "street_address": response[0][0]['street_address'],
            "city": response[0][0]['city'],
            "state": response[0][0]['state'],
            "country": response[0][0]['country'],
            "created_at" : response[0][0]['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        }
        logger.info("Leaving Get User Handler: " + str(response))
        return response
    else:
        logger.warning("Leaving Get User Handler: " + str(response))
        return {
            "result": response
        }, 400
        
        
def getUserPreferences(user_id):
    logger.info("Entering Get User Preferences Handler: " + "(user_id: {})".format(str(user_id)))
    response = user.User.getPreferences(user_id)
    if 'account_value_optin' in response[0][0]:
        response = {
            "account_value_optin": response[0][0]['account_value_optin'],
            "email_optin": response[0][0]['email_optin']
        }
        logger.info("Leaving Get User Preferences Handler: " + str(response))
        return response
    else:
        logger.warning("Leaving Get User Preferences Handler: " + str(response))
        return {
            "result": response
        }, 400
        
        
def toggleAvTracking(user_id):
    logger.info("Entering Toggle Account Value Tracking Handler: " + "(user_id: {})".format(str(user_id)))
    response = user.User.toggleAccountValueFeatureOptin(user_id) 
    if response[0]:
        logger.warning("Leaving Toggle Account Value Tracking Handler: " + str(response))
        return {
            "result": response
        }, 400   
    response = user.User.getPreferences(user_id)
    if 'account_value_optin' in response[0][0]:
        response = {
            "account_value_optin": response[0][0]['account_value_optin'],
            "email_optin": response[0][0]['email_optin']
        }
        logger.info("Leaving Toggle Account Value Tracking Handler: " + str(response))
        return response
    else:
        logger.warning("Leaving Toggle Account Value Tracking Handler: " + str(response))
        return {
            "result": response
        }, 400
        
        
def toggleEmailOptInHandler(user_id):
    logger.info("Entering Toggle Email Opt In Handler: " + "(user_id: {})".format(str(user_id)))
    response = user.User.toggleEmailOptIn(user_id) 
    if response[0]:
        logger.warning("Leaving Toggle Email Opt In Handler: " + str(response))
        return {
            "result": response
        }, 400   
    response = user.User.getPreferences(user_id)
    if 'account_value_optin' in response[0][0]:
        response = {
            "account_value_optin": response[0][0]['account_value_optin'],
            "email_optin": response[0][0]['email_optin']
        }
        logger.info("Leaving Toggle Email Opt In Handler: " + str(response))
        return response
    else:
        logger.warning("Leaving Toggle Email Opt In Handler: " + str(response))
        return {
            "result": response
        }, 400
        
    
def toggleFeatureFlagsHandler(user_id,requestBody):
    logger.info("Entering Toggle Feature Flags Handler: " + "(user_id: {})".format(str(user_id)))
    response = userValidator.validateToggleFeatureFlags(requestBody)
    if response != True:
        logger.warning("Leaving Toggle Feature Flags Handler: " + str(response))
        return response
    for ff in requestBody:
        if ff == 'email_optin':
            response = user.User.toggleEmailOptIn(user_id) 
            if response[0]:
                logger.warning("Leaving Toggle Feature Flags Handler: " + str(response))
                return {
                    "result": response
                }, 400   
        if ff == 'account_value_optin':
            response = user.User.toggleAccountValueFeatureOptin(user_id) 
            if response[0]:
                logger.warning("Leaving Toggle Feature Flags Handler: " + str(response))
                return {
                    "result": response
                }, 400   
    response = user.User.getPreferences(user_id)
    if 'account_value_optin' in response[0][0]:
        response = {
            "account_value_optin": response[0][0]['account_value_optin'],
            "email_optin": response[0][0]['email_optin']
        }
        logger.info("Leaving Toggle Feature Flags Handler: " + str(response))
        return response
    else:
        logger.warning("Leaving Toggle Feature Flags Handler: " + str(response))
        return {
            "result": response
        }, 400
        
    
def getUserFromSession(auth_token):
    logger.info("Entering Get User From Session Handler: " + "(auth_token: {})".format(str(auth_token)))
    response = user.User.getUserBySessionToken(auth_token)
    if 'user_id' in response[0][0]:
        response = {
            "user_id": response[0][0]['user_id'],
            "first_name": response[0][0]['first_name'],
            "last_name": response[0][0]['last_name'],
            "birthday": response[0][0]['birthday'],
            "email": response[0][0]['email'],
            "street_address": response[0][0]['street_address'],
            "city": response[0][0]['city'],
            "state": response[0][0]['state'],
            "country": response[0][0]['country'],
            "created_at" : response[0][0]['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        }
        logger.info("Leaving Get User From Session Handler: " + str(response))
        return response
    else:
        logger.warning("Leaving Get User From Session Handler: " + str(response))
        return {
            "result": response
        }, 400

def editExistingUser(user_id,requestBody):
    logger.info("Entering Edit User Handler: " + "(user_id: {}, request: {})".format(str(user_id),str(requestBody)))
    response = userValidator.validateEditUser(requestBody)
    if response != True:
        logger.warning("Leaving Edit User Handler: " + str(response))
        return response
    requestTransformed = userTransformer.transformEditUser(requestBody)
    response = user.User.updateUser(user_id,requestTransformed)
    response = user.User.getUserbyID(user_id)
    if 'user_id' in response[0][0]:
        response = {
            "user_id": response[0][0]['user_id'],
            "first_name": response[0][0]['first_name'],
            "last_name": response[0][0]['last_name'],
            "birthday": response[0][0]['birthday'],
            "email": response[0][0]['email'],
            "street_address": response[0][0]['street_address'],
            "city": response[0][0]['city'],
            "state": response[0][0]['state'],
            "country": response[0][0]['country'],
            "created_at" : response[0][0]['created_at'].strftime("%Y-%m-%d %H:%M:%S"),
            "result": "User Edited Successfully"
        }
        logger.info("Leaving Edit User Handler: " + str(response))
        return response
    else:
        logger.warning("Leaving Edit User Handler: " + str(response))
        return {
            "result": response
        }, 400

def deleteExistingUser(user_id):
    logger.info("Entering Delete User Handler: " + "(user_id: {})".format(str(user_id)))
    response = trade.Trade.deleteUserTrades(user_id)
    response = session.Session.deleteUserSessions(user_id)
    response = user.User.deleteUser(user_id)
    if response[0]:
        logger.warning("Leaving Delete User Handler: " + str(response))
        return {
            "result": response
        }, 400
    else:
        response = "User Successfully Deleted"
        logger.info("Leaving Delete User Handler: " + response)
        return {
            "result": response
        }
        
def reportBug(requestBody, email):
    logger.info("Entering Report Bug Handler: " + "(email: {}, request: {})".format(str(email),str(requestBody)))
    response = userValidator.validateReportBug(requestBody)
    if response != True:
        logger.warning("Leaving Report Bug Handler: " + str(response))
        return response
    response = userTransformer.transformReportBug(requestBody, email)
    response = requests.post(("https://"+JIRA_URL+"/rest/api/2/issue"), auth=(JIRA_EMAIL, JIRA_API_KEY), json=response)
    if response.status_code == 201:
        response = "Feedback Submitted Successfully"
        logger.info("Leaving Report Bug Handler: " + response)
        return {
            "result": response
        }
    else:
        brreponse = 'Error calling API: {}'.format(response)
        logger.warning("Leaving Report Bug Handler: " + brreponse)
        return brreponse, response.status_code
   

def getUserTrades(user_id,filters=None):
    logger.info("Entering Get User Trades Handler: " + "(user_id: {}, filters: {})".format(str(user_id),str(filters)))
    if not filters:
        response = user.User.getUserTrades(user_id)
    else:
        filterBody = filters.to_dict()
        if 'date_range' in filters:
            filterBody['date_range'] = userTransformer.transformDateRange(filters['date_range'])
        response = user.User.getUserTradesFilter(user_id,filterBody)
    if len(response[0]) != 0 and "trade_id" in response[0][0]:
        numTrades = 0
        numLosses = 0
        numWins = 0
        numDT = 0
        numDTWin = 0
        numDTLoss = 0
        numSwT = 0
        numSwTWin = 0
        numSwTLoss = 0
        numOT = 0
        numOTWin = 0
        numOTLoss = 0
        numShT = 0
        numShTWin = 0
        numShTLoss = 0
        largestWin = 0
        largestLoss = 0
        sumWin = 0
        sumLoss = 0
        avgWin = 0
        avgLoss = 0
        totalPNL = 0
        winPercent = 0
        for trade in response[0]:
            numTrades += 1
            if (trade['pnl'] > 0):
                numWins += 1
                sumWin += trade['pnl']
                totalPNL += trade['pnl']
            else:
                numLosses += 1
                sumLoss += trade['pnl']
                totalPNL += trade['pnl']
                
            if (trade['trade_type'] == "Day Trade"):
                numDT += 1
                if (trade['pnl'] > 0):
                    numDTWin += 1
                elif (trade['pnl'] < 0):
                    numDTLoss += 1
            elif (trade['trade_type'] == "Swing Trade"):
                numSwT += 1
                if (trade['pnl'] > 0):
                    numSwTWin += 1
                elif (trade['pnl'] < 0):
                    numSwTLoss += 1
                    
            if (trade['security_type'] == "Options"):
                numOT += 1
                if (trade['pnl'] > 0):
                    numOTWin += 1
                elif (trade['pnl'] < 0):
                    numOTLoss += 1
            elif (trade['security_type'] == "Shares"):
                numShT += 1
                if (trade['pnl'] > 0):
                    numShTWin += 1
                elif (trade['pnl'] < 0):
                    numShTLoss += 1
            
            if (trade['pnl'] > largestWin):
                largestWin = trade['pnl']
            elif (trade['pnl'] < largestLoss):
                largestLoss = trade['pnl']
        if(numWins > 0):
            avgWin = sumWin/numWins
        if(numLosses > 0):
            avgLoss = sumLoss/numLosses  
        if(numTrades > 0):
            winPercent = (numWins/numTrades)*100 
        response = {
            "trades": response[0],
            "stats": {
                "num_trades": numTrades,
                "num_losses": numLosses,
                "num_wins": numWins,
                "num_day": numDT,
                "num_day_win": numDTWin,
                "num_day_loss": numDTLoss,
                "num_swing": numSwT,
                "num_swing_win": numSwTWin,
                "num_swing_loss": numSwTLoss,
                "num_options": numOT,
                "num_options_win": numOTWin,
                "num_options_loss": numOTLoss,
                "num_shares": numShT,
                "num_shares_win": numShTWin,
                "num_shares_loss": numShTLoss,
                "largest_win": largestWin,
                "largest_loss": largestLoss,
                "avg_win": "{:.2f}".format(avgWin),
                "avg_loss": "{:.2f}".format(avgLoss),
                "total_pnl": totalPNL,
                "win_percent": "{:.2f}".format(winPercent)
            }
        }
        logger.info("Leaving Get User Trades Handler: " + str(response))
        return response
    else:
        numTrades = 0
        numLosses = 0
        numWins = 0
        numDT = 0
        numDTWin = 0
        numDTLoss = 0
        numSwT = 0
        numSwTWin = 0
        numSwTLoss = 0
        numOT = 0
        numOTWin = 0
        numOTLoss = 0
        numShT = 0
        numShTWin = 0
        numShTLoss = 0
        largestWin = 0
        largestLoss = 0
        sumWin = 0
        sumLoss = 0
        avgWin = 0
        avgLoss = 0
        totalPNL = 0
        winPercent = 0
        response = {
            "trades": [],
            "stats": {
                "num_trades": numTrades,
                "num_losses": numLosses,
                "num_wins": numWins,
                "num_day": numDT,
                "num_day_win": numDTWin,
                "num_day_loss": numDTLoss,
                "num_swing": numSwT,
                "num_swing_win": numSwTWin,
                "num_swing_loss": numSwTLoss,
                "num_options": numOT,
                "num_options_win": numOTWin,
                "num_options_loss": numOTLoss,
                "num_shares": numShT,
                "num_shares_win": numShTWin,
                "num_shares_loss": numShTLoss,
                "largest_win": largestWin,
                "largest_loss": largestLoss,
                "avg_win": "{:.2f}".format(avgWin),
                "avg_loss": "{:.2f}".format(avgLoss),
                "total_pnl": totalPNL,
                "win_percent": "{:.2f}".format(winPercent)
            }
        }
        logger.info("Leaving Get User Trades Handler: " + str(response))
        return response
        
        
def getUserTradesStats(user_id,filters=None):
    logger.info("Entering Get User Trades Statistics Handler: " + "(user_id: {}, filters: {})".format(str(user_id),str(filters)))
    if not filters:
        response = user.User.getUserTradesStats(user_id)
    else:
        filterBody = filters.to_dict()
        if 'date_range' in filters:
            filterBody['date_range'] = userTransformer.transformDateRange(filters['date_range'])
        response = user.User.getUserTradesStatsFilter(user_id,filterBody)
    if len(response[0]) != 0 and "numTrades" in response[0][0]:   
        avgWin = 0
        avgLoss = 0
        winPercent = 0         
        if(response[0][0]['numWins'] > 0):
            avgWin = response[0][0]['sumWin']/response[0][0]['numWins']
        if(response[0][0]['numLosses'] > 0):
            avgLoss = response[0][0]['sumLoss']/response[0][0]['numLosses']  
        if(response[0][0]['numTrades'] > 0):
            winPercent = (response[0][0]['numWins']/response[0][0]['numTrades'])*100
        response = {
            "stats": {
                "num_trades": response[0][0]['numTrades'],
                "num_losses": response[0][0]['numLosses'],
                "num_wins": response[0][0]['numWins'],
                "num_day": response[0][0]['numDT'],
                "num_day_win": response[0][0]['numDTWin'],
                "num_day_loss": response[0][0]['numDTLoss'],
                "num_swing": response[0][0]['numSwT'],
                "num_swing_win": response[0][0]['numSwTWin'],
                "num_swing_loss": response[0][0]['numSwTLoss'],
                "num_options": response[0][0]['numOT'],
                "num_options_win": response[0][0]['numOTWin'],
                "num_options_loss": response[0][0]['numOTLoss'],
                "num_shares": response[0][0]['numShT'],
                "num_shares_win": response[0][0]['numShTWin'],
                "num_shares_loss": response[0][0]['numShTLoss'],
                "largest_win": response[0][0]['largestWin'],
                "largest_loss": response[0][0]['largestLoss'],
                "avg_win": "{:.2f}".format(avgWin),
                "avg_loss": "{:.2f}".format(avgLoss),
                "total_pnl": response[0][0]['totalPNL'],
                "win_percent": "{:.2f}".format(winPercent)
            }
        }
        logger.info("Leaving Get User Trades Statistics Handler: " + str(response))
        return response
    else:
        response = {
            "stats": {
                "num_trades": 0,
                "num_losses": 0,
                "num_wins": 0,
                "num_day": 0,
                "num_day_win": 0,
                "num_day_loss": 0,
                "num_swing": 0,
                "num_swing_win": 0,
                "num_swing_loss": 0,
                "num_options": 0,
                "num_options_win": 0,
                "num_options_loss": 0,
                "num_shares": 0,
                "num_shares_win": 0,
                "num_shares_loss": 0,
                "largest_win": 0,
                "largest_loss": 0,
                "avg_win": "{:.2f}".format(0),
                "avg_loss": "{:.2f}".format(0),
                "total_pnl": 0,
                "win_percent": "{:.2f}".format(0)
            }
        }
        logger.info("Leaving Get User Trades Statistics Handler: " + str(response))
        return response
        
        
def getUserTradesPage(user_id,filters):
    logger.info("Entering Get User Trades Page Handler: " + "(user_id: {}, filters: {})".format(str(user_id),str(filters)))
    if not filters:
        response = "Please include Page Number and Rows per Page"
        logger.warning("Leaving Get User Trades Page Handler: " + str(response))
        return {
            "result": response
        }, 400
    else:
        page = filters['page']
        numrows = filters['numrows']
        filterBody = filters.to_dict()
        del filterBody['page'], filterBody['numrows']
        if 'date_range' in filters:
            filterBody['date_range'] = userTransformer.transformDateRange(filters['date_range'])
        count = user.User.getTotalTrades(user_id,filterBody)[0][0]['COUNT(*)']
        offset = (int(page)-1)*int(numrows)
        response = user.User.getUserTradesPage(user_id,int(numrows),offset,filterBody)
    if len(response[0]) != 0 and "trade_id" in response[0][0]:
        response = {
            "trades": response[0],
            "page": page,
            "count": count,
            "numrows": numrows 
        }
        logger.info("Leaving Get User Trades Page Handler: " + str(response))
        return response
    else:
        response = {
            "trades": [],
            "page": 0,
            "count": 0,
            "numrows": 0 
        }
        logger.info("Leaving Get User Trades Page Handler: " + str(response))
        return response

        
def getPnLbyYear(user_id, date_year, filters=None):
    logger.info("Entering Get PnL By Year Handler: " + "(user_id: {}, date_year: {}, filters: {})".format(str(user_id),str(date_year),str(filters)))
    if not filters:
        response = user.User.getUserPnLbyYear(user_id, date_year)
    else:
        response = user.User.getUserPnLbyYearFilter(user_id, date_year, filters)
    months = numpy.zeros((12,31))
    if len(response[0]) != 0 and "trade_date" in response[0][0]:
        for day in response[0]:
            date = datetime.strptime(day['trade_date'], "%Y-%m-%d")
            curr_month = date.month
            curr_day = date.day
            months[curr_month-1][curr_day-1] = day['day_pnl'] 
            monthsJSON = months.tolist() 
        response = {
            "months": [
                {"0" : monthsJSON[0]},
                {"1" : monthsJSON[1]},
                {"2" : monthsJSON[2]},
                {"3" : monthsJSON[3]},
                {"4" : monthsJSON[4]},
                {"5" : monthsJSON[5]},
                {"6" : monthsJSON[6]},
                {"7" : monthsJSON[7]},
                {"8" : monthsJSON[8]},
                {"9" : monthsJSON[9]},
                {"10" : monthsJSON[10]},
                {"11" : monthsJSON[11]}
            ]
        }
        logger.info("Leaving Get PnL By Year Handler: " + str(response))
        return response
    else:
        monthsJSON = months.tolist()
        response = {
            "months": [
                {"0" : monthsJSON[0]},
                {"1" : monthsJSON[1]},
                {"2" : monthsJSON[2]},
                {"3" : monthsJSON[3]},
                {"4" : monthsJSON[4]},
                {"5" : monthsJSON[5]},
                {"6" : monthsJSON[6]},
                {"7" : monthsJSON[7]},
                {"8" : monthsJSON[8]},
                {"9" : monthsJSON[9]},
                {"10" : monthsJSON[10]},
                {"11" : monthsJSON[11]}
            ]
        }
        logger.info("Leaving Get PnL By Year Handler: " + str(response))
        return response
    
def generateResetCode(requestBody):
    logger.info("Entering Generate Reset Code Handler: " + "(request: {})".format(str(requestBody)))
    response = user.User.getUserbyEmail(requestBody['email'])
    if not response[0]:
        response = "No Account Found with this Email, Please Use a Valid Email or Create an Account"
        logger.warning("Leaving Generate Reset Code Handler: " + response)
        return {
            "result": response
        }, 403
    else:
        code = utils.generate_code()
        newResetCode = resetcode.Resetcode(None,response[0][0]['user_id'],code,datetime.now()+timedelta(minutes=15))
        resetcodeResponse = resetcode.Resetcode.addResetCode(newResetCode)
        if resetcodeResponse[0]:
            logger.warning("Leaving Generate Reset Code Handler: " + str(resetcodeResponse))
            return {
                "result": str(resetcodeResponse)
            }, 400

        try:
            reset_code_email = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'resources', 'resetcode.html')
            with open(reset_code_email, 'r') as file:
                reset_code_html = file.read()
            email_subject = 'MyTradingTracker - Reset Your Password'
            email_body = reset_code_html.replace('RESET_CODE', code)
            message = MIMEText(email_body, 'html')
            message['Subject'] = email_subject
            message['From'] = SMTP_USERNAME
            message['To'] = requestBody['email']
            # Send the email
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(SMTP_USERNAME, requestBody['email'], message.as_string())
            response = "Reset Code Generated Successfully"
            logger.info("Leaving Generate Reset Code Handler: " + response)
            return {
                "result": response
            }
                
        except Exception as e:
            response = "Error: " + str(e)
            logger.error("Leaving Generate Reset Code Handler: " + response)
            return {
                "result": response
            }, 403
            

def validateResetCode(requestBody):
    logger.info("Entering Validate Reset Code Handler: " + "(request: {})".format(str(requestBody)))
    response = user.User.getUserbyEmail(requestBody['email'])
    if not response[0]:
        response = "No Account Found with this Email, Please Use a Valid Email or Create an Account"
        logger.warning("Leaving Validate Reset Code Handler: " + response)
        return {
            "result": response
        }, 403
    response = resetcode.Resetcode.getResetCode(requestBody['code'],response[0][0]['user_id'])
    if not response[0]:
        response = "Reset Code Doesn't Exist"
        logger.warning("Leaving Validate Reset Code Handler: " + response)
        return {
            "result": response
        }, 401
    elif 'expiration' in response[0][0]:
        if response[0][0]['expiration'] < datetime.now():
            response = "Reset Code Has Expired"
            logger.warning("Leaving Validate Reset Code Handler: " + response)
            return {
                "result": response
            }, 401
        else:
            response = "Reset Code Verified Successfully"
            logger.info("Leaving Validate Reset Code Handler: " + response)
            return {
                "result": response   
            }
    else:
        response = "An Issue Occurred Validating Reset Code, Please Try Again"
        logger.warning("Leaving Validate Reset Code Handler: " + response)
        return {
            "result": response
        }, 403
        

def resetPassword(requestBody):
    logger.info("Entering Reset Password Handler: " + "(request: {})".format(str(requestBody)))
    response = userValidator.validateResetPassword(requestBody)
    if response != True:
        logger.warning("Leaving Reset Password Handler: " + str(response))
        return response
    userResponse = user.User.getUserbyEmail(requestBody['email'])
    if not userResponse[0]:
        response = "No Account Found with this Email, Please Use a Valid Email or Create an Account"
        logger.warning("Leaving Reset Password Handler: " + response)
        return {
            "result": response
        }, 403
    validateCodeResponse = validateResetCode({"code": requestBody['code'], "email": requestBody['email']})
    if validateCodeResponse['result'] == "Reset Code Verified Successfully":
        hashPass = userTransformer.hashPassword(requestBody['new_pass_1'])
        response = user.User.updatePass(userResponse[0][0]['user_id'],hashPass)
        if response[0]:
            logger.warning("Leaving Reset Password Handler: " + str(response))
            return {
                "result": response
            }, 400
        else:
            response = resetcode.Resetcode.getResetCode(requestBody['code'],userResponse[0][0]['user_id'])
            if not response[0]:
                response = "Reset Code Doesn't Exist"
                logger.warning("Leaving Reset Password Handler: " + response)
                return {
                    "result": response
                }, 401
            response = resetcode.Resetcode.deleteResetCode(response[0][0]['resetcode_id'])
            if response[0]:
                logger.warning("Leaving Reset Password Handler: " + str(response))
                return {
                    "result": str(response)
                }, 400
            else:
                response = "Password Reset Successfully"
                logger.info("Leaving Reset Password Handler: " + response)
                return {
                    "result": response
                }
            
    else:
        return validateCodeResponse
    
    
def setAccountValue(user_id,requestBody):
    logger.info("Entering Set Account Value Handler: " + "(user_id: {}, request: {})".format(str(user_id),str(requestBody)))
    response = userValidator.validateSetAccountValue(requestBody)
    if response != True:
        logger.warning("Leaving Set Account Value Handler: " + str(response))
        return response
    response = user.User.getPreferences(user_id)
    if 'account_value_optin' in response[0][0]:
        if(response[0][0]['account_value_optin'] == 0):
            response = user.User.accountValueFeatureOptin(user_id) 
            if response[0]:
                logger.warning("Leaving Set Account Value Handler: " + str(response))
                return {
                    "result": response
                }, 400   
        response = accountvalue.Accountvalue.getAccountValue(requestBody['date'],user_id)
        if(len(response[0]) != 0 and 'accountvalue_id' in response[0][0]):
            response = accountvalue.Accountvalue.updateAccountValue(response[0][0]['user_id'],response[0][0]['date'],requestBody['accountvalue'])
            if response[0]:
                logger.warning("Leaving Set Account Value Handler: " + str(response))
                return {
                    "result": response
                }, 400
        else:
            newAccountValueEntry = accountvalue.Accountvalue(None,user_id,requestBody['accountvalue'],requestBody['date'])
            response = accountvalue.Accountvalue.addAccountValue(newAccountValueEntry)
            if response[0]:
                logger.warning("Leaving Set Account Value Handler: " + str(response))
                return {
                    "result": response
                }, 400
        response = "Account Value Set Successfully"
        logger.info("Leaving Set Account Value Handler: " + response)
        return {
            "result": response,
            "accountvalue": requestBody['accountvalue'],
            "date": requestBody['date']
        }
    else:
        logger.warning("Leaving Set Account Value Handler: " + str(response))
        return {
            "result": response
        }, 400
        

def getAccountValue(user_id,filters):
    logger.info("Entering Get Account Value Handler: " + "(user_id: {}, filters: {})".format(str(user_id),str(filters)))
    response = userValidator.validateGetAccountValue(filters)
    if response != True:
        logger.warning("Leaving Get Account Value Handler: " + str(response))
        return response
    response = user.User.getPreferences(user_id)
    if 'account_value_optin' in response[0][0]:
        if(response[0][0]['account_value_optin'] == 0):
            date_range = [datetime.strptime(filters['date'], '%Y-%m-%d').date() - timedelta(days=i) for i in range(6, -1, -1)]
            result = [{'accountvalue': 0, 'date': date.strftime('%Y-%m-%d')} for date in date_range]
            logger.info("Leaving Get Account Value Handler: " + str(result))
            return {
                "accountvalues": result
            }
        else:
            response = accountvalue.Accountvalue.getAccountValue(filters['date'],user_id)
            if(len(response[0]) == 0 or 'accountvalue_id' not in response[0][0]):
                response = accountvalue.Accountvalue.insertFutureDay(user_id,filters['date'])
                if response[0]:
                    logger.warning("Leaving Get Account Value Handler: " + str(response))
                    return {
                        "result": response
                    }, 400
            if 'time_frame' in filters:
                tfdaterange = userTransformer.transformAVtf(filters['date'],filters['time_frame'])
                # Next is to get values from DB
                response = accountvalue.Accountvalue.getAccountValuesTF(user_id,tfdaterange)
                # Then check if all 7 got returned otherwise set to 0
                if len(response[0]) != 0 and "accountvalue" in response[0][0]:
                    data = {row['date'] : row['accountvalue'] for row in response[0]}
                    result = [{'accountvalue': data.get(date, 0), 'date': date.strftime('%Y-%m-%d')} for date in tfdaterange]
                    # format and return 7 values in response
                    logger.info("Leaving Get Account Value Handler: " + str(result))
                    return {
                        "accountvalues": result
                    }
                else:
                    logger.warning("Leaving Get Account Value Handler: " + str(response))
                    return {
                        "result": response
                    }, 400
            else:
                response = accountvalue.Accountvalue.getAccountValues(user_id,datetime.strptime(filters['date'], '%Y-%m-%d').date())
                if len(response[0]) != 0 and "accountvalue" in response[0][0]:
                    data = {row['date'] : row['accountvalue'] for row in response[0]}
                    date_range = [datetime.strptime(filters['date'], '%Y-%m-%d').date() - timedelta(days=i) for i in range(6, -1, -1)]
                    result = [{'accountvalue': data.get(date, 0), 'date': date.strftime('%Y-%m-%d')} for date in date_range]
                    logger.info("Leaving Get Account Value Handler: " + str(result))
                    return {
                        "accountvalues": result
                    }
                else:
                    logger.warning("Leaving Get Account Value Handler: " + str(response))
                    return {
                        "result": response
                    }, 400
    else:
        logger.warning("Leaving Get Account Value Handler: " + str(response))
        return {
            "result": response
        }, 400

  

#--------Tests--------# 

#Testing registerUser()
#testUserDict = {
#    "first_name": "Stevie",
#    "last_name": "Wonder",
#    "birthday": "12-31-2014",
#    "email": "xxxxxx@gmail.com",
#    "password": "testpassword",
#    "street_address": "25 Lenox Hill Rd",
#    "city": "Brewster",
#    "state": "MD",
#    "country": "US",
#}
#response = registerUser(testUserDict)

#Testing validateUser()
#testUserDict = {
#    "email": "alexi.bollella@gmail.com",
#    "password": "Modperl1!",
#}
#response = validateUser(testUserDict)

#Testing getExistingUser()
#response = getExistingUser(1)

#Testing editExistingUser()
#testChanges = {
#    "first_name": "Jonathan",
#    "last_name": "Palmieri"
#}
#response = editExistingUser(62,testChanges)

#Testing deleteExistingUser()
#response = deleteExistingUser(62)

#Testing getUserTrades()
#response = getUserTrades(77)

#Testing getUserTradesFilter
#testUserID = 71
#testFilters = {
#   "ticker_name": "SPY",
#   "trade_type": "Swing Trade",
#   "security_type": "Options"
#}
#response = getUserTrades(testUserID,testFilters)

#Testing getUserTradesPage
#testUserID = 71
#testFilters = {
#   "page": "1",
#   "numrows": "100",
#}
#response = getUserTradesPage(testUserID,testFilters)

#print(response)