import unittest
from src.transformers.tradeTransformer import *
from src.models.utils import execute_db
from datetime import datetime, date
import os




class TestTradeTransformer(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT


    def test_transform_new_trade(self):
        # 1. Shares Trade
        #   a. Make sure all other if statements for blanks are addressed in one of the two options
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "qqq",
            "trade_date": "",
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "1:3",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        transformedRequest = transformNewTrade(request)
        self.assertEqual(transformedRequest['security_type'], 'Shares')
        self.assertEqual(transformedRequest['ticker_name'], 'QQQ')
        self.assertEqual(transformedRequest['expiry'], None)
        self.assertEqual(transformedRequest['strike'], None)
        self.assertEqual(transformedRequest['trade_date'], None)
        self.assertEqual(transformedRequest['pnl'], None)
        self.assertEqual(transformedRequest['units'], None)
        self.assertEqual(transformedRequest['percent_wl'], None)
        self.assertEqual(transformedRequest['buy_value'], None)
        
        
    def test_transform_edit_trade(self):
        #need to add support for trade_id now
        # setup queries 
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","transformedittradetradetransformerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("transformedittradetradetransformerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"transformedittradetradetransformerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_id = response[0][0]['trade_id']
        
        request = {
            "trade_type": "",
            "security_type": "Shares",
            "ticker_name": "spy",
            "trade_date": "2023-08-03",
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        transformedRequest = transformEditTrade(trade_id,request)
        self.assertEqual(len(transformedRequest), 6)
        self.assertEqual(transformedRequest['security_type'], 'Shares')
        self.assertEqual(transformedRequest['trade_date'], '2023-08-03')
        self.assertEqual(transformedRequest['ticker_name'], 'SPY')
        self.assertEqual(transformedRequest['expiry'], 'NULL')
        self.assertEqual(transformedRequest['strike'], 'NULL')
        self.assertEqual(transformedRequest['percent_wl'], 25.0)
        
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))


    def test_transform_process_csv(self):
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_trade_history.csv')
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            user_id = 0
            transformedRequest = processCsv(user_id, file)
            self.assertEqual(transformedRequest[0], True)
            self.assertEqual(len(transformedRequest[1]), 5)
            
    
    def test_transform_process_update_csv(self):
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_bulk_trade_updates.csv')
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            transformedRequest = processUpdateCsv(file)
            self.assertEqual(transformedRequest[0], True)
            self.assertEqual(len(transformedRequest[1]), 3)
        
    
    def test_transform_date_format(self):
        
        #1 - non-accepted date format
        input_date = "21 December 2022"
        final_date = transformDateFormart(input_date)
        self.assertEqual(final_date, input_date)
        
        #2 - accepted date format
        input_date = "4/18/23"
        final_date = transformDateFormart(input_date)
        self.assertEqual(final_date, "2023-04-18")
        
        
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS