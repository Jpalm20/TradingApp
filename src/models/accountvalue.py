import utils
from datetime import date, datetime, timedelta

class Accountvalue:
    
    def __init__(self,accountvalueID,userID,accountvalue,date):
        self.accountvalueID = accountvalueID
        self.userID = userID
        self.accountvalue = accountvalue
        self.date = date
  
    
    def getAccountValue(date,user_id):
            
        Query = """SELECT accountvalue_id, accountvalue, date FROM Accountvalue WHERE date = %s AND user_id = %s"""
        Args = (date,user_id)
        response = utils.execute_db(Query,Args)
        return response
    
    def getAccountValues(user_id):
            
        Query = """SELECT accountvalue, date FROM Accountvalue WHERE date >= %s AND date <= %s AND user_id = %s ORDER BY date DESC"""
        Args = (date.today()-timedelta(days=7),date.today(),user_id)
        response = utils.execute_db(Query,Args)
        return response
    
    def accountValueJob():
            
        Query = """CALL CopyAccountValue()"""
        Args = ()
        response = utils.execute_db(Query,Args)
        return response
    
    def addAccountValue(accountvalueInfo):
            
        Query = """INSERT INTO Accountvalue VALUES (null,%s,%s,%s)"""
        Args = (accountvalueInfo.userID,accountvalueInfo.accountvalue,accountvalueInfo.date)
        response = utils.execute_db(Query,Args)
        return response
    
    def updateAccountValue(accountvalue_id,accountvalue):
            
        Query = """UPDATE Accountvalue SET accountvalue = %s WHERE accountvalue_id = %s"""
        Args = (accountvalue,accountvalue_id)
        response = utils.execute_db(Query,Args)
        return response
    
    def deleteAccountValue(accountvalue_id):
        
        Query = """DELETE FROM Accountvalue WHERE accountvalue_id = %s"""
        Args = (accountvalue_id,)
        response = utils.execute_db(Query,Args)
        return response
    
    def handleAddTrade(trade_id):
        
        Query = """UPDATE Accountvalue
                    SET accountvalue = accountvalue + (
                        SELECT pnl
                        FROM trade
                        WHERE trade_id = %s
                    )
                    WHERE date >= (
                        SELECT trade_date
                        FROM trade
                        WHERE trade_id = %s
                    ) 
                    AND date <= UTC_DATE()
                    AND user_id = (
                        SELECT user_id
                        FROM trade
                        WHERE trade_id = %s
                    )
                """
        Args = (trade_id,trade_id,trade_id)
        response = utils.execute_db(Query,Args)
        return response
    
    def handleDeleteTrade(trade_id):
        
        Query = """UPDATE Accountvalue
                    SET accountvalue = accountvalue - (
                        SELECT pnl
                        FROM trade
                        WHERE trade_id = %s
                    )
                    WHERE date >= (
                        SELECT trade_date
                        FROM trade
                        WHERE trade_id = %s
                    ) 
                    AND date <= UTC_DATE()
                    AND user_id = (
                        SELECT user_id
                        FROM trade
                        WHERE trade_id = %s
                    )
                """
        Args = (trade_id,trade_id,trade_id)
        response = utils.execute_db(Query,Args)
        return response
    
    def handlePnlUpdate(pnl_diff,trade_id):
        
        Query = """UPDATE Accountvalue
                    SET accountvalue = accountvalue + %s
                    WHERE date >= (
                        SELECT trade_date
                        FROM trade
                        WHERE trade_id = %s
                    ) 
                    AND date <= UTC_DATE()
                    AND user_id = (
                        SELECT user_id
                        FROM trade
                        WHERE trade_id = %s
                    )
                """
        Args = (pnl_diff,trade_id,trade_id)
        response = utils.execute_db(Query,Args)
        return response
    
    def handleDateUpdateAdd(first_date,second_date,trade_id):
            
        Query = """UPDATE Accountvalue
                    SET accountvalue = accountvalue + (
                        SELECT pnl
                        FROM trade
                        WHERE trade_id = %s
                    )
                    WHERE date >= %s
                    AND date < %s
                    AND user_id = (
                        SELECT user_id
                        FROM trade
                        WHERE trade_id = %s
                    )
                """
        Args = (trade_id,first_date,second_date,trade_id)
        response = utils.execute_db(Query,Args)
        return response
    
    def handleDateUpdateSub(first_date,second_date,trade_id):
            
        Query = """UPDATE Accountvalue
                    SET accountvalue = accountvalue - (
                        SELECT pnl
                        FROM trade
                        WHERE trade_id = %s
                    )
                    WHERE date >= %s
                    AND date < %s
                    AND user_id = (
                        SELECT user_id
                        FROM trade
                        WHERE trade_id = %s
                    )
                """
        Args = (trade_id,first_date,second_date,trade_id)
        response = utils.execute_db(Query,Args)
        return response