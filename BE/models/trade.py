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
        
        #Send to DB to Save
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='TradingApp',
                                         user='root',
                                         password='tRaDiNgApP25!')

            mySql_Create_Table_Query = """INSERT INTO Trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            mySql_Create_Table_Args = (newTrade.userID,newTrade.tradeType,newTrade.securityType,newTrade.tickerName,
                                       newTrade.expiry,newTrade.strike,newTrade.value,newTrade.numOfShares,newTrade.rr,
                                       newTrade.pnl,newTrade.percentwl,newTrade.comment)

            cursor = connection.cursor()
            result = cursor.execute(mySql_Create_Table_Query,mySql_Create_Table_Args)
            connection.commit()
            print(cursor.rowcount, "Trade added successfully into Trade table")
            response = "Trade added successfully into Trade table"
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to Add Trade in MySQL: {}".format(error))
            response = "Failed to Add Trade in MySQL: {}".format(error)
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")
        
        return response
    
testTrade = Trade(None,1,"Swing Trade","Options","TSLA","9-21-2023",1000,500,5,"3:1",2532.52,254.3,"Test for Sunny :)")
response = Trade.addTrade(testTrade)
print(response)
        
    #def updateTrade(tradeID, key, newValue):
        #tradeInfo.list.update({key: newValue})
        #Update DB entry for trade
        
        
    #def deleteTrade(tradeID):
        #Delete DB Entry