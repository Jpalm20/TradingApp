import os
import sys
import re
from datetime import date, datetime, timedelta
import logging
from forex_python.converter import CurrencyCodes

logger = logging.getLogger(__name__)


script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import utils


def validateNewUser(request):
    logger.info("Entering Validate New User Validator: " + "(request: {})".format(str(utils.censor_log(request))))
    if 'password' not in request or request['password'] == '' or len(request['password']) < 8:
        response = "Must Include a Password of at Least 8 Characters, Please Try Again"
        logger.warning("Leaving Validate New User Validator: " + response)
        return {
            "result": response
        }, 403
    if 'email' not in request or request['email'] == '' or '@' not in request['email'] or '.' not in request['email']:
        response = "Must Include a Valid Email Format, Please Try Again"
        logger.warning("Leaving Validate New User Validator: " + response)
        return {
            "result": response
        }, 403
    response = user.User.getUserbyEmail(request['email'])
    if response[0] and 'email' in response[0][0]:
        response = "A User with this Email Already Exist, Sign Up with a Different Email"
        logger.warning("Leaving Validate New User Validator: " + response)
        return {
            "result": response
        }, 403 
    #need to validate blanks as well, might be easier to set required fields on FE if possible
    logger.info("Leaving Validate New User Validator: ")
    return True

def validateEditUser(request):
    logger.info("Entering Validate Edit User Validator: " + "(request: {})".format(str(request)))
    if 'password' in request:
        response = "You Can't Change Password This Way, Please Try Again"
        logger.warning("Leaving Validate Edit User Validator: " + response)
        return {
            "result": response
        }, 403
    if 'email' in request and request['email'] != '' and ('@' not in request['email'] or '.' not in request['email']):
        response = "Invalid Email Format, Try Upating Again"
        logger.warning("Leaving Validate Edit User Validator: " + response)
        return {
            "result": response
        }, 403
    if 'email' in request:
        response = user.User.getUserbyEmail(request['email'])
        if response[0] and 'email' in response[0][0]:
            response = "A User with this Email Already Exist, Try Updating with a Different Email"
            logger.warning("Leaving Validate Edit User Validator: " + response)
            return {
                "result": response
            }, 403
    logger.info("Leaving Validate Edit User Validator: ")
    return True

def validateChangePassword(request):
    logger.info("Entering Validate Change Password Validator: " + "(request: {})".format(str(utils.censor_log(request))))
    if ('curr_pass' not in request or request['curr_pass'] == '' or len(request['curr_pass']) < 8) or ('new_pass_1' not in request or request['new_pass_1'] == '' or len(request['new_pass_1']) < 8) or ('new_pass_2' not in request or request['new_pass_2'] == '' or len(request['new_pass_2']) < 8):
        response = "All Passwords Must be at Least 8 Characters, Please Try Again"
        logger.warning("Leaving Validate Change Password Validator: " + response)
        return {
            "result": response
        }, 403 
    if (request['new_pass_1'] != request['new_pass_2']):
        response = "Both New Password Entries Must Match, Please Try Again"
        logger.warning("Leaving Validate Change Password Validator: " + response)
        return {
            "result": response
        }, 403 
    logger.info("Leaving Validate Change Password Validator: ")
    return True

def validateReportBug(request):
    logger.info("Entering Validate Bug Report Validator: " + "(request: {})".format(str(request)))
    if ('summary' not in request or request['summary'] == '') or ('page' not in request or request['page'] == '') or ('description' not in request or request['description'] == '') or ('requestType' not in request or request['requestType'] == ''):
        response = "Please Include All Fields"
        logger.warning("Leaving Validate Bug Report Validator: " + response)
        return {
            "result": response
        }, 403 
    if (request['requestType'] != 'Bug Report' and request['requestType'] != 'Feature Request'):
        response = "Please Select a Valid Request Type"
        logger.warning("Leaving Validate Bug Report Validator: " + response)
        return {
            "result": response
        }, 403 
    logger.info("Leaving Validate Bug Report Validator: ")
    return True

def validateResetPassword(request):
    logger.info("Entering Validate Reset Password Validator: " + "(request: {})".format(str(utils.censor_log(request))))
    if ('new_pass_1' not in request or request['new_pass_1'] == '' or len(request['new_pass_1']) < 8) or ('new_pass_2' not in request or request['new_pass_2'] == '' or len(request['new_pass_2']) < 8):
        response = "Password Must be at Least 8 Characters, Please Try Again"
        logger.warning("Leaving Validate Reset Password Validator: " + response)
        return {
            "result": response
        }, 403 
    if (request['new_pass_1'] != request['new_pass_2']):
        response = "Both New Password Entries Must Match, Please Try Again"
        logger.warning("Leaving Validate Reset Password Validator: " + response)
        return {
            "result": response
        }, 403 
    logger.info("Leaving Validate Reset Password Validator: ")
    return True

def validateSetAccountValue(request):
    logger.info("Entering Validate Set Account Value Validator: " + "(request: {})".format(str(request)))
    if('accountvalue' not in request):
        response = "Must Include an Account Value"
        logger.warning("Leaving Validate Set Account Value Validator: " + response)
        return {
            "result": response
        }, 400
    if('date' not in request or re.match(r'^\d{4}-\d{2}-\d{2}$', request['date']) is None):
        response = "Missing or invalid 'date' key, Please provide the Date where you wish to update your Account Value in YYYY-MM-DD format"
        logger.warning("Leaving Validate Set Account Value Validator: " + response)
        return {
            "result": response
        }, 400
    if('date' in request and datetime.strptime(request['date'], '%Y-%m-%d').date() > datetime.now().date() + timedelta(days=1)):
        response = "Invalid date. The 'date' provided is more than one day into the future of the current UTC date."
        logger.warning("Leaving Validate Set Account Value Validator: " + response)
        return {
            "result": response
        }, 400
    logger.info("Leaving Validate Set Account Value Validator: ")
    return True

def validateGetAccountValue(request):
    logger.info("Entering Validate Get Account Value Validator: " + "(request: {})".format(str(request)))
    if('date' not in request or re.match(r'^\d{4}-\d{2}-\d{2}$', request['date']) is None):
        response = "Missing or invalid 'date' key, Please provide the Date where you wish to start from in YYYY-MM-DD format"
        logger.warning("Leaving Validate Get Account Value Validator: " + response)
        return {
            "result": response
        }, 400
    if('date' in request and datetime.strptime(request['date'], '%Y-%m-%d').date() > datetime.now().date() + timedelta(days=1)):
        response = "Invalid date. The 'date' provided is more than one day into the future of the current UTC date."
        logger.warning("Leaving Validate Get Account Value Validator: " + response)
        return {
            "result": response
        }, 400
    if('time_frame' in request and request['time_frame'] not in ['Day', 'Week', 'Month', 'Year']):
        response = "Invalid Time Frame. The 'time frame' provided is not a valid option (Day, Week, Month, Year)"
        logger.warning("Leaving Validate Get Account Value Validator: " + response)
        return {
            "result": response
        }, 400
    logger.info("Leaving Validate Get Account Value Validator: ")
    return True

def validateToggleFeatureFlags(request):
    logger.info("Entering Validate Toggle Feature Flags Validator: " + "(request: {})".format(str(request)))
    valid_featureflags = ['email_optin','account_value_optin','2fa_optin']
    for ff in request:
        if(ff not in valid_featureflags):
            response = "Please provide only valid feature flags in your request"
            logger.warning("Leaving Validate Toggle Feature Flags Validator: " + response)
            return {
                "result": response
            }, 400
    logger.info("Leaving Validate Toggle Feature Flags Validator: ")
    return True

def validateUpdatePreferredCurrency(request):
    logger.info("Entering Validate Update Preferred Currency Validator: " + "(request: {})".format(str(request)))
    currency_codes = CurrencyCodes()
    if 'preferred_currency' not in request or request['preferred_currency'] == '':
        response = "New Currency Code Missing"
        logger.warning("Leaving Validate Update Preferred Currency Validator: " + response)
        return {
            "result": response
        }, 400
    if len(request['preferred_currency']) != 3 or currency_codes.get_symbol(request['preferred_currency']) is None:
        response = "New Currency Code is Invalid"
        logger.warning("Leaving Validate Update Preferred Currency Validator: " + response)
        return {
            "result": response
        }, 400
    logger.info("Leaving Validate Update Preferred Currency Validator: ")
    return True

def validate2FA(request):
    logger.info("Entering Validate 2FA Validator: " + "(request: {})".format(str(request)))
    if 'email' not in request or request['email'] == '':
        response = "Email is a required field, Try Again"
        logger.warning("Leaving Validate 2FA Validator: " + response)
        return {
            "result": response
        }, 400
    if 'code' not in request or request['code'] == '':
        response = "2FA Code is a required field, Try Again"
        logger.warning("Leaving Validate 2FA Validator: " + response)
        return {
            "result": response
        }, 400
    logger.info("Leaving Validate 2FA Validator: ")
    return True