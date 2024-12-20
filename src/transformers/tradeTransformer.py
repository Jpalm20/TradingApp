import os
import sys
import csv
from datetime import date, datetime, timedelta
from dateutil.parser import parse
from collections import defaultdict
import logging
from werkzeug.datastructures import FileStorage


logger = logging.getLogger(__name__)

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import trade

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'validators',)
sys.path.append( mymodule_dir )
import tradeValidator

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'handlers',)
sys.path.append( mymodule_dir )
import tradeHandler

def transformNewTrade(request):
    logger.info("Entering Transform New Trade Transformer: " + "(request: {})".format(str(request)))
    if request['security_type'] == "Shares":
        request['expiry'] = None
        request['strike'] = None
    if 'trade_date' in request and request['trade_date'] == "":
        request['trade_date'] = None
    if 'pnl' in request and request['pnl'] == "":
        request['pnl'] = None
    if 'units' in request and request['units'] == "":
        request['units'] = None
    if 'strike' in request and request['strike'] == "":
        request['strike'] = None
    if 'buy_value' in request and request['buy_value'] == "":
        request['buy_value'] = None
    if 'percent_wl' in request and request['percent_wl'] == "":
        request['percent_wl'] = None
        if ('pnl' in request and request['pnl'] not in ["",None]) and ('units' in request and request['units'] not in ["",None]) and ('buy_value' in request and request['buy_value'] not in ["",None]):
            pnl_float = float(request['pnl'])
            units_float = float(request['units'])
            buy_value_float = float(request['buy_value'])
            request['percent_wl'] = round((pnl_float / (buy_value_float * units_float)) * 100, 2)
    request['ticker_name'] = request['ticker_name'].upper()
    logger.info("Leaving Transform New Trade Transformer: " + "(transformed_request: {})".format(str(request)))
    return request

def transformEditTrade(trade_id,request):
    logger.info("Entering Transform Edit Trade Transformer: " + "(request: {})".format(str(request)))
    transformedRequest = {}
                
    for key in request:
        if request[key] != "" and request[key] != None:
            transformedRequest[key] = request[key]
        if key == 'ticker_name' and request['ticker_name'] != '':
            transformedRequest['ticker_name'] = request['ticker_name'].upper()
        if request[key] == None:
            transformedRequest[key] = 'NULL'
    if ('security_type' in transformedRequest) and (transformedRequest['security_type'] == "Shares"):
        transformedRequest['expiry'] = 'NULL'
        transformedRequest['strike'] = 'NULL'
    
    # Autocalculating perccent_wl
    # Step 1: Check if '%wl' is missing in the request data
    if 'percent_wl' not in request or request['percent_wl'] in ["", None]:
        
        # Step 2: Check if at least one of PNL, units, or buy_value is present in the new request
        valid_pnl = 'pnl' in request and request['pnl'] not in [None]
        valid_units = 'units' in request and request['units'] not in [None]
        valid_buy_value = 'buy_value' in request and request['buy_value'] not in [None]
        
        if valid_pnl and valid_units and valid_buy_value:
            # Step 3: Get the existing trade data (assume `trade_data` has previous values)
            trade_info = tradeHandler.getExistingTrade(trade_id)
            existing_pnl = trade_info.get('pnl') if trade_info.get('pnl') not in ["", None] else None
            existing_units = trade_info.get('units') if trade_info.get('units') not in ["", None] else None
            existing_buy_value = trade_info.get('buy_value') if trade_info.get('buy_value') not in ["", None] else None

            # Step 4: Determine which fields are missing from the request and calculate the missing value
            pnl = request.get('pnl') if request.get('pnl') not in ["", None] else existing_pnl
            units = request.get('units') if request.get('units') not in ["", None] else existing_units
            buy_value = request.get('buy_value') if request.get('buy_value') not in ["", None] else existing_buy_value
            
            # Ensure we have at least two fields to calculate the third
            if pnl is not None and units is not None and buy_value is not None:
                # Calculate the % win/loss
                percent_wl = round((float(pnl) / (float(buy_value) * float(units))) * 100, 2)
                
                # Update the request data with the calculated % win/loss
                transformedRequest['percent_wl'] = percent_wl
        else:
            transformedRequest['percent_wl'] = 'NULL'
    
    logger.info("Leaving Transform Edit Trade Transformer: " + "(transformed_request: {})".format(str(transformedRequest)))
    return transformedRequest

def processUpdateCsv(file):
    #setup file to be ready for development
    logger.info("Entering Process Update CSV Transformer: " + "(file: {})".format(str(file)))
    trades_to_update = []
    
    if isinstance(file, FileStorage):
        logger.info("FileStorage Type")
        file.stream.seek(0)
        csv_string = file.stream.read().decode("utf-8-sig")
    else:
        # Assuming it's a standard file object
        logger.info("Standard File Type")
        file.seek(0)  # Reset the file pointer
        csv_string = file.read()
    #loop through entries and setup updates
    reader = csv.DictReader(csv_string.splitlines())
    rows = list(reader)
    
    for row in rows:
        #if not all(col in row for col in ["trade_id", "trade_date", "trade_type", "security_type", "ticker_name", "buy_value", "units", "expiry", "strike", "pnl", "percent_wl", "rr"]):
        if not all(col in row and row.get(col) not in [''] for col in ["trade_id", "trade_date", "trade_type", "security_type", "ticker_name", "buy_value", "units", "expiry", "strike", "pnl", "percent_wl", "rr"]):
            continue
        logger.info("Row: {})".format(str(row)))
        #just need to map row of csv to trade object and then sent all the trades back
        trade = {
            "trade_id": row['trade_id'],
            "trade_type": row['trade_type'],
            "security_type": row['security_type'],
            "ticker_name": row['ticker_name'],
            "trade_date": row['trade_date'],
            "expiry": row['expiry'],
            "strike": row['strike'],
            "buy_value": row['buy_value'],
            "units": row['units'],
            "rr": row['rr'],
            "pnl": row['pnl'],
            "percent_wl": row['percent_wl'],
            "comments": ""
        }
        for key in trade: 
            if trade[key] == 'None':
                trade[key] = None
        if trade['security_type'] == "Shares" and trade['expiry'] == None and trade['strike'] == None:
            trade['expiry'] = ''
            trade['strike'] = ''
        if trade['trade_date'] != None:
            trade['trade_date'] = transformDateFormart(trade['trade_date'])
        if trade['expiry'] != None:
            trade['expiry'] = transformDateFormart(trade['expiry'])
        if trade['pnl'] not in ["",None] and trade['units'] not in ["",None] and trade['buy_value'] not in ["",None]:
            trade['percent_wl'] = None
        trades_to_update.append(trade)
    if len(trades_to_update) == 0:
        result = "No Valid Rows in CSV"
        logger.warning("Leaving Process Update CSV Transformer: " + "(result: {})".format(str(result)))
        return False, result
    logger.info("Leaving Process Update CSV Transformer: " + "(trades_to_update: {})".format(str(trades_to_update)))
    return True, trades_to_update

def processCsv(user_id, file):
    logger.info("Entering Process CSV Transformer: " + "(user_id: {}, file: {})".format(str(user_id),str(file)))
    ## algorithm
    trades = []
    buy_trades = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
    sell_trades = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))

    if isinstance(file, FileStorage):
        logger.info("FileStorage Type")
        file.stream.seek(0)
        csv_string = file.stream.read().decode("utf-8-sig")
    else:
        # Assuming it's a standard file object
        logger.info("Standard File Type")
        file.seek(0)  # Reset the file pointer
        csv_string = file.read()

    #file.stream.seek(0)
    #csv_string = file.stream.read().decode("utf-8-sig")
    reader = csv.DictReader(csv_string.splitlines())
    rows = list(reader)
    sorted_rows = sorted(rows, key=lambda row: (row['execution_time'], row['side']))

    for row in sorted_rows:
        #if not all(col in row for col in ['security_type', 'ticker_name', 'execution_time', 'side', 'quantity', 'cost_basis']):
        if not all(col in row and row.get(col) not in [None, ''] for col in ['security_type', 'ticker_name', 'execution_time', 'side', 'quantity', 'cost_basis']):
            continue
        logger.info("Row: {})".format(str(row)))
        if row['quantity'] == '' or row['security_type'] == '' or row['ticker_name'] == '' or row['execution_time'] == '' or row['side'] == '' or row['cost_basis'] == '':
            response = "Empty fields exist in .csv please resolve"
            logger.warning("Leaving Process CSV Transformer: " + response)
            return False, response
        if int(row['quantity']) < 0:
            quantity = int(row['quantity']) * -1
        else:
            quantity = int(row['quantity'])
        cost_basis = float(row['cost_basis'])
        if row['security_type'].upper() == "PUT" or row['security_type'].upper() == "CALL":
            security_type = "Options"
            if 'expiry' not in row or 'strike' not in row or row['expiry'] == '' or row['strike'] == '' :
                response = "Upload Failed, Options Trades must include Expiration and Strike Price"
                logger.warning("Leaving Process CSV Transformer: " + response)
                return False, response
            expiry = row['expiry']
            strike = row['strike']
            cost_basis = float(row['cost_basis']) * 100  # cost_basis is per-share for options
        else:
            security_type = "Shares"
            cost_basis = float(row['cost_basis'])
        ticker_name = row['ticker_name'].upper()
        execution_time = parse(row['execution_time'])
        execution_time = execution_time.strftime('%Y-%m-%d')

        # Handle buy trades
        # both buy and sell data structure will basically be one entry for each trade combination, so for buys and sell classified as the same trade will be kept/updated in one entry which is a running total
        # once the buys and sells are done and quantity different = 0 then the final comparison would take place to create trade object and determine if day/swing trade
        # then you would verify trade object and append to trades array for return
        # when trade is considered closed the entry for that trade combination will need to be cleared to open up possibility for a new trade to be created with that combination
        if row['side'].upper() == 'BUY':
            # can add a check if security type is option then if same expiry and strike entry exists
            if security_type == 'Options':
                if ticker_name in buy_trades and row['security_type'] in buy_trades[ticker_name] and expiry in buy_trades[ticker_name][row['security_type']] and strike in buy_trades[ticker_name][row['security_type']][expiry] and len(buy_trades[ticker_name][row['security_type']][expiry][strike]) > 0:
                    #Need a comparison of execution time
                    if buy_trades[ticker_name][row['security_type']][expiry][strike]['execution_time'] > execution_time:
                        buy_trades[ticker_name][row['security_type']][expiry][strike]['execution_time'] = execution_time
                    #Need to use Qty and Cost Basis to Calculate new Cost Basis for entry (averging and using qty as weight/ratio) 
                    buy_trades[ticker_name][row['security_type']][expiry][strike]['cost_basis'] = ((buy_trades[ticker_name][row['security_type']][expiry][strike]['quantity'] * buy_trades[ticker_name][row['security_type']][expiry][strike]['cost_basis']) + cost_basis * quantity) / (buy_trades[ticker_name][row['security_type']][expiry][strike]['quantity'] + quantity)
                    #Need to add to Qty
                    buy_trades[ticker_name][row['security_type']][expiry][strike]['quantity'] += quantity
                else:
                    buy_trades[ticker_name][row['security_type']][expiry][strike] = {
                        'execution_time': execution_time,
                        'quantity': quantity,
                        'cost_basis': cost_basis,
                    }
            else:
                if ticker_name in buy_trades and row['security_type'] in buy_trades[ticker_name] and len(buy_trades[ticker_name][row['security_type']]) > 0:
                    #Need a comparison of execution time
                    if buy_trades[ticker_name][row['security_type']]['execution_time'] > execution_time:
                        buy_trades[ticker_name][row['security_type']]['execution_time'] = execution_time
                    #Need to use Qty and Cost Basis to Calculate new Cost Basis for entry (averging and using qty as weight/ratio) 
                    buy_trades[ticker_name][row['security_type']]['cost_basis'] = ((buy_trades[ticker_name][row['security_type']]['quantity'] * buy_trades[ticker_name][row['security_type']]['cost_basis']) + cost_basis * quantity) / (buy_trades[ticker_name][row['security_type']]['quantity'] + quantity)
                    #Need to add to Qty
                    buy_trades[ticker_name][row['security_type']]['quantity'] += quantity
                else:
                    buy_trades[ticker_name][row['security_type']] = {
                        'execution_time': execution_time,
                        'quantity': quantity,
                        'cost_basis': cost_basis,
                    }

        # Handle sell trades
        # This will be taking in the sell order and do the following:
        # Perform checks to see if this is a valid sell order -- DONE
        # Once checks are performed, we will go into simmilar process of buy trades where we add and adjust entries in the sell_trades table -- DONE
        # Once done, will do a check against matching qty for the matching buy and sell entries in their md arrays
        # If this is true we will create trade object, delete buy and sell trade array entried for that configuration, validate trade objects and append to final trades array
        elif row['side'].upper() == 'SELL':
            #Need to check if options or not then proceed
            if security_type == 'Options':
                if not buy_trades[ticker_name][row['security_type']][expiry][strike] or buy_trades[ticker_name][row['security_type']][expiry][strike]['quantity'] == 0:
                    response = "No contracts remaining for " + str(ticker_name) + " " + str(expiry) + " " + str(strike) + " " + str(row['security_type'].upper()) + " but reporting another SELL Order"
                    logger.warning("Leaving Process CSV Transformer: " + response)
                    return False, response
                elif quantity > buy_trades[ticker_name][row['security_type']][expiry][strike]['quantity']:
                    response = "Not enough contracts remaining for " + str(ticker_name) + " " + str(expiry) + " " + str(strike) + " " + str(row['security_type'].upper())
                    logger.warning("Leaving Process CSV Transformer: " + response)
                    return False, response
                if sell_trades[ticker_name][row['security_type']][expiry][strike]:
                    #Need a comparison of execution time
                    if sell_trades[ticker_name][row['security_type']][expiry][strike]['execution_time'] < execution_time:
                        sell_trades[ticker_name][row['security_type']][expiry][strike]['execution_time'] = execution_time
                    #Need to use Qty and Cost Basis to Calculate new Cost Basis for entry (averging and using qty as weight/ratio) 
                    sell_trades[ticker_name][row['security_type']][expiry][strike]['cost_basis'] = ((sell_trades[ticker_name][row['security_type']][expiry][strike]['quantity'] * sell_trades[ticker_name][row['security_type']][expiry][strike]['cost_basis']) + cost_basis * quantity) / (sell_trades[ticker_name][row['security_type']][expiry][strike]['quantity'] + quantity)
                    #Need to add to Qty
                    sell_trades[ticker_name][row['security_type']][expiry][strike]['quantity'] += quantity
                else:
                    sell_trades[ticker_name][row['security_type']][expiry][strike] = {
                        'execution_time': execution_time,
                        'quantity': quantity,
                        'cost_basis': cost_basis,
                    }
            else:
                if not buy_trades[ticker_name][row['security_type']] or buy_trades[ticker_name][row['security_type']]['quantity'] == 0:
                    response = "No shares remaining for " + str(ticker_name) + " but reporting another SELL Order"
                    logger.warning("Leaving Process CSV Transformer: " + response)
                    return False, response
                elif quantity > buy_trades[ticker_name][row['security_type']]['quantity']:
                    response = "Not enough shares remaining for " + str(ticker_name)
                    logger.warning("Leaving Process CSV Transformer: " + response)
                    return False, response
                if sell_trades[ticker_name][row['security_type']]:
                    #Need a comparison of execution time
                    if sell_trades[ticker_name][row['security_type']]['execution_time'] < execution_time:
                        sell_trades[ticker_name][row['security_type']]['execution_time'] = execution_time
                    #Need to use Qty and Cost Basis to Calculate new Cost Basis for entry (averging and using qty as weight/ratio) 
                    sell_trades[ticker_name][row['security_type']]['cost_basis'] = ((sell_trades[ticker_name][row['security_type']]['quantity'] * sell_trades[ticker_name][row['security_type']]['cost_basis']) + cost_basis * quantity) / (sell_trades[ticker_name][row['security_type']]['quantity'] + quantity)
                    #Need to add to Qty
                    sell_trades[ticker_name][row['security_type']]['quantity'] += quantity
                else:
                    sell_trades[ticker_name][row['security_type']] = {
                        'execution_time': execution_time,
                        'quantity': quantity,
                        'cost_basis': cost_basis,
                    }
        
        ## create trade object       
        trade = {
            "buy_value" : "",
            "comments" : "",
            "expiry" : "",
            "percent_wl" : "",
            "pnl" : "",
            "rr" : "1:1",
            "security_type" : "",
            "strike" : "",
            "ticker_name" : "",
            "trade_date" : "",
            "trade_type" : "",
            "units" : "",
            "user_id" : user_id
        }
        
        if security_type == 'Options':
            if ('quantity' in buy_trades.get(ticker_name, {}).get(row['security_type'], {}).get(expiry, {}).get(strike, {})
                and 'quantity' in sell_trades.get(ticker_name, {}).get(row['security_type'], {}).get(expiry, {}).get(strike, {})
                and buy_trades[ticker_name][row['security_type']][expiry][strike]['quantity'] == sell_trades[ticker_name][row['security_type']][expiry][strike]['quantity']):
                # Determine if trade is a day trade or swing trade
                if (buy_trades[ticker_name][row['security_type']][expiry][strike]['execution_time'] != sell_trades[ticker_name][row['security_type']][expiry][strike]['execution_time']):
                    trade['trade_type'] = "Swing Trade"
                else:
                    trade['trade_type'] = "Day Trade"
                trade['buy_value'] = buy_trades[ticker_name][row['security_type']][expiry][strike]['cost_basis']
                final_expiry = transformDateFormart(expiry)
                trade['expiry'] = final_expiry
                trade['security_type'] = security_type
                trade['strike'] = strike
                trade['ticker_name'] = ticker_name
                trade['trade_date'] = sell_trades[ticker_name][row['security_type']][expiry][strike]['execution_time']
                trade['units'] = sell_trades[ticker_name][row['security_type']][expiry][strike]['quantity']
                #need to add for percent_wl and pnl calculations
                trade['pnl'] = (sell_trades[ticker_name][row['security_type']][expiry][strike]['cost_basis'] - buy_trades[ticker_name][row['security_type']][expiry][strike]['cost_basis']) * sell_trades[ticker_name][row['security_type']][expiry][strike]['quantity']
                trade['percent_wl'] = round((float(trade['pnl']) / (float(trade['buy_value'] * trade['units']))) * 100, 2)

                # need to call validateNewTradeFromCsv() to validate trade fields before running it through the algorithm if it doesnt pass validation, skip it
                response = tradeValidator.validateNewTradeFromCsv(trade)
                if response == True:
                    ## add trade object to trades array
                    trades.append(trade)
                    buy_trades[ticker_name][row['security_type']][expiry][strike] = {}
                    sell_trades[ticker_name][row['security_type']][expiry][strike] = {}
                else:
                    logger.warning("Leaving Process CSV Transformer: " + str(response))
                    return False, response[0]['result']
        else:
            if 'quantity' in buy_trades[ticker_name][row['security_type']] and 'quantity' in sell_trades[ticker_name][row['security_type']] and buy_trades[ticker_name][row['security_type']]['quantity'] == sell_trades[ticker_name][row['security_type']]['quantity']:
                # Determine if trade is a day trade or swing trade
                if (buy_trades[ticker_name][row['security_type']]['execution_time'] != sell_trades[ticker_name][row['security_type']]['execution_time']):
                    trade['trade_type'] = "Swing Trade"
                else:
                    trade['trade_type'] = "Day Trade"
                trade['buy_value'] = buy_trades[ticker_name][row['security_type']]['cost_basis']
                trade['expiry'] = None
                trade['security_type'] = security_type
                trade['strike'] = None
                trade['ticker_name'] = ticker_name
                trade['trade_date'] = sell_trades[ticker_name][row['security_type']]['execution_time']
                trade['units'] = sell_trades[ticker_name][row['security_type']]['quantity']
                #need to add for percent_wl and pnl calculations
                trade['pnl'] = (sell_trades[ticker_name][row['security_type']]['cost_basis'] - buy_trades[ticker_name][row['security_type']]['cost_basis']) * sell_trades[ticker_name][row['security_type']]['quantity']
                trade['percent_wl'] = round((float(trade['pnl']) / (float(trade['buy_value'] * trade['units']))) * 100, 2)

                # need to call validateNewTradeFromCsv() to validate trade fields before running it through the algorithm if it doesnt pass validation, skip it
                response = tradeValidator.validateNewTradeFromCsv(trade)
                if response == True:
                    ## add trade object to trades array
                    trades.append(trade)
                    buy_trades[ticker_name][row['security_type']] = {}
                    sell_trades[ticker_name][row['security_type']] = {}
                else:
                    logger.warning("Leaving Process CSV Transformer: " + str(response))
                    return False, response[0]['result']
        
    logger.info("Leaving Process CSV Transformer: " + str(trades))
    return True, trades

