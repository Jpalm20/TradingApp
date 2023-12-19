import unittest
from models.journalentry import *
from models.utils import execute_db
from datetime import datetime, timedelta

class TestJournalEntry(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
        
    def test_get_journalentry(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getjournalentryunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("getjournalentryunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO Journalentry VALUES (null,%s,%s,%s)",(user_id,'getjournalentryunittestentry','2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Journalentry WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['entrytext'], "getjournalentryunittestentry")
        date = response[0][0]['date']
        journalentry_id = response[0][0]['journalentry_id']
        response = Journalentry.getEntry(user_id,date)
        self.assertEqual(response[0][0]['journalentry_id'], journalentry_id)
        response = execute_db("DELETE FROM Journalentry WHERE journalentry_id = %s", (journalentry_id,))
        response = execute_db("DELETE FROM User WHERE email = %s", ("getjournalentryunittest@gmail.com",))

        
    def test_create_journalentry(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","createjournalentryunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("createjournalentryunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        testJournalentry = Journalentry(None,user_id,'createjournalentryunittestentry','2023-01-01')
        response = Journalentry.createEntry(testJournalentry)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Journalentry WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['entrytext'], "createjournalentryunittestentry")
        journalentry_id = response[0][0]['journalentry_id']
        response = execute_db("DELETE FROM Journalentry WHERE journalentry_id = %s", (journalentry_id,))
        response = execute_db("DELETE FROM User WHERE email = %s", ("createjournalentryunittest@gmail.com",))

    
    def test_delete_journalentry(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deletejournalentryunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("deletejournalentryunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO Journalentry VALUES (null,%s,%s,%s)",(user_id,'deletejournalentryunittestentry','2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Journalentry WHERE user_id = %s and date = %s", (user_id,'2023-01-01',))
        self.assertEqual(response[0][0]['entrytext'], "deletejournalentryunittestentry")
        date = response[0][0]['date']
        journalentry_id = response[0][0]['journalentry_id']
        response = Journalentry.deleteEntry(user_id,date)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT journalentry_id FROM Journalentry WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0], [])
        response = execute_db("DELETE FROM User WHERE email = %s", ("deletejournalentryunittest@gmail.com",))


    def test_update_journalentry(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","updatejournalentryunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("updatejournalentryunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO Journalentry VALUES (null,%s,%s,%s)",(user_id,'updatejournalentryunittestentry','2023-01-01'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Journalentry WHERE user_id = %s and date = %s", (user_id,'2023-01-01',))
        self.assertEqual(response[0][0]['entrytext'], "updatejournalentryunittestentry")
        date = response[0][0]['date']
        journalentry_id = response[0][0]['journalentry_id']
        entry = "newupdatejournalentryunittestentry"
        response = Journalentry.updateEntry(user_id,date,entry)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Journalentry WHERE user_id = %s and date = %s", (user_id,'2023-01-01',))
        self.assertEqual(response[0][0]['entrytext'], "newupdatejournalentryunittestentry")
        response = execute_db("DELETE FROM Journalentry WHERE journalentry_id = %s", (journalentry_id,))
        response = execute_db("DELETE FROM User WHERE email = %s", ("updatejournalentryunittest@gmail.com",))


    def test_get_journalentries_for_month(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getjournalentriesformonthunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM User WHERE email = %s", ("getjournalentriesformonthunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO Journalentry VALUES (null,%s,%s,%s)",(user_id,'getjournalentriesformonthunittestentry','2023-01-01'))
        response = execute_db("INSERT INTO Journalentry VALUES (null,%s,%s,%s)",(user_id,'getjournalentriesformonthunittestentry','2023-01-05'))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM Journalentry WHERE user_id = %s", (user_id,))
        self.assertEqual(len(response[0]), 2)
        response = Journalentry.getEntriesForMonth(user_id,"2023-01-01","2023-01-31")
        self.assertEqual(len(response[0]), 2)
        response = execute_db("DELETE FROM Journalentry WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM User WHERE email = %s", ("getjournalentriesformonthunittest@gmail.com",))

    
    
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