import unittest
from handlers.journalentryHandler import *
from models.utils import execute_db
from datetime import datetime, date, timedelta


class TestJournalEntryHandler(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
    
    def test_get_journal_entries(self):
        # 1 good path with entries
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getjournalentrieshandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getjournalentrieshandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO journalentry VALUES (null,%s,%s,%s)",(user_id,'getjournalentrieshandlerunittestentry','2023-12-10'))
        self.assertEqual(response[0], [])
        
        date = "2023-12-10"
        response = getJournalEntries(user_id,date)
        self.assertEqual(len(response['entries']), 1)
        self.assertEqual(response['entries'][0]['date'], date)
        # 2 good path without entries
        date = "2023-10-05"
        response = getJournalEntries(user_id,date)
        self.assertEqual(len(response['entries']), 0)
        # 3 fail validation
        date = "10-10-2023"
        response = getJournalEntries(user_id,date)
        self.assertEqual(response[0]['result'], "Invalid 'date' format, Please provide the Date in YYYY-MM-DD format")
        
        response = execute_db("DELETE FROM journalentry WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))

    
    def test_post_journal_entry(self):
        # 1 good path with entry
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","postjournalentryhandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("postjournalentryhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO journalentry VALUES (null,%s,%s,%s)",(user_id,'getjournalentrieshandlerunittestentry','2023-12-10'))
        self.assertEqual(response[0], [])
        request = {
            'entry': 'postjournalentryhandlerunittestentry'
        }
        date = "2023-12-10"
        response = postJournalEntry(user_id,date,request)
        self.assertEqual(response['result'], "Journal Entry Successfully Updated")
        # 2 good path without entry
        date = "2023-10-05"
        response = postJournalEntry(user_id,date,request)
        self.assertEqual(response['result'], "Journal Entry Successfully Saved")
        # 3 fail validation
        date = "10-10-2023"
        response = postJournalEntry(user_id,date,request)
        self.assertEqual(response[0]['result'], "Invalid 'date' format, Please provide the Date in YYYY-MM-DD format")
        
        response = execute_db("DELETE FROM journalentry WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
       
       
    def test_delete_journal_entry(self):
        # 1 good path with entries
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deletejournalentryhandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deletejournalentryhandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO journalentry VALUES (null,%s,%s,%s)",(user_id,'deletejournalentryhandlerunittestentry','2023-12-10'))
        self.assertEqual(response[0], [])
        
        date = "2023-12-10"
        response = deleteJournalEntry(user_id,date)
        self.assertEqual(response['result'], "Journal Entry Successfully Deleted")
        # 2 good path without entries
        date = "2023-10-05"
        response = deleteJournalEntry(user_id,date)
        self.assertEqual(response[0]['result'], "Error: Journal Entry Does Not Exist for Given User and Date Combination")
        # 3 fail validation
        date = "10-10-2023"
        response = deleteJournalEntry(user_id,date)
        self.assertEqual(response[0]['result'], "Invalid 'date' format, Please provide the Date in YYYY-MM-DD format")
        
        response = execute_db("DELETE FROM journalentry WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS