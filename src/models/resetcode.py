import utils
from datetime import date, datetime, timedelta

class Resetcode:
    
    def __init__(self,resetcodeID,userID,code,expiration):
        self.resetcodeID = resetcodeID
        self.userID = userID
        self.code = code
        self.expiration = expiration
  
    
    def getResetCode(code,user_id):
            
        Query = """SELECT resetcode_id, expiration FROM Resetcode WHERE code = %s AND user_id = %s"""
        Args = (code,user_id)
        response = utils.execute_db(Query,Args)
        return response
    
    def addResetCode(resetcodeInfo):
            
        Query = """INSERT INTO Resetcode VALUES (null,%s,%s,%s)"""
        Args = (resetcodeInfo.userID,resetcodeInfo.code,resetcodeInfo.expiration)
        response = utils.execute_db(Query,Args)
        return response
    
    def deleteResetCode(resetcode_id):
        
        Query = """DELETE FROM Resetcode WHERE resetcode_id = %s"""
        Args = (resetcode_id,)
        response = utils.execute_db(Query,Args)
        return response