import utils

class User:
    
    def __init__(self,userID,firstName,lastName,birthday,email,password,streetAddress,city,state,country):
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
    
    def getUserbyID(userID):
    
        Query = """SELECT * FROM User WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        return response  
    
    def getUserbyEmail(userEmail):
        
        Query = """SELECT * FROM User WHERE email = %s"""
        Args = (userEmail,)
        response = utils.execute_db(Query,Args)
        return response  
    
    def getUserTrades(userID):
        
        Query = """SELECT * FROM Trade WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        return response  
    
    def getUserTradesFilter(userID,filters):
        
        Query = """SELECT * FROM Trade WHERE user_id = %s"""
        if filters:
            Query += " AND "
        conditions = []
        for key, value in filters.items():
            if value:
                conditions.append(f"{key}='{value}'")
        Query += " AND ".join(conditions)
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        return response 
    
    def getUserPnLbyYear(userID,year):
            
        Query = """SELECT trade_date, SUM(pnl) AS day_pnl FROM Trade WHERE user_id = %s AND YEAR(DATE(trade_date)) = %s GROUP BY trade_date ORDER BY trade_date ASC;"""
        Args = (userID,year)
        response = utils.execute_db(Query,Args)
        return response  
    
    def addUser(newUser):

        Query = """INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        Args = (newUser.firstName,newUser.lastName,newUser.birthday,newUser.email,
                                       newUser.password,newUser.streetAddress,newUser.city,
                                       newUser.state,newUser.country)
        response = utils.execute_db(Query,Args)
        return response
        
    def updateUser(userID,changes):
        
        response = ""
            
        for key,value in changes.items():

            Query = """UPDATE User SET {} = %s WHERE user_id = %s""".format(key)
            Args = (value,userID)
            response = utils.execute_db(Query,Args)
        
        return response
        
    def deleteUser(userID):
        
        Query = """DELETE FROM User WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        return response
    
    def updatePass(userID, newPass):
        
        Query = """UPDATE User SET password = %s WHERE user_id = %s"""
        Args = (newPass,userID)
        response = utils.execute_db(Query,Args)
        return response
 
 
#--------Tests--------# 

#Testing addUser       
#testUser = User(None,"Jon","Palmiery","08-30-2020","palmierijon@gmail.com","password","11 Danand Lane","Patterson","NY","USA")
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
    