import os
import sys
from datetime import date, datetime, timedelta
import csv
import logging
from werkzeug.datastructures import FileStorage


logger = logging.getLogger(__name__)


script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import trade

def validateNewTrade(request):
    logger.info("Entering Validate New Trade Validator: " + "(request: {})".format(str(request)))
    if (request['security_type'] == "Options") and ('expiry' not in request or 'strike' not in request or request['expiry'] == "" or request['strike'] == "" ):
        response = "Options require Strike Price and Expiry, Try Again"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif (request['security_type'] == "Shares") and (('expiry' in request and request['expiry'] != "") or ('strike' in request and request['strike'] != "")):
        response = "Shares require no Strike Price or Expiry, Try Again"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif (request['security_type'] != "Shares" and request['security_type'] != "Options"):
        response = "Security Type is either Shares or Options, Try Again"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif ('ticker_name' not in request or request['ticker_name'] == "" or request['ticker_name'] == " " ):
        response = "Must Include a Valid Ticker Symbol"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif ('rr' not in request or request['rr'] == "" or request['rr'] == " " or ':' not in request['rr']):
        response = "Must Include a Valid Risk to Reward Ratio"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif ('trade_date' in request and request['trade_date'] != "" and datetime.strptime(request['trade_date'], '%Y-%m-%d').date() > datetime.now().date() + timedelta(days=1)):
        response = "Trade Closure Date Can't be in the Future"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    #need to validate blanks as well, might be easier to set required fields on FE if possible
    logger.info("Leaving Validate New Trade Validator: ")
    return True

def validateEditTrade(request):
    logger.info("Entering Validate Edit Trade Validator: " + "(request: {})".format(str(request)))
    if (request['security_type'] == "Options") and ('expiry' not in request or 'strike' not in request or request['expiry'] == "" or request['strike'] == "" ):
        response = "Options require Strike Price and Expiry, Try Again"
        logger.warning("Leaving Validate Edit Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif (request['security_type'] == "Shares") and (('expiry' in request and request['expiry'] != "") or ('strike' in request and request['strike'] != "")):
        response = "Shares require no Strike Price or Expiry, Try Again"
        logger.warning("Leaving Validate Edit Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif ('ticker_name' in request and request['ticker_name'] != "" and request['ticker_name'] == " "):
        response = "Invalid Ticker Symbol, Try Updating Again"
        logger.warning("Leaving Validate Edit Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif ('rr' in request and request['rr'] != "" and (request['rr'] == " " or ':' not in request['rr'])):
        response = "Must Include a Valid Risk to Reward Ratio"
        logger.warning("Leaving Validate Edit Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif ('trade_date' in request and request['trade_date'] != "" and datetime.strptime(request['trade_date'], '%Y-%m-%d').date() > datetime.now().date() + timedelta(days=1)):
        response = "Trade Closure Date Can't be in the Future"
        logger.warning("Leaving Validate Edit Trade Validator: " + response)
        return {
            "result": response
        }, 400
    logger.info("Leaving Validate Edit Trade Validator: ")
    return True

def validateCsv(file):
    logger.info("Entering Validate CSV Validator: " + "(file: {})".format(str(file)))
    #csv_string = file.stream.read().decode("utf-8-sig")
    if isinstance(file, FileStorage):
        csv_string = file.stream.read().decode("utf-8-sig")
    else:
        # Assuming it's a standard file object
        file.seek(0)  # Reset the file pointer
        csv_string = file.read()
    reader = csv.DictReader(csv_string.splitlines())
    headers = next(reader, None) 
    required_headers = ["security_type", "ticker_name", "execution_time", "side", "quantity", "cost_basis"]
    for header in required_headers:
        if header not in headers:
            logger.warning("Leaving Validate CSV Validator: ")
            return False
    logger.info("Leaving Validate CSV Validator: ")
    return True

def validateNewTradeFromCsv(request):
    logger.info("Entering Validate New Trade Validator: " + "(request: {})".format(str(request)))
    if (request['security_type'] == "Options") and ('expiry' not in request or 'strike' not in request or request['expiry'] == "" or request['strike'] == "" ):
        response = "Options require Strike Price and Expiry, Try Again"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif (request['security_type'] == "Shares") and (('expiry' in request and request['expiry'] != None) or ('strike' in request and request['strike'] != None)):
        response = "Shares require no Strike Price or Expiry, Try Again"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif (request['security_type'] != "Shares" and request['security_type'] != "Options"):
        response = "Security Type is either Shares or Options, Try Again"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif ('ticker_name' not in request or request['ticker_name'] == "" or request['ticker_name'] == " " ):
        response = "Must Include a Valid Ticker Symbol"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    elif ('trade_date' in request and request['trade_date'] != "" and datetime.strptime(request['trade_date'], '%Y-%m-%d').date() > datetime.now().date() + timedelta(days=1)):
        response = "Trade Closure Date Can't be in the Future"
        logger.warning("Leaving Validate New Trade Validator: " + response)
        return {
            "result": response
        }, 400
    logger.info("Leaving Validate New Trade Validator: ")
    return True


def validateExportTrades(request):
    logger.info("Entering Validate Export Trades Validator: " + "(request: {})".format(str(request)))
    if 'exported_trades' not in request:
        logger.warning("Leaving Validate Export Trades Validator: ")
        return False

    trades = request['exported_trades']
    if trades is None or not trades:
        logger.warning("Leaving Validate Export Trades Validator: ")
        return False
    
    # List of keys expected in each trade object
    expected_keys = ['buy_value', 'comments', 'expiry', 'percent_wl', 'pnl', 'rr', 'security_type', 'strike', 'ticker_name', 'trade_date', 'trade_id', 'trade_type', 'units', 'user_id']

    for trade in trades:
        if not all(key in trade for key in expected_keys):
            logger.warning("Leaving Validate Export Trades Validator: ")
            return False
    logger.info("Leaving Validate Export Trades Validator: ")
    return True


def validateSearchTicker(filter):
    logger.info("Entering Validate Search Ticker Validator: " + "(filter: {})".format(str(filter)))
    if 'ticker_name' not in filter:
        response = "Please include ticker_name only for filtering parameters"
        logger.warning("Leaving Validate Search Ticker Validator: " + response)
        return False, response
    response = "Passed"
    logger.warning("Leaving Validate Search Ticker Validator: " + response)
    return True, response

