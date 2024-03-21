import unittest
from models.user import *
from models.utils import execute_db

class TestUser(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT

    def test_add_user(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        testUser = User(None,"Jon","Palmieri","08-30-2020","adduserunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA",None,None)
        response = User.addUser(testUser)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("adduserunittest@gmail.com",))
        self.assertEqual(response[0][0]['email'], "adduserunittest@gmail.com")
        response = execute_db("DELETE FROM user WHERE email = %s", ("adduserunittest@gmail.com",))
        
    
    def test_update_user(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","updateuserunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        changes = {
            "first_name": "James"
        }
        response = execute_db("SELECT * FROM user WHERE email = %s", ("updateuserunittest@gmail.com",))
        response = User.updateUser(response[0][0]['user_id'],changes)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("updateuserunittest@gmail.com",))
        self.assertEqual(response[0][0]['first_name'], "James")
        response = execute_db("DELETE FROM user WHERE email = %s", ("updateuserunittest@gmail.com",))
    
    
    def test_delete_user(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteuserunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteuserunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = User.deleteUser(user_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteuserunittest@gmail.com",))
        self.assertEqual(response[0], [])
        
    
    def test_update_pass(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","updatepassunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("updatepassunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = User.updatePass(user_id,'newpassword')
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("updatepassunittest@gmail.com",))
        self.assertEqual(response[0][0]['password'], 'newpassword')
        response = execute_db("DELETE FROM user WHERE email = %s", ("updatepassunittest@gmail.com",))
        self.assertEqual(response[0], [])
        
    
    def test_account_value_feature_optin(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","accountvaluefeatureoptinunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("accountvaluefeatureoptinunittest@gmail.com",))
        self.assertEqual(response[0][0]['account_value_optin'], 0)
        user_id = response[0][0]['user_id']
        response = User.accountValueFeatureOptin(user_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("accountvaluefeatureoptinunittest@gmail.com",))
        self.assertEqual(response[0][0]['account_value_optin'], 1)
        response = execute_db("DELETE FROM user WHERE email = %s", ("accountvaluefeatureoptinunittest@gmail.com",))
        self.assertEqual(response[0], [])
        
        
    def test_toggle_account_value_feature_optin(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","toggleaccountvaluefeatureoptinunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("toggleaccountvaluefeatureoptinunittest@gmail.com",))
        self.assertEqual(response[0][0]['account_value_optin'], 0)
        user_id = response[0][0]['user_id']
        response = User.toggleAccountValueFeatureOptin(user_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("toggleaccountvaluefeatureoptinunittest@gmail.com",))
        self.assertEqual(response[0][0]['account_value_optin'], 1)
        response = User.toggleAccountValueFeatureOptin(user_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("toggleaccountvaluefeatureoptinunittest@gmail.com",))
        self.assertEqual(response[0][0]['account_value_optin'], 0)
        response = execute_db("DELETE FROM user WHERE email = %s", ("toggleaccountvaluefeatureoptinunittest@gmail.com",))
        self.assertEqual(response[0], [])
        
        
    def test_toggle_email_optin(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","toggleemailoptinunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("toggleemailoptinunittest@gmail.com",))
        self.assertEqual(response[0][0]['email_optin'], 1)
        user_id = response[0][0]['user_id']
        response = User.toggleEmailOptIn(user_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("toggleemailoptinunittest@gmail.com",))
        self.assertEqual(response[0][0]['email_optin'], 0)
        response = User.toggleEmailOptIn(user_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("toggleemailoptinunittest@gmail.com",))
        self.assertEqual(response[0][0]['email_optin'], 1)
        response = execute_db("DELETE FROM user WHERE email = %s", ("toggleemailoptinunittest@gmail.com",))
        self.assertEqual(response[0], [])

    
    def test_get_user_by_email(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getuserbyemailunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = User.getUserbyEmail("getuserbyemailunittest@gmail.com")
        self.assertEqual(response[0][0]['email'], "getuserbyemailunittest@gmail.com")
        response = execute_db("DELETE FROM user WHERE email = %s", ("getuserbyemailunittest@gmail.com",))
        response = User.getUserbyEmail("getuserbyemailunittest@gmail.com")
        self.assertEqual(response[0], [])
        
        
    def test_get_user_by_id(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getuserbyidunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getuserbyidunittest@gmail.com",))
        response = User.getUserbyID(response[0][0]['user_id'])
        self.assertEqual(response[0][0]['email'], "getuserbyidunittest@gmail.com")
        response = execute_db("DELETE FROM user WHERE email = %s", ("getuserbyidunittest@gmail.com",))
        response = User.getUserbyID("getuserbyidunittest@gmail.com")
        self.assertEqual(response[0], [])
        
    
    def test_get_preferences(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getpreferencesunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getpreferencesunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = User.getPreferences(user_id)
        self.assertEqual(response[0][0]['account_value_optin'], 0)
        self.assertEqual(response[0][0]['email_optin'], 1)
        response = execute_db("DELETE FROM user WHERE email = %s", ("getpreferencesunittest@gmail.com",))
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getpreferencesunittest@gmail.com",))
        response = User.getPreferences(user_id)
        self.assertEqual(response[0], [])
    
    
    def test_get_total_trades(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","gettotaltradesunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("gettotaltradesunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        #ADD TRADE(S)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"gettotaltradesunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Swing Trade","Shares","QQQ","2022-01-01","2023-01-01",410,400,1,"1:3",100,25,"gettotaltradesunittest"))        
        #CHECK FOR ALL TRADES WITHOUT FILTER
        response = User.getTotalTrades(user_id)
        self.assertEqual(response[0][0]['COUNT(*)'], 2)
        self.assertNotEqual(response[0][0]['COUNT(*)'], 1)
        #CHECK FOR TRADES WITH A VALID FILTER
        filters = {
            'ticker_name': 'SPY'
        }
        response = User.getTotalTrades(user_id,filters)
        self.assertNotEqual(response[0][0]['COUNT(*)'], 2)
        self.assertEqual(response[0][0]['COUNT(*)'], 1)
        #CHECK FOR TRADES WITH FILTER THAT RETURNS NO RESULTS (TICKER THAT USER DOESNT HAVE)
        filters = {
            'ticker_name': 'AMD'
        }
        response = User.getTotalTrades(user_id,filters)
        self.assertEqual(response[0][0]['COUNT(*)'], 0)
        filters = {
            'date_range': 'trade_date >= DATE_ADD(NOW(), INTERVAL -1 DAY)'
        }
        response = User.getTotalTrades(user_id,filters)
        self.assertEqual(response[0][0]['COUNT(*)'], 0)
        #DELETE TRADES UNDER USER ID
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("gettotaltradesunittest@gmail.com",))
        #CHECK FOR TRADES AFTER EVERYTHINGS BEEN DELETED
        response = User.getTotalTrades(user_id)
        self.assertEqual(response[0][0]['COUNT(*)'], 0)
    
    
    def test_get_user_by_session_token(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getuserbysessiontokenunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getuserbysessiontokenunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO session VALUES (null,%s,%s,%s)",(user_id,'getuserbysessiontokenunittesttoken','2023-01-01 00:00:01'))
        self.assertEqual(response[0], [])
        response = User.getUserBySessionToken('getuserbysessiontokenunittesttoken')
        self.assertEqual(response[0][0]['email'], "getuserbysessiontokenunittest@gmail.com")
        response = execute_db("DELETE FROM session WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getuserbysessiontokenunittest@gmail.com",))
        response = User.getUserBySessionToken("getuserbysessiontokenunittesttoken")
        self.assertEqual(response[0], [])
        
        
    def test_get_user_trades(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getusertradesunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getusertradesunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        #ADD TRADE(S)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Swing Trade","Shares","QQQ","2022-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesunittest"))        
        #CHECK FOR ALL TRADES WITHOUT FILTER
        response = User.getUserTrades(user_id)
        self.assertEqual(len(response[0]), 2)
        #DELETE TRADES UNDER USER ID
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getusertradesunittest@gmail.com",))
        #CHECK FOR TRADES AFTER EVERYTHINGS BEEN DELETED
        response = User.getUserTrades(user_id)
        self.assertEqual(response[0], [])
        
    
    def test_get_user_trades_filter(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getusertradesfilterunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getusertradesfilterunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        #ADD TRADE(S)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesfilterunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Swing Trade","Shares","QQQ","2022-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesfilterunittest"))        
        #CHECK FOR ALL TRADES WITHOUT FILTER
        filters = {}
        response = User.getUserTradesFilter(user_id,filters)
        self.assertEqual(len(response[0]), 2)
        #CHECK FOR TRADES WITH A VALID FILTER
        filters = {
            'ticker_name': 'SPY'
        }
        response = User.getUserTradesFilter(user_id,filters)
        self.assertEqual(len(response[0]), 1)
        #CHECK FOR TRADES WITH FILTER THAT RETURNS NO RESULTS (TICKER THAT USER DOESNT HAVE)
        filters = {
            'ticker_name': 'AMD'
        }
        response = User.getUserTradesFilter(user_id,filters)
        self.assertEqual(len(response[0]), 0)
        filters = {
            'date_range': 'trade_date >= DATE_ADD(NOW(), INTERVAL -1 DAY)'
        }
        response = User.getUserTradesFilter(user_id,filters)
        self.assertEqual(len(response[0]), 0)
        #DELETE TRADES UNDER USER ID
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getusertradesfilterunittest@gmail.com",))
        #CHECK FOR TRADES AFTER EVERYTHINGS BEEN DELETED
        filters = {}
        response = User.getUserTradesFilter(user_id,filters)
        self.assertEqual(response[0], [])
        
        
    def test_get_user_trades_status(self): 
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getusertradesstatsunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getusertradesstatsunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        #ADD TRADE(S)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesstatsunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Swing Trade","Shares","QQQ","2022-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesstatsunittest"))        
        #CHECK FOR ALL TRADES WITHOUT FILTER
        response = User.getUserTradesStats(user_id)
        self.assertEqual(response[0][0]['numTrades'], 2)
        #DELETE TRADES UNDER USER ID
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getusertradesstatsunittest@gmail.com",))
        #CHECK FOR TRADES AFTER EVERYTHINGS BEEN DELETED
        response = User.getUserTradesStats(user_id)
        self.assertEqual(response[0][0]['numTrades'], 0)
        
    
    def test_get_user_trades_stats_filter(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getusertradesstatsfilterunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getusertradesstatsfilterunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        #ADD TRADE(S)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesstatsfilterunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Swing Trade","Shares","QQQ","2022-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradesstatsfilterunittest"))        
        #CHECK FOR ALL TRADES WITHOUT FILTER
        filters = {}
        response = User.getUserTradesStatsFilter(user_id,filters)
        self.assertEqual(response[0][0]['numTrades'], 2)
        #CHECK FOR TRADES WITH A VALID FILTER
        filters = {
            'ticker_name': 'SPY'
        }
        response = User.getUserTradesStatsFilter(user_id,filters)
        self.assertEqual(response[0][0]['numTrades'], 1)
        #CHECK FOR TRADES WITH FILTER THAT RETURNS NO RESULTS (TICKER THAT USER DOESNT HAVE)
        filters = {
            'ticker_name': 'AMD'
        }
        response = User.getUserTradesStatsFilter(user_id,filters)
        self.assertEqual(response[0][0]['numTrades'], 0)
        filters = {
            'date_range': 'trade_date >= DATE_ADD(NOW(), INTERVAL -1 DAY)'
        }
        response = User.getUserTradesStatsFilter(user_id,filters)
        self.assertEqual(response[0][0]['numTrades'], 0)
        #DELETE TRADES UNDER USER ID
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getusertradesstatsfilterunittest@gmail.com",))
        #CHECK FOR TRADES AFTER EVERYTHINGS BEEN DELETED
        filters = {}
        response = User.getUserTradesStatsFilter(user_id,filters)
        self.assertEqual(response[0][0]['numTrades'], 0)
    
    
    def test_get_user_trades_page(self):
        
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getusertradespageunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getusertradespageunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        #ADD TRADE(S)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradespageunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Swing Trade","Shares","QQQ","2022-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertradespageunittest"))        
        #CHECK FOR ALL TRADES WITHOUT FILTER
        filters = {}
        response = User.getUserTradesPage(user_id,100,0,filters)
        self.assertEqual(len(response[0]), 2)
        #CHECK FOR TRADES WITH A VALID FILTER
        filters = {
            'ticker_name': 'SPY'
        }
        response = User.getUserTradesPage(user_id,100,0,filters)
        self.assertEqual(len(response[0]), 1)
        #CHECK FOR TRADES WITH FILTER THAT RETURNS NO RESULTS (TICKER THAT USER DOESNT HAVE)
        filters = {
            'ticker_name': 'AMD'
        }
        response = User.getUserTradesPage(user_id,100,0,filters)
        self.assertEqual(len(response[0]), 0)
        filters = {
            'date_range': 'trade_date >= DATE_ADD(NOW(), INTERVAL -1 DAY)'
        }
        response = User.getUserTradesPage(user_id,100,0,filters)
        self.assertEqual(len(response[0]), 0)
        #DELETE TRADES UNDER USER ID
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getusertradespageunittest@gmail.com",))
        #CHECK FOR TRADES AFTER EVERYTHINGS BEEN DELETED
        filters = {}
        response = User.getUserTradesPage(user_id,100,0,filters)
        self.assertEqual(response[0], [])
    
    
    def test_get_user_pnl_by_year(self):
            
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getuserpnlbyyearunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getuserpnlbyyearunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        #ADD TRADE(S)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getuserpnlbyyearunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Swing Trade","Shares","QQQ","2022-01-01","2023-01-01",410,400,1,"1:3",100,25,"getuserpnlbyyearunittest"))       
        #CHECK FOR TRADES WITH A VALID FILTER
        response = User.getUserPnLbyYear(user_id,2023)
        self.assertEqual(len(response[0]), 1)
        #CHECK FOR TRADES WITH FILTER THAT RETURNS NO RESULTS (TICKER THAT USER DOESNT HAVE)
        response = User.getUserPnLbyYear(user_id,2022)
        self.assertEqual(len(response[0]), 1)
        response = User.getUserPnLbyYear(user_id,2021)
        self.assertEqual(len(response[0]), 0)
        #DELETE TRADES UNDER USER ID
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getuserpnlbyyearunittest@gmail.com",))
        #CHECK FOR TRADES AFTER EVERYTHINGS BEEN DELETED
        response = User.getUserPnLbyYear(user_id,2023)
        self.assertEqual(response[0], [])
        
    
    def test_get_user_pnl_by_year_filter(self):
            
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getuserpnlbyyearfilterunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getuserpnlbyyearfilterunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        #ADD TRADE(S)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getuserpnlbyyearfilterunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Swing Trade","Shares","QQQ","2022-01-01","2023-01-01",410,400,1,"1:3",100,25,"getuserpnlbyyearfilterunittest"))       
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Swing Trade","Shares","SPY","2022-01-01","2023-01-01",410,400,1,"1:3",100,25,"getuserpnlbyyearfilterunittest"))       
        #CHECK FOR TRADES WITHOUT A FILTER
        filters = {}
        response = User.getUserPnLbyYearFilter(user_id,2023,filters)
        self.assertEqual(len(response[0]), 1)
        #CHECK FOR TRADES WITH A VALID FILTER
        filters = {
            'ticker_name': 'SPY'
        }
        response = User.getUserPnLbyYearFilter(user_id,2023,filters)
        self.assertEqual(len(response[0]), 1)
        #CHECK FOR TRADES WITH FILTER THAT RETURNS NO RESULTS (TICKER THAT USER DOESNT HAVE)
        filters = {
            'ticker_name': 'SPY'
        }
        response = User.getUserPnLbyYearFilter(user_id,2022,filters)
        self.assertEqual(len(response[0]), 1)
        filters = {
            'ticker_name': 'SPY'
        }
        response = User.getUserPnLbyYearFilter(user_id,2021,filters)
        self.assertEqual(len(response[0]), 0)
        #DELETE TRADES UNDER USER ID
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getuserpnlbyyearfilterunittest@gmail.com",))
        #CHECK FOR TRADES AFTER EVERYTHINGS BEEN DELETED
        filters = {}
        response = User.getUserPnLbyYearFilter(user_id,2023,filters)
        self.assertEqual(response[0], [])
    
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS
        
        
#--------Tests--------# 

#Testing addUser       
#testUser = User(None,"Jon","Palmiery","08-30-2020","palmierijon@gmail.com","password","11 Danand Lane","Patterson","NY","USA",None)
#response = User.addUser(testUser)

#Testing updateUser
#testUserID = 4;
#testUpdateUserInfo = {
#    "last_name": "Palmieri",
#    "password": "testestest20"
#}
#response = User.updateUser(testUserID,testUpdateUserInfo)

#Testing deleteUser
#testUserID = 4
#response = User.deleteUser(testUserID)

#Testing getUserbyID
#testUserID = 2
#response = User.getUser(testUserID)

#Test getUserbyEmail
#testUserEmail = "testemail@gmail.com"   
#response = User.getUserbyEmail(testUserEmail)

#Testing getUserTrades
#testUserID = 77
#response = User.getUserTrades(testUserID)

#Testing getUserTradesFilter
#testUserID = 71
#testFilters = {
#   "ticker_name": "SPY",
#   "trade_type": "Swing Trade",
#   "security_type": "Options"
#}
#response = User.getUserTradesFilter(testUserID,testFilters)

#Testing getUserTradesbyYear
#testUserID = 77
#testYear = 2022
#response = User.getUserTrades(testUserID,testYear)

#print(response)