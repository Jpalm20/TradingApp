import src.models.utils as utils
import logging

logger = logging.getLogger(__name__)

class Trade:
    
    def __init__(self,tradeID,userID,tradeType,securityType,tickerName,tradeDate,expiry,strike,value,numOfShares,rr,pnl,percentwl,comment):
        self.tradeID = tradeID
        self.userID = userID
        self.tradeType = tradeType
        self.securityType = securityType
        self.tickerName = tickerName
        self.tradeDate = tradeDate
        self.expiry = expiry
        self.strike = strike
        self.value = value
        self.numOfShares = numOfShares
        self.rr = rr
        self.pnl = pnl
        self.percentwl = percentwl
        self.comment = comment
        
    def getTrade(tradeID):
        
        logger.info("Entering Get Trade Model Function: " + "(trade_id: {})".format(str(tradeID)))
        Query = """SELECT * FROM trade WHERE trade_id = %s"""
        Args = (tradeID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Trade Model Function: " + str(response))
        return response
    
    def addTrade(newTrade):
        
        logger.info("Entering Add Trade Model Function: " + "(new_trade: {})".format(str(newTrade)))
        Query = """INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        Args = (newTrade.userID,newTrade.tradeType,newTrade.securityType,newTrade.tickerName,newTrade.tradeDate,
                            newTrade.expiry,newTrade.strike,newTrade.value,newTrade.numOfShares,newTrade.rr,
                            newTrade.pnl,newTrade.percentwl,newTrade.comment)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Add Trade Model Function: " + str(response))
        return response
    
    def addTrades(newTrades):
        
        logger.info("Entering Add Trades Model Function: " + "(new_trades: {})".format(str(newTrades)))
        response = {}
        Query = """INSERT INTO trade VALUES """
        Args = []
        
        for newTrade in newTrades:
            placeholders = "(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            Args.extend([newTrade['user_id'],newTrade['trade_type'],newTrade['security_type'],newTrade['ticker_name'],newTrade['trade_date'],
                        newTrade['expiry'],newTrade['strike'],newTrade['buy_value'],newTrade['units'],newTrade['rr'],
                        newTrade['pnl'],newTrade['percent_wl'],newTrade['comments']])
            if newTrades.index(newTrade) == 0:
                Query += placeholders
            else:
                Query += ", " + placeholders

        response = utils.execute_db(Query, tuple(Args))
        if response[0]:
            logger.warning("Leaving Add Trades Model Function: " + str(response))
            return False, response
        logger.info("Leaving Add Trades Model Function: " + str(response))
        return True, "Pass"
        
    def updateTrade(tradeID,changes):
        
        logger.info("Entering Update Trade Model Function: " + "(trade_id: {}, changes: {})".format(str(tradeID),str(changes)))
        updates = []
        for key,value in changes.items():
            if value is not None and value != 'NULL':
                updates.append(f"{key}='{value}'")
            if value == 'NULL':
                updates.append(f"{key}=NULL")
        updates = ", ".join(updates)
        Query = """UPDATE trade SET {} WHERE trade_id = %s""".format(updates)
        Query += ';'
        Args = (tradeID,)
        response = utils.execute_db(Query,Args)
        
        logger.info("Leaving Update Trade Model Function: " + str(response))
        return response
        
    def deleteTrade(tradeID):

        logger.info("Entering Delete Trade Model Function: " + "(trade_id: {})".format(str(tradeID)))
        Query = """DELETE FROM trade WHERE trade_id = %s"""
        Args = (tradeID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete Trade Model Function: " + str(response))
        return response
    
    def deleteTradesByID(tradeIDs):
    
        logger.info("Entering Delete Trades by ID Model Function: " + "(trade_ids: {})".format(str(tradeIDs)))
        Query = f"DELETE FROM trade WHERE trade_id in ({', '.join(str(tid) for tid in tradeIDs)})"
        Args = ()
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete Trades by ID Model Function: " + str(response))
        return response
    
    def deleteUserTrades(userID):
    
        logger.info("Entering Delete User Trades Model Function: " + "(user_id: {})".format(str(userID)))
        Query = """DELETE FROM trade WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete User Trades Model Function: " + str(response))
        return response
    
    def getUserTicker(userID,ticker=None):
        
        logger.info("Entering Get User Ticker Model Function: " + "(user_id: {}, ticker: {})".format(str(userID),str(ticker)))
        if (ticker == '' or ticker is None):
            Query = """SELECT distinct ticker_name FROM trade WHERE user_id = %s"""
            Args = (userID,)
            response = utils.execute_db(Query,Args)
            logger.info("Leaving Get User Ticker Model Function: " + str(response))
            return response
        else:
            Query = """SELECT distinct ticker_name FROM trade WHERE user_id = %s and ticker_name like %s """
            parameter = f"{ticker}%"
            Args = (userID,parameter)
            response = utils.execute_db(Query,Args)
            logger.info("Leaving Get User Ticker Model Function: " + str(response))
            return response
    