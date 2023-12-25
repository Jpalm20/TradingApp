import unittest
from models.session import *
from models.utils import execute_db
from datetime import datetime, timedelta

class TestSession(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
        
    def test_get_session(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getsessionunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("getsessionunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO Session VALUES (null,%s,%s,%s)",(user_id,'getsessionunittesttoken','2023-01-01 00:00:01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Session WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['token'], "getsessionunittesttoken")
        token = response[0][0]['token']
        session_id = response[0][0]['session_id']
        response = Session.getSession(token)
        self.assertEqual(response[0][0]['session_id'], session_id)
        response = execute_db("DELETE FROM Session WHERE token = %s", (token,))
        response = execute_db("DELETE FROM User WHERE email = %s", ("getsessionunittest@gmail.com",))

        
    def test_add_session(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","addsessionunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("addsessionunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        testSession = Session(None,user_id,'addsessionunittesttoken','2023-01-01 00:00:01')
        response = Session.addSession(testSession)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Session WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['token'], "addsessionunittesttoken")
        session_id = response[0][0]['session_id']
        response = execute_db("DELETE FROM Session WHERE session_id = %s", (session_id,))
        response = execute_db("DELETE FROM User WHERE email = %s", ("addsessionunittest@gmail.com",))

    
    def test_refresh_expiration(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","refreshexpirationunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("refreshexpirationunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO Session VALUES (null,%s,%s,%s)",(user_id,'refreshexpirationunittesttoken','2023-01-01 00:00:01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Session WHERE user_id = %s", (user_id,))
        self.assertEqual(str(response[0][0]['expiration']), "2023-01-01 00:00:01")
        session_id = response[0][0]['session_id']
        response = Session.refreshExpiration(session_id)
        response = execute_db("SELECT * FROM Session WHERE user_id = %s", (user_id,))
        self.assertTrue(response[0][0]['expiration'] > datetime.now())
        response = execute_db("DELETE FROM Session WHERE session_id = %s", (session_id,))
        response = execute_db("DELETE FROM User WHERE email = %s", ("refreshexpirationunittest@gmail.com",))

    
    def test_delete_user_sessions(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteusersessionsunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("deleteusersessionsunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO Session VALUES (null,%s,%s,%s)",(user_id,'deleteusersessionsunittesttoken','2023-01-01 00:00:01'))
        response = execute_db("INSERT INTO Session VALUES (null,%s,%s,%s)",(user_id,'deleteusersessionsunittesttoken','2023-01-01 00:00:02'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT session_id FROM Session WHERE user_id = %s", (user_id,))
        self.assertEqual(len(response[0]), 2)
        response = Session.deleteUserSessions(user_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT session_id FROM Session WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0], [])
        response = execute_db("DELETE FROM User WHERE email = %s", ("deleteusersessionsunittest@gmail.com",))
    
    
    def test_expire_session(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","expiresessionunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("expiresessionunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO Session VALUES (null,%s,%s,%s)",(user_id,'expiresessionunittesttoken',datetime.now()+timedelta(hours=24)))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Session WHERE user_id = %s", (user_id,))
        self.assertTrue(response[0][0]['expiration'] > datetime.now())
        token = response[0][0]['token']
        session_id = response[0][0]['session_id']
        response = Session.expireSession(token)
        response = execute_db("SELECT * FROM Session WHERE user_id = %s", (user_id,))
        self.assertTrue(response[0][0]['expiration'] < datetime.now())
        response = execute_db("DELETE FROM Session WHERE session_id = %s", (session_id,))
        response = execute_db("DELETE FROM User WHERE email = %s", ("expiresessionunittest@gmail.com",))


    def test_get_user_from_session(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getuserfromsessionunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("getuserfromsessionunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO Session VALUES (null,%s,%s,%s)",(user_id,'getuserfromsessionunittesttoken','2023-01-01 00:00:01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Session WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['token'], "getuserfromsessionunittesttoken")
        token = response[0][0]['token']
        session_id = response[0][0]['session_id']
        response = Session.getUserFromSession(token)
        self.assertEqual(response[0][0]['user_id'], user_id)
        response = execute_db("DELETE FROM Session WHERE token = %s", (session_id,))
        response = execute_db("DELETE FROM User WHERE email = %s", ("getuserfromsessionunittest@gmail.com",))


    def test_get_email_from_session(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getemailfromsessionunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("getemailfromsessionunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        email = response[0][0]['email']
        response = execute_db("INSERT INTO Session VALUES (null,%s,%s,%s)",(user_id,'getemailfromsessionunittesttoken','2023-01-01 00:00:01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Session WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['token'], "getemailfromsessionunittesttoken")
        token = response[0][0]['token']
        session_id = response[0][0]['session_id']
        response = Session.getEmailFromSession(token)
        self.assertEqual(response[0][0]['email'], email)
        response = execute_db("DELETE FROM Session WHERE token = %s", (session_id,))
        response = execute_db("DELETE FROM User WHERE email = %s", ("getemailfromsessionunittest@gmail.com",))

    
    
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