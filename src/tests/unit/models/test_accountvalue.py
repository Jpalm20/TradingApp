import unittest
from src.models.accountvalue import *
from src.models.utils import execute_db
from datetime import datetime, timedelta

class TestAccountValue(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
        
    def test_get_accountvalue(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getaccountvalueunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getaccountvalueunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        date = response[0][0]['date']
        accountvalue_id = response[0][0]['accountvalue_id']
        response = Accountvalue.getAccountValue(date,user_id)
        self.assertEqual(response[0][0]['accountvalue_id'], accountvalue_id)
        response = execute_db("DELETE FROM accountvalue WHERE accountvalue_id = %s", (accountvalue_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getaccountvalueunittest@gmail.com",))


    def test_get_accountvalues(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getaccountvaluesunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getaccountvaluesunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,300,'2023-01-02'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,400,'2023-01-03'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,500,'2023-01-04'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(len(response[0]), 4)
        response = Accountvalue.getAccountValues(user_id,datetime.strptime('2023-01-04', '%Y-%m-%d').date())
        self.assertEqual(len(response[0]), 4)
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getaccountvaluesunittest@gmail.com",))


    def test_get_accountvalues_timeframe(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getaccountvaluestfunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getaccountvaluestfunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,300,'2023-01-02'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,400,'2023-01-03'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,500,'2023-01-04'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,500,'2023-01-05'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,500,'2023-01-06'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,500,'2023-01-07'))
        dates = [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3), datetime(2023, 1, 4), datetime(2023, 1, 5), datetime(2023, 1, 6), datetime(2023, 1, 7)]
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(len(response[0]), 7)
        response = Accountvalue.getAccountValuesTF(user_id,dates)
        self.assertEqual(len(response[0]), 7)
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getaccountvaluestfunittest@gmail.com",))

        
    def test_add_accountvalue(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","addaccountvalueunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("addaccountvalueunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        testAccountvalue = Accountvalue(None,user_id,200,'2023-01-01')
        response = Accountvalue.addAccountValue(testAccountvalue)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("addaccountvalueunittest@gmail.com",))

    
    def test_delete_accountvalue(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteaccountvalueunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteaccountvalueunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        accountvalue_id = response[0][0]['accountvalue_id']
        response = Accountvalue.deleteAccountValue(accountvalue_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT accountvalue_id FROM accountvalue WHERE accountvalue_id = %s", (accountvalue_id,))
        self.assertEqual(response[0], [])
        response = execute_db("DELETE FROM user WHERE email = %s", ("deleteaccountvalueunittest@gmail.com",))
        
    
    def test_delete_user_account_values(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteuseraccountvaluesunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteuseraccountvaluesunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        accountvalue_id = response[0][0]['accountvalue_id']
        response = Accountvalue.deleteUserAccountValues(user_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT accountvalue_id FROM accountvalue WHERE accountvalue_id = %s", (accountvalue_id,))
        self.assertEqual(response[0], [])
        response = execute_db("DELETE FROM user WHERE email = %s", ("deleteuseraccountvaluesunittest@gmail.com",))


    def test_update_accountvalue(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","updateaccountvalueunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("updateaccountvalueunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        accountvalue_id = response[0][0]['accountvalue_id']
        date = response[0][0]['date']
        accountvalue = 300
        response = Accountvalue.updateAccountValue(user_id,date,accountvalue)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE accountvalue_id = %s", (accountvalue_id,))
        self.assertEqual(response[0][0]['accountvalue'], 300)
        response = execute_db("DELETE FROM accountvalue WHERE accountvalue_id = %s", (accountvalue_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("updateaccountvalueunittest@gmail.com",))
    
    
    def test_insert_future_day(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","insertfuturedayunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("insertfuturedayunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        date = response[0][0]['date']
        response = Accountvalue.insertFutureDay(user_id,date+timedelta(days=1))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE date = %s and user_id = %s", (date+timedelta(days=1),user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        self.assertEqual(response[0][0]['date'], date+timedelta(days=1))
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("insertfuturedayunittest@gmail.com",))


    def test_handle_add_trade(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","handleaddtradeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("handleaddtradeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"handleaddtradeunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("handleaddtradeunittest",))
        self.assertEqual(response[0][0]['comments'], "handleaddtradeunittest")
        trade_id = response[0][0]['trade_id']
        response = Accountvalue.handleAddTrade(trade_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 300)
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("handleaddtradeunittest@gmail.com",))


    def test_handle_delete_trade(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","handledeletetradeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("handledeletetradeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"handledeletetradeunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("handledeletetradeunittest",))
        self.assertEqual(response[0][0]['comments'], "handledeletetradeunittest")
        trade_id = response[0][0]['trade_id']
        response = Accountvalue.handleDeleteTrade(trade_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 100)
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("handledeletetradeunittest@gmail.com",))

    
    def test_handle_pnl_update(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","handlepnlupdateunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("handlepnlupdateunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"handlepnlupdateunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("handlepnlupdateunittest",))
        self.assertEqual(response[0][0]['comments'], "handlepnlupdateunittest")
        trade_id = response[0][0]['trade_id']
        response = Accountvalue.handlePnlUpdate(200,trade_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['accountvalue'], 400)
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("handlepnlupdateunittest@gmail.com",))


    def test_handle_date_update_add(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","handledateupdateaddunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("handledateupdateaddunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,300,'2023-01-02'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(len(response[0]), 2)
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s and date = %s", (user_id,'2023-01-01',))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-02",410,400,1,"1:3",100,25,"handledateupdateaddunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("handledateupdateaddunittest",))
        self.assertEqual(response[0][0]['comments'], "handledateupdateaddunittest")
        trade_id = response[0][0]['trade_id']
        response = Accountvalue.handleDateUpdateAdd('2023-01-01','2023-01-02',trade_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(len(response[0]), 2)
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s and date = %s", (user_id,'2023-01-01',))
        self.assertEqual(response[0][0]['accountvalue'], 300)
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("handledateupdateaddunittest@gmail.com",))


    def test_handle_date_update_sub(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","handledateupdatesubunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("handledateupdatesubunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,200,'2023-01-01'))
        response = execute_db("INSERT INTO accountvalue VALUES (null,%s,%s,%s)",(user_id,300,'2023-01-02'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(len(response[0]), 2)
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s and date = %s", (user_id,'2023-01-01',))
        self.assertEqual(response[0][0]['accountvalue'], 200)
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-02",410,400,1,"1:3",100,25,"handledateupdatesubunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("handledateupdatesubunittest",))
        self.assertEqual(response[0][0]['comments'], "handledateupdatesubunittest")
        trade_id = response[0][0]['trade_id']
        response = Accountvalue.handleDateUpdateSub('2023-01-01','2023-01-02',trade_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s", (user_id,))
        self.assertEqual(len(response[0]), 2)
        response = execute_db("SELECT * FROM accountvalue WHERE user_id = %s and date = %s", (user_id,'2023-01-01',))
        self.assertEqual(response[0][0]['accountvalue'], 100)
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("handledateupdatesubunittest@gmail.com",))

    
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS
        
