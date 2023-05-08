import os
import sys
import csv
from datetime import date, datetime, timedelta
from dateutil.parser import parse
from collections import defaultdict



script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import trade

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'validators',)
sys.path.append( mymodule_dir )
import tradeValidator

def transformNewTrade(request):
    if request['security_type'] == "Shares":
        request['expiry'] = None
        request['strike'] = None
    return request

def transformEditTrade(request):
    transformedRequest = {}
    for key in request:
        if request[key] != "":
            transformedRequest[key] = request[key]
    if ('security_type' in transformedRequest) and (transformedRequest['security_type'] == "Shares"):
        transformedRequest['expiry'] = None
        transformedRequest['strike'] = None
    return transformedRequest

def processCsv(user_id, file):
    ## algorithm
    trades = []
    buy_trades = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
    sell_trades = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))


    file.stream.seek(0)
    csv_string = file.stream.read().decode("utf-8-sig")
    reader = csv.DictReader(csv_string.splitlines())
    rows = list(reader)
    sorted_rows = sorted(rows, key=lambda row: (row['execution_time'], row['side']))

    for row in sorted_rows:
        if not all(col in row for col in ['security_type', 'ticker_name', 'execution_time', 'side', 'quantity', 'cost_basis']):
            continue

        if row['quantity'] == '' or row['security_type'] == '' or row['ticker_name'] == '' or row['execution_time'] == '' or row['side'] == '' or row['cost_basis'] == '':
            return False, "Empty fields exist in .csv please resolve"
        if int(row['quantity']) < 0:
            quantity = int(row['quantity']) * -1
        else:
            quantity = int(row['quantity'])
        cost_basis = float(row['cost_basis'])
        if row['security_type'].upper() == "PUT" or row['security_type'].upper() == "CALL":
            security_type = "Options"
            if 'expiry' not in row or 'strike' not in row or row['expiry'] == '' or row['strike'] == '' :
                return False, "Upload Failed, Options Trades must include Expiration and Strike Price"
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
                    return False, "No contracts remaining for " + str(ticker_name) + " " + str(expiry) + " " + str(strike) + " " + str(row['security_type'].upper()) + " but reporting another SELL Order"
                elif quantity > buy_trades[ticker_name][row['security_type']][expiry][strike]['quantity']:
                    return False, "Not enough contracts remaining for " + str(ticker_name) + " " + str(expiry) + " " + str(strike) + " " + str(row['security_type'].upper())
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
                    return False, "No shares remaining for " + str(ticker_name) + " but reporting another SELL Order"
                elif quantity > buy_trades[ticker_name][row['security_type']]['quantity']:
                    return False, "Not enough shares remaining for " + str(ticker_name)
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
            "comments" : None,
            "expiry" : "",
            "percent_wl" : "",
            "pnl" : "",
            "rr" : None,
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
                trade['expiry'] = expiry
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
                    return False, response
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
                    return False, response
        
        
    return True, trades
