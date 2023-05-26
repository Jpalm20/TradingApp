import utils
from datetime import date, datetime, timedelta

class Session:
    
    def __init__(self,sessionID,userID,token,expiration):
        self.sessionID = sessionID
        self.userID = userID
        self.token = token
        self.expiration = expiration
  
    
    def getSession(token):
            
        Query = """SELECT session_id, expiration FROM Session WHERE token = %s"""
        Args = (token,)
        response = utils.execute_db(Query,Args)
        return response
    
    def addSession(tokenInfo):
            
        Query = """INSERT INTO Session VALUES (null,%s,%s,%s)"""
        Args = (tokenInfo.userID,tokenInfo.token,tokenInfo.expiration)
        response = utils.execute_db(Query,Args)
        return response
    
    def refreshExpiration(sessionID):
        
        Query = """UPDATE Session SET expiration = %s WHERE session_id = %s"""
        Args = (datetime.now()+timedelta(hours=24),sessionID)
        response = utils.execute_db(Query,Args)
        return response
    
    def deleteUserSessions(userID):
        
        Query = """DELETE FROM Session WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        return response
    
    def expireSession(token):
        
        Query = """UPDATE Session SET expiration = %s WHERE token = %s"""
        Args = (datetime.now(),token)
        response = utils.execute_db(Query,Args)
        return response
    
    def getUserFromSession(token):
            
        Query = """SELECT user_id FROM Session WHERE token = %s"""
        Args = (token,)
        response = utils.execute_db(Query,Args)
        return response
    
    def getEmailFromSession(token):
            
        Query = """SELECT u.email FROM User u JOIN Session s on s.user_id = u.user_id where s.token = %s"""
        Args = (token,)
        response = utils.execute_db(Query,Args)
        return response
    
#--------Tests--------# 

#Testing addSession      
#testSession = Session(None,71,"testtoken",datetime.now())
#response = Session.addSession(testSession)

#print(response)