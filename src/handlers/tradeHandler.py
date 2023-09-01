import os
import sys
from unittest import result
from datetime import date, datetime, timedelta
import csv
from flask import make_response



script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import trade

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import accountvalue

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'validators',)
sys.path.append( mymodule_dir )
import tradeValidator

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'transformers',)
sys.path.append( mymodule_dir )
import tradeTransformer

def logTrade(user_id, requestBody):
    response = tradeValidator.validateNewTrade(requestBody)
    if response != True:
        return response
    requestTransformed = tradeTransformer.transformNewTrade(requestBody)
    newTrade = trade.Trade(None,user_id,requestTransformed['trade_type'],requestTransformed['security_type'],
                        requestTransformed['ticker_name'],requestTransformed['trade_date'],requestTransformed['expiry'],requestTransformed['strike'],
                        requestTransformed['buy_value'],requestTransformed['units'],requestTransformed['rr'],requestTransformed['pnl'],
                        requestTransformed['percent_wl'],requestTransformed['comments'])
    response = trade.Trade.addTrade(newTrade)
    if response[0]:
        return {
            "result": response
        }, 400
    else:
        if ('trade_date' in requestTransformed and requestTransformed['trade_date'] is not None) and ('pnl' in requestTransformed and requestTransformed['pnl'] is not None):
            if (datetime.strptime(requestTransformed['trade_date'], '%Y-%m-%d').date() == datetime.now().date() + timedelta(days=1)):
                fdresponse = accountvalue.Accountvalue.insertFutureDay(user_id,requestTransformed['trade_date'])
                if fdresponse[0]:
                    return {
                    "result": fdresponse
                }, 400
            avresponse = accountvalue.Accountvalue.handleAddTrade(response[1])
            if avresponse[0]:
                return {
                    "result": avresponse
                }, 400
        return {
            "trade_id": response[1],
            "user_id": newTrade.userID,
            "trade_type": newTrade.tradeType,
            "security_type": newTrade.securityType,
            "ticker_name": newTrade.tickerName,
            "trade_date": newTrade.tradeDate,
            "expiry": newTrade.expiry,
            "strike": newTrade.strike,
            "buy_value": newTrade.value,
            "units": newTrade.numOfShares,
            "rr": newTrade.rr,
            "pnl": newTrade.pnl,
            "percent_wl": newTrade.percentwl,
            "comments": newTrade.comment,
            "result": "Trade Logged Successfully"
        }
        
def getExistingTrade(trade_id):
    response = trade.Trade.getTrade(trade_id)
    if 'trade_id' in response[0][0]:
        return {
            "trade_id": response[0][0]['trade_id'],
            "user_id": response[0][0]['user_id'],
            "trade_type": response[0][0]['trade_type'],
            "security_type": response[0][0]['security_type'],
            "ticker_name": response[0][0]['ticker_name'],
            "trade_date": response[0][0]['trade_date'],
            "expiry": response[0][0]['expiry'],
            "strike": response[0][0]['strike'],
            "buy_value": response[0][0]['buy_value'],
            "units": response[0][0]['units'],
            "rr": response[0][0]['rr'],
            "pnl": response[0][0]['pnl'],
            "percent_wl": response[0][0]['percent_wl'],
            "comments": response[0][0]['comments']
        }
    else:
        return {
            "result": response
        }, 400
    

def searchUserTicker(user_id, filter=None):
    if filter:
        filterBody = filter.to_dict()
        eval, response = tradeValidator.validateSearchTicker(filterBody)
        if eval == False:
            return {
                "result": response
            }, 400
        response = trade.Trade.getUserTicker(user_id,filter['ticker_name'])
    else:
        response = trade.Trade.getUserTicker(user_id)
    if response[0] or response[0] == []:
        return {
            "tickers": response[0]
        }
    else:
        return {
            "result": response
        }, 400


