import unittest
from src.models.trade import *
from src.models.utils import execute_db

class TestTrade(unittest.TestCase):
    
    #def setUp(self):
        #self.transaction = start_new_transaction()
        #THIS SHOULD BE CREATING THE USER OBJECT
        
    def test_get_trade(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","gettradeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("gettradeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"gettradeunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("gettradeunittest",))
        self.assertEqual(response[0][0]['comments'], "gettradeunittest")
        trade_id = response[0][0]['trade_id']
        response = Trade.getTrade(trade_id)
        self.assertEqual(response[0][0]['comments'], "gettradeunittest")
        response = execute_db("DELETE FROM trade WHERE trade_id = %s", (trade_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("gettradeunittest@gmail.com",))

        
    def test_add_trade(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","addtradeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("addtradeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        testTrade = Trade(None,user_id,"Swing Trade","Options","TSLA","12-12-2022","9-21-2023",1000,500,5,"3:1",2532.52,254.3,"addtradeunittest")
        response = Trade.addTrade(testTrade)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("addtradeunittest",))
        self.assertEqual(response[0][0]['comments'], "addtradeunittest")
        trade_id = response[0][0]['trade_id']
        response = execute_db("DELETE FROM trade WHERE trade_id = %s", (trade_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("addtradeunittest@gmail.com",))

    
    def test_add_trades(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","addtradesunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("addtradesunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        trades = [
            {
                "buy_value" : 100,
                "comments" : "addtradesunittest",
                "expiry" : "2023-01-01",
                "percent_wl" : 10.5,
                "pnl" : 10.5,
                "rr" : None,
                "security_type" : "Options",
                "strike" : 100,
                "ticker_name" : "SPY",
                "trade_date" : "2023-01-01",
                "trade_type" : "Day Trade",
                "units" : 1,
                "user_id" : user_id
            },
            {
                "buy_value" : 100,
                "comments" : "addtradesunittest",
                "expiry" : "2023-01-01",
                "percent_wl" : 10.5,
                "pnl" : 21,
                "rr" : None,
                "security_type" : "Options",
                "strike" : 100,
                "ticker_name" : "QQQ",
                "trade_date" : "2023-01-01",
                "trade_type" : "Day Trade",
                "units" : 2,
                "user_id" : user_id
            }
        ]
        response = Trade.addTrades(trades)
        self.assertEqual(response[0], True)
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("addtradesunittest",))
        self.assertEqual(len(response[0]), 2)
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("addtradesunittest@gmail.com",))


    def test_update_trade(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","updatetradeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("updatetradeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"updatetradeunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("updatetradeunittest",))
        self.assertEqual(response[0][0]['ticker_name'], "SPY")
        trade_id = response[0][0]['trade_id']
        changes = {
            "ticker_name": "QQQ",
            "pnl": "NULL"
        }
        response = Trade.updateTrade(trade_id,changes)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("updatetradeunittest",))
        self.assertEqual(response[0][0]['ticker_name'], "QQQ")
        self.assertEqual(response[0][0]['pnl'], None)
        response = execute_db("DELETE FROM trade WHERE trade_id = %s", (trade_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("updatetradeunittest@gmail.com",))


    def test_delete_trade(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deletetradeunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deletetradeunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"deletetradeunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("deletetradeunittest",))
        self.assertEqual(response[0][0]['ticker_name'], "SPY")
        trade_id = response[0][0]['trade_id']
        response = Trade.deleteTrade(trade_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("deletetradeunittest",))
        self.assertEqual(response[0], [])
        response = execute_db("DELETE FROM user WHERE email = %s", ("deletetradeunittest@gmail.com",))


    def test_delete_trades_by_id(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deletetradesbyidunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deletetradesbyidunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"deletetradesbyidunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","QQQ","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"deletetradesbyidunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","AMD","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"deletetradesbyidunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT trade_id FROM trade WHERE comments = %s", ("deletetradesbyidunittest",))
        self.assertEqual(len(response[0]), 3)
        trade_ids = [d['trade_id'] for d in response[0]]
        response = Trade.deleteTradesByID(trade_ids)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("deletetradesbyidunittest",))
        self.assertEqual(response[0], [])
        response = execute_db("DELETE FROM user WHERE email = %s", ("deletetradesbyidunittest@gmail.com",))
    
    
    def test_delete_user_trades(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","deleteusertradesunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("deleteusertradesunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"deleteusertradesunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","QQQ","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"deleteusertradesunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","AMD","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"deleteusertradesunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT trade_id FROM trade WHERE comments = %s", ("deleteusertradesunittest",))
        self.assertEqual(len(response[0]), 3)
        response = Trade.deleteUserTrades(user_id)
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM trade WHERE comments = %s", ("deleteusertradesunittest",))
        self.assertEqual(response[0], [])
        response = execute_db("DELETE FROM user WHERE email = %s", ("deleteusertradesunittest@gmail.com",))
    
    
    def test_get_user_ticker(self):
        
        ## Need all logic paths tested
        ## 1. Good Path
        ## 2. DB Level Failures
        response = execute_db("INSERT INTO user VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT,DEFAULT)",("Jon","Palmieri","08-30-2020","getusertickerunittest@gmail.com","password","11 Danand Lane","Patterson","NY","USA"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT * FROM user WHERE email = %s", ("getusertickerunittest@gmail.com",))
        user_id = response[0][0]['user_id']
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SPY","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertickerunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","QQQ","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertickerunittest"))
        response = execute_db("INSERT INTO trade VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id,"Day Trade","Options","SOS","2023-01-01","2023-01-01",410,400,1,"1:3",100,25,"getusertickerunittest"))
        self.assertEqual(response[0], [])
        response = execute_db("SELECT trade_id FROM trade WHERE comments = %s", ("getusertickerunittest",))
        self.assertEqual(len(response[0]), 3)
        response = Trade.getUserTicker(user_id)
        self.assertEqual(len(response[0]), 3)
        response = Trade.getUserTicker(user_id,"S")
        self.assertEqual(len(response[0]), 2)
        response = Trade.getUserTicker(user_id,"SP")
        self.assertEqual(len(response[0]), 1)
        response = execute_db("DELETE FROM trade WHERE user_id = %s", (user_id,))
        response = execute_db("DELETE FROM user WHERE email = %s", ("getusertickerunittest@gmail.com",))
    
    
    #def tearDown(self):
        #self.transaction.rollback()
        #THIS SHOULD BE DELETING THE USER SO IT ALWAYS HAPPENS
        
