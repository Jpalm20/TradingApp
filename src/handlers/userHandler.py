import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user

import json
import hashlib

def registerUser(requestBody):
    newUser_info1 = json.dumps(requestBody)
    newUser_info = json.loads(newUser_info1)
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

#print(response)