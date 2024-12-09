import unittest
from unittest.mock import patch
from src.handlers.userHandler import *
from src.models.utils import execute_db
from datetime import datetime, date, timedelta


class TestUserHandler(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
    
    def test_register_user(self):
        # 1 good path
        requestBody = {
            "first_name": "RegisterUser",
            "last_name": "Test",
            "birthday": "2024-01-01",
            "email": "registeruseruserhandlerunittest@gmail.com",
            "password": "password",
            "street_address": "",
            "city": "",
            "state": "",
            "country": ""
        }
        
        response = registerUser(requestBody)
        self.assertEqual(response['result'], "User Created Successfully")
        user_id = response['user_id']
        
        # 2 bad path - fail on validateNewUser missing email
        requestBody = {
            "first_name": "RegisterUser",
            "last_name": "Test",
            "birthday": "2024-01-01",
            "email": "",
            "password": "password",
            "street_address": "",
            "city": "",
            "state": "",
            "country": ""
        }
        
        response = registerUser(requestBody)
        self.assertEqual(response[0]['result'], "Must Include a Valid Email Format, Please Try Again")
        
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    @patch('src.handlers.userHandler.create_access_token')
    def test_validate_user(self,mock_create_access_token):
        
        mock_create_access_token.return_value = 'mock_access_token'
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","validateuseruserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("validateuseruserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 good path full login
        requestBody = {
            "email": "validateuseruserhandlerunittest@gmail.com",
            "password": "password"
        }
        
        response = validateUser(requestBody)
        self.assertEqual(response['user_id'], user_id)
        
        # 2 bad path - fail on getUserbyEmail
        requestBody = {
            "email": "validateuseruserhandlerunittestt@gmail.com",
            "password": "password"
        }
        
        response = validateUser(requestBody)
        self.assertEqual(response[0]['result'], "No User Found with this Email, Please Use a Different Email or Create an Account")
        
        # 3 bad path - fail on password not being corroect
        requestBody = {
            "email": "validateuseruserhandlerunittest@gmail.com",
            "password": "passwordd"
        }
        
        response = validateUser(requestBody)
        self.assertEqual(response[0]['result'], "Incorrect Password, Please Try Again")
        
        # 4 good path - 2fa success response
        response = execute_db("UPDATE user SET `2fa_optin` = 1 WHERE user_id = %s", (user_id,))
        
        requestBody = {
            "email": "validateuseruserhandlerunittest@gmail.com",
            "password": "password"
        }
        
        response = validateUser(requestBody)
        self.assertEqual(response[0]['result'], "2FA Enabled, Verification Code Sent to Email")
        self.assertEqual(response[1], 202)
        
        response = execute_db("DELETE FROM session WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM verificationcode WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        
        
    def test_change_password(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","changepassworduserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("changepassworduserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 Good Path
        requestBody = {
            "curr_pass": "password",
            "new_pass_1": "password1",
            "new_pass_2": "password1"
        }
        
        response = changePassword(user_id,requestBody)
        self.assertEqual(response['result'], "Password Successfully Changed")
        response = execute_db("SELECT * FROM user WHERE email = %s", ("changepassworduserhandlerunittest@gmail.com",))
        password = response[0][0]['password']
        self.assertEqual(password, hashlib.sha256('password1'.encode()).hexdigest())
        
        # 2 Bad Path - Fail on validateChangePassword
        requestBody = {
            "curr_pass": "password",
            "new_pass_1": "password1",
            "new_pass_2": "password11"
        }
        
        response = changePassword(user_id,requestBody)
        self.assertEqual(response[0]['result'], "Both New Password Entries Must Match, Please Try Again")
        
        # 4 Bad Path - Fail on Incorrect Current Password
        requestBody = {
            "curr_pass": "passwordd",
            "new_pass_1": "password1",
            "new_pass_2": "password1"
        }
        
        response = changePassword(user_id,requestBody)
        self.assertEqual(response[0]['result'], "Incorrect Current Password, Please Try Again")
        
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 3 Bad Path - Fail on User Does Not Exist (getUserbyID)
        requestBody = {
            "curr_pass": "password",
            "new_pass_1": "password1",
            "new_pass_2": "password1"
        }
        
        response = changePassword(user_id,requestBody)
        self.assertEqual(response[0]['result'], "User Does Not Exist")
        
    
    def test_get_existing_user(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getexistinguseruserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getexistinguseruserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 Good Path
        response = getExistingUser(user_id)
        self.assertEqual(response['user_id'], user_id)
        
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 2 Bad Path - No User with this user_id
        response = getExistingUser(user_id)
        self.assertEqual(response[1], 400)
        
        
    def test_get_user_preferences(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getuserpreferencesuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getuserpreferencesuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 Good Path
        response = getUserPreferences(user_id)
        self.assertEqual(response['preferred_currency'], 'USD')
        self.assertEqual(response['2fa_optin'], False)
        self.assertEqual(response['public_profile_optin'], True)
        
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 2 Bad Path - No User with this user_id
        response = getUserPreferences(user_id)
        self.assertEqual(response[1], 400)
        
    
    def test_toggle_av_tracking(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","toggleavtrackinguserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("toggleavtrackinguserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 Good Path
        response = toggleAvTracking(user_id)
        self.assertEqual(response['account_value_optin'], True)
        
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 2 Bad Path - No User with this user_id
        response = toggleAvTracking(user_id)
        self.assertEqual(response[1], 400)
        
    
    def test_toggle_email_optin(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","toggleemailoptinuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("toggleemailoptinuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 Good Path
        response = toggleEmailOptInHandler(user_id)
        self.assertEqual(response['email_optin'], False)
        
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 2 Bad Path - No User with this user_id
        response = toggleEmailOptInHandler(user_id)
        self.assertEqual(response[1], 400)
        
        
    def test_toggle_feature_flags(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","togglefeatureflagsuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("togglefeatureflagsuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 Good Path Email Opt In
        requestBody = ['email_optin']
        response = toggleFeatureFlagsHandler(user_id,requestBody)
        self.assertEqual(response['email_optin'], False)
        
        # 2 Good Path AV Tracking
        requestBody = ['account_value_optin']
        response = toggleFeatureFlagsHandler(user_id,requestBody)
        self.assertEqual(response['account_value_optin'], True)
        
        # 3 Good Path 2FA Optin
        requestBody = ['2fa_optin']
        response = toggleFeatureFlagsHandler(user_id,requestBody)
        self.assertEqual(response['2fa_optin'], True)
        
        # 4 Good Path Public Profile Optin
        requestBody = ['public_profile_optin']
        response = toggleFeatureFlagsHandler(user_id,requestBody)
        self.assertEqual(response['public_profile_optin'], False)
        
        # 5 Bad Path - Fail validateToggleFeatureFlags
        requestBody = ['test_flag']
        response = toggleFeatureFlagsHandler(user_id,requestBody)
        self.assertEqual(response[0]['result'], "Please provide only valid feature flags in your request")
        
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 6 Bad Path - No User with this user_id
        requestBody = ['account_value_optin']
        response = toggleFeatureFlagsHandler(user_id,requestBody)
        self.assertEqual(response[1], 400)
        
        
    def test_update_preferred_currency(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","updatepreferredcurrencyuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("updatepreferredcurrencyuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 Good Path
        requestBody = {
            "preferred_currency": "JPY"
        }
        response = updatePreferredCurrencyHandler(user_id,requestBody)
        self.assertEqual(response['preferred_currency'], 'JPY')
        
        # 2 Bad Path - Fail on validateUpdatePreferredCurrency
        requestBody = {
            "preferred_currency": ""
        }
        response = updatePreferredCurrencyHandler(user_id,requestBody)
        self.assertEqual(response[0]['result'], "New Currency Code Missing")
        
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 3 Bad Path - No User with this user_id
        requestBody = {
            "preferred_currency": "USD"
        }
        response = toggleFeatureFlagsHandler(user_id,requestBody)
        self.assertEqual(response[1], 400)
        
    
    def test_get_user_from_session(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getuserfromsessionuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getuserfromsessionuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO session VALUES (null,%s,%s,%s)",(user_id,'getuserfromsessionuserhandlerunittesttoken',datetime.now()+timedelta(hours=24)))
        self.assertEqual(response[0], [])
        
        # 1 Good Path
        response = getUserFromSession('getuserfromsessionuserhandlerunittesttoken')
        self.assertEqual(response['user_id'], user_id)
        
        response = execute_db("DELETE FROM session WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 2 Bad Path - No User with this user_id
        response = getUserFromSession('getuserfromsessionuserhandlerunittesttoken')
        self.assertEqual(response[1], 400)
        
    
    def test_edit_existing_user(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","editexistinguseruserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("editexistinguseruserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 Good Path
        requestBody = {
            "first_name": "Jonathan",
        }
        response = editExistingUser(user_id,requestBody)
        self.assertEqual(response['first_name'], 'Jonathan')
        
        # 2 Bath Path - Fail on validateEditUser
        requestBody = {
            "password": "testpassword",
        }
        response = editExistingUser(user_id,requestBody)
        self.assertEqual(response[0]['result'], "You Can't Change Password This Way, Please Try Again")
        
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 3 Bath Path - No User with this user_id
        requestBody = {
            "first_name": "Jonathan",
        }
        response = editExistingUser(user_id,requestBody)
        self.assertEqual(response[1], 400)
        
        
    def test_delete_existing_user(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteexistinguseruserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteexistinguseruserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 Good Path
        response = deleteExistingUser(user_id)
        self.assertEqual(response['result'], "User Successfully Deleted")
        
        # 2 Bad Path - Fail due to worng data type for user_id
        #response = deleteExistingUser('user_id')
        #self.assertEqual(response[1], 400)
        
        
    def test_report_bug(self):
        
        email = "reportbuguserhandlerunittest@gmail.com"
        
        # 1 Good Path
        requestBody = {
            "summary": "Report Bug User Handler Unit Test",
            "page": "Other",
            "description": "reportbuguserhandlerunittest",
            "requestType": "Bug Report"
        }
        # response = reportBug(requestBody,email)
        # self.assertEqual(response['result'],"Feedback Submitted Successfully")
        
        # 2 Bath Path - Fail on validateReportBug
        requestBody = {
            "summary": "Report Bug User Handler Unit Test",
            "pagee": "Other",
            "description": "reportbuguserhandlerunittest",
            "requestType": "Bug Report"
        }
        # response = reportBug(requestBody,email)
        # self.assertEqual(response[0]['result'],"Please Include All Fields")
        # self.assertEqual(response[1],403)
        
        # 3 Bath Path - Error Calling JIRA API --TODO
        
    
    def test_get_user_trades(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getusertradesuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getusertradesuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesuserhandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","QQQ","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesuserhandlerunittest"))
        self.assertEqual(response[0], [])
        
        # 1 Good Path w/o Filters w/ Results
        response = getUserTrades(user_id)
        self.assertEqual(response['stats']['num_trades'], 2)
        
        # 2 Good Path w/ Filters w/ Results
        filters = {
            'ticker_name': 'SPY'
        }
        response = getUserTrades(user_id,filters)
        self.assertEqual(response['stats']['num_trades'], 1)
        
        # 3 Good Path w/o Results 
        filters = {
            'ticker_name': 'AMD'
        }
        response = getUserTrades(user_id,filters)
        self.assertEqual(response['stats']['num_trades'], 0)
        
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        
    def test_get_user_trades_stats(self):
    
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getusertradesstatsuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getusertradesstatsuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesstatsuserhandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","QQQ","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesstatsuserhandlerunittest"))
        self.assertEqual(response[0], [])
        
        # 1 Good Path w/o Filters w/ Results
        response = getUserTradesStats(user_id)
        self.assertEqual(response['stats']['num_trades'], 2)
        
        # 2 Good Path w/ Filters w/ Results
        filters = {
            'ticker_name': 'SPY'
        }
        response = getUserTradesStats(user_id,filters)
        self.assertEqual(response['stats']['num_trades'], 1)
        
        # 3 Good Path w/o Results 
        filters = {
            'ticker_name': 'AMD'
        }
        response = getUserTradesStats(user_id,filters)
        self.assertEqual(response['stats']['num_trades'], 0)
        
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    
    def test_get_user_trades_page(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getusertradespageuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getusertradespageuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradespageuserhandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","QQQ","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradespageuserhandlerunittest"))
        self.assertEqual(response[0], [])
        
        # 1 Bad Path - w/o Filters Error
        response = getUserTradesPage(user_id)
        self.assertEqual(response[0]['result'], "Please include Page Number and Rows per Page")
        
        # 2 Good Path w/ Results
        filters = {
            'page': 1,
            'numrows': 100
        }
        response = getUserTradesPage(user_id,filters)
        self.assertEqual(response['count'], 2)
        
        # 3 Good Path w/o Results 
        filters = {
            'page': 1,
            'numrows': 100,
            'ticker_name': 'AMD'
        }
        response = getUserTradesPage(user_id,filters)
        self.assertEqual(response['count'], 0)
        
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    
    def test_get_pnl_by_year(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getpnlbyyearuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getpnlbyyearuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getpnlbyyearuserhandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","QQQ","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getpnlbyyearuserhandlerunittest"))
        self.assertEqual(response[0], [])
        
        # 1 Good Path w/o Filters w/ Results
        response = getPnLbyYear(user_id,2023)
        self.assertEqual(response["months"][0]["0"][0]["count"], 2)
        self.assertEqual(response["months"][0]["0"][5]["count"], 0)
        
        # 2 Good Path w/ Filters w/ Results
        filters = {
            'ticker_name': 'SPY'
        }
        response = getPnLbyYear(user_id,2023,filters)
        self.assertEqual(response["months"][0]["0"][0]["count"], 1)
        self.assertEqual(response["months"][0]["0"][5]["count"], 0)
        
        # 3 Good Path w/o Results
        filters = {
            'ticker_name': 'AMD'
        }
        response = getPnLbyYear(user_id,2023,filters)
        self.assertEqual(response["months"][0]["0"][0]["count"], 0)
        self.assertEqual(response["months"][0]["0"][5]["count"], 0)
        
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    
    def test_generate_reset_code(self):
    
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","generateresetcodeuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("generateresetcodeuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 Good Path
        requestBody = {
            'email': 'generateresetcodeuserhandlerunittest@gmail.com'
        }
        #response = generateResetCode(requestBody)
        #self.assertEqual(response['result'],"Reset Code Generated Successfully")
        
        # 2 Bath Path - Fail for Invalid Email
        requestBody = {
            'email': 'ggenerateresetcodeuserhandlerunittest@gmail.com'
        }
        #response = generateResetCode(requestBody)
        #self.assertEqual(response[0]['result'],"No Account Found with this Email, Please Use a Valid Email or Create an Account")
        #self.assertEqual(response[1],403)
        
        
        response = execute_db("DELETE FROM resetcode WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    
    def test_validate_reset_code(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","validateresetcodeuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("validateresetcodeuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO resetcode VALUES (null,%s,%s,%s,%s)",(user_id,'validateresetcodeuserhandlerunittestcode',str(datetime.now().date() + timedelta(days=1)),0))
        self.assertEqual(response[0], [])
        
        # 1 Good Path
        requestBody = {
            "email": "validateresetcodeuserhandlerunittest@gmail.com",
            "code": "validateresetcodeuserhandlerunittestcode"
        }
        response = validateResetCode(requestBody)
        self.assertEqual(response['result'],"Reset Code Verified Successfully")
        response = execute_db("SELECT * FROM resetcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['validated'],1)
        
        # 2 Bad Path - Fail for Invalid Email
        requestBody = {
            "email": "vvalidateresetcodeuserhandlerunittest@gmail.com",
            "code": "validateresetcodeuserhandlerunittestcode"
        }
        response = validateResetCode(requestBody)
        self.assertEqual(response[0]['result'],"No Account Found with this Email, Please Use a Valid Email or Create an Account")
        self.assertEqual(response[1],403)
        
        # 3 Bad Path - Fail for Invalid Reset Code
        requestBody = {
            "email": "validateresetcodeuserhandlerunittest@gmail.com",
            "code": "vvalidateresetcodeuserhandlerunittestcode"
        }
        response = validateResetCode(requestBody)
        self.assertEqual(response[0]['result'],"Reset Code Doesn't Exist")
        self.assertEqual(response[1],401)
        
        # 4 Bad Path - Fail for Expired Reset Code
        response = execute_db("UPDATE resetcode SET expiration = %s WHERE user_id = %s", (str(datetime.now().date() - timedelta(days=1)),user_id,))
        requestBody = {
            "email": "validateresetcodeuserhandlerunittest@gmail.com",
            "code": "validateresetcodeuserhandlerunittestcode"
        }
        response = validateResetCode(requestBody)
        self.assertEqual(response[0]['result'],"Reset Code Has Expired")
        self.assertEqual(response[1],401)
        
        response = execute_db("DELETE FROM resetcode WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        
    def test_reset_password(self):
        
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","resetcodeuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("resetcodeuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO resetcode VALUES (null,%s,%s,%s,%s)",(user_id,'resetcodeuserhandlerunittestcode',str(datetime.now().date() + timedelta(days=1)),1))
        self.assertEqual(response[0], [])
        
        # 1 Good Path
        requestBody = {
            "email": "resetcodeuserhandlerunittest@gmail.com",
            "code": "resetcodeuserhandlerunittestcode",
            "new_pass_1": "password1",
            "new_pass_2": "password1"
        }
        response = resetPassword(requestBody)
        self.assertEqual(response['result'],"Password Reset Successfully")
        response = execute_db("SELECT * FROM user WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['password'],hashlib.sha256('password1'.encode()).hexdigest())
        
        # 2 Bad Path - Fail on validateResetPassword
        requestBody = {
            "email": "resetcodeuserhandlerunittest@gmail.com",
            "code": "resetcodeuserhandlerunittestcode",
            "new_pass_1": "password1",
            "new_pass_2": "password11"
        }
        response = resetPassword(requestBody)
        self.assertEqual(response[0]['result'],"Both New Password Entries Must Match, Please Try Again")
        self.assertEqual(response[1],403)
        
        # 3 Bad Path - Fail for Invalid Email
        requestBody = {
            "email": "rresetcodeuserhandlerunittest@gmail.com",
            "code": "resetcodeuserhandlerunittestcode",
            "new_pass_1": "password1",
            "new_pass_2": "password1"
        }
        response = resetPassword(requestBody)
        self.assertEqual(response[0]['result'],"No Account Found with this Email, Please Use a Valid Email or Create an Account")
        self.assertEqual(response[1],403)
        
        # 4 Bad Path - Fail for Invalid Reset Code
        requestBody = {
            "email": "resetcodeuserhandlerunittest@gmail.com",
            "code": "rresetcodeuserhandlerunittestcode",
            "new_pass_1": "password1",
            "new_pass_2": "password1"
        }
        response = resetPassword(requestBody)
        self.assertEqual(response[0]['result'],"Reset Code Doesn't Exist")
        self.assertEqual(response[1],401)
        
        # 5 Bad Path - Fail for Expired Reset Code
        response = execute_db("INSERT INTO resetcode VALUES (null,%s,%s,%s,%s)",(user_id,'resetcodeuserhandlerunittestcode',str(datetime.now().date() + timedelta(days=1)),1))
        self.assertEqual(response[0], [])
        response = execute_db("UPDATE resetcode SET expiration = %s WHERE user_id = %s", (str(datetime.now().date() - timedelta(days=1)),user_id,))
        requestBody = {
            "email": "resetcodeuserhandlerunittest@gmail.com",
            "code": "resetcodeuserhandlerunittestcode",
            "new_pass_1": "password1",
            "new_pass_2": "password1"
        }
        response = resetPassword(requestBody)
        self.assertEqual(response[0]['result'],"Reset Code Has Expired")
        self.assertEqual(response[1],401)
        
        # 6 Bad Path - Fail on Reset Code not Validated yet
        response = execute_db("UPDATE resetcode SET expiration = %s, validated = %s WHERE user_id = %s", (str(datetime.now().date() + timedelta(days=1)),0,user_id,))
        requestBody = {
            "email": "resetcodeuserhandlerunittest@gmail.com",
            "code": "resetcodeuserhandlerunittestcode",
            "new_pass_1": "password1",
            "new_pass_2": "password1"
        }
        response = resetPassword(requestBody)
        self.assertEqual(response[0]['result'],"Reset Code has not been validated yet")
        self.assertEqual(response[1],401)
        
        response = execute_db("DELETE FROM resetcode WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    @patch('src.handlers.userHandler.create_access_token')
    def test_verify_2fa(self,mock_create_access_token):
        #verify2FA
        
        mock_create_access_token.return_value = 'mock_access_token'
        
        # setup queries
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","verify2fauserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("verify2fauserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("UPDATE user SET `2fa_optin` = 1 WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0], [])
        response = execute_db("INSERT INTO verificationcode VALUES (null,%s,%s,%s,%s)",(user_id,'verify2fauserhandlerunittestcode',str(datetime.now().date() + timedelta(days=1)),1))
        self.assertEqual(response[0], [])
        
        # 1 - Bad Path - Fail on validate2FA
        requestBody = {
            'code': "verify2fauserhandlerunittestcode"
        }
        response = verify2FA(requestBody)
        self.assertEqual(response[0]['result'],"Email is a required field, Try Again")
        self.assertEqual(response[1],400)
        
        # 2 - Bad Path - Fail on getUserbyEmail
        requestBody = {
            'email': "erify2fauserhandlerunittest@gmail.com",
            'code': "verify2fauserhandlerunittestcode"
        }
        response = verify2FA(requestBody)
        self.assertEqual(response[0]['result'],"No Account Found with this Email, Please Use a Valid Email or Create an Account")
        self.assertEqual(response[1],403)
        
        # 3 - Bad Path - Fail on getVerificationCode
        requestBody = {
            'email': "verify2fauserhandlerunittest@gmail.com",
            'code': "erify2fauserhandlerunittestcode"
        }
        response = verify2FA(requestBody)
        self.assertEqual(response[0]['result'],"2FA Code Doesn't Exist")
        self.assertEqual(response[1],401)
        
        # 4 - Bad Path - Fail on 2FA Code already used
        requestBody = {
            'email': "verify2fauserhandlerunittest@gmail.com",
            'code': "verify2fauserhandlerunittestcode"
        }
        response = verify2FA(requestBody)
        self.assertEqual(response[0]['result'],"2FA Code Has Already Been Used")
        self.assertEqual(response[1],401)
        
        
        # 5 - Bad Path - Fail on 2FA Code Expired
        # Update code to expired in DB
        response = execute_db("UPDATE verificationcode SET expiration = %s, validated = %s WHERE user_id = %s", (str(datetime.now().date() - timedelta(days=1)),False,user_id,))
        requestBody = {
            'email': "verify2fauserhandlerunittest@gmail.com",
            'code': "verify2fauserhandlerunittestcode"
        }
        response = verify2FA(requestBody)
        self.assertEqual(response[0]['result'],"2FA Code Has Expired")
        self.assertEqual(response[1],401)
        
        
        # 6 - Good Path
        # Update code to not expired in DB
        response = execute_db("UPDATE verificationcode SET expiration = %s, validated = %s WHERE user_id = %s", (str(datetime.now().date() + timedelta(days=1)),0,user_id,))
        requestBody = {
            'email': "verify2fauserhandlerunittest@gmail.com",
            'code': "verify2fauserhandlerunittestcode"
        }
        response = verify2FA(requestBody)
        self.assertEqual(response['user_id'],user_id)
        
        
        # teardown queries
        response = execute_db("DELETE FROM verificationcode WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM session WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    
    def test_set_account_value(self):
    
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","setaccountvalueuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("setaccountvalueuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
    
        # 1 Good Path - addAccountValue & accountValueFeatureOptin
        requestBody = {
            "accountvalue": 600,
            "date": "2023-10-11"
        }
        response = setAccountValue(user_id,requestBody)
        self.assertEqual(response['result'],"Account Value Set Successfully")
        
        # 2 Good Path - updateAccountValue
        requestBody = {
            "accountvalue": 700,
            "date": "2023-10-11"
        }
        response = setAccountValue(user_id,requestBody)
        self.assertEqual(response['result'],"Account Value Set Successfully")
        self.assertEqual(response['accountvalue'],700)
                
        # 3 Bad Path - Fail on validateSetAccountValue
        requestBody = {
            "accountvaluee": 600,
            "date": "2023-10-11"
        }
        response = setAccountValue(user_id,requestBody)
        self.assertEqual(response[0]['result'],"Must Include an Account Value")
        self.assertEqual(response[1],400)
        
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 4 Bad Path - Fail on now user_id
        requestBody = {
            "accountvalue": 600,
            "date": "2023-10-11"
        }
        response = setAccountValue(user_id,requestBody)
        self.assertEqual(response[1],400)
        
    
    def test_get_account_value(self):
    
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getaccountvalueuserhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getaccountvalueuserhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
    
        # 1 Good Path not opted into feature
        filters = {
            'date': '2023-10-11'
        }
        response = getAccountValue(user_id,filters)
        self.assertEqual(len(response['accountvalues']),7)
        self.assertEqual(response['accountvalues'][0]['date'],'2023-10-05')
        self.assertEqual(response['accountvalues'][0]['accountvalue'],0)
    
        # 2 Good Path w/ TF Filter
        response = execute_db("UPDATE user SET account_value_optin = 1 WHERE user_id = %s", (user_id,))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)", (user_id,200,'2023-10-11')) 
        filters = {
            'date': '2023-10-11',
            'time_frame': 'Week'
        }
        response = getAccountValue(user_id,filters)
        self.assertEqual(len(response['accountvalues']),7)
        self.assertEqual(response['accountvalues'][5]['date'],'2023-10-09')
        self.assertEqual(response['accountvalues'][5]['accountvalue'],0)
        
        # 3 Good Path w/o TF Filter     
        filters = {
            'date': '2023-10-11'
        }
        response = getAccountValue(user_id,filters)
        self.assertEqual(len(response['accountvalues']),7)
        self.assertEqual(response['accountvalues'][6]['date'],'2023-10-11')
        self.assertEqual(response['accountvalues'][6]['accountvalue'],200)
        
        # 4 Good Path insertFutureDay
        filters = {
            'date': '2023-10-12'
        }
        response = getAccountValue(user_id,filters)
        self.assertEqual(len(response['accountvalues']),7)
        self.assertEqual(response['accountvalues'][6]['date'],'2023-10-12')
        self.assertEqual(response['accountvalues'][6]['accountvalue'],200)
        
        # 5 Bad Path - Fail on validateGetAccountValue
        filters = {
            'datee': '2023-10-12'
        }
        response = getAccountValue(user_id,filters)
        self.assertEqual(response[0]['result'],"Missing or invalid 'date' key, Please provide the Date where you wish to start from in YYYY-MM-DD format")
        self.assertEqual(response[1],400)
        
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        # 6 Bad Path - Fail on now user_id
        filters = {
            'date': '2023-10-11'
        }
        response = getAccountValue(user_id,filters)
        self.assertEqual(response[1],400)
        
    
    def test_get_user_leaderboard(self):
        
        #setup
        hashPass = hashlib.sha256('password'.encode()).hexdigest()
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getuserleaderboardhandlerunittest@gmail.com",hashPass,"11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getuserleaderboardhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getuserleaderboardhandlerunittest"))
        self.assertEqual(response[0], [])
        
        #1 Good Path w/Results
        filters = {
            'time_filter': 'All%20Time',
            'value_filter': 'Total%20PNL'
        }
        response = getUserLeaderboard(user_id,filters)
        self.assertEqual(len(response['leaderboard']),2)
        self.assertEqual(response['leaderboard'][1]['leaderboard_value'],100)
        
        #2 Good Path w/o Results
        filters = {
            'time_filter': 'YTD',
            'value_filter': 'Total%20PNL'
        }
        response = getUserLeaderboard(user_id,filters)
        self.assertEqual(len(response['leaderboard']),0)
        self.assertEqual(response['leaderboard'],[])
        
        #3 Bad Path - Fail Validation
        filters = {
            'time_filterr': 'YTD',
            'value_filter': 'Total%20PNL'
        }
        response = getUserLeaderboard(user_id,filters)
        self.assertEqual(response[0]['result'],"Please provide both a time and value filter")
        self.assertEqual(response[1],400)
        
        #delete
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS