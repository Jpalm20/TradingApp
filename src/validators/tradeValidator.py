import os
import sys
from datetime import date, datetime, timedelta

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import trade

def validateNewTrade(request):
    if (request['security_type'] == "Options") and ('expiry' not in request or 'strike' not in request or request['expiry'] == "" or request['strike'] == "" ):
        return {
            "result": "Options require Strike Price and Expiry, Try Again"
        }, 400
    elif (request['security_type'] == "Shares") and (('expiry' in request and request['expiry'] != "") or ('strike' in request and request['strike'] != "")):
        return {
            "result": "Shares require no Strike Price or Expiry, Try Again"
        }, 400
    elif (request['security_type'] != "Shares" and request['security_type'] != "Options"):
        return {
            "result": "Security Type is either Shares or Options, Try Again"
        }, 400
    elif ('ticker_name' not in request or request['ticker_name'] == "" or request['ticker_name'] == " " ):
        return {
            "result": "Must Include a Valid Ticker Symbol"
        }, 400
    elif ('rr' not in request or request['rr'] == "" or request['rr'] == " " or ':' not in request['rr']):
        return {
            "result": "Must Include a Valid Risk to Reward Ratio"
        }, 400
    elif ('trade_date' in request and request['trade_date'] != "" and datetime.strptime(request['trade_date'], '%Y-%m-%d') >= datetime.now()):
        return {
            "result": "Trade Closure Date Can't be in the Future"
        }, 400
    #need to validate blanks as well, might be easier to set required fields on FE if possible
    
    return True

def validateEditTrade(request):
    if (request['security_type'] == "Options") and ('expiry' not in request or 'strike' not in request or request['expiry'] == "" or request['strike'] == "" ):
        return {
            "result": "Options require Strike Price and Expiry, Try Again"
        }, 400
    elif (request['security_type'] == "Shares") and (('expiry' in request and request['expiry'] != "") or ('strike' in request and request['strike'] != "")):
        return {
            "result": "Shares require no Strike Price or Expiry, Try Again"
        }, 400
    elif ('ticker_name' in request and request['ticker_name'] != "" and request['ticker_name'] == " "):
        return {
            "result": "Invalid Ticker Symbol, Try Updating Again"
        }, 400
    elif ('rr' in request and request['rr'] != "" and (request['rr'] == " " or ':' not in request['rr'])):
        return {
            "result": "Must Include a Valid Risk to Reward Ratio"
        }, 400
    elif ('trade_date' in request and request['trade_date'] != "" and datetime.strptime(request['trade_date'], '%Y-%m-%d') >= datetime.now()):
        return {
            "result": "Trade Closure Date Can't be in the Future"
        }, 400
    return True
