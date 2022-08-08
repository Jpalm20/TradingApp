import json

from matplotlib import ticker
import mysql.connector

from sympy import sec

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
    
    def addTrade(newTrade):
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='TradingApp',
                                         user='root',
                                         password='tRaDiNgApP25!')

            Query = """INSERT INTO Trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            Args = (newTrade.userID,newTrade.tradeType,newTrade.securityType,newTrade.tickerName,
                                       newTrade.expiry,newTrade.strike,newTrade.value,newTrade.numOfShares,newTrade.rr,
                                       newTrade.pnl,newTrade.percentwl,newTrade.comment)

            cursor = connection.cursor()
            result = cursor.execute(Query,Args)
            connection.commit()
            
            print(cursor.rowcount, "Trade Added successfully into Trade table")
            response = "Trade Added successfully into Trade table"
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to Add Trade in MySQL: {}".format(error))
            response = "Failed to Add Trade in MySQL: {}".format(error)
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")
        
        return response
        
    def updateTrade(tradeID,changes):
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='TradingApp',
                                         user='root',
                                         password='tRaDiNgApP25!')
            
            for key,value in changes.items():

                Query = """UPDATE Trade SET {} = %s WHERE trade_id = %s""".format(key)
                Args = (value,tradeID)

                cursor = connection.cursor(dictionary=True)
                result = cursor.execute(Query,Args)
                connection.commit()

            print("Trade Updated successfully into Trade table")
            response = "Trade Updated successfully into Trade table"
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to Update Trade in MySQL: {}".format(error))
            response = "Failed to Update Trade in MySQL: {}".format(error)
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")
        
        return response
        
    def deleteTrade(tradeID):
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='TradingApp',
                                         user='root',
                                         password='tRaDiNgApP25!')

            Query = """DELETE FROM Trade WHERE trade_id = %s"""
            Args = (tradeID,)

            cursor = connection.cursor()
            result = cursor.execute(Query,Args)
            connection.commit()

            print("Trade Deleted successfully from Trade table")
            response = "Trade Deleted successfully from Trade table"
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to Delete Trade in MySQL: {}".format(error))
            response = "Failed to Delete Trade in MySQL: {}".format(error)
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")
        
        return response
 
#--------Tests--------# 

#Testing addTrade       
#testTrade = Trade(None,1,"Swing Trade","Options","TSLA","9-21-2023",1000,500,5,"3:1",2532.52,254.3,"Test for Sunny :)")
#response = Trade.addTrade(testTrade)

#Testing updateTrade
#testTradeID = 2;
#testUpdateTradeInfo = {
#    "ticker_name": "QQQ",
#    "pnl": 250
#}
#response = Trade.updateTrade(testTradeID,testUpdateTradeInfo)

#Testing deleteTrade
#testTradeID = 2
#response = Trade.deleteTrade(testTradeID)

#print(response)