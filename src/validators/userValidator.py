import os
import sys
import re
from datetime import date, datetime, timedelta


script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user


def validateNewUser(request):
    if 'password' not in request or request['password'] == '' or len(request['password']) < 8:
        return {
            "result": "Must Include a Password of at Least 8 Characters, Please Try Again"
        }, 403
    if 'email' not in request or request['email'] == '' or '@' not in request['email'] or '.' not in request['email']:
        return {
            "result": "Must Include a Valid Email Format, Please Try Again"
        }, 403
    response = user.User.getUserbyEmail(request['email'])
    if response[0] and 'email' in response[0][0]:
        return {
            "result": "A User with this Email Already Exist, Sign Up with a Different Email"
        }, 403
        
    #need to validate blanks as well, might be easier to set required fields on FE if possible
    
    return True

def validateEditUser(request):
    if 'password' in request:
        return {
            "result": "You Can't Change Password This Way, Please Try Again"
        }, 403
    if 'email' in request and request['email'] != '' and ('@' not in request['email'] or '.' not in request['email']):
        return {
            "result": "Invalid Email Format, Try Upating Again"
        }, 403
    response = user.User.getUserbyEmail(request['email'])
    if response[0] and 'email' in response[0][0]:
        return {
            "result": "A User with this Email Already Exist, Try Updating with a Different Email"
        }, 403
    return True

def validateChangePassword(request):
    if ('curr_pass' not in request or request['curr_pass'] == '' or len(request['curr_pass']) < 8) or ('new_pass_1' not in request or request['new_pass_1'] == '' or len(request['new_pass_1']) < 8) or ('new_pass_2' not in request or request['new_pass_2'] == '' or len(request['new_pass_2']) < 8):
        return {
            "result": "All Passwords Must be at Least 8 Characters, Please Try Again"
        }, 403 
    if ('new_pass_1' == 'new_pass_2'):
        return {
            "result": "Both New Password Entries Must Match, Please Try Again"
        }, 403 
    return True

def validateReportBug(request):
    if ('summary' not in request or request['summary'] == '') or ('page' not in request or request['page'] == '') or ('description' not in request or request['description'] == '') or ('requestType' not in request or request['requestType'] == ''):
        return {
            "result": "Please Include All Fields"
        }, 403 
    if (request['requestType'] != 'Bug Report' and request['requestType'] != 'Feature Request'):
        return {
            "result": "Please Select a Valid Request Type"
        }, 403 
    return True

def validateResetPassword(request):
    if ('new_pass_1' not in request or request['new_pass_1'] == '' or len(request['new_pass_1']) < 8) or ('new_pass_2' not in request or request['new_pass_2'] == '' or len(request['new_pass_2']) < 8):
        return {
            "result": "Password Must be at Least 8 Characters, Please Try Again"
        }, 403 
    if ('new_pass_1' == 'new_pass_2'):
        return {
            "result": "Both New Password Entries Must Match, Please Try Again"
        }, 403 
    return True

def validateSetAccountValue(request):
    if('accountvalue' not in request):
        return {
            "result": "Must Include an Account Value"
        }, 400
    if('date' not in request or re.match(r'^\d{4}-\d{2}-\d{2}$', request['date']) is None):
        return {
            "result": "Missing or invalid 'date' key, Please provide the Date where you wish to update your Account Value in YYYY-MM-DD format"
        }, 400
    if('date' in request and datetime.strptime(request['date'], '%Y-%m-%d').date() > datetime.now().date() + timedelta(days=1)):
        return {
            "result": "Invalid date. The 'date' provided is more than one day into the future of the current UTC date."
        }, 400
    return True

def validateGetAccountValue(request):
    if('date' not in request or re.match(r'^\d{4}-\d{2}-\d{2}$', request['date']) is None):
        return {
            "result": "Missing or invalid 'date' key, Please provide the Date where you wish to start from in YYYY-MM-DD format"
        }, 400
    if('date' in request and datetime.strptime(request['date'], '%Y-%m-%d').date() > datetime.now().date() + timedelta(days=1)):
        return {
            "result": "Invalid date. The 'date' provided is more than one day into the future of the current UTC date."
        }, 400
    if('time_frame' in request and request['time_frame'] not in ['Day', 'Week', 'Month', 'Year']):
        return {
            "result": "Invalid Time Frame. The 'time frame' provided is not a valid option (Day, Week, Month, Year)"
        }, 400
    return True