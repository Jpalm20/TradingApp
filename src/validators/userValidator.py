import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user

def validateNewUser(request):
    response = user.User.getUserbyEmail(request['email'])
    if response[0] and 'email' in response[0][0]:
        return {
            "result": "A User with this Email Already Exist, User a Different Email"
        }, 403
    if 'password' not in request:
        return {
            "result": "Must Include a Password, Please Try Again"
        }, 403
    return True
