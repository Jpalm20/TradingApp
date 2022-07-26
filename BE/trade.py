import json
import storage

class Trade:
    
    def add(tradeID, tradeType, securityType, expiry, strike, value, numOfShares, rr, pnl, percentwl):
        tradeInfo = {
            "tradeID": tradeID,
            "tradeType": tradeType,
            "securityType": securityType,
            "xpiry": expiry,
            "strike": strike,
            "value": value,
            "numOfShares": numOfShares,
            "rr": rr,
            "pnl": pnl,
            "percentwl": percentwl
        }
        #Send to DB to Save
        storage.Trades.insert(tradeInfo)
        
    def update(tradeID, key, newValue):
        #tradeInfo.list.update({key: newValue})
        #Update DB entry for trade
        storage.Trades.update(self)
        
    def delete(tradeID):
        del self
        #Delete DB Entry
        storage.Trades.remove(self)