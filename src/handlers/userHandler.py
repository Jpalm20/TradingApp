import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user

import json
import hashlib

def registerUser(requestBody):
    if 'password' in requestBody:
        hashPass = hashlib.sha256(requestBody['password'].encode()).hexdigest()
    newUser = user.User(None,requestBody['first_name'],requestBody['last_name'],requestBody['birthday'],
                        requestBody['email'],hashPass,requestBody['street_address'],
                        requestBody['city'],requestBody['state'],requestBody['country'])
    response = user.User.addUser(newUser)
    if response:
        return response
    else:
        return "Successfully Registered " + newUser.firstName

def changePassword(requestBody):
    response = user.User.updateUser(userID,changes)
    return response

def validateUser(requestBody):
    response = user.User.getUserbyEmail(requestBody['email'])
    if 'password' in response[0]:
        hashPass = hashlib.sha256(requestBody['password'].encode()).hexdigest()
        if response[0]['password'] == hashPass:
            return "User " + str(response[0]['user_id']) + " Found, Logging In"
        else:
            return "Incorrect Password, Try Again"
    else:
        return "No User Found with these Credentials, Please Try Again"

#--------Tests--------# 

#Testing registerUser()
testUserDict = {
    "first_name": "Stevie",
    "last_name": "Wonder",
    "birthday": "12-31-2014",
    "email": "jpballer20@gmail.com",
    "password": "testpassword",
    "street_address": "25 Lenox Hill Rd",
    "city": "Brewster",
    "state": "MD",
    "country": "US",
}
#testUserJSON = json.dumps(testUserDict)
response = registerUser(testUserDict)

#Testing changePassword()

#Testing validateUser()
#testUserDict = {
#    "email": "testemail@gmail.com",
#    "password": "testpassword",
#}
#testUserJSON = json.dumps(testUserDict)
#response = validateUser(testUserDict)

print(response)