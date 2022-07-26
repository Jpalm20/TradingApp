import utils

class Trade:
    
    def __init__(self,tradeID,userID,tradeType,securityType,tickerName,expiry,strike,value,numOfShares,rr,pnl,percentwl,comment):
        self.tradeID = tradeID
        self.userID = userID
        self.tradeType = tradeType
        self.securityType = securityType
        self.tickerName = tickerName
        self.expiry = expiry
        self.strike = strike
        self.value = value
        self.numOfShares = numOfShares
        self.rr = rr
        self.pnl = pnl
        self.percentwl = percentwl
        self.comment = comment
        
    def getTrade(tradeID):
        
        Query = """SELECT * FROM Trade WHERE trade_id = %s"""
        Args = (tradeID,)
        response = utils.execute_db(Query,Args)
        return response
    
    def addTrade(newTrade):
        
        Query = """INSERT INTO Trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        Args = (newTrade.userID,newTrade.tradeType,newTrade.securityType,newTrade.tickerName,
                            newTrade.expiry,newTrade.strike,newTrade.value,newTrade.numOfShares,newTrade.rr,
                            newTrade.pnl,newTrade.percentwl,newTrade.comment)
        response = utils.execute_db(Query,Args)
        return response
        
    def updateTrade(tradeID,changes):
        
        response = ""
        
        for key,value in changes.items():

            Query = """UPDATE Trade SET {} = %s WHERE trade_id = %s""".format(key)
            Args = (value,tradeID)
            response = response + '\n' + str(utils.execute_db(Query,Args)[0])
        
        return response
        
    def deleteTrade(tradeID):

        Query = """DELETE FROM Trade WHERE trade_id = %s"""
        Args = (tradeID,)
        response = utils.execute_db(Query,Args)
        return response
    
    
#--------Tests--------# 

#Testing addTrade       
#testTrade = Trade(None,1,"Swing Trade","Options","TSLA","9-21-2023",1000,500,5,"3:1",2532.52,254.3,"Test for Sunny :)")
#response = Trade.addTrade(testTrade)

#Testing updateTrade
#testTradeID = 3;
#testUpdateTradeInfo = {
#    "ticker_name": "QQQ",
#    "pnl": 250
#}
#response = Trade.updateTrade(testTradeID,testUpdateTradeInfo)

#Testing deleteTrade
#testTradeID = 7
#response = Trade.deleteTrade(testTradeID)

#Testing getTrade
#testTradeID = 3
#response = Trade.getTrade(testTradeID)

#print(response)