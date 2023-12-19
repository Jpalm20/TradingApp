import unittest
from transformers.userTransformer import *
from models.utils import execute_db
from datetime import datetime, date


class TestUserTransformer(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT


    def test_transform_new_user(self):
        request = {
            "first_name": "Test",
            "last_name": "Test",
            "birthday": "2023-01-01",
            "email": "transformnewuserunittest@gmail.com",
            "password": "password",
            "street_address": "10 Brewster Lane",
            "city": "New Jersey",
            "state": "NJ",
            "country": "US"
        }
        transformedRequest = transformNewUser(request)
        self.assertNotEqual(transformedRequest['password'], 'password')
        self.assertEqual(transformedRequest['first_name'], 'Test')


    def test_hash_password(self):
        password = 'password'
        hashedPassword = hashPassword(password)
        self.assertNotEqual(hashedPassword, password)
        #can I add another to verify the string length, is it always the same for this hash?
        
        
    def test_transform_edit_user(self):
        request = {
            "first_name": "",
            "last_name": "",
            "birthday": "2023-01-01",
            "email": "",
            "password": "",
            "street_address": "10 Brewster Lane",
            "city": "",
            "state": "",
            "country": ""
        }
        transformedRequest = transformEditUser(request)
        self.assertTrue('password' not in transformedRequest)
        self.assertEqual(transformedRequest['street_address'], '10 Brewster Lane')


    def test_transform_report_bug(self):
        # 1 Bug
        # 2 Feature Request
        request = {
            "requestType": "Feature Request",
            "page": "Test Page",
            "summary": "Test Transform Report Bug",
            "description": "transformreportbugunittest",
        }
        email = 'transformreportbugunittest@gmail.com'
        transformedRequest = transformReportBug(request,email)
        expected = {
            "fields": {
                "project":
                { 
                    "id": 'None' #Will need to resolve this so env var is read this should be 10000
                },
                "summary": "Test Page" + " - " + "Test Transform Report Bug",
                "description": "transformreportbugunittest" + " \n\nSubmitted By: " + "transformreportbugunittest@gmail.com",
                "issuetype": {
                    "name": "Story"
                }
            }
        }
        self.assertEqual(transformedRequest, expected)

        
    def test_transform_date_range(self):
        # 1 Year
        date_range = 'Year' 
        query = transformDateRange(date_range)
        self.assertEqual(query, "trade_date >= DATE_ADD(NOW(), INTERVAL -1 YEAR)")
        # 2 Month
        date_range = 'Month' 
        query = transformDateRange(date_range)
        self.assertEqual(query, "trade_date >= DATE_ADD(NOW(), INTERVAL -1 MONTH)")
        # 3 Week
        date_range = 'Week' 
        query = transformDateRange(date_range)
        self.assertEqual(query, "trade_date >= DATE_ADD(NOW(), INTERVAL -1 WEEK)")
        # 4 Day
        date_range = 'Day' 
        query = transformDateRange(date_range)
        self.assertEqual(query, "trade_date >= DATE_ADD(NOW(), INTERVAL -1 DAY)")
        
    
    def test_transform_av_tf(self):
        today_date = '2023-01-01'
        # 1 Year
        time_frame = 'Year' 
        dates = transformAVtf(today_date,time_frame)
        expected_dates = [
            date(2017, 12, 31), 
            date(2018, 12, 31), 
            date(2019, 12, 31), 
            date(2020, 12, 31), 
            date(2021, 12, 31), 
            date(2022, 12, 31), 
            date(2023, 1, 1)
        ]
        self.assertEqual(dates, expected_dates)
        # 2 Month
        time_frame = 'Month' 
        dates = transformAVtf(today_date,time_frame)
        expected_dates = [
            date(2022, 7, 31), 
            date(2022, 8, 31), 
            date(2022, 9, 30), 
            date(2022, 10, 31), 
            date(2022, 11, 30), 
            date(2022, 12, 31), 
            date(2023, 1, 1)
        ]
        self.assertEqual(dates, expected_dates)
        # 3 Week
        time_frame = 'Week' 
        dates = transformAVtf(today_date,time_frame)
        expected_dates = [
            date(2022, 11, 21), 
            date(2022, 11, 28), 
            date(2022, 12, 5), 
            date(2022, 12, 12), 
            date(2022, 12, 19), 
            date(2022, 12, 26), 
            date(2023, 1, 1)
        ]
        self.assertEqual(dates, expected_dates)
        # 4 Day
        time_frame = 'Day' 
        dates = transformAVtf(today_date,time_frame)
        expected_dates = [
            date(2022, 12, 26), 
            date(2022, 12, 27), 
            date(2022, 12, 28), 
            date(2022, 12, 29), 
            date(2022, 12, 30), 
            date(2022, 12, 31), 
            date(2023, 1, 1)
        ]
        self.assertEqual(dates, expected_dates)

        
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS