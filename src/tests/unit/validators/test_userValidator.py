import unittest
from src.validators.userValidator import *
from src.models.utils import execute_db
from datetime import datetime, date, timedelta


class TestUserValidator(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT


    def test_validate_new_user(self):
        # 1 good path
        request = {
            "first_name": "Test",
            "last_name": "Test",
            "birthday": "2023-01-01",
            "email": "transformnewuserunittest@gmail.com",
            "password": "password",
            "street_address": "10 Brewster Lane",
            "city": "New Jersey",
            "state": "NJ",
            "country": "US"
        }
        response = validateNewUser(request)
        self.assertEqual(response, True)
        # 2 fail on password check
        request = {
            "first_name": "Test",
            "last_name": "Test",
            "birthday": "2023-01-01",
            "email": "transformnewuserunittest@gmail.com",
            "password": "pass",
            "street_address": "10 Brewster Lane",
            "city": "New Jersey",
            "state": "NJ",
            "country": "US"
        }
        response = validateNewUser(request)
        self.assertEqual(response[0]['result'], "Must Include a Password of at Least 8 Characters, Please Try Again")
        # 3 fail on email format check
        request = {
            "first_name": "Test",
            "last_name": "Test",
            "birthday": "2023-01-01",
            "email": "transformnewuserunittestgmail.com",
            "password": "password",
            "street_address": "10 Brewster Lane",
            "city": "New Jersey",
            "state": "NJ",
            "country": "US"
        }
        response = validateNewUser(request)
        self.assertEqual(response[0]['result'], "Must Include a Valid Email Format, Please Try Again")
        # 4 fail on email existing check
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","validatenewuseruservalidatorunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        request = {
            "first_name": "Test",
            "last_name": "Test",
            "birthday": "2023-01-01",
            "email": "validatenewuseruservalidatorunittest@gmail.com",
            "password": "password",
            "street_address": "10 Brewster Lane",
            "city": "New Jersey",
            "state": "NJ",
            "country": "US"
        }
        response = validateNewUser(request)
        self.assertEqual(response[0]['result'], "A User with this Email Already Exist, Sign Up with a Different Email")
        response = execute_db("DELETE FROM user WHERE email = %s", ("validatenewuseruservalidatorunittest@gmail.com",))

        
    def test_validate_edit_user(self):
        # 1 good path
        request = {
            "first_name": "",
            "last_name": "",
            "birthday": "2023-01-01",
            "email": "",
            "street_address": "10 Brewster Lane",
            "city": "",
            "state": "",
            "country": ""
        }
        response = validateEditUser(request)
        self.assertEqual(response, True)
        # 2 fail password
        request = {
            "first_name": "",
            "last_name": "",
            "birthday": "2023-01-01",
            "email": "",
            "password": "",
            "street_address": "10 Brewster Lane",
            "city": "",
            "state": "",
            "country": ""
        }
        response = validateEditUser(request)
        self.assertEqual(response[0]['result'], "You Can't Change Password This Way, Please Try Again")
        # 3 fail email format
        request = {
            "first_name": "",
            "last_name": "",
            "birthday": "2023-01-01",
            "email": "testemailgmail.com",
            "street_address": "10 Brewster Lane",
            "city": "",
            "state": "",
            "country": ""
        }
        response = validateEditUser(request)
        self.assertEqual(response[0]['result'], "Invalid Email Format, Try Upating Again")
        # 4 fail email existing
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","validateedituseruservalidatorunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        request = {
            "first_name": "",
            "last_name": "",
            "birthday": "2023-01-01",
            "email": "validateedituseruservalidatorunittest@gmail.com",
            "street_address": "10 Brewster Lane",
            "city": "",
            "state": "",
            "country": ""
        }
        response = validateEditUser(request)
        self.assertEqual(response[0]['result'], "A User with this Email Already Exist, Try Updating with a Different Email")
        response = execute_db("DELETE FROM user WHERE email = %s", ("validateedituseruservalidatorunittest@gmail.com",))


    def test_validate_change_password(self):
        # 1 good path
        request = {
            "curr_pass": "password1",
            "new_pass_1": "password",
            "new_pass_2": "password"
        }
        response = validateChangePassword(request)
        self.assertEqual(response, True)
        # 2 fail password format
        request = {
            "curr_pass": "password1",
            "new_pass_1": "password",
            "new_pass_2": "passwor"
        }
        response = validateChangePassword(request)
        self.assertEqual(response[0]['result'], "All Passwords Must be at Least 8 Characters, Please Try Again")
        # 3 fail password match
        request = {
            "curr_pass": "password1",
            "new_pass_1": "password",
            "new_pass_2": "password2"
        }
        response = validateChangePassword(request)
        self.assertEqual(response[0]['result'], "Both New Password Entries Must Match, Please Try Again")


    def test_validate_report_bug(self):
        # 1 good path
        request = {
            "requestType": "Feature Request",
            "page": "Test Page",
            "summary": "Test Transform Report Bug",
            "description": "validatereportbugunittest",
        }
        response = validateReportBug(request)
        self.assertEqual(response, True)
        # 2 fail missing fields
        request = {
            "requestType": "Feature Request",
            "page": "",
            "summary": "Test Transform Report Bug",
            "description": "validatereportbugunittest",
        }
        response = validateReportBug(request)
        self.assertEqual(response[0]['result'], "Please Include All Fields")
        # 3 fail request type check
        request = {
            "requestType": "Feature",
            "page": "Test Page",
            "summary": "Test Transform Report Bug",
            "description": "validatereportbugunittest",
        }
        response = validateReportBug(request)
        self.assertEqual(response[0]['result'], "Please Select a Valid Request Type")

    
    # validate reset password
    def test_validate_reset_password(self):
        # 1 good path
        request = {
            "new_pass_1": "password",
            "new_pass_2": "password"
        }
        response = validateResetPassword(request)
        self.assertEqual(response, True)
        # 2 fail password length
        request = {
            "new_pass_1": "passwor",
            "new_pass_2": "passwor"
        }
        response = validateResetPassword(request)
        self.assertEqual(response[0]['result'], "Password Must be at Least 8 Characters, Please Try Again")
        
        # 3 fail password match
        request = {
            "new_pass_1": "password",
            "new_pass_2": "password1"
        }
        response = validateResetPassword(request)
        self.assertEqual(response[0]['result'], "Both New Password Entries Must Match, Please Try Again")
    
    
    # validate set account value
    def test_validate_set_account_value(self):
        # 1 good path
        request = {
            "accountvalue": 600,
            "date": "2023-10-11"
        }
        response = validateSetAccountValue(request)
        self.assertEqual(response, True)
        # 2 fail no account value
        request = {
            "date": "2023-10-11"
        }
        response = validateSetAccountValue(request)
        self.assertEqual(response[0]['result'], "Must Include an Account Value")
        # 3 fail no date
        request = {
            "accountvalue": 600,
        }
        response = validateSetAccountValue(request)
        self.assertEqual(response[0]['result'], "Missing or invalid 'date' key, Please provide the Date where you wish to update your Account Value in YYYY-MM-DD format")
        # 4 fail invalid format date
        request = {
            "accountvalue": 600,
            "date": "10-11-2023"
        }
        response = validateSetAccountValue(request)
        self.assertEqual(response[0]['result'], "Missing or invalid 'date' key, Please provide the Date where you wish to update your Account Value in YYYY-MM-DD format")
        # 5 fail future date
        date = (datetime.now()+timedelta(days=2)).strftime('%Y-%m-%d')
        request = {
            "accountvalue": 600,
            "date": date
        }
        response = validateSetAccountValue(request)
        self.assertEqual(response[0]['result'], "Invalid date. The 'date' provided is more than one day into the future of the current UTC date.")
        
    
    # validate get account value
    def test_validate_get_account_value(self):
        # 1 good path
        request = {
            "time_frame": "Day",
            "date": "2023-10-11"
        }
        response = validateGetAccountValue(request)
        self.assertEqual(response, True)
        # 2 fail invalid time frame
        request = {
            "time_frame": "Days",
            "date": "2023-10-11"
        }
        response = validateGetAccountValue(request)
        self.assertEqual(response[0]['result'], "Invalid Time Frame. The 'time frame' provided is not a valid option (Day, Week, Month, Year)")
        # 3 fail no date
        request = {
            "time_frame": "Day",
        }
        response = validateGetAccountValue(request)
        self.assertEqual(response[0]['result'], "Missing or invalid 'date' key, Please provide the Date where you wish to start from in YYYY-MM-DD format")
        # 4 fail invalid format date
        request = {
            "time_frame": "Day",
            "date": "10-11-2023"
        }
        response = validateGetAccountValue(request)
        self.assertEqual(response[0]['result'], "Missing or invalid 'date' key, Please provide the Date where you wish to start from in YYYY-MM-DD format")
        # 5 fail future date
        date = (datetime.now()+timedelta(days=2)).strftime('%Y-%m-%d')
        request = {
            "accountvalue": 600,
            "date": date
        }
        response = validateSetAccountValue(request)
        self.assertEqual(response[0]['result'], "Invalid date. The 'date' provided is more than one day into the future of the current UTC date.")
        
    
    def test_validate_toggle_feature_flags(self):
        # 1 good path
        request = ['email_optin','account_value_optin','2fa_optin','public_profile_optin']
        response = validateToggleFeatureFlags(request)
        self.assertEqual(response, True)
        # 2 fail invalid flag name
        request = ['email_optin','account_value_optins']
        response = validateToggleFeatureFlags(request)
        self.assertEqual(response[0]['result'], "Please provide only valid feature flags in your request")
        
    
    def test_validate_update_preferred_currency(self):
        # 1 good path
        request = {
            'preferred_currency': "JPY"
        }
        response = validateUpdatePreferredCurrency(request)
        self.assertEqual(response, True)
        # 2 fail invalid currency code
        request = {
            'preferred_currency': "JPYY"
        }
        response = validateUpdatePreferredCurrency(request)
        self.assertEqual(response[0]['result'], "New Currency Code is Invalid")
        # 3 fail bad request body
        request = {
            'preferred_currencyy': "JPY"
        }
        response = validateUpdatePreferredCurrency(request)
        self.assertEqual(response[0]['result'], "New Currency Code Missing")
        
        
    def test_validate_2fa(self):
        # 1 good path
        request = {
            'email': "validate2favalidatorunittest@gmail.com",
            'code': "123456"
        }
        response = validate2FA(request)
        self.assertEqual(response, True)
        # 2 fail missing email
        request = {
            'emaill': "validate2favalidatorunittest@gmail.com",
            'code': "123456"
        }
        response = validate2FA(request)
        self.assertEqual(response[0]['result'], "Email is a required field, Try Again")
        # 3 fail missing code
        request = {
            'email': "validate2favalidatorunittest@gmail.com",
        }
        response = validate2FA(request)
        self.assertEqual(response[0]['result'], "2FA Code is a required field, Try Again")
        
    
    def test_validate_leaderboard_filters(self):
        #1 Good Path
        filters = {
            'time_filter': 'All%20Time',
            'value_filter': 'Total%20PNL'
        }
        response = validateUserLeaderboardFilters(filters)
        self.assertEqual(response, True)
        
        #2 Fail on Empty Filters
        filters = {}
        response = validateUserLeaderboardFilters(filters)
        self.assertEqual(response[0]['result'], "Please include Necessary Time and Value Filters")
        
        #3 Fail on time_filter or value_filter not in Filters
        filters = {
            'time_filterr': 'All%20Time',
            'value_filter': 'Total%20PNL'
        }
        response = validateUserLeaderboardFilters(filters)
        self.assertEqual(response[0]['result'], "Please provide both a time and value filter")
        
        #4 Fail on not valid time_filter
        filters = {
            'time_filter': 'All%20Timee',
            'value_filter': 'Total%20PNL'
        }
        response = validateUserLeaderboardFilters(filters)
        self.assertEqual(response[0]['result'], "Please provide only valid time filter options")
        
        #5 Fail on not valid value_filter
        filters = {
            'time_filter': 'All%20Time',
            'value_filter': 'Total%20PNLL'
        }
        response = validateUserLeaderboardFilters(filters)
        self.assertEqual(response[0]['result'], "Please provide only valid value filter options")
    
        
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS