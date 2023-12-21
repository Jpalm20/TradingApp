import models.utils as utils
from datetime import date, datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Resetcode:
    
    def __init__(self,resetcodeID,userID,code,expiration):
        self.resetcodeID = resetcodeID
        self.userID = userID
        self.code = code
        self.expiration = expiration
  
    
    def getResetCode(code,user_id):
            
        logger.info("Entering Get Reset Code Model Function: " + "(code: {}, user_id: {})".format(str(code),str(user_id)))
        Query = """SELECT resetcode_id, expiration FROM resetcode WHERE code = %s AND user_id = %s"""
        Args = (code,user_id)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Reset Code Model Function: " + str(response))
        return response
    
    def addResetCode(resetcodeInfo):
            
        logger.info("Entering Add Reset Code Model Function: " + "(resetcode_info: {})".format(str(resetcodeInfo)))
        Query = """INSERT INTO resetcode VALUES (null,%s,%s,%s)"""
        Args = (resetcodeInfo.userID,resetcodeInfo.code,resetcodeInfo.expiration)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Add Reset Code Model Function: " + str(response))
        return response
    
    def deleteResetCode(resetcode_id):
        
        logger.info("Entering Delete Reset Code Model Function: " + "(resetcode_id: {})".format(str(resetcode_id)))
        Query = """DELETE FROM resetcode WHERE resetcode_id = %s"""
        Args = (resetcode_id,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete Reset Code Model Function: " + str(response))
        return response