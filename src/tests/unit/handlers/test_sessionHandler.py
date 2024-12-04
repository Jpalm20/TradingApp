import unittest
from src.handlers.sessionHandler import *
from src.models.utils import execute_db
from datetime import datetime, date, timedelta


class TestSessionHandler(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
    
    def test_validate_token(self):
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","validatetokensessionhandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("validatetokensessionhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO session VALUES (null,%s,%s,%s)",(user_id,'validatetokensessionhandlerunittesttoken',datetime.now()+timedelta(hours=24)))
        self.assertEqual(response[0], [])
        
        # 1 good path refresh expiration
        token = "validatetokensessionhandlerunittesttoken"
        response = validateToken(token)
        self.assertEqual(response[0], True)
        self.assertEqual(response[1], "Token Validated")
        # 2 fail token doesnt exist
        token = "token"
        response = validateToken(token)
        self.assertEqual(response[0], False)
        self.assertEqual(response[1], "Auth Token Doesn't Exist")
        # 3 fail token expired
        response = execute_db("UPDATE session SET expiration = %s WHERE token = %s", (datetime.now()-timedelta(hours=24),"validatetokensessionhandlerunittesttoken",))
        token = "validatetokensessionhandlerunittesttoken"
        response = validateToken(token)
        self.assertEqual(response[0], False)
        self.assertEqual(response[1], "Auth Token Has Expired")
        
        response = execute_db("DELETE FROM session WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))


    def test_logout_session(self):
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","logoutsessionsessionhandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("logoutsessionsessionhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO session VALUES (null,%s,%s,%s)",(user_id,'logoutsessionsessionhandlerunittesttoken',datetime.now()+timedelta(hours=24)))
        self.assertEqual(response[0], [])
        
        # 1 good path session expired and logged out
        token = "logoutsessionsessionhandlerunittesttoken"
        response = logoutSession(token)
        self.assertEqual(response['result'], "User Logged Out")
        # 2 fail token doesnt exist or other issue
        token = "token"
        response = logoutSession(token)
        self.assertEqual(response[0]['result'], "There was an issue expiring this Session, User not Logged Out")

        response = execute_db("DELETE FROM session WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))


    def test_get_user_from_token(self):
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getuserfromtokensessionhandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getuserfromtokensessionhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO session VALUES (null,%s,%s,%s)",(user_id,'getuserfromtokensessionhandlerunittesttoken',datetime.now()+timedelta(hours=24)))
        self.assertEqual(response[0], [])
        
        # 1 good path found user with token
        token = "getuserfromtokensessionhandlerunittesttoken"
        response = getUserFromToken(token)
        self.assertEqual(response[0], True)
        self.assertEqual(response[1], user_id)
        # 2 fail no user found with token
        token = "token"
        response = getUserFromToken(token)
        self.assertEqual(response[0], False)
        self.assertEqual(response[1], "No User Associated with this Session")

        response = execute_db("DELETE FROM session WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))


    def test_get_email_from_token(self):
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getemailfromtokensessionhandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getemailfromtokensessionhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        email = response[0][0]['email']
        response = execute_db("INSERT INTO session VALUES (null,%s,%s,%s)",(user_id,'getemailfromtokensessionhandlerunittesttoken',datetime.now()+timedelta(hours=24)))
        self.assertEqual(response[0], [])
        
        # 1 good path found user with token
        token = "getemailfromtokensessionhandlerunittesttoken"
        response = getEmailFromToken(token)
        self.assertEqual(response[0], True)
        self.assertEqual(response[1], email)
        # 2 fail no user found with token
        token = "token"
        response = getEmailFromToken(token)
        self.assertEqual(response[0], False)
        self.assertEqual(response[1], "No Email Associated with this Session")

        response = execute_db("DELETE FROM session WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))

        
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS