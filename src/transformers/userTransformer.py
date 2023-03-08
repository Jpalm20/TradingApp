import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user

import hashlib

def transformNewUser(request):
    hashPass = hashPassword(request['password'])
    request['password'] = hashPass
    return request

def hashPassword(password):
    hashPass = hashlib.sha256(password.encode()).hexdigest()
    return hashPass

def transformEditUser(request):
    transformedRequest = {}
    for key in request:
        if request[key] != "":
            transformedRequest[key] = request[key]
    return transformedRequest

def transformDateRange(date_range):
    query = "trade_date >= "
    if date_range == "Year":
        query += "DATE_ADD(NOW(), INTERVAL -1 YEAR)"
    elif date_range == "Month":
        query += "DATE_ADD(NOW(), INTERVAL -1 MONTH)"
    elif date_range == "Week":
        query += "DATE_ADD(NOW(), INTERVAL -1 WEEK)"
    elif date_range == "Day":
        query += "DATE_ADD(NOW(), INTERVAL -1 DAY)"
    return query