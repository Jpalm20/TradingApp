import utils
from datetime import date, datetime, timedelta

class Accountvalue:
    
    def __init__(self,accountvalueID,userID,accountvalue,date):
        self.accountvalueID = accountvalueID
        self.userID = userID
        self.accountvalue = accountvalue
        self.date = date
  
    
    def getAccountValue(date,user_id):
            
        Query = """SELECT * FROM Accountvalue WHERE date = %s AND user_id = %s"""
        Args = (date,user_id)
        response = utils.execute_db(Query,Args)
        return response
    
    def getAccountValues(user_id,start_date):
            
        Query = """SELECT accountvalue, date FROM Accountvalue WHERE date >= %s AND date <= %s AND user_id = %s ORDER BY date DESC"""
        Args = (start_date-timedelta(days=7),start_date,user_id)
        response = utils.execute_db(Query,Args)
        return response
    
    def getAccountValuesTF(user_id,dates):
            
        Query = """SELECT accountvalue, date FROM Accountvalue WHERE user_id = %s and date in (%s, %s, %s, %s, %s, %s, %s) ORDER BY date DESC"""
        Args = (user_id,) + tuple([date.strftime('%Y-%m-%d') for date in dates])
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
    
    def updateAccountValue(user_id,date,accountvalue):
            
        Query = """UPDATE Accountvalue SET accountvalue = %s WHERE user_id = %s and date >= %s"""
        Args = (accountvalue,user_id,date)
        response = utils.execute_db(Query,Args)
        return response
    
    def deleteAccountValue(accountvalue_id):
        
        Query = """DELETE FROM Accountvalue WHERE accountvalue_id = %s"""
        Args = (accountvalue_id,)
        response = utils.execute_db(Query,Args)
        return response
    
    def insertFutureDay(user_id, date):
            
        Query = """INSERT IGNORE INTO Accountvalue (user_id, date, accountvalue)
                    SELECT %s,%s,prev.accountvalue
                    FROM Accountvalue AS your_new_value
                    LEFT JOIN Accountvalue AS prev ON prev.date = DATE_SUB(%s, INTERVAL 1 DAY) AND prev.user_id = %s
                    WHERE your_new_value.user_id = %s AND your_new_value.date = DATE_SUB(%s, INTERVAL 1 DAY)
                    AND NOT EXISTS (
                        SELECT 1
                        FROM Accountvalue AS existing
                        WHERE existing.user_id = %s AND existing.date = %s
                    )
                """
        Args = (user_id,date,date,user_id,user_id,date,user_id,date)
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
                    AND date <= DATE_ADD(UTC_DATE(), INTERVAL 1 DAY)
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
                    AND date <= DATE_ADD(UTC_DATE(), INTERVAL 1 DAY)
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
                    AND date <= DATE_ADD(UTC_DATE(), INTERVAL 1 DAY)
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