def transformDateFormart(input_date):
    logger.info("Enter Transform Date Format - Input Date: {}".format(str(input_date)))
    
    accepted_formats = [
        "%d-%b-%y",   # 21-Dec-22
        "%Y-%m-%d",   # 2022-12-21
        "%m/%d/%Y",   # 12/21/2022
        "%d/%m/%Y",   # 21/12/2022
        "%b %d, %Y",  # Dec 21, 2022
        "%d-%m-%Y",   # 21-12-2022
        "%m-%d-%Y",   # 12-21-2022
        "%Y/%m/%d",   # 2022/12/21
        "%Y.%m.%d",   # 2022.12.21
        "%d.%m.%Y",   # 21.12.2022
        "%m.%d.%Y",   # 12.21.2022
        "%m/%d/%y",   # 12/21/22
    ]
    
    parts = input_date.split('/')
    if len(parts) == 3:
        month, day, year = parts
        # Check if month or day is a single digit (i.e., without leading zero)
        if len(year) == 2 and year.isdigit() and month.isdigit() and day.isdigit() and (len(month) == 1 or len(day) == 1):
            month = parts[0].zfill(2)  # Add leading zero to month if needed
            day = parts[1].zfill(2)    # Add leading zero to day if needed
            year = parts[2]
            input_date = f"{month}/{day}/{year}"
            
    final_expiry = input_date
    for fmt in accepted_formats:
        logger.info("Checking... Date: {}, Tested Format: {}".format(str(input_date),str(fmt)))
        try:
            parsed_date = datetime.strptime(input_date, fmt)
            final_expiry = parsed_date.strftime("%Y-%m-%d")  # Convert to standard format
            logger.info("Date Format Match Found... Date: {}, Format: {}".format(str(input_date),str(fmt)))
            break
        except ValueError:
            logger.warning("Date Format Match Failed... Date: {}, Format: {}".format(str(input_date),str(fmt)))
            pass
    logger.info("Leaving Transform Date Format - Final Expiry Date: {}".format(str(final_expiry)))
    return final_expiry