def editExistingTrade(trade_id,requestBody):
    og_trade_info = getExistingTrade(trade_id)
    response = tradeValidator.validateEditTrade(requestBody)
    if response != True:
        return response
    requestTransformed = tradeTransformer.transformEditTrade(requestBody)
    response = trade.Trade.updateTrade(trade_id,requestTransformed)
    response = trade.Trade.getTrade(trade_id)
    if ('pnl' in requestBody and requestBody['pnl'] != ""): #if updating pnl
        if ('pnl' in og_trade_info and og_trade_info['pnl'] is not None) and ('trade_date' in og_trade_info and og_trade_info['trade_date'] is not None): #pnl already exists, need to take difference and add it amonstg the days
            pnl_diff = float(requestBody['pnl']) - float(og_trade_info['pnl'])
            avresponse = accountvalue.Accountvalue.handlePnlUpdate(pnl_diff,trade_id)
            if avresponse[0]:
                return {
                    "result": avresponse
                }, 400
        elif ('pnl' in og_trade_info and og_trade_info['pnl'] is None) and ('trade_date' in og_trade_info and og_trade_info['trade_date'] is not None): #pnl was null originally, need to set value to full pnl not different from adding trade
            if (datetime.strptime(og_trade_info['trade_date'], '%Y-%m-%d').date() == datetime.now().date() + timedelta(days=1)):
                fdresponse = accountvalue.Accountvalue.insertFutureDay(og_trade_info['user_id'],og_trade_info['trade_date'])
                if fdresponse[0]:
                    return {
                    "result": fdresponse
                }, 400
            avresponse = accountvalue.Accountvalue.handleAddTrade(trade_id)
            if avresponse[0]:
                return {
                    "result": avresponse
                }, 400
    if('trade_date' in requestBody and requestBody['trade_date'] != ""):#if updating trade_date
        if ('pnl' in og_trade_info and og_trade_info['pnl'] is not None) and ('trade_date' in og_trade_info and og_trade_info['trade_date'] is not None): #trade_date already exists, need to add to extra days or subtract from days dependng on if updated date is further back or closer to today
            if (datetime.strptime(requestBody['trade_date'], '%Y-%m-%d').date() == datetime.now().date() + timedelta(days=1)):
                fdresponse = accountvalue.Accountvalue.insertFutureDay(og_trade_info['user_id'],requestBody['trade_date'])
                if fdresponse[0]:
                    return {
                    "result": fdresponse
                }, 400
            if (requestBody['trade_date'] < og_trade_info['trade_date']):
                first_date = requestBody['trade_date']
                second_date = og_trade_info['trade_date']
                avresponse = accountvalue.Accountvalue.handleDateUpdateAdd(first_date,second_date,trade_id)
                if avresponse[0]:
                    return {
                        "result": avresponse
                    }, 400
            elif (requestBody['trade_date'] > og_trade_info['trade_date']):
                second_date = requestBody['trade_date']
                first_date = og_trade_info['trade_date']
                avresponse = accountvalue.Accountvalue.handleDateUpdateSub(first_date,second_date,trade_id)
                if avresponse[0]:
                    return {
                        "result": avresponse
                    }, 400
        elif ('pnl' in og_trade_info and og_trade_info['pnl'] is not None) and ('trade_date' in og_trade_info and og_trade_info['trade_date'] is None): #trade_date was null originally, need to set all days with pnl fully as normal
            if (datetime.strptime(requestBody['trade_date'], '%Y-%m-%d').date() == datetime.now().date() + timedelta(days=1)):
                fdresponse = accountvalue.Accountvalue.insertFutureDay(og_trade_info['user_id'],requestBody['trade_date'])
                if fdresponse[0]:
                    return {
                    "result": fdresponse
                }, 400
            avresponse = accountvalue.Accountvalue.handleAddTrade(trade_id)
            if avresponse[0]:
                return {
                    "result": avresponse
                }, 400
        
    if 'trade_id' in response[0][0]:
        return {
            "trade_id": response[0][0]['trade_id'],
            "user_id": response[0][0]['user_id'],
            "trade_type": response[0][0]['trade_type'],
            "security_type": response[0][0]['security_type'],
            "ticker_name": response[0][0]['ticker_name'],
            "trade_date": response[0][0]['trade_date'],
            "expiry": response[0][0]['expiry'],
            "strike": response[0][0]['strike'],
            "buy_value": response[0][0]['buy_value'],
            "units": response[0][0]['units'],
            "rr": response[0][0]['rr'],
            "pnl": response[0][0]['pnl'],
            "percent_wl": response[0][0]['percent_wl'],
            "comments": response[0][0]['comments'],
            "result": "Trade Edited Successfully"
        }
    else:
        return {
            "result": response
        }, 400

