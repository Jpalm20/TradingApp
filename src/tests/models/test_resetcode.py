import unittest
from models.resetcode import *
from models.utils import execute_db
from datetime import datetime, timedelta

class TestResetCode(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
        
    def test_get_resetcode(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getresetcodeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getresetcodeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO resetcode VALUES (null,%s,%s,%s)",(user_id,'getresetcodeunittestcode','2023-01-01 00:00:01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM resetcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['code'], "getresetcodeunittestcode")
        code = response[0][0]['code']
        resetcode_id = response[0][0]['resetcode_id']
        response = Resetcode.getResetCode(code,user_id)
        self.assertEqual(response[0][0]['resetcode_id'], resetcode_id)
        response = execute_db("DELETE FROM resetcode WHERE resetcode_id = %s", (resetcode_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getresetcodeunittest@gmail.com",))

        
    def test_add_resetcode(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","addresetcodeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("addresetcodeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        testResetcode = Resetcode(None,user_id,'addresetcodeunittestcode','2023-01-01 00:00:01')
        response = Resetcode.addResetCode(testResetcode)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM resetcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['code'], "addresetcodeunittestcode")
        resetcode_id = response[0][0]['resetcode_id']
        response = execute_db("DELETE FROM resetcode WHERE resetcode_id = %s", (resetcode_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("addresetcodeunittest@gmail.com",))

    
    def test_delete_resetcode(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteresetcodeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteresetcodeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO resetcode VALUES (null,%s,%s,%s)",(user_id,'deleteresetcodeunittestcode','2023-01-01 00:00:01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM resetcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['code'], "deleteresetcodeunittestcode")
        resetcode_id = response[0][0]['resetcode_id']
        response = Resetcode.deleteResetCode(resetcode_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT resetcode_id FROM resetcode WHERE user_id = %s", (resetcode_id,))
        self.assertEqual(response[0], [])
        response = execute_db("DELETE FROM user WHERE email = %s", ("deleteresetcodeunittest@gmail.com",))

    
    
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS
        
        
#--------Tests--------# 

#Testing addTrade       
#testTrade = Trade(None,1,"Swing Trade","Options","TSLA","12-12-2022","9-21-2023",1000,500,5,"3:1",2532.52,254.3,"Test for Sunny :)")
#response = Trade.addTrade(testTrade)

#Testing updateTrade
#testTradeID = 3;
#testUpdateTradeInfo = {
#    "ticker_name": "QQQ",
#    "pnl": 250
#}
#response = Trade.updateTrade(testTradeID,testUpdateTradeInfo)

#Testing deleteTrade
#testTradeID = 7
#response = Trade.deleteTrade(testTradeID)

#Testing getTrade
#testTradeID = 3
#response = Trade.getTrade(testTradeID)

#print(response)