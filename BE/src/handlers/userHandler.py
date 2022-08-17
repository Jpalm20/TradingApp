import sys
sys.path.append("/Users/jp/Documents/TradingApp/TradingApp/BE/models")
import user

import json
import hashlib

def registerUser(response):
    newUser_info = json.loads(response)
    if 'password' in newUser_info:
        hashPass = hashlib.sha256(newUser_info['password'].encode()).hexdigest()
    newUser = user.User(None,newUser_info['first_name'],newUser_info['last_name'],newUser_info['birthday'],
                        newUser_info['email'],hashPass,newUser_info['street_address'],
                        newUser_info['city'],newUser_info['state'],newUser_info['country'])
    response = user.User.addUser(newUser)
    return response

def changePassword(response):
    #
    response = user.User.updateUser(userID,changes)
    return response

#--------Tests--------# 

#Testing registerUser()
#testUserDict = {
#    "first_name": "Stevie",
#    "last_name": "Wonder",
#    "birthday": "12-31-2014",
#    "email": "jpballer20@gmail.com",
#    "password": "testpassword",
#    "street_address": "25 Lenox Hill Rd",
#    "city": "Brewster",
#    "state": "MD",
#    "country": "US",
#}
#testUserJSON = json.dumps(testUserDict)
#response = registerUser(testUserJSON)

#Testing changePassword()