def deleteExistingTrade(trade_id):
    trade_info = getExistingTrade(trade_id)
    if ('trade_date' in trade_info and trade_info['trade_date'] is not None) and ('pnl' in trade_info and trade_info['pnl'] is not None):
        avresponse = accountvalue.Accountvalue.handleDeleteTrade(trade_id)
        if avresponse[0]:
            return {
                "result": avresponse
            }, 400
    response = trade.Trade.deleteTrade(trade_id)
    if response[0]:
        return {
            "result": response
        }, 400
    else:
        return {
            "result": "Trade Successfully Deleted"
        }
        
def deleteTrades(requestBody):
    for trade_id in requestBody:
        trade_info = getExistingTrade(trade_id)
        if ('trade_date' in trade_info and trade_info['trade_date'] is not None) and ('pnl' in trade_info and trade_info['pnl'] is not None):
            avresponse = accountvalue.Accountvalue.handleDeleteTrade(trade_id)
            if avresponse[0]:
                return {
                    "result": avresponse
                }, 400
    response = trade.Trade.deleteTradesByID(requestBody)
    if response[0]:
        return {
            "result": response
        }, 400
    else:
        if len(requestBody) == 1:
            return {
                "result": "Trade Successfully Deleted"
            }
        elif len(requestBody) > 1:
            return {
                "result": "Trades Successfully Deleted"
            }

def importCsv(file, user_id):
    if not tradeValidator.validateCsv(file):
        return {
            "result": "Invalid CSV file. Missing required Headers"
        }, 400
    eval,result = tradeTransformer.processCsv(user_id, file)
    if eval:
        eval, response = trade.Trade.addTrades(result)
        if not eval:
            return {
                "result": response
            }, 400
        else:
            return {
                "result": "Trades Imported Successfully", 
                "trades": result
            } 
    else:
        return {
            "result": result
        }, 400   
        

def exportCsv(requestBody):
    if not tradeValidator.validateExportTrades(requestBody):
        return {
            "result": "Error Generating CSV"
        }, 400
    trades = requestBody['exported_trades']
    table_data = [list(trades[0].keys())]  # Header row
    for trade in trades:
        row = [str(trade[key]) for key in trade.keys()]
        table_data.append(row)
        
    final_trades = []    
    for row in table_data:
        final_trades.append([row[9],row[11],row[6],row[8],row[0],row[12],row[2],row[7],row[4],row[3],row[5]])

    csv_data = ''.join([','.join(row) + '\n' for row in final_trades])
    response = make_response(csv_data)
    response.headers['Content-Disposition'] = 'attachment; filename=trades.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response

        
        
#--------Tests--------# 

#Testing logUser()
#testTradeDict = {
#    "user_id": 1,
#   "trade_type": "Day Trade",
#    "security_type": "Options",
#    "ticker_name": "SPY",
#    "trade_date": "12-12-2022",
#    "expiry": "8-30-1998",
#    "strike": 420,
#    "buy_value": 50,
#    "units": 10,
#    "rr": "3:1",
#    "pnl": 150,
#    "percent_wl": 54.4,
#    "comments": "Test Comment"
#}
#response = logTrade(testTradeDict)

#Testing getExistingTrade()
#response = getExistingTrade(11)

#Testing editExistingTrade()
#testChanges = {
#    "pnl": 500,
#    "ticker_name": "MSFT"
#}
#response = editExistingTrade(11,testChanges)

#Testing deleteExistingTrade()
#response = deleteExistingTrade(9)

#print(response)