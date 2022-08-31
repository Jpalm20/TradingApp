import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user

import hashlib

def transformNewUser(request):
    hashPass = hashPassword(request['password'])
    return hashPass

def hashPassword(password):
    hashPass = hashlib.sha256(password.encode()).hexdigest()
    return hashPass