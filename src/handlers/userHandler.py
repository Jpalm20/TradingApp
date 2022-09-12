import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'validators',)
sys.path.append( mymodule_dir )
import userValidator

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'transformers',)
sys.path.append( mymodule_dir )
import userTransformer

import hashlib

def registerUser(requestBody):
    response = userValidator.validateNewUser(requestBody)
    if response != True:
        return response
    requestTransformed = userTransformer.transformNewUser(requestBody)
    newUser = user.User(None,requestTransformed['first_name'],requestTransformed['last_name'],requestTransformed['birthday'],
                        requestTransformed['email'],requestTransformed['password'],requestTransformed['street_address'],
                        requestTransformed['city'],requestTransformed['state'],requestTransformed['country'])
    response = user.User.addUser(newUser)
    if response[0]:
        return response, 400
    else:
        return {
            "user_id": response[1],
            "first_name": newUser.firstName,
            "last_name": newUser.lastName,
            "birthday": newUser.birthday,
            "email": newUser.email,
            "street_address": newUser.streetAddress,
            "city": newUser.city,
            "state": newUser.state,
            "country": newUser.country
        }

def validateUser(requestBody):
    response = user.User.getUserbyEmail(requestBody['email'])
    if 'password' in response[0][0]:
        hashPass = userTransformer.hashPassword(requestBody['password'])
        if response[0][0]['password'] == hashPass:
            return {
                "user_id": response[0][0]['user_id'],
                "first_name": response[0][0]['first_name'],
                "last_name": response[0][0]['last_name'],
                "birthday": response[0][0]['birthday'],
                "email": response[0][0]['email'],
                "street_address": response[0][0]['street_address'],
                "city": response[0][0]['city'],
                "state": response[0][0]['state'],
                "country": response[0][0]['country']
            }
        else:
            return {
                "result": "Incorrect Password, Please Try Again"
            }, 403
    else:
        return {
            "result": "No User Found with these Credentials, Please Try Again"
        }, 403
        
def getExistingUser(user_id):
    response = user.User.getUserbyID(user_id)
    if 'user_id' in response[0][0]:
        return {
            "user_id": response[0][0]['user_id'],
            "first_name": response[0][0]['first_name'],
            "last_name": response[0][0]['last_name'],
            "birthday": response[0][0]['birthday'],
            "email": response[0][0]['email'],
            "street_address": response[0][0]['street_address'],
            "city": response[0][0]['city'],
            "state": response[0][0]['state'],
            "country": response[0][0]['country']
        }
    else:
        return response, 400

def editExistingUser(user_id,requestBody):
    response = user.User.updateUser(user_id,requestBody)
    response = user.User.getUserbyID(user_id)
    if 'user_id' in response[0][0]:
        return {
            "user_id": response[0][0]['user_id'],
            "first_name": response[0][0]['first_name'],
            "last_name": response[0][0]['last_name'],
            "birthday": response[0][0]['birthday'],
            "email": response[0][0]['email'],
            "street_address": response[0][0]['street_address'],
            "city": response[0][0]['city'],
            "state": response[0][0]['state'],
            "country": response[0][0]['country']
        }
    else:
        return response, 400

def deleteExistingUser(user_id):
    response = user.User.deleteUser(user_id)
    if response[0]:
        return response, 400
    else:
        return {
            "result": "User " + str(user_id) + " Successfully Deleted"
        }

def getUserTrades(user_id):
    response = user.User.getUserTrades(user_id)
    if "trade_id" in response[0][0]:
        return {
            "trades": response[0]
        }
    else:
        return response, 400
        

#--------Tests--------# 

#Testing registerUser()
#testUserDict = {
#    "first_name": "Stevie",
#    "last_name": "Wonder",
#    "birthday": "12-31-2014",
#    "email": "xxxxxx@gmail.com",
#    "password": "testpassword",
#    "street_address": "25 Lenox Hill Rd",
#    "city": "Brewster",
#    "state": "MD",
#    "country": "US",
#}
#response = registerUser(testUserDict)

#Testing validateUser()
#testUserDict = {
#    "email": "xxxxxx@gmail.com",
#    "password": "testpassword",
#}
#response = validateUser(testUserDict)

#Testing getExistingUser()
#response = getExistingUser(1)

#Testing editExistingUser()
#testChanges = {
#    "first_name": "Jonathan",
#    "last_name": "Palmieri"
#}
#response = editExistingUser(62,testChanges)

#Testing deleteExistingUser()
#response = deleteExistingUser(62)

#Testing getUserTrades()
#response = getUserTrades(1)

#print(response)