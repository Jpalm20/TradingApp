import src.models.utils as utils
from datetime import date, datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Verificationcode:
    
    def __init__(self,verificationcodeID,userID,code,expiration,validated):
        self.verificationcodeID = verificationcodeID
        self.userID = userID
        self.code = code
        self.expiration = expiration
        self.validated = validated
        
    def to_dict(self):
        return {
            'verificationcode_id': self.verificationcodeID,
            'user_id': self.userID,
            'code': self.code,
            'expiration': self.expiration,
            'validated': self.validated
        }
    
    def getVerificationCode(code,user_id):
            
        logger.info("Entering Get Verification Code Model Function: " + "(code: ******, user_id: {})".format(str(user_id)))
        Query = """SELECT verificationcode_id, validated, expiration FROM verificationcode WHERE code = %s AND user_id = %s"""
        Args = (code,user_id)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Verification Code Model Function: " + str(response))
        return response
    
    def addVerificationCode(verificationcodeInfo):
            
        logger.info("Entering Add Verification Code Model Function: " + "(verificationcode_info: {})".format(str(utils.censor_log(Verificationcode.to_dict(verificationcodeInfo)))))
        Query = """INSERT INTO verificationcode VALUES (null,%s,%s,%s,DEFAULT)"""
        Args = (verificationcodeInfo.userID,verificationcodeInfo.code,verificationcodeInfo.expiration)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Add Verification Code Model Function: " + str(response))
        return response
    
    def deleteVerificationCode(verificationcode_id):
        
        logger.info("Entering Delete Verification Code Model Function: " + "(verificationcode_id: {})".format(str(verificationcode_id)))
        Query = """DELETE FROM verificationcode WHERE verificationcode_id = %s"""
        Args = (verificationcode_id,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete Verification Code Model Function: " + str(response))
        return response
    
    def expireVerificationCodes(user_id,time):
        
        logger.info("Entering Expire Verification Codes Model Function: " + "(user_id: {})".format(str(user_id)))
        Query = """UPDATE verificationcode SET expiration = %s WHERE user_id = %s"""
        Args = (time,user_id,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Expire Verification Codes Model Function: " + str(response))
        return response
    
    def validateVerificationCode(verificationcode_id):
        
        logger.info("Entering Validate Verification Code Model Function: " + "(verificationcode_id: {})".format(str(verificationcode_id)))
        Query = """UPDATE verificationcode SET validated = 1 WHERE verificationcode_id = %s"""
        Args = (verificationcode_id,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Validate Verification Code Model Function: " + str(response))
        return response
    
    def deleteUserVerificationCodes(user_id):
        
        logger.info("Entering Delete User Verification Codes Model Function: " + "(user_id: {})".format(str(user_id)))
        Query = """DELETE FROM verificationcode WHERE user_id = %s"""
        Args = (user_id,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete User Verification Codes Model Function: " + str(response))
        return response