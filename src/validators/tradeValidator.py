import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import trade

def validateNewTrade(request):
    if (request['security_type'] == "Options") and ('expiry' not in request or 'strike' not in request or request['expiry'] == "" or request['strike'] == "" ):
        return {
            "result": "Options require Strike Price and Expiry, Try Again"
        }, 400
    elif (request['security_type'] == "Shares") and (('expiry' in request and request['expiry'] != "") or ('strike' in request and request['strike'] != "")):
        return {
            "result": "Shares require no Strike Price or Expiry, Try Again"
        }, 400
    elif (request['security_type'] != "Shares" and request['security_type'] != "Options"):
        return {
            "result": "Security Type is either Shares or Options, Try Again"
        }, 400
    
    #need to validate blanks as well, might be easier to set required fields on FE if possible
    
    return True

def validateEditTrade(request):
    if (request['security_type'] == "Options") and ('expiry' not in request or 'strike' not in request or request['expiry'] == "" or request['strike'] == "" ):
        return {
            "result": "Options require Strike Price and Expiry, Try Again"
        }, 400
    elif (request['security_type'] == "Shares") and (('expiry' in request and request['expiry'] != "") or ('strike' in request and request['strike'] != "")):
        return {
            "result": "Shares require no Strike Price or Expiry, Try Again"
        }, 400
    return True
