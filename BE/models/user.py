import json

from matplotlib import ticker
import mysql.connector

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
        
    def addUser(newUser):
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='TradingApp',
                                         user='root',
                                         password='tRaDiNgApP25!')

            Query = """INSERT INTO User VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            Args = (newUser.firstName,newUser.lastName,newUser.birthday,newUser.email,
                                       newUser.password,newUser.streetAddress,newUser.city,
                                       newUser.state,newUser.country)

            cursor = connection.cursor()
            result = cursor.execute(Query,Args)
            connection.commit()
            
            print(cursor.rowcount, "User Added successfully into User table")
            response = "User Added successfully into User table"
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to Add User in MySQL: {}".format(error))
            response = "Failed to Add User in MySQL: {}".format(error)
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")
        
        return response
        
    def updateUser(userID,changes):
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='TradingApp',
                                         user='root',
                                         password='tRaDiNgApP25!')
            
            for key,value in changes.items():

                Query = """UPDATE User SET {} = %s WHERE user_id = %s""".format(key)
                Args = (value,userID)

                cursor = connection.cursor(dictionary=True)
                result = cursor.execute(Query,Args)
                connection.commit()

            print("User Updated successfully into User table")
            response = "User Updated successfully into User table"
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to Update User in MySQL: {}".format(error))
            response = "Failed to Update User in MySQL: {}".format(error)
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")
        
        return response
        
    def deleteUser(userID):
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='TradingApp',
                                         user='root',
                                         password='tRaDiNgApP25!')

            Query = """DELETE FROM User WHERE user_id = %s"""
            Args = (userID,)

            cursor = connection.cursor()
            result = cursor.execute(Query,Args)
            connection.commit()

            print("User Deleted successfully from User table")
            response = "User Deleted successfully from User table"
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to Delete User in MySQL: {}".format(error))
            response = "Failed to Delete User in MySQL: {}".format(error)
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")
        
        return response
 
#--------Tests--------# 

#Testing addUser       
#testUser = User(None,"Jon","Palmiero","08-30-2020","palmierijon@gmail.com","password","11 Danand Lane","Patterson","NY","USA")
#response = User.addUser(testUser)

#Testing updateUser
#testUserID = 3;
#testUpdateUserInfo = {
#    "birthday": "08-30-1998",
#    "password": "testestest20"
#}
#response = User.updateUser(testUserID,testUpdateUserInfo)

#Testing deleteUser
#testUserID = 3
#response = User.deleteUser(testUserID)

#print(response)
    