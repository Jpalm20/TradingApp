from asyncio.log import logger
from cgitb import reset
import unittest
import time
import requests
import os
from datetime import datetime, timedelta
from src.models.utils import execute_db
import copy
import csv
import io

user_id = None
token = None
trade_id = None
trade_ids = []
reset_code = None
verification_code = None

class TestAPIs(unittest.TestCase):
    
    # Retrieve the base URL from the environment variable
    ENV = os.getenv('ENV', 'prod')
    if ENV == 'docker':
        BASE_URL = os.getenv('DOCKER_INTEGRATION_TEST_URL')  # Default to a local URL if not set
    else:
        BASE_URL = os.getenv('INTEGRATION_TEST_URL') 


    def setUp(self):
        # Set up any common data or state here
        self.headers = {'Content-Type': 'application/json'}
        
        global token
        if token is not None:
            self.headers['Authorization'] = f'Bearer {token}'
    
    
    def test_01_register_user(self):
        # /user/register
        
        request_body = {
            "first_name": "",
            "last_name": "",
            "birthday": "",
            "email": "registeruserapitest@gmail.com",
            "password": "password",
            "street_address": "10 Brewster Lane",
            "city": "new york",
            "state": "ny",
            "country": "united states"
        }
        response = requests.post(f"{self.BASE_URL}/user/register", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'],"User Created Successfully")
        global user_id
        user_id = response_data['user_id']
        
    
    def test_02_login_user(self):
        # /user/login

        request_body = {
            "email": "registeruserapitest@gmail.com",
            "password": "password"
        }
        response = requests.post(f"{self.BASE_URL}/user/login", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['email'],"registeruserapitest@gmail.com")
        global token
        token = response_data['token']
        
    
    def test_03_user_preferences(self):
        # /user/preferences

        response = requests.get(f"{self.BASE_URL}/user/preferences", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['account_value_optin'],0)
        self.assertEqual(response_data['email_optin'],1)
        self.assertEqual(response_data['preferred_currency'],"USD")
        self.assertEqual(response_data['2fa_optin'],0)
        
    
    def test_04_toggle_account_value_tracking(self):
        #/user/preferences/toggleav
        
        response = requests.post(f"{self.BASE_URL}/user/preferences/toggleav", json={}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['account_value_optin'],1)
        self.assertEqual(response_data['email_optin'],1)
        self.assertEqual(response_data['preferred_currency'],"USD")
        self.assertEqual(response_data['2fa_optin'],0)
        
    
    def test_05_toggle_email_optin(self):
        #/user/preferences/toggleeoi
        
        response = requests.post(f"{self.BASE_URL}/user/preferences/toggleeoi", json={}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['account_value_optin'],1)
        self.assertEqual(response_data['email_optin'],0)
        self.assertEqual(response_data['preferred_currency'],"USD")
        self.assertEqual(response_data['2fa_optin'],0)
        
    
    def test_06_toggle_feature_flags(self):
        #/user/preferences/toggleff
        
        request_body = ["email_optin","account_value_optin","2fa_optin"]
        response = requests.post(f"{self.BASE_URL}/user/preferences/toggleff", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['account_value_optin'],0)
        self.assertEqual(response_data['email_optin'],1)
        self.assertEqual(response_data['preferred_currency'],"USD")
        self.assertEqual(response_data['2fa_optin'],1)
        
        
    def test_07_update_currency(self):
        #/user/preferences/updatecurrency
        
        request_body = {
            "preferred_currency": "JPY"
        }
        response = requests.post(f"{self.BASE_URL}/user/preferences/updatecurrency", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['account_value_optin'],0)
        self.assertEqual(response_data['email_optin'],1)
        self.assertEqual(response_data['preferred_currency'],"JPY")
        self.assertEqual(response_data['2fa_optin'],1)
        
    
    def test_08_get_user_from_session(self):
        #/user/getUserFromSession
        
        response = requests.get(f"{self.BASE_URL}/user/getUserFromSession", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user_id'],user_id)
        
    
    def test_09_log_trade(self):
        #/trade/create
        
        request_body = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "SPY",
            "trade_date": "2024-01-01",
            "expiry": "",
            "strike": "",
            "buy_value": "250",
            "units": "3",
            "rr": "1:3",
            "pnl": "20",
            "percent_wl": "3.07",
            "comments": ""
        }
        response = requests.post(f"{self.BASE_URL}/trade/create", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'],"Trade Logged Successfully")
        self.assertEqual(response_data['trade_date'],"2024-01-01")
        global trade_id
        trade_id = response_data['trade_id']
    
    
    def test_10_get_user_trades(self):
        #/user/trades
        
        #Good without filters
        response = requests.get(f"{self.BASE_URL}/user/trades", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data['trades']),1)
        self.assertEqual(response_data['stats']['num_trades'],1)
        self.assertEqual(response_data['trades'][0]['trade_date'],'2024-01-01')
        
        #Good with filters
        response = requests.get(f"{self.BASE_URL}/user/trades?ticker_name=QQQ", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data['trades']),0)
        self.assertEqual(response_data['stats']['num_trades'],0)
        self.assertEqual(response_data['trades'],[])
        
    
    def test_11_get_user_stats(self):
        #/user/trades/stats
        
        #Good without filters
        response = requests.get(f"{self.BASE_URL}/user/trades/stats", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['stats']['num_trades'],1)
        self.assertEqual(response_data['stats']['num_wins'],1)
        
        #Good with filters
        response = requests.get(f"{self.BASE_URL}/user/trades/stats?ticker_name=QQQ", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['stats']['num_trades'],0)
        self.assertEqual(response_data['stats']['num_wins'],0)
        
    
    def test_12_set_account_value(self):
        #/user/accountValue  
          
        request_body = {
            "accountvalue": 520,
            "date": "2024-01-01"
        } 
        response = requests.post(f"{self.BASE_URL}/user/accountValue", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'],"Account Value Set Successfully")
        self.assertEqual(response_data['accountvalue'],520)
        self.assertEqual(response_data['date'],'2024-01-01')
       
    
    def test_13_get_trade(self):
        #/trade/<int:trade_id>
        tradeID = None
        
        global trade_id
        if trade_id is not None:
            tradeID = trade_id 
            
        response = requests.get(f"{self.BASE_URL}/trade/{tradeID}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['trade_id'],tradeID)
        self.assertEqual(response_data['pnl'],'20')
        
        
    def test_14_edit_trade(self):
        #/trade/<int:trade_id>
        tradeID = None
        
        global trade_id
        if trade_id is not None:
            tradeID = trade_id
            
        request_body = {
            "trade_type": "",
            "security_type": "",
            "ticker_name": "",
            "trade_date": "",
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "",
            "pnl": "50",
            "percent_wl": "",
            "comments": ""
        }
        response = requests.post(f"{self.BASE_URL}/trade/{tradeID}", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'],"Trade Edited Successfully")
        self.assertEqual(response_data['trade_id'],tradeID)
        self.assertEqual(response_data['pnl'],50)
        
            
    def test_15_get_account_value(self):
        #/user/accountValue
        
        response = requests.get(f"{self.BASE_URL}/user/accountValue?date=2024-01-01&time_frame=Day", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['accountvalues'][6]['date'],'2024-01-01')
        self.assertEqual(response_data['accountvalues'][6]['accountvalue'],550)
        
    
    def test_16_get_user_trades_page(self):
        #/user/trades/page
        
        # Without Filters
        response = requests.get(f"{self.BASE_URL}/user/trades/page?page=1&numrows=100", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['count'],1)
        self.assertEqual(len(response_data['trades']),1)
        self.assertEqual(response_data['trades'][0]['ticker_name'],'SPY')
        global trade_ids
        for trade in response_data['trades']:
            trade_ids.append(trade['trade_id'])       
        
        # With Filters
        response = requests.get(f"{self.BASE_URL}/user/trades/page?page=1&numrows=200&ticker_name=QQQ", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['count'],0)
        self.assertEqual(response_data['trades'],[])
        
    
    def test_17_search_user_ticker(self):
        #/trade/searchTicker
        
        # No Filter
        response = requests.get(f"{self.BASE_URL}/trade/searchTicker", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data['tickers']),1)
        self.assertEqual(response_data['tickers'][0]['ticker_name'],'SPY')  
        
        # Valid Result with Filter
        response = requests.get(f"{self.BASE_URL}/trade/searchTicker?ticker_name=S", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data['tickers']),1)
        self.assertEqual(response_data['tickers'][0]['ticker_name'],'SPY')        
        
        # No Result with Filter
        response = requests.get(f"{self.BASE_URL}/trade/searchTicker?ticker_name=SY", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data['tickers']),0)
        self.assertEqual(response_data['tickers'],[])   
        
    
    def test_18_pnl_year(self):
        #/user/pnlbyYear/<int:date_year>
        
        # Without Filter
        response = requests.get(f"{self.BASE_URL}/user/pnlbyYear/2024", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['months'][0]['0'][0]['pnl'],50)
        self.assertEqual(response_data['months'][0]['0'][0]['count'],1)
        
        # With Filter
        response = requests.get(f"{self.BASE_URL}/user/pnlbyYear/2024?ticker_name=QQQ", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['months'][0]['0'][0]['pnl'],0)
        self.assertEqual(response_data['months'][0]['0'][0]['count'],0)
        
        
    
    def test_19_import_csv(self):
        #/trade/importCsv/<string:account_value_import_enable>
        
        account_value_import_enable = 'true'
        
        boundary = '----WebKitFormBoundaryySqtS1tZeUD7xapy'
        headers_copy = copy.deepcopy(self.headers)  # Create a deep copy of the headers

        # Overwrite the Content-Type to multipart/form-data
        headers_copy['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        
        body = (
            f'--{boundary}\r\n'
            'Content-Disposition: form-data; name="csv_file"; filename="example_trade_history.csv"\r\n'
            'Content-Type: text/csv\r\n'
            '\r\n'
            'execution_time,side,quantity,ticker_name,expiry,strike,security_type,cost_basis\n'
            '12/12/22 9:09,BUY,1,SPY,13-Dec-22,393,PUT,3.39\n'
            '12/12/22 9:17,SELL,-1,SPY,13-Dec-22,393,PUT,3.31\n'
            '12/13/22 8:47,BUY,1,QQQ,15-Dec-22,290,PUT,3.47\n'
            '12/13/22 8:47,SELL,-1,QQQ,15-Dec-22,290,PUT,3.59\n'
            '12/15/22 7:41,BUY,1,SPY,19-Dec-22,390,CALL,3.41\n'
            '12/15/22 7:47,SELL,-1,SPY,19-Dec-22,390,CALL,3.27\n'
            '12/16/22 12:11,BUY,1,SPY,21-Dec-22,383,CALL,3.45\n'
            '12/16/22 12:14,SELL,-1,SPY,21-Dec-22,383,CALL,3.55\n'
            '4/18/23 7:24,BUY,1,SPY,21-Apr-23,414,PUT,1.96\n'
            '4/18/23 7:25,SELL,-1,SPY,21-Apr-23,414,PUT,2.24\n'
            f'--{boundary}--\r\n'
        )
        
        response = requests.post(f'{self.BASE_URL}/trade/importCsv/{account_value_import_enable}', data=body, headers=headers_copy)
        response_data = response.json()
        self.assertEqual(response_data['result'],"Trades Imported Successfully")
        self.assertEqual(len(response_data['trades']),5)
    
    
    def test_20_export_trades(self):
        #/trade/exportCsv
        
        request_body = {
            "exported_trades": [
                {
                    "buy_value": 234,
                    "comments": "",
                    "expiry": None,
                    "percent_wl": 25,
                    "pnl": 234,
                    "rr": "1:3",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "PSQ",
                    "trade_date": "2023-07-04",
                    "trade_id": 236,
                    "trade_type": "Day Trade",
                    "units": 4,
                    "user_id": 77
                },
                {
                    "buy_value": 240,
                    "comments": "",
                    "expiry": None,
                    "percent_wl": None,
                    "pnl": 100,
                    "rr": "1:2",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "CQQQ",
                    "trade_date": "2023-08-03",
                    "trade_id": 237,
                    "trade_type": "Day Trade",
                    "units": 4,
                    "user_id": 77
                },
                {
                    "buy_value": 250,
                    "comments": "",
                    "expiry": None,
                    "percent_wl": 35.4,
                    "pnl": 354,
                    "rr": "1:3",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "PSQ",
                    "trade_date": "2023-07-19",
                    "trade_id": 238,
                    "trade_type": "Day Trade",
                    "units": 4,
                    "user_id": 77
                },
                {
                    "buy_value": 250,
                    "comments": "",
                    "expiry": None,
                    "percent_wl": 13.33,
                    "pnl": 100,
                    "rr": "1:1",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "SPY",
                    "trade_date": "2023-07-18",
                    "trade_id": 239,
                    "trade_type": "Day Trade",
                    "units": 3,
                    "user_id": 77
                },
                {
                    "buy_value": 246,
                    "comments": "",
                    "expiry": None,
                    "percent_wl": 30.22,
                    "pnl": 223,
                    "rr": "1:1",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "ADUS",
                    "trade_date": "2023-07-20",
                    "trade_id": 240,
                    "trade_type": "Day Trade",
                    "units": 3,
                    "user_id": 77
                },
                {
                    "buy_value": 234,
                    "comments": "",
                    "expiry": None,
                    "percent_wl": 22.3,
                    "pnl": 1200,
                    "rr": "1:1",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "QID",
                    "trade_date": "2023-07-21",
                    "trade_id": 241,
                    "trade_type": "Swing Trade",
                    "units": 23,
                    "user_id": 77
                },
                {
                    "buy_value": 250,
                    "comments": "testing",
                    "expiry": None,
                    "percent_wl": 3.4,
                    "pnl": 34,
                    "rr": "1:3",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "SPY",
                    "trade_date": "2023-08-01",
                    "trade_id": 242,
                    "trade_type": "Day Trade",
                    "units": 4,
                    "user_id": 77
                },
                {
                    "buy_value": 250,
                    "comments": "",
                    "expiry": None,
                    "percent_wl": 3.07,
                    "pnl": 23,
                    "rr": "1:3",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "SPY",
                    "trade_date": "2023-08-03",
                    "trade_id": 243,
                    "trade_type": "Day Trade",
                    "units": 3,
                    "user_id": 77
                },
                {
                    "buy_value": 250,
                    "comments": "",
                    "expiry": None,
                    "percent_wl": 3.07,
                    "pnl": 23,
                    "rr": "1:3",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "SPY",
                    "trade_date": "2023-08-03",
                    "trade_id": 244,
                    "trade_type": "Day Trade",
                    "units": 3,
                    "user_id": 77
                },
                {
                    "buy_value": 250,
                    "comments": "",
                    "expiry": None,
                    "percent_wl": 66.67,
                    "pnl": 500,
                    "rr": "1:1",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "SPY",
                    "trade_date": "2023-08-03",
                    "trade_id": 245,
                    "trade_type": "Day Trade",
                    "units": 3,
                    "user_id": 77
                },
                {
                    "buy_value": 250,
                    "comments": "",
                    "expiry": None,
                    "percent_wl": 13.33,
                    "pnl": 100,
                    "rr": "1:1",
                    "security_type": "Shares",
                    "strike": None,
                    "ticker_name": "SPY",
                    "trade_date": "2023-08-03",
                    "trade_id": 246,
                    "trade_type": "Day Trade",
                    "units": 3,
                    "user_id": 77
                }
            ]
        }
        response = requests.post(f"{self.BASE_URL}/trade/exportCsv", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        
        # Verify the status code
        self.assertEqual(response.status_code, 200)
        
        # Verify the content type
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        
        # Verify the content disposition
        self.assertIn('attachment; filename=trades.csv', response.headers['Content-Disposition'])
        
        # Parse the CSV content
        csv_content = response.text
        csv_reader = csv.reader(io.StringIO(csv_content))

        # Extract the CSV data into a list of lists
        csv_data = list(csv_reader)

        # Verify the headers
        expected_headers = [
            "trade_id", "trade_date", "trade_type", "security_type", "ticker_name",
            "buy_value", "units", "expiry", "strike", "pnl", "percent_wl", "rr"
        ]
        self.assertEqual(csv_data[0], expected_headers)

        # Verify the first row of data (you can add more rows as needed)
        expected_first_row = [
            "236", "2023-07-04", "Day Trade", "Shares", "PSQ", "234", "4", "None", "None", "234", "25", "1:3"
        ]
        self.assertEqual(csv_data[1], expected_first_row)
    
    
    def test_21_report_bug(self):
        #/user/reportBug
        
        request_body = {
            "summary": "Test API",
            "page": "Other",
            "description": "Testing API",
            "requestType": "Bug Report"
        }
        
        response = requests.post(f"{self.BASE_URL}/user/reportBug", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'],"Feedback Submitted Successfully")
        
    
    def test_22_change_password(self):
        #/user/changePassword

        request_body = {
            "curr_pass": "password",
            "new_pass_1": "password1",
            "new_pass_2": "password1"
        }
        
        response = requests.post(f"{self.BASE_URL}/user/changePassword", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'],"Password Successfully Changed")
        
    
    def test_23_get_user(self):
        #/user
        
        response = requests.get(f"{self.BASE_URL}/user", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        global user_id
        self.assertEqual(response_data['user_id'],user_id)
    
    
    def test_24_update_trades(self):
        #/trade/updateTrades
        
        global trade_ids
        
        verify_one_id = trade_ids[0]
        response = requests.get(f"{self.BASE_URL}/trade/{verify_one_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['ticker_name'],'SPY')
        
        request_body = {
            "ids": trade_ids,
            "update_info": {
                "trade_type": "",
                "security_type": "",
                "ticker_name": "QQQ",
                "trade_date": "",
                "expiry": "",
                "strike": "",
                "buy_value": "",
                "units": "",
                "rr": "",
                "pnl": "",
                "percent_wl": "",
                "comments": ""
            }
        }
        
        response = requests.post(f"{self.BASE_URL}/trade/updateTrades", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        trade_ids_str = ', '.join(map(str, trade_ids))
        self.assertEqual(response_data['result'], f"Trades Updated Successfully: {trade_ids_str}")
        verify_one_id = trade_ids[0]
        response = requests.get(f"{self.BASE_URL}/trade/{verify_one_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['ticker_name'],'QQQ')
    
    
    def test_25_bulk_update_csv(self):
        #/trade/bulkUpdateCsv
    
        boundary = '----WebKitFormBoundaryySqtS1tZeUD7xapy'
        headers_copy = copy.deepcopy(self.headers)  # Create a deep copy of the headers

        # Overwrite the Content-Type to multipart/form-data
        headers_copy['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        
        global trade_ids
        trade_id_0 = str(trade_ids[0])
        
        body = (
            f'--{boundary}\r\n'
            'Content-Disposition: form-data; name="csv_file"; filename="trades.csv"\r\n'
            'Content-Type: text/csv\r\n'
            '\r\n'
            'trade_id,trade_date,trade_type,security_type,ticker_name,buy_value,units,expiry,strike,pnl,percent_wl,rr\n'
            f'{trade_id_0},None,Day Trade,Shares,SPY,250,3,None,None,230,30.67,1:1\n'
            f'0,None,Day Trade,Options,NVDA,120,3,13-Dec-22,393,25,6.94,1:1\n'
            f'--{boundary}--\r\n'
        )
        
        response = requests.post(f'{self.BASE_URL}/trade/bulkUpdateCsv', data=body, headers=headers_copy)

        response_data = response.json()
        trade_array = [trade_id_0]
        expected_message = f"Trades Updates Imported Successfully: {', '.join(map(str, trade_array))}"
        self.assertEqual(response_data['result'], expected_message)
        self.assertEqual(len(response_data['updated_ids']), 1)
        self.assertEqual(len(response_data['error_ids']), 1)
        self.assertEqual(response_data['error_ids'][0]['trade_id'], '0')
        self.assertEqual(response_data['error_ids'][0]['error_message'], "trade_id: 0 does not exist")
        
    
    def test_26_generate_reset_code(self):
        #/user/generateResetCode
        
        request_body = {
            "email": "registeruserapitest@gmail.com"
        }
        response = requests.post(f"{self.BASE_URL}/user/generateResetCode", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'], "Reset Code Generated Successfully")
        global reset_code, user_id
        response = execute_db("SELECT * FROM resetcode WHERE user_id = %s", (user_id,))
        reset_code = response[0][0]['code']
        self.assertEqual(response[0][0]['validated'],0)
        
    
    def test_27_validate_reset_code(self):
        #/user/confirmResetCode
        
        global reset_code
        request_body = {
            "email": "registeruserapitest@gmail.com",
            "code": str(reset_code)
        }
        response = requests.post(f"{self.BASE_URL}/user/confirmResetCode", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'], "Reset Code Verified Successfully")
        global user_id
        response = execute_db("SELECT * FROM resetcode WHERE user_id = %s", (user_id,))
        self.assertEqual(response[0][0]['code'], reset_code)
        self.assertEqual(response[0][0]['validated'],1)
    
    
    def test_28_reset_password(self):
        #/user/resetPassword
        
        global reset_code
        request_body = {
            "email": "registeruserapitest@gmail.com",
            "code": str(reset_code),
            "new_pass_1": "password11",
            "new_pass_2": "password11"
        }
        response = requests.post(f"{self.BASE_URL}/user/resetPassword", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'], "Password Reset Successfully")
        
    
    def test_29_post_journal_entry(self):
        #/journal/<string:date>
        
        # Create Journal
        request_body = {
            "entry": "TESTING"
        }
        response = requests.post(f"{self.BASE_URL}/journal/2024-01-01", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'], "Journal Entry Successfully Saved")
        self.assertEqual(response_data['date'], "2024-01-01")
        self.assertEqual(response_data['entry'], "TESTING")
        
    
    def test_30_get_journal_entries(self):
        #/journal/<string:date>
        
        # Get Journal
        response = requests.get(f"{self.BASE_URL}/journal/2024-01-01", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_response_body = {
            "entries": [
                {
                    "date": "2024-01-01",
                    "entrytext": "TESTING"
                }
            ]
        }
        self.assertEqual(response_data, expected_response_body)
        self.assertEqual(len(response_data['entries']), 1)
        self.assertEqual(response_data['entries'][0]['date'], "2024-01-01")
        self.assertEqual(response_data['entries'][0]['entrytext'], "TESTING")
        
    
    def test_31_delete_journal_entry(self):
        #/journal/<string:date>
        
        # Delete Journal
        response = requests.delete(f"{self.BASE_URL}/journal/2024-01-01", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'], "Journal Entry Successfully Deleted")
        self.assertEqual(response_data['date'], "2024-01-01")
    
    
    def test_32_delete_trade(self):
        #/trade/<int:trade_id>
        
        # Delete trade_id global variable
        global trade_id, user_id
        response = requests.delete(f"{self.BASE_URL}/trade/{trade_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'], "Trade Successfully Deleted")
        self.assertEqual(response_data['user_id'], user_id)

    
    def test_33_delete_trades(self):
        #/trade/deleteTrades
        
        # Delete all remaining trade_id by calling user_trades_page API
        
        # Call User Trades Page API, gather all trade_id
        response = requests.get(f"{self.BASE_URL}/user/trades/page?page=1&numrows=100", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        trade_ids_to_del = []
        for trade in response_data['trades']:
            trade_ids_to_del.append(trade['trade_id'])
        
        # Delete Trades API
        response = requests.delete(f"{self.BASE_URL}/trade/deleteTrades", json=trade_ids_to_del, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        global user_id
        self.assertEqual(response_data['result'], "Trades Successfully Deleted")
        self.assertEqual(response_data['user_id'], user_id)
        

    def test_34_2fa_flow(self):
        #/user/verify2fa
                
        #Log back in, getting 2FA code created
        request_body = {
            "email": "registeruserapitest@gmail.com",
            "password": "password11"
        }
        response = requests.post(f"{self.BASE_URL}/user/login", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 202)
        response_data = response.json()
        self.assertEqual(response_data['result'],"2FA Enabled, Verification Code Sent to Email")
        
        #Get 2fa code from db for verify2fa api
        global verification_code, user_id
        response = execute_db("SELECT * FROM verificationcode WHERE user_id = %s", (user_id,))
        verification_code = response[0][0]['code']
        self.assertEqual(response[0][0]['validated'],0)
        
        #Verify 2FA code and complete login

        request_body = {
            "email": "registeruserapitest@gmail.com",
            "code": str(verification_code)
        }
        response = requests.post(f"{self.BASE_URL}/user/verify2fa", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user_id'], user_id)
        self.assertEqual(response_data['email'],"registeruserapitest@gmail.com")
        global token
        new_token = response_data['token']
        token = new_token
        
        headers_copy = copy.deepcopy(self.headers)  # Create a deep copy of the headers
        headers_copy['Authorization'] = f'Bearer {new_token}'
        
        # Toggle 2fa_optin ff back to false before logging in again
        request_body = ["2fa_optin"]
        response = requests.post(f"{self.BASE_URL}/user/preferences/toggleff", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['2fa_optin'],0)
        
    
    def test_35_upload_profile_pic(self):
        #/user/profilePicture
                
        boundary = '----WebKitFormBoundaryySqtS1tZeUD7xapy'
        headers_copy = copy.deepcopy(self.headers)  # Create a deep copy of the headers
        
        # Overwrite the Content-Type to multipart/form-data with the boundary
        headers_copy['Content-Type'] = f'multipart/form-data; boundary={boundary}'

        # Construct the file path for the test image
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_image.JPG")
        
        # Read the image file in binary mode
        with open(file_path, "rb") as file:
            file_content = file.read()

        # Construct the body for the multipart/form-data
        body = (
            f'--{boundary}\r\n'
            'Content-Disposition: form-data; name="profile_pic"; filename="test_image.JPG"\r\n'
            'Content-Type: image/jpeg\r\n'
            '\r\n'
        ).encode('utf-8') + file_content + f'\r\n--{boundary}--\r\n'.encode('utf-8')

        # Make the POST request with the constructed body
        response = requests.post(
            f"{self.BASE_URL}/user/profilePicture",
            data=body,  # Use `data` instead of `files` since we're manually constructing the body
            headers=headers_copy
        )
                    
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'], "Profile Picture Uploaded Successfully")
            
    
    def test_36_get_profile_pic(self):
        #/user/profilePicture

        response = requests.get(
            f"{self.BASE_URL}/user/profilePicture",
            headers=self.headers
        )
    
        # Assert response status and data
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual('profile_picture_url' in response_data,True)
        
    
    def test_37_delete_profile_pic(self):
        #/user/profilePicture
        
        response = requests.delete(
            f"{self.BASE_URL}/user/profilePicture",
            headers=self.headers
        )
    
        # Assert response status and data
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'],"Profile Picture Deleted Successfully")
        
    
    def test_38_logout_user(self):
        #/user/logout
        
        # Logout
        response = requests.post(f"{self.BASE_URL}/user/logout", json={}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_date = response.json()
        self.assertEqual(response_date['result'],"User Logged Out")
        
        
    def test_39_delete_user(self):
        #/user 
        
        # Log back in to generate new token, logout expired the token
        request_body = {
            "email": "registeruserapitest@gmail.com",
            "password": "password11"
        }
        response = requests.post(f"{self.BASE_URL}/user/login", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['email'],"registeruserapitest@gmail.com")
        global token
        new_token = response_data['token']
        token = new_token
        
        headers_copy = copy.deepcopy(self.headers)  # Create a deep copy of the headers
        headers_copy['Authorization'] = f'Bearer {new_token}'
        
        # Delete all remaining data for user_id
        response = requests.delete(f"{self.BASE_URL}/user", headers=headers_copy)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'],"User Successfully Deleted")
            

    def tearDown(self):
        # Any cleanup actions that need to occur after each test can be performed here.
        # pass
        time.sleep(2)
    
    
    @classmethod
    def tearDownClass(cls):
        global user_id
        if user_id is not None:
            execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
            execute_db("DELETE FROM session WHERE user_id = %s", (user_id,))
            execute_db("DELETE FROM resetcode WHERE user_id = %s", (user_id,))
            execute_db("DELETE FROM verificationcode WHERE user_id = %s", (user_id,))
            execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
            execute_db("DELETE FROM journalentry WHERE user_id = %s", (user_id,))
            execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
            
        

if __name__ == '__main__':
    unittest.main()
