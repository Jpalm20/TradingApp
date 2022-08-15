import json

from matplotlib import ticker
import utils

from sympy import sec

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
    
    def getUser(userID):
    
        Query = """SELECT * FROM User WHERE user_id = %s"""
        Args = (userID,)
        response = utils.execute_db(Query,Args)
        return response  
    
    def getUserTrades(userID):
        
        Query = """SELECT * FROM Trade WHERE user_id = %s"""
        Args = (userID,)
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

#Testing getUser
#testUserID = 2
#response = User.getUser(testUserID)

#Testing getUserTrades
#testUserID = 1
#response = User.getUserTrades(testUserID)

#print(response)
    