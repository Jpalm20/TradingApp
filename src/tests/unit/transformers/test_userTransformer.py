import unittest
from src.transformers.userTransformer import *
from src.models.utils import execute_db
from datetime import datetime, date


class TestUserTransformer(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT


    def test_transform_new_user(self):
        request = {
            "first_name": "test",
            "last_name": "test",
            "birthday": "2023-01-01",
            "email": "transformnewuserunittest@gmail.com",
            "password": "password",
            "street_address": "10 Brewster Lane",
            "city": "new Jersey",
            "state": "nj",
            "country": "united states"
        }
        transformedRequest = transformNewUser(request)
        self.assertNotEqual(transformedRequest['password'], 'password')
        self.assertEqual(transformedRequest['first_name'], 'Test')
        self.assertEqual(transformedRequest['last_name'], 'Test')
        self.assertEqual(transformedRequest['city'], 'New Jersey')
        self.assertEqual(transformedRequest['state'], 'NJ')
        self.assertEqual(transformedRequest['country'], 'United States')


    def test_hash_password(self):
        password = 'password'
        hashedPassword = hashPassword(password)
        self.assertNotEqual(hashedPassword, password)
        #can I add another to verify the string length, is it always the same for this hash?
        
        
    def test_transform_edit_user(self):
        request = {
            "first_name": "test",
            "last_name": "test",
            "birthday": "2023-01-01",
            "email": "",
            "password": "",
            "street_address": "10 Brewster Lane",
            "city": "new jersey",
            "state": "nj",
            "country": "united states"
        }
        transformedRequest = transformEditUser(request)
        self.assertTrue('password' not in transformedRequest)
        self.assertEqual(transformedRequest['street_address'], '10 Brewster Lane')
        self.assertEqual(transformedRequest['first_name'], 'Test')
        self.assertEqual(transformedRequest['last_name'], 'Test')
        self.assertEqual(transformedRequest['city'], 'New Jersey')
        self.assertEqual(transformedRequest['state'], 'NJ')
        self.assertEqual(transformedRequest['country'], 'United States')


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
                    "id": '10000'
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
        
    
    def test_transform_from_and_to_date(self):
        # 1 Year
        from_date = '2024-01-10' 
        to_date = '2024-01-20'
        query = transformFromAndToDate(from_date,to_date)
        self.assertEqual(query, "trade_date >= '2024-01-10' AND trade_date <= '2024-01-20'")
        
    
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
        
    
    def test_transform_leaderboard_time_filter(self):
        # Today's date
        today = date.today()
        # First day of the year
        first_day_of_year = date(today.year, 1, 1)
        # First day of the quarter
        quarter_start_month = 3 * ((today.month - 1) // 3) + 1
        first_day_of_quarter = date(today.year, quarter_start_month, 1)
        # First day of the month
        first_day_of_month = date(today.year, today.month, 1)
        # First day of the week (assuming week starts on Monday)
        first_day_of_week = today - timedelta(days=today.weekday())
                
        #1 All Time
        result = transformLeaderboardTimeFilter("All Time")
        self.assertEqual(result, "t.trade_date is not NULL")
        
        #2 YTD
        result = transformLeaderboardTimeFilter("YTD")
        self.assertEqual(result, "t.trade_date >= '{}'".format(str(first_day_of_year)))
        
        #3 Quarter
        result = transformLeaderboardTimeFilter("Quarter")
        self.assertEqual(result, "t.trade_date >= '{}'".format(str(first_day_of_quarter)))
        
        #4 Quarter
        result = transformLeaderboardTimeFilter("Month")
        self.assertEqual(result, "t.trade_date >= '{}'".format(str(first_day_of_month)))
        
        #5 Week
        result = transformLeaderboardTimeFilter("Week")
        self.assertEqual(result, "t.trade_date >= '{}'".format(str(first_day_of_week)))
        
        #6 Today
        result = transformLeaderboardTimeFilter("Today")
        self.assertEqual(result, "t.trade_date >= '{}'".format(str(today)))
                
    
    def test_transform_leaderboard_value_filter(self):
                
        #1 Total PNL
        result = transformLeaderboardValueFilter("Total PNL")
        self.assertEqual(result, ["SUM(COALESCE(t.pnl, 0))","COUNT(t.trade_id) > 0","DESC"])
        
        #2 Avg PNL
        result = transformLeaderboardValueFilter("Avg PNL")
        self.assertEqual(result, ["SUM(COALESCE(t.pnl, 0)) / COUNT(t.trade_id)","COUNT(t.trade_id) > 0","DESC"])
        
        #3 Win %
        result = transformLeaderboardValueFilter("Win %")
        self.assertEqual(result, ["COUNT(CASE WHEN t.pnl > 0 THEN 1 END) * 100.0 / COUNT(t.trade_id)","COUNT(t.trade_id) > 0","DESC"])
        
        #4 Largest Win
        result = transformLeaderboardValueFilter("Largest Win")
        self.assertEqual(result, ["MAX(CASE WHEN t.pnl > 0 THEN t.pnl ELSE NULL END)","MAX(CASE WHEN t.pnl > 0 THEN t.pnl ELSE NULL END) IS NOT NULL","DESC"])
        
        #5 Avg Win
        result = transformLeaderboardValueFilter("Avg Win")
        self.assertEqual(result, ["AVG(CASE WHEN t.pnl > 0 THEN t.pnl ELSE NULL END)","AVG(CASE WHEN t.pnl > 0 THEN t.pnl ELSE NULL END) IS NOT NULL","DESC"])
        
        #6 Avg Loss
        result = transformLeaderboardValueFilter("Avg Loss")
        self.assertEqual(result, ["AVG(CASE WHEN t.pnl < 0 THEN t.pnl ELSE NULL END)","AVG(CASE WHEN t.pnl < 0 THEN t.pnl ELSE NULL END) IS NOT NULL","ASC"])
                
        
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS