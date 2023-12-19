import unittest
from validators.journalentryValidator import *
from models.utils import execute_db
from datetime import datetime, date, timedelta


class TestJournalEntryValidator(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
    
    # validate get account value
    def test_validate_date(self):
        # 1 good path
        date = "2023-10-10"
        response = validateDate(date)
        self.assertEqual(response, True)
        # 2 fail invalid format date
        date = "10-10-2023"
        response = validateDate(date)
        self.assertEqual(response[0]['result'], "Invalid 'date' format, Please provide the Date in YYYY-MM-DD format")
        # 3 fail future date
        date = (datetime.now()+timedelta(days=2)).strftime('%Y-%m-%d')
        response = validateDate(date)
        self.assertEqual(response[0]['result'], "Invalid date. The 'date' provided can't be in the future")
        
        
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS