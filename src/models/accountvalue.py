import utils as utils
from datetime import date, datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Accountvalue:
    
    def __init__(self,accountvalueID,userID,accountvalue,date):
        self.accountvalueID = accountvalueID
        self.userID = userID
        self.accountvalue = accountvalue
        self.date = date
  
    
    def getAccountValue(date,user_id):
        
        logger.info("Entering Get Account Value Model Function: " + "(user_id: {}, date: {})".format(str(user_id),str(date)))
        Query = """SELECT * FROM accountvalue WHERE date = %s AND user_id = %s"""
        Args = (date,user_id)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Account Value Model Function: " + str(response))
        return response
    
    def getAccountValues(user_id,start_date):
            
        logger.info("Entering Get Account Values Model Function: " + "(user_id: {}, start_date: {})".format(str(user_id),str(start_date)))
        Query = """SELECT accountvalue, date FROM accountvalue WHERE date >= %s AND date <= %s AND user_id = %s ORDER BY date DESC"""
        Args = (start_date-timedelta(days=7),start_date,user_id)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Account Values Model Function: " + str(response))
        return response
    
    def getAccountValuesTF(user_id,dates):
            
        logger.info("Entering Get Account Values Time Frame Model Function: " + "(user_id: {}, dates: {})".format(str(user_id),str(dates)))
        Query = """SELECT accountvalue, date FROM accountvalue WHERE user_id = %s and date in (%s, %s, %s, %s, %s, %s, %s) ORDER BY date DESC"""
        Args = (user_id,) + tuple([date.strftime('%Y-%m-%d') for date in dates])
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Account Values Time Frame Model Function: " + str(response))
        return response
    
    def accountValueJob():
            
        logger.info("Entering accountValueJob Model Function: ")
        Query = """CALL CopyAccountValue()"""
        Args = ()
        response = utils.execute_db(Query,Args)
        logger.info("Leaving accountValueJob Model Function: " + str(response))
        return response
    
    def addAccountValue(accountvalueInfo):
            
        logger.info("Entering Add Account Value Model Function: " + "(accountvalue_info: {})".format(str(accountvalueInfo)))
        Query = """INSERT INTO accountvalue VALUES (null,%s,%s,%s)"""
        Args = (accountvalueInfo.userID,accountvalueInfo.accountvalue,accountvalueInfo.date)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Add Account Value Model Function: " + str(response))
        return response
    
    def updateAccountValue(user_id,date,accountvalue):
            
        logger.info("Entering Update Account Value Model Function: " + "(user_id: {}, date: {}, accountvalue: {})".format(str(user_id),str(date),str(accountvalue)))
        Query = """UPDATE accountvalue SET accountvalue = %s WHERE user_id = %s and date >= %s"""
        Args = (accountvalue,user_id,date)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Update Account Value Model Function: " + str(response))
        return response
    
    def deleteAccountValue(accountvalue_id):
        
        logger.info("Entering Delete Account Value Model Function: " + "(accountvalue_id: {})".format(str(accountvalue_id)))
        Query = """DELETE FROM accountvalue WHERE accountvalue_id = %s"""
        Args = (accountvalue_id,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete Account Value Model Function: " + str(response))
        return response
    
    def deleteUserAccountValues(user_id):
        
        logger.info("Entering Delete User Account Values Model Function: " + "(user_id: {})".format(str(user_id)))
        Query = """DELETE FROM accountvalue WHERE user_id = %s"""
        Args = (user_id,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete User Account Values Model Function: " + str(response))
        return response
    
    def insertFutureDay(user_id, date):
            
        logger.info("Entering Insert Future Day Model Function: " + "(user_id: {}, date: {})".format(str(user_id),str(date)))
        Query = """INSERT IGNORE INTO accountvalue (user_id, date, accountvalue)
                    SELECT %s,%s,prev.accountvalue
                    FROM accountvalue AS your_new_value
                    LEFT JOIN accountvalue AS prev ON prev.date = DATE_SUB(%s, INTERVAL 1 DAY) AND prev.user_id = %s
                    WHERE your_new_value.user_id = %s AND your_new_value.date = DATE_SUB(%s, INTERVAL 1 DAY)
                    AND NOT EXISTS (
                        SELECT 1
                        FROM accountvalue AS existing
                        WHERE existing.user_id = %s AND existing.date = %s
                    )
                """
        Args = (user_id,date,date,user_id,user_id,date,user_id,date)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Insert Future Day Model Function: " + str(response))
        return response
    
    def handleAddTrade(trade_id):
        
        logger.info("Entering Handle Add Trade Model Function: " + "(trade_id: {})".format(str(trade_id)))
        Query = """UPDATE accountvalue
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
        logger.info("Leaving Handle Add Trade Model Function: " + str(response))
        return response
    
    def handleDeleteTrade(trade_id):
        
        logger.info("Entering Handle Delete Trade Model Function: " + "(trade_id: {})".format(str(trade_id)))
        Query = """UPDATE accountvalue
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
        logger.info("Leaving Handle Delete Trade Model Function: " + str(response))
        return response
    
    def handlePnlUpdate(pnl_diff,trade_id):
        
        logger.info("Entering Handle PnL Update Model Function: " + "(trade_id: {}, pnl_diff: {})".format(str(trade_id),str(pnl_diff)))
        Query = """UPDATE accountvalue
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
        logger.info("Leaving Handle Delete Trade Model Function: " + str(response))
        return response
    
    def handleDateUpdateAdd(first_date,second_date,trade_id):
            
        logger.info("Entering Handle Date Update Add Model Function: " + "(trade_id: {}, first_date: {}, second_date: {})".format(str(trade_id),str(first_date),str(second_date)))
        Query = """UPDATE accountvalue
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
        logger.info("Leaving Handle Date Update Add Model Function: " + str(response))
        return response
    
    def handleDateUpdateSub(first_date,second_date,trade_id):
            
        logger.info("Entering Handle Date Update Subtract Model Function: " + "(trade_id: {}, first_date: {}, second_date: {})".format(str(trade_id),str(first_date),str(second_date)))
        Query = """UPDATE accountvalue
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
        logger.info("Leaving Handle Date Update Subtract Model Function: " + str(response))
        return response