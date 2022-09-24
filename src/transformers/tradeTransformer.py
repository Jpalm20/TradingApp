import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import trade

def transformNewTrade(request):
    if request['security_type'] == "Shares":
        request['expiry'] = None
        request['strike'] = None
    return request

def transformEditTrade(request):
    transformedRequest = {}
    for key in request:
        if request[key] != "":
            transformedRequest[key] = request[key]
    if ('security_type' in transformedRequest) and (transformedRequest['security_type'] == "Shares"):
        transformedRequest['expiry'] = None
        transformedRequest['strike'] = None
    return transformedRequest