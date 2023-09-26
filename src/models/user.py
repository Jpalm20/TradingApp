import utils
import logging

logger = logging.getLogger(__name__)

class User:
    
    def __init__(self,userID,firstName,lastName,birthday,email,password,streetAddress,city,state,country,accountValueOptin):
        self.userID = userID
        self.firstName = firstName
        self.lastName = lastName
        self.birthday = birthday
        self.email = email
        self.password = password
        self.streetAddress = streetAddress
        self.city = city
        self.state = state
        self.country = country
        self.accountValueOptin = accountValueOptin
    
    def getUserbyID(userID):
        
        logger.info("Entering Get User by ID Model Function: " + "(user_id: {})".format(str(userID)))
        Query = """SELECT * FROM User WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User by ID Model Function: " + str(response))
        return response  
    
    def getPreferences(userID):
        
        logger.info("Entering Get User Preferences Model Function: " + "(user_id: {})".format(str(userID)))
        Query = """SELECT account_value_optin, email_optin FROM User WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User Preferences Model Function: " + str(response))
        return response  
    
    def getTotalTrades(userID,filters):
        
        logger.info("Entering Get Total User Trades Count Model Function: " + "(user_id: {}, filters: {})".format(str(userID),str(filters)))
        Query = """SELECT COUNT(*) FROM Trade WHERE user_id = %s"""
            
        if filters:
            Query += " AND "
        conditions = []
        for key, value in filters.items():
            if key == 'date_range':
                continue
            if value:
                conditions.append(f"{key}='{value}'")
        if 'date_range' in filters: 
            conditions.append(filters['date_range'])
        Query += " AND ".join(conditions)
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Total User Trades Count Model Function: " + str(response))
        return response  
    
    def getUserbyEmail(userEmail):
        
        logger.info("Entering Get User by Email Model Function: " + "(user_id: {})".format(str(userEmail)))
        Query = """SELECT * FROM User WHERE email = %s"""
        Args = (userEmail,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User by Email Model Function: " + str(response))
        return response  
    
    def getUserBySessionToken(token):
        
        logger.info("Entering Get User by Session Token Model Function: " + "(token: {})".format(str(token)))
        Query = """SELECT * from User u JOIN Session s ON s.user_id = u.user_id WHERE s.token = %s"""
        Args = (token,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User by Session Token Model Function: " + str(response))
        return response  
    
    def getUserTrades(userID):
        
        logger.info("Entering Get User Trades Model Function: " + "(user_id: {})".format(str(userID)))
        Query = """SELECT * FROM Trade WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User Trades Model Function: " + str(response))
        return response  
    
    def getUserTradesFilter(userID,filters):
        
        logger.info("Entering Get User Trades with Filters Model Function: " + "(user_id: {}, filters: {})".format(str(userID),str(filters)))
        Query = """SELECT * FROM Trade WHERE user_id = %s"""
        if filters:
            Query += " AND "
        conditions = []
        for key, value in filters.items():
            if key == 'date_range':
                continue
            if value:
                conditions.append(f"{key}='{value}'")
        if 'date_range' in filters: 
            conditions.append(filters['date_range'])
        Query += " AND ".join(conditions)
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User Trades with Filters Model Function: " + str(response))
        return response 
    
    def getUserTradesStats(userID):
        
        logger.info("Entering Get User Trades Stats Model Function: " + "(user_id: {})".format(str(userID)))
        Query = """SELECT
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s) AS numTrades,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and pnl < 0) AS numLosses,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and pnl > 0) AS numWins,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and trade_type = 'Day Trade') AS numDT,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and trade_type = 'Day Trade' and pnl > 0) AS numDTWin,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and trade_type = 'Day Trade' and pnl < 0) AS numDTLoss,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and trade_type = 'Swing Trade') AS numSwT,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and trade_type = 'Swing Trade' and pnl > 0) AS numSwTWin,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and trade_type = 'Swing Trade' and pnl < 0) AS numSwTLoss,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and security_type = 'Options') AS numOT,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and security_type = 'Options' and pnl > 0) AS numOTWin,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and security_type = 'Options' and pnl < 0) AS numOTLoss,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and security_type = 'Shares') AS numShT,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and security_type = 'Shares' and pnl > 0) AS numShTWin,
                    (SELECT COUNT(*) FROM trade WHERE user_id = %s and security_type = 'Shares' and pnl < 0) AS numShTLoss,
                    (SELECT MAX(pnl) FROM trade WHERE user_id = %s) AS largestWin,
                    (SELECT MIN(pnl) FROM trade WHERE user_id = %s) AS largestLoss,
                    (SELECT SUM(pnl) FROM trade WHERE user_id = %s and pnl > 0) AS sumWin,
                    (SELECT SUM(pnl) FROM trade WHERE user_id = %s and pnl < 0) AS sumLoss,
                    (SELECT SUM(pnl) FROM trade WHERE user_id = %s) AS totalPNL;"""
        Args = (userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User Trades Stats Model Function: " + str(response))
        return response  
    
    def getUserTradesStatsFilter(userID,filters):
        
        logger.info("Entering Get User Trades Stats with Filters Model Function: " + "(user_id: {}, filters: {})".format(str(userID),str(filters)))
        Query = "SELECT" + \
                   utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + ") AS numTrades," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and pnl < 0) AS numLosses," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and pnl > 0) AS numWins," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and trade_type = 'Day Trade') AS numDT," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and trade_type = 'Day Trade' and pnl > 0) AS numDTWin," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and trade_type = 'Day Trade' and pnl < 0) AS numDTLoss," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and trade_type = 'Swing Trade') AS numSwT," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and trade_type = 'Swing Trade' and pnl > 0) AS numSwTWin," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and trade_type = 'Swing Trade' and pnl < 0) AS numSwTLoss," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and security_type = 'Options') AS numOT," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and security_type = 'Options' and pnl > 0) AS numOTWin," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and security_type = 'Options' and pnl < 0) AS numOTLoss," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and security_type = 'Shares') AS numShT," + \
                    utils.add_filters_to_query_sring("(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and security_type = 'Shares' and pnl > 0) AS numShTWin," + \
                    utils.add_filters_to_query_sring( "(SELECT COUNT(*) FROM trade WHERE user_id = " + str(userID),filters) + " and security_type = 'Shares' and pnl < 0) AS numShTLoss," + \
                    utils.add_filters_to_query_sring( "(SELECT MAX(pnl) FROM trade WHERE user_id = " + str(userID),filters) + ") AS largestWin," + \
                    utils.add_filters_to_query_sring( "(SELECT MIN(pnl) FROM trade WHERE user_id = " + str(userID),filters) + ") AS largestLoss," + \
                    utils.add_filters_to_query_sring( "(SELECT SUM(pnl) FROM trade WHERE user_id = " + str(userID),filters) + " and pnl > 0) AS sumWin," + \
                    utils.add_filters_to_query_sring("(SELECT SUM(pnl) FROM trade WHERE user_id = " + str(userID),filters) + " and pnl < 0) AS sumLoss," + \
                    utils.add_filters_to_query_sring("(SELECT SUM(pnl) FROM trade WHERE user_id = " + str(userID),filters) + ") AS totalPNL"
        Args = ()
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User Trades Stats with Filters Model Function: " + str(response))
        return response 
    
    def getUserTradesPage(userID,limit,offset,filters):
        
        logger.info("Entering Get User Trades Page Model Function: " + "(user_id: {}, limit: {}, offset: {}, filters: {})".format(str(userID),str(limit),str(offset),str(filters)))
        Query = """SELECT * FROM Trade WHERE user_id = %s"""
        if filters:
            Query += " AND "
        conditions = []
        for key, value in filters.items():
            if key == 'date_range':
                continue
            if value:
                conditions.append(f"{key}='{value}'")
        if 'date_range' in filters: 
            conditions.append(filters['date_range'])
        Query += " AND ".join(conditions)
        Query += " LIMIT %s OFFSET %s"
        Args = (userID,limit,offset)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User Trades Page Model Function: " + str(response))
        return response 
    
    def getUserPnLbyYear(userID,year):
            
        logger.info("Entering Get User PnL by Year Model Function: " + "(user_id: {}, year: {})".format(str(userID),str(year)))
        Query = """SELECT trade_date, SUM(pnl) AS day_pnl FROM Trade WHERE user_id = %s AND YEAR(DATE(trade_date)) = %s GROUP BY trade_date ORDER BY trade_date ASC;"""
        Args = (userID,year)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User PnL by Year Model Function: " + str(response))
        return response  
    
    def getUserPnLbyYearFilter(userID,year,filters):
        
        logger.info("Entering Get User PnL by Year with Filters Model Function: " + "(user_id: {}, year: {}, filters: {})".format(str(userID),str(year),str(filters)))
        Query = """SELECT trade_date, SUM(pnl) AS day_pnl FROM Trade WHERE user_id = %s AND YEAR(DATE(trade_date)) = %s"""
        if filters:
            Query += " AND "
        conditions = []
        for key, value in filters.items():
            if value:
                conditions.append(f"{key}='{value}'")
        Query += " AND ".join(conditions)
        Query += " GROUP BY trade_date ORDER BY trade_date ASC;"
        Args = (userID,year)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get User PnL by Year with Filters Model Function: " + str(response))
        return response 
    
    def addUser(newUser):

        logger.info("Entering Add User Model Function: " + "(new_user: {})".format(str(newUser)))
        Query = """INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,DEFAULT,DEFAULT)"""
        Args = (newUser.firstName,newUser.lastName,newUser.birthday,newUser.email,
                                       newUser.password,newUser.streetAddress,newUser.city,
                                       newUser.state,newUser.country)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Add User Model Function: " + str(response))
        return response
        
    def updateUser(userID,changes):
        
        logger.info("Entering Update User Model Function: " + "(user_id: {}, changes: {})".format(str(userID),str(changes)))
        response = ""
            
        for key,value in changes.items():

            Query = """UPDATE User SET {} = %s WHERE user_id = %s""".format(key)
            Args = (value,userID)
            response = utils.execute_db(Query,Args)
        
        logger.info("Leaving Update User Model Function: " + str(response))
        return response
        
    def deleteUser(userID):
        
        logger.info("Entering Delete User Model Function: " + "(user_id: {})".format(str(userID)))
        Query = """DELETE FROM User WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete User Model Function: " + str(response))
        return response
    
    def updatePass(userID, newPass):
        
        logger.info("Entering Update Password Model Function: " + "(user_id: {}, new_pass: {})".format(str(userID),str(newPass)))
        Query = """UPDATE User SET password = %s WHERE user_id = %s"""
        Args = (newPass,userID)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Update Password Model Function: " + str(response))
        return response
    
    def accountValueFeatureOptin(userID):
        
        logger.info("Entering Acount Value Feature Optin Model Function: " + "(user_id: {})".format(str(userID)))
        Query = """UPDATE User SET account_value_optin = 1 WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Acount Value Feature Flag Model Function: " + str(response))
        return response 
    
    def toggleAccountValueFeatureOptin(userID):
        
        logger.info("Entering Toggle Acount Value Feature Flag Model Function: " + "(user_id: {})".format(str(userID)))
        Query = """UPDATE User SET account_value_optin = NOT account_value_optin WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Toggle Acount Value Feature Flag Model Function: " + str(response))
        return response 
    
    def toggleEmailOptIn(userID):
        
        logger.info("Entering Toggle Email Alerts Feature Flag Model Function: " + "(user_id: {})".format(str(userID)))
        Query = """UPDATE User SET email_optin = NOT email_optin WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Toggle Email Alerts Feature Flag Model Function: " + str(response))
        return response 
 
 
#--------Tests--------# 

#Testing addUser       
#testUser = User(None,"Jon","Palmiery","08-30-2020","palmierijon@gmail.com","password","11 Danand Lane","Patterson","NY","USA",None)
#response = User.addUser(testUser)

#Testing updateUser
#testUserID = 4;
#testUpdateUserInfo = {
#    "last_name": "Palmieri",
#    "password": "testestest20"
#}
#response = User.updateUser(testUserID,testUpdateUserInfo)

#Testing deleteUser
#testUserID = 4
#response = User.deleteUser(testUserID)

#Testing getUserbyID
#testUserID = 2
#response = User.getUser(testUserID)

#Test getUserbyEmail
#testUserEmail = "testemail@gmail.com"   
#response = User.getUserbyEmail(testUserEmail)

#Testing getUserTrades
#testUserID = 77
#response = User.getUserTrades(testUserID)

#Testing getUserTradesFilter
#testUserID = 71
#testFilters = {
#   "ticker_name": "SPY",
#   "trade_type": "Swing Trade",
#   "security_type": "Options"
#}
#response = User.getUserTradesFilter(testUserID,testFilters)

#Testing getUserTradesbyYear
#testUserID = 77
#testYear = 2022
#response = User.getUserTrades(testUserID,testYear)

#print(response)
    