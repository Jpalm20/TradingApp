import os
import sys
from datetime import date, datetime, timedelta
import json

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import session


def validateToken(auth_token):
    response = session.Session.getSession(auth_token)
    if not response[0]:
        return False, "Auth Token Doesn't Exist"
    elif 'expiration' in response[0][0]:
        if response[0][0]['expiration'] < datetime.now():
            return False, "Auth Token Has Expired"
        else:
            response = session.Session.refreshExpiration(response[0][0]['session_id'])
            return True, "True"   
    else:
        return False, "An Issue Occurred Validating Auth Token, Please Try Again"