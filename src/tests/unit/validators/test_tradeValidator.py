import unittest
from src.validators.tradeValidator import *
from src.models.utils import execute_db
from datetime import datetime, date, timedelta


class TestTradeValidator(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT


    def test_validate_new_trade(self):
        # 1 good path
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
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
        response = validateNewTrade(request)
        self.assertEqual(response, True)
        # 2 fail on options check
        request = {
            "trade_type": "Day Trade",
            "security_type": "Options",
            "ticker_name": "QQQ",
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
        response = validateNewTrade(request)
        self.assertEqual(response[0]['result'], "Options require Strike Price and Expiry, Try Again")
        # 3 fail on shares check
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
            "trade_date": "",
            "expiry": "",
            "strike": "400",
            "buy_value": "",
            "units": "",
            "rr": "1:3",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        response = validateNewTrade(request)
        self.assertEqual(response[0]['result'], "Shares require no Strike Price or Expiry, Try Again")
        # 4 fail on invalid security type
        request = {
            "trade_type": "Day Trade",
            "security_type": "Share",
            "ticker_name": "QQQ",
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
        response = validateNewTrade(request)
        self.assertEqual(response[0]['result'], "Security Type is either 'Shares' or 'Options', Try Again")
        # 5 fail on ticker name
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "",
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
        response = validateNewTrade(request)
        self.assertEqual(response[0]['result'], "Must Include a Valid Ticker Symbol")
        # 6 fail on r/r
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
            "trade_date": "",
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "13",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        response = validateNewTrade(request)
        self.assertEqual(response[0]['result'], "Must Include a Valid Risk to Reward Ratio")
        # 7 fail on trade date future
        date = (datetime.now()+timedelta(days=2)).strftime('%Y-%m-%d')
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
            "trade_date": date,
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "1:3",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        response = validateNewTrade(request)
        self.assertEqual(response[0]['result'], "Trade Closure Date Can't be in the Future")
        # 8 fail on invalid trade_type
        request = {
            "trade_type": "Day",
            "security_type": "Shares",
            "ticker_name": "QQQ",
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
        response = validateNewTrade(request)
        self.assertEqual(response[0]['result'], "Trade Type must be 'Day Trade' or 'Swing Trade', Try Again")
        # 9 fail on invalid security_type
        request = {
            "trade_type": "Day Trade",
            "security_type": "Share",
            "ticker_name": "QQQ",
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
        response = validateNewTrade(request)
        self.assertEqual(response[0]['result'], "Security Type is either 'Shares' or 'Options', Try Again")


    def test_validate_edit_trade(self):
        # setup queries 
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","validateedittradetradevalidatorunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("validateedittradetradevalidatorunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"validateedittradetradevalidatorunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_id = response[0][0]['trade_id']
        
        # 1 good path
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
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
        response = validateEditTrade(user_id,trade_id,request)
        self.assertEqual(response, True)
        # 2 fail on options check
        request = {
            "trade_type": "Day Trade",
            "security_type": "Options",
            "ticker_name": "QQQ",
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
        response = validateEditTrade(user_id,trade_id,request)
        self.assertEqual(response[0]['result'], "Options require Strike Price and Expiry, Try Again")
        # 3 fail on shares check
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
            "trade_date": "",
            "expiry": "",
            "strike": "400",
            "buy_value": "",
            "units": "",
            "rr": "1:3",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        response = validateEditTrade(user_id,trade_id,request)
        self.assertEqual(response[0]['result'], "Shares require no Strike Price or Expiry, Try Again")
        # 4 fail on ticker name
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": " ",
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
        response = validateEditTrade(user_id,trade_id,request)
        self.assertEqual(response[0]['result'], "Invalid Ticker Symbol, Try Updating Again")
        # 5 fail on r/r
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
            "trade_date": "",
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "13",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        response = validateEditTrade(user_id,trade_id,request)
        self.assertEqual(response[0]['result'], "Must Include a Valid Risk to Reward Ratio")
        # 6 fail on trade date future
        date = (datetime.now()+timedelta(days=2)).strftime('%Y-%m-%d')
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
            "trade_date": date,
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "1:3",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        response = validateEditTrade(user_id,trade_id,request)
        self.assertEqual(response[0]['result'], "Trade Closure Date Can't be in the Future")
        
        #7 fail on user_id not matching
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
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
        response = validateEditTrade(0,trade_id,request)
        self.assertEqual(response[0]['result'], "trade_id: {} does not belong to this user_id".format(trade_id))
        self.assertEqual(response[1], 400)
        
        # 8 fail on invalid trade_type
        request = {
            "trade_type": "Day",
            "security_type": "Shares",
            "ticker_name": "QQQ",
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
        response = validateEditTrade(user_id,trade_id,request)
        self.assertEqual(response[0]['result'], "Trade Type must be 'Day Trade' or 'Swing Trade', Try Again")
        # 9 fail on invalid security_type
        request = {
            "trade_type": "Day Trade",
            "security_type": "Share",
            "ticker_name": "QQQ",
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
        response = validateEditTrade(user_id,trade_id,request)
        self.assertEqual(response[0]['result'], "Security Type is either 'Shares' or 'Options', Try Again")
        
        # 10 fail on trade_id doesnt exist
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
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
        response = validateEditTrade(user_id,trade_id,request)
        self.assertEqual(response[0]['result'], "trade_id: {} does not exist".format(trade_id))
        self.assertEqual(response[1], 400)
        
        
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))

        
    def test_validate_csv(self):
        # 1 good path
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_trade_history_good.csv')
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            response = validateCsv(file)
            self.assertEqual(response, True)
        # 2 bad header
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_trade_history_bad.csv')
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            response = validateCsv(file)
            self.assertEqual(response, False)
            
        
    def test_validate_update_csv(self):
        # 1 good path
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_bulk_trade_updates_good.csv')
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            response = validateUpdateCsv(file)
            self.assertEqual(response, True)
        # 2 bad header
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_bulk_trade_updates_bad.csv')
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            response = validateUpdateCsv(file)
            self.assertEqual(response, False)
    
    
    def test_validate_new_trade_from_csv(self):
        # 1 good path
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
            "trade_date": "",
            "expiry": None,
            "strike": None,
            "buy_value": "",
            "units": "",
            "pnl": "",
            "percent_wl": "",
        }
        response = validateNewTradeFromCsv(request)
        self.assertEqual(response, True)
        # 2 fail on options check
        request = {
            "trade_type": "Day Trade",
            "security_type": "Options",
            "ticker_name": "QQQ",
            "trade_date": "",
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "pnl": "",
            "percent_wl": "",
        }
        response = validateNewTradeFromCsv(request)
        self.assertEqual(response[0]['result'], "Options require Strike Price and Expiry, Try Again")
        # 3 fail on shares check
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
            "trade_date": "",
            "expiry": None,
            "strike": "400",
            "buy_value": "",
            "units": "",
            "pnl": "",
            "percent_wl": "",
        }
        response = validateNewTradeFromCsv(request)
        self.assertEqual(response[0]['result'], "Shares require no Strike Price or Expiry, Try Again")
        # 4 fail on invalid security type
        request = {
            "trade_type": "Day Trade",
            "security_type": "Share",
            "ticker_name": "QQQ",
            "trade_date": "",
            "expiry": None,
            "strike": None,
            "buy_value": "",
            "units": "",
            "pnl": "",
            "percent_wl": "",
        }
        response = validateNewTradeFromCsv(request)
        self.assertEqual(response[0]['result'], "Security Type is either Shares or Options, Try Again")
        # 5 fail on ticker name
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "",
            "trade_date": "",
            "expiry": None,
            "strike": None,
            "buy_value": "",
            "units": "",
            "pnl": "",
            "percent_wl": "",
        }
        response = validateNewTradeFromCsv(request)
        self.assertEqual(response[0]['result'], "Must Include a Valid Ticker Symbol")
        # 6 fail on trade date future
        date = (datetime.now()+timedelta(days=2)).strftime('%Y-%m-%d')
        request = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
            "trade_date": date,
            "expiry": None,
            "strike": None,
            "buy_value": "",
            "units": "",
            "pnl": "",
            "percent_wl": "",
        }
        response = validateNewTradeFromCsv(request)
        self.assertEqual(response[0]['result'], "Trade Closure Date Can't be in the Future")

    
    def test_validate_export_trades(self):
        # 1 good path
        request = {
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
                }
            ]
        }
        response = validateExportTrades(request)
        self.assertEqual(response, True)
        # 2 no exported_trades
        request = {
            "exported_trade": [
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
                }
            ]
        }
        response = validateExportTrades(request)
        self.assertEqual(response, False)
        # 3 no trades
        request = {
            "exported_trades": []
        }
        response = validateExportTrades(request)
        self.assertEqual(response, False)
        # 4 failed on expected keys
        request = {
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
                }
            ]
        }
        response = validateExportTrades(request)
        self.assertEqual(response, False)
            
        
    def test_validate_search_ticker(self):
        # 1 good path
        filter = {
            "ticker_name": "S"
        }
        response = validateSearchTicker(filter)
        self.assertEqual(response[0], True)
        self.assertEqual(response[1], "Passed")
        # 2 bad path
        filter = {
            "ticker": "S"
        }
        response = validateSearchTicker(filter)
        self.assertEqual(response[0], False)
        self.assertEqual(response[1], "Please include ticker_name only for filtering parameters")
        
    
    def test_validate_delete_trades(self):
        #setup queries
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","validatedeletetradestradevalidatorunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("validatedeletetradestradevalidatorunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"validatedeletetradestradevalidatorunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_id = response[0][0]['trade_id']
        
        # 1 good path, pass
        response = validateDeleteTrades(user_id,[trade_id])
        self.assertEqual(response, True)
        
        # 2 bad path fail on user id not matching
        response = validateDeleteTrades(0,[trade_id])
        self.assertEqual(response[0]['result'], "trade_id: {} does not belong to this user_id".format(trade_id))
        self.assertEqual(response[1], 400)
        
        # 3 bad path fail on trade not existing
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
                
        response = validateDeleteTrades(user_id,[trade_id])
        self.assertEqual(response[0]['result'], "trade_id: {} does not exist".format(trade_id))
        self.assertEqual(response[1], 400)
    
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS