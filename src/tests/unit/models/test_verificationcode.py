import unittest
from src.models.verificationcode import *
from src.models.utils import execute_db
from datetime import datetime, timedelta

class TestVerificationCode(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
        
    def test_get_verificationcode(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getverificationcodeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getverificationcodeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO verificationcode VALUES (null,%s,%s,%s,%s)",(user_id,'getverificationcodeunittestcode','2023-01-01 00:00:01',0))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM verificationcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['code'], "getverificationcodeunittestcode")
        code = response[0][0]['code']
        verificationcode_id = response[0][0]['verificationcode_id']
        validated = response[0][0]['validated']
        expiration = response[0][0]['expiration']
        response = Verificationcode.getVerificationCode(code,user_id)
        self.assertEqual(response[0][0]['verificationcode_id'], verificationcode_id)
        self.assertEqual(response[0][0]['validated'], validated)
        self.assertEqual(response[0][0]['expiration'], expiration)
        response = execute_db("DELETE FROM verificationcode WHERE verificationcode_id = %s", (verificationcode_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getverificationcodeunittest@gmail.com",))

        
    def test_add_verificationcode(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","addverificationcodeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("addverificationcodeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        testVerificationcode = Verificationcode(None,user_id,'addverificationcodeunittestcode','2023-01-01 00:00:01',None)
        response = Verificationcode.addVerificationCode(testVerificationcode)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM verificationcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['code'], "addverificationcodeunittestcode")
        self.assertEqual(response[0][0]['validated'], 0)
        verificationcode_id = response[0][0]['verificationcode_id']
        response = execute_db("DELETE FROM verificationcode WHERE verificationcode_id = %s", (verificationcode_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("addverificationcodeunittest@gmail.com",))

    
    def test_delete_verificationcode(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteverificationcodeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteverificationcodeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO verificationcode VALUES (null,%s,%s,%s,%s)",(user_id,'deleteverificationcodeunittestcode','2023-01-01 00:00:01',0))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM verificationcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['code'], "deleteverificationcodeunittestcode")
        verificationcode_id = response[0][0]['verificationcode_id']
        response = Verificationcode.deleteVerificationCode(verificationcode_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT verificationcode_id FROM verificationcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0], [])
        response = execute_db("DELETE FROM user WHERE email = %s", ("deleteverificationcodeunittest@gmail.com",))
        
    
    def test_delete_user_verification_codes(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteuserverificationcodesunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteuserverificationcodesunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO verificationcode VALUES (null,%s,%s,%s,%s)",(user_id,'deleteuserverificationcodesunittestcode','2023-01-01 00:00:01',0))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM verificationcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['code'], "deleteuserverificationcodesunittestcode")
        verificationcode_id = response[0][0]['verificationcode_id']
        response = Verificationcode.deleteUserVerificationCodes(user_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT verificationcode_id FROM verificationcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0], [])
        response = execute_db("DELETE FROM user WHERE email = %s", ("deleteuserverificationcodesunittest@gmail.com",))
        
    
    def test_expire_codes(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","expirecodesunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("expirecodesunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO verificationcode VALUES (null,%s,%s,%s,%s)",(user_id,'expirecodesunittestcode','2023-01-01 00:00:01',0))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM verificationcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['code'], "expirecodesunittestcode")
        verificationcode_id = response[0][0]['verificationcode_id']
        time = datetime.now()
        response = Verificationcode.expireVerificationCodes(user_id,time)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM verificationcode WHERE verificationcode_id = %s", (verificationcode_id,))
        self.assertNotEqual(response[0][0]['expiration'], '2023-01-01 00:00:01')
        self.assertAlmostEqual(response[0][0]['expiration'].replace(microsecond=0),time.replace(microsecond=0),delta=timedelta(seconds=1))
        response = execute_db("DELETE FROM verificationcode WHERE verificationcode_id = %s", (verificationcode_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        
    def test_validate_verification_code(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","validateverificationcodeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("validateverificationcodeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO verificationcode VALUES (null,%s,%s,%s,%s)",(user_id,'validateverificationcodeunittestcode','2023-01-01 00:00:01',0))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM verificationcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['code'], "validateverificationcodeunittestcode")
        verificationcode_id = response[0][0]['verificationcode_id']
        response = Verificationcode.validateVerificationCode(verificationcode_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM verificationcode WHERE verificationcode_id = %s", (verificationcode_id,))
        self.assertEqual(response[0][0]['validated'], 1)
        response = execute_db("DELETE FROM verificationcode WHERE verificationcode_id = %s", (verificationcode_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))

    
    
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS
        
