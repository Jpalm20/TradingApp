import utils as utils
from datetime import date, datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Session:
    
    def __init__(self,sessionID,userID,token,expiration):
        self.sessionID = sessionID
        self.userID = userID
        self.token = token
        self.expiration = expiration
  
    
    def getSession(token):
            
        logger.info("Entering Get Session Model Function: " + "(token: {})".format(str(token)))
        Query = """SELECT session_id, expiration FROM Session WHERE token = %s"""
        Args = (token,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Session Model Function: " + str(response))
        return response
    
    def addSession(tokenInfo):
        
        logger.info("Entering Add Session Model Function: " + "(token_info: {})".format(str(tokenInfo)))
        Query = """INSERT INTO Session VALUES (null,%s,%s,%s)"""
        Args = (tokenInfo.userID,tokenInfo.token,tokenInfo.expiration)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Add Session Model Function: " + str(response))
        return response
    
    def refreshExpiration(sessionID):
        
        logger.info("Entering Refresh Expiration Model Function: " + "(session_id: {})".format(str(sessionID)))
        Query = """UPDATE Session SET expiration = %s WHERE session_id = %s"""
        Args = (datetime.now()+timedelta(hours=24),sessionID)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Refresh Expiration Model Function: " + str(response))
        return response
    
    def deleteUserSessions(userID):
        
        logger.info("Entering Delete User Session Model Function: " + "(user_id: {})".format(str(userID)))
        Query = """DELETE FROM Session WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete User Session Model Function: " + str(response))
        return response
    
    def expireSession(token):
        
        logger.info("Entering Expire Session Model Function: " + "(token: {})".format(str(token)))
        Query = """UPDATE Session SET expiration = %s WHERE token = %s"""
        Args = (datetime.now(),token)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Expire Session Model Function: " + str(response))
        return response
    
    def getUserFromSession(token):
            
        logger.info("Entering Get User from Session Model Function: " + "(token: {})".format(str(token)))
        Query = """SELECT user_id FROM Session WHERE token = %s"""
        Args = (token,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User from Session Model Function: " + str(response))
        return response
    
    def getEmailFromSession(token):
            
        logger.info("Entering Get Email from Session Model Function: " + "(token: {})".format(str(token)))
        Query = """SELECT u.email FROM User u JOIN Session s on s.user_id = u.user_id where s.token = %s"""
        Args = (token,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Email from Session Model Function: " + str(response))
        return response
    
#--------Tests--------# 

#Testing addSession      
#testSession = Session(None,71,"testtoken",datetime.now())
#response = Session.addSession(testSession)

#print(response)