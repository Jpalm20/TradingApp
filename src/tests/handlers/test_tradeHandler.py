import unittest
from handlers.tradeHandler import *
from models.utils import execute_db
from datetime import datetime, date, timedelta


class TestTradeHandler(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
    
    def test_log_trade(self):
        # setup queries
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","logtradetradehandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("logtradetradehandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 fail on validation
        requestBody = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_names": "QQQ",
            "trade_date": "",
            "expiry": "",
            "strike": "",
            "buy_value": "250",
            "units": "3",
            "rr": "1:3",
            "pnl": "",
            "percent_wl": "3.07",
            "comments": ""
        }
        
        response = logTrade(user_id,requestBody)
        self.assertEqual(response[0]['result'], "Must Include a Valid Ticker Symbol")
        
        # 2 fail on addTrade to DB (TODO)
        
        # 3 good path with account value logic
        requestBody = {
            "trade_type": "Day Trade",
            "security_type": "Shares",
            "ticker_name": "QQQ",
            "trade_date": "2023-01-01",
            "expiry": "",
            "strike": "",
            "buy_value": "250",
            "units": "3",
            "rr": "1:3",
            "pnl": "250",
            "percent_wl": "3.07",
            "comments": ""
        }
        
        response = logTrade(user_id,requestBody)
        self.assertEqual(response['user_id'], user_id)
        
        # 4 fail on insertFutureDay (TODO)
        
        # 5 fail on handleAddTrade (TODO)
        
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    
    def test_get_existing_trade(self):
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getexistingtradetradehandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getexistingtradetradehandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getexistingtradetradehandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_id = response[0][0]['trade_id']
        
        # 1 good path return trade
        response = getExistingTrade(trade_id)
        self.assertEqual(len(response), 14)
        self.assertEqual(response['trade_id'], trade_id)
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        
        # 2 fail
        response = getExistingTrade(trade_id)
        self.assertEqual(response[1], 400)

        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))


    def test_search_user_ticker(self):
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","searchusertickertradehandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("searchusertickertradehandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"searchusertickertradehandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","QQQ","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"searchusertickertradehandlerunittest"))
        self.assertEqual(response[0], [])

        
        # 1 good path no filter
        response = searchUserTicker(user_id)
        self.assertEqual(len(response['tickers']), 2)
        self.assertEqual(response['tickers'][0]['ticker_name'], "SPY")
        
        # 2 good path filter
        filter = {
            "ticker_name": "S"
        }
        response = searchUserTicker(user_id)
        self.assertEqual(len(response), 1)
        self.assertEqual(response['tickers'][0]['ticker_name'], "SPY")
        
        # 3 fail no tickers or filters
        esponse = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = searchUserTicker(user_id)
        self.assertEqual(response['tickers'], [])
        
        # 4 fail on filter validation
        filter = {
            "ticker": "SPY"
        }
        response = searchUserTicker(user_id,filter)
        self.assertEqual(response[1], 400)
        self.assertEqual(response[0]['result'], "Please include ticker_name only for filtering parameters")
        
        # 5 fail on bad query
        #response = searchUserTicker("datetime.now()")
        #print(response)
        #self.assertEqual(response[1], 400)

        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))


    def test_edit_existing_trade(self):
        # setup queries
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","editexistingtradetradehandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("editexistingtradetradehandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"editexistingtradetradehandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_id = response[0][0]['trade_id']
        
        # 1 fail on validation
        requestBody = {
            "trade_type": "",
            "security_type": "Shares",
            "ticker_name": "",
            "trade_date": "",
            "expiry": "2023-02-02",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        
        response = editExistingTrade(user_id,trade_id,requestBody)
        self.assertEqual(response[0]['result'], "Shares require no Strike Price or Expiry, Try Again")
        
        # 2 good path not updating any account value logic
        requestBody = {
            "trade_type": "",
            "security_type": "",
            "ticker_name": "AMD",
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
        
        response = editExistingTrade(user_id,trade_id,requestBody)
        self.assertEqual(response['trade_id'], trade_id)
        self.assertEqual(response['ticker_name'], "AMD")
        
        # 3a good path updating pnl - pnl already exists, need to take difference and add it amonstg the days
        requestBody = {
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
        
        response = editExistingTrade(user_id,trade_id,requestBody)
        self.assertEqual(response['trade_id'], trade_id)
        self.assertEqual(response['pnl'], 50.0)
        
        # 3b fail updating pnl - pnl already exists, need to take difference and add it amonstg the days, fail on handlePnlUpdate (TODO)

        # 4a good path updating pnl - pnl was null originally, need to set value to full pnl not different from adding trade
        response = execute_db("DELETE FROM trade WHERE trade_id = %s", (trade_id,))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",None,None,"editexistingtradetradehandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_id = response[0][0]['trade_id']
        
        requestBody = {
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
        
        response = editExistingTrade(user_id,trade_id,requestBody)
        self.assertEqual(response['trade_id'], trade_id)
        self.assertEqual(response['pnl'], 50.0)
        
        # 4b fail updating pnl - pnl was null originally, need to set value to full pnl not different from adding trade, fail on insertFutureDay (TODO)
        
        # 4c fail updating pnl - pnl was null originally, need to set value to full pnl not different from adding trade, fail on handleAddTrade (TODO)
        
        # 5a good path updating trade date - trade_date already exists, need to add to extra days or subtract from days dependng on if updated date is further back or closer to today, handleDateUpdateAdd
        requestBody = {
            "trade_type": "",
            "security_type": "",
            "ticker_name": "",
            "trade_date": "2023-02-01",
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        
        response = editExistingTrade(user_id,trade_id,requestBody)
        self.assertEqual(response['trade_id'], trade_id)
        self.assertEqual(response['trade_date'], "2023-02-01")
        
        # 5b good path updating trade date - trade_date already exists, need to add to extra days or subtract from days dependng on if updated date is further back or closer to today, handleDateUpdateSub
        requestBody = {
            "trade_type": "",
            "security_type": "",
            "ticker_name": "",
            "trade_date": "2022-12-01",
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        
        response = editExistingTrade(user_id,trade_id,requestBody)
        self.assertEqual(response['trade_id'], trade_id)
        self.assertEqual(response['trade_date'], "2022-12-01")
        
        # 5c fail updating trade date - trade_date already exists, need to add to extra days or subtract from days dependng on if updated date is further back or closer to today, fail on insertFutureDay (TODO)
                
        # 5d fail updating trade date - trade_date already exists, need to add to extra days or subtract from days dependng on if updated date is further back or closer to today, fail on handleDateUpdateAdd (TODO)

        # 5e fail updating trade date - trade_date already exists, need to add to extra days or subtract from days dependng on if updated date is further back or closer to today, fail on handleDateUpdateSub (TODO)

        # 6a good path updating trade date - trade_date was null originally, need to set all days with pnl fully as normal
        response = execute_db("DELETE FROM trade WHERE trade_id = %s", (trade_id,))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY",None,"2023-01-01",410,400,1,"1:3",100,25,"editexistingtradetradehandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_id = response[0][0]['trade_id']
        
        requestBody = {
            "trade_type": "",
            "security_type": "",
            "ticker_name": "",
            "trade_date": "2023-01-01",
            "expiry": "",
            "strike": "",
            "buy_value": "",
            "units": "",
            "rr": "",
            "pnl": "",
            "percent_wl": "",
            "comments": ""
        }
        
        response = editExistingTrade(user_id,trade_id,requestBody)
        self.assertEqual(response['trade_id'], trade_id)
        self.assertEqual(response['trade_date'], "2023-01-01")
        # 6b fail updating trade date - trade_date was null originally, need to set all days with pnl fully as normal, fail on insertFutureDay (TODO)

        # 6c fail updating trade date - trade_date was null originally, need to set all days with pnl fully as normal, fail on handleAddTrade (TODO)
        
        # 7 fail on not found trade_id, fail on validator pt 2(doesnt exist)
        response = execute_db("DELETE FROM trade WHERE trade_id = %s", (trade_id,))
        requestBody = {
            "trade_type": "",
            "security_type": "",
            "ticker_name": "AMD",
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
        response = editExistingTrade(user_id,trade_id,requestBody)
        self.assertEqual(response[0]['result'], "trade_id: {} does not exist".format(trade_id))
        
        
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        
        
    def test_delete_existing_trade(self):
        # setup queries
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteexistingtradetradehandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteexistingtradetradehandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"deleteexistingtradetradehandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_id = response[0][0]['trade_id']
                
        # 1 good path updating account value
        response = deleteExistingTrade(user_id,trade_id)
        self.assertEqual(response['result'], "Trade Successfully Deleted")
        self.assertEqual(response['user_id'], user_id)
        
        # 2 good path not updating account value
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Shares","SPY","","",410,400,1,"1:3",100,25,"deleteexistingtradetradehandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_id = response[0][0]['trade_id']
        
        response = deleteExistingTrade(user_id,trade_id)
        self.assertEqual(response['result'], "Trade Successfully Deleted")
        self.assertEqual(response['user_id'], user_id)
        
        # 3 fail on validation (Does Not Exist Yet)
        response = deleteExistingTrade(user_id,trade_id)
        self.assertEqual(response[0]['result'], "trade_id: {} does not exist".format(trade_id))

        # 4 fail on handleDeleteTrade (TODO)
        
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))

        
        
    def test_delete_trades(self):
        # setup queries
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteexistingtradestradehandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteexistingtradestradehandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"deleteexistingtradestradehandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Shares","SPY","","",410,400,1,"1:3",100,25,"deleteexistingtradestradehandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_ids = [trade['trade_id'] for trade in response[0]]
        
        
        # 1 good path deleting > 1 trade
        response = deleteTrades(user_id,trade_ids)
        self.assertEqual(response['result'], "Trades Successfully Deleted")
        self.assertEqual(response['user_id'], user_id)

        # 2 good path deleteing 1 trade
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Shares","SPY","","",410,400,1,"1:3",100,25,"deleteexistingtradestradehandlerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE user_id = %s", (user_id,))
        trade_ids = [trade['trade_id'] for trade in response[0]]
        
        response = deleteTrades(user_id,trade_ids)
        self.assertEqual(response['result'], "Trade Successfully Deleted")
        self.assertEqual(response['user_id'], user_id)
        
        # 3 fail on validation (Does Not Exist Yet)
        response = deleteTrades(user_id,trade_ids)
        self.assertEqual(response[0]['result'], "trade_id: {} does not exist".format(trade_ids[0]))

        # 4 fail on deleteTradesByID (TODO)
        
        # 5 fail on handleDeleteTrade (TODO)
        
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
    
    def test_import_csv(self):
        # setup queries
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","importcsvtradehandlerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("importcsvtradehandlerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        
        # 1 fail on validation
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_trade_history_bad.csv')
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            response = importCsv(file,user_id)
            self.assertEqual(response[0]['result'], "Invalid CSV file. Missing required Headers or Empty CSV")
        
        # 2 fail during csv processing processCsv
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_trade_history_bad_2.csv')
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            response = importCsv(file,user_id)
            self.assertEqual(response[0]['result'], "No shares remaining for SPY but reporting another SELL Order")
            
        # 3 fail on number of valid trades to add is 0
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_trade_history_bad_3.csv')
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            response = importCsv(file,user_id)
            self.assertEqual(response[0]['result'], "No contracts remaining for QQQ 15-Dec-22 290 PUT but reporting another SELL Order")
            
        # 4 good path adding trades from csv addTrades
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_trade_history_good.csv')
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            response = importCsv(file,user_id)
            self.assertEqual(response['result'], "Trades Imported Successfully")
        
        # 5 fail on addTrades (TODO)
                
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM accountvalue WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        
    
    def test_export_csv(self):
        requestBody = {
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
                }
            ]
        }
        
        # 1 fail on validation
        response = exportCsv(requestBody)
        self.assertEqual(response[0]['result'], "Error Generating CSV")
        
        # 2 good path exporting csv file/object
        requestBody = {
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
                }
            ]
        }
        
        # For some reason you need application context to run make_response function in exportCsv handler, so will come back to this
        #response = exportCsv(requestBody)
        #print(response)
        #self.assertNotEqual(response[0]['result'], "Error Generating CSV")
        
    
        
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS