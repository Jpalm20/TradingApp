import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import trade

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'validators',)
sys.path.append( mymodule_dir )
import tradeValidator

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'transformers',)
sys.path.append( mymodule_dir )
import tradeTransformer

def logTrade(requestBody):
    response = tradeValidator.validateNewTrade(requestBody)
    if response != True:
        return response
    requestTransformed = tradeTransformer.transformNewTrade(requestBody)
    newTrade = trade.Trade(None,requestTransformed['user_id'],requestTransformed['trade_type'],requestTransformed['security_type'],
                        requestTransformed['ticker_name'],requestTransformed['expiry'],requestTransformed['strike'],
                        requestTransformed['buy_value'],requestTransformed['units'],requestTransformed['rr'],requestTransformed['pnl'],
                        requestTransformed['percent_wl'],requestTransformed['comments'])
    response = trade.Trade.addTrade(newTrade)
    if response[0]:
        return response, 400
    else:
        return {
            "trade_id": response[1],
            "user_id": newTrade.userID,
            "trade_type": newTrade.tradeType,
            "security_type": newTrade.securityType,
            "ticker_name": newTrade.tickerName,
            "expiry": newTrade.expiry,
            "strike": newTrade.strike,
            "buy_value": newTrade.value,
            "units": newTrade.numOfShares,
            "rr": newTrade.rr,
            "pnl": newTrade.pnl,
            "percent_wl": newTrade.percentwl,
            "comments": newTrade.comment
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
        return response, 400

def editExistingTrade(trade_id,requestBody):
    response = trade.Trade.updateTrade(trade_id,requestBody)
    response = trade.Trade.getTrade(trade_id)
    if 'trade_id' in response[0][0]:
        return {
            "trade_id": response[0][0]['trade_id'],
            "user_id": response[0][0]['user_id'],
            "trade_type": response[0][0]['trade_type'],
            "security_type": response[0][0]['security_type'],
            "ticker_name": response[0][0]['ticker_name'],
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
        return response, 400

def deleteExistingTrade(trade_id):
    response = trade.Trade.deleteTrade(trade_id)
    if response[0]:
        return response, 400
    else:
        return {
            "result": "Trade " + str(trade_id) + " Successfully Deleted"
        }
        
#--------Tests--------# 

#Testing logUser()
#testTradeDict = {
#    "user_id": 1,
#   "trade_type": "Day Trade",
#    "security_type": "Options",
#    "ticker_name": "SPY",
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