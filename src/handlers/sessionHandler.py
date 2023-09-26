import os
import sys
from datetime import date, datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)


script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import session


def validateToken(auth_token):
    logger.info("Entering Validate Token Handler: " + "(auth_token: {})".format(str(auth_token)))
    response = session.Session.getSession(auth_token)
    if not response[0]:
        response = "Auth Token Doesn't Exist"
        logger.warning("Leaving Validate Token Handler: " + response)
        return False, response
    elif 'expiration' in response[0][0]:
        if response[0][0]['expiration'] < datetime.now():
            response = "Auth Token Has Expired"
            logger.warning("Leaving Validate Token Handler: " + response)
            return False, response
        else:
            response = session.Session.refreshExpiration(response[0][0]['session_id'])
            response = "Token Validated"
            logger.info("Leaving Validate Token Handler: " + response)
            return True, response   
    else:
        response = "An Issue Occurred Validating Auth Token, Please Try Again"
        logger.warning("Leaving Validate Token Handler: " + response)
        return False, response
    
def logoutSession(auth_token):
    logger.info("Entering Logout Session Handler: " + "(auth_token: {})".format(str(auth_token)))
    response = session.Session.expireSession(auth_token)
    responseSession = session.Session.getSession(auth_token)
    if 'expiration' in responseSession[0][0] and responseSession[0][0]['expiration'] <= datetime.now()+timedelta(seconds=1):
        response = {
            "result": "User Logged Out"
        }
        logger.info("Leaving Logout Session Handler: " + str(response))
        return response
    else:
        response = {
            "result": "There was an issue expiring this Session, User not Logged Out",
            "expiration": str(responseSession[0][0]['expiration']),
            "now" : str(datetime.now())
        }
        logger.warning("Leaving Logout Session Handler: " + str(response))
        return response, 400
        
def getUserFromToken(auth_token):
    logger.info("Entering Get User From Token Handler: " + "(auth_token: {})".format(str(auth_token)))
    response = session.Session.getUserFromSession(auth_token)
    if 'user_id' in response[0][0]:
        logger.info("Leaving Get User From Token Handler: " + "(user_id: {})".format(str(response[0][0]['user_id'])))
        return True, response[0][0]['user_id']
    else:
        response = "No User Associated with this Session"
        logger.warning("Leaving Get User From Token Handler: " + response)
        return False, response
    
def getEmailFromToken(auth_token):
    logger.info("Entering Get Email From Token Handler: " + "(auth_token: {})".format(str(auth_token)))
    response = session.Session.getEmailFromSession(auth_token)
    if 'email' in response[0][0]:
        logger.info("Leaving Get Email From Token Handler: " + + "(email: {})".format(str(response[0][0]['email'])))
        return True, response[0][0]['email']
    else:
        response = "No Email Associated with this Session"
        logger.warning("Leaving Get Email From Token Handler: " + response)
        return False, response