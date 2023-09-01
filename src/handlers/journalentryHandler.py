import os
import sys
from datetime import date, datetime, timedelta
import json

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import journalentry

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'validators',)
sys.path.append( mymodule_dir )
import journalentryValidator


def getJournalEntries(user_id, date):
    response = journalentryValidator.validateDate(date)
    if response != True:
        return response
    date_object = datetime.strptime(date, '%Y-%m-%d')
    first_day = date_object.replace(day=1)
    next_month = first_day.replace(month=first_day.month + 1)
    last_day = next_month - timedelta(days=1)
    response = journalentry.Journalentry.getEntriesForMonth(user_id, first_day, last_day)
    if len(response[0]) != 0 and "date" in response[0][0]:
        entries = [{'date': entry['date'].strftime('%Y-%m-%d'), 'entrytext': entry['entrytext']} for entry in response[0]]
        return {
            "entries": entries
        }
    else:
        return {
            "entries": []
        }
    
def postJournalEntry(user_id, date, requestBody):
    response = journalentryValidator.validateDate(date)
    if response != True:
        return response
    response = journalentry.Journalentry.getEntry(user_id, date)
    if len(response[0]) != 0 and "journalentry_id" in response[0][0]:
        response = journalentry.Journalentry.updateEntry(user_id, date, requestBody['entry'])
        if response[0]:
            return {
                "result": response
            }, 400
        else:
            return {
                "date": date,
                "entry": requestBody['entry'],
                "result": "Journal Entry Successfully Updated"
            }
    else:
        newJournalEntry = journalentry.Journalentry(None,user_id,requestBody['entry'],date)
        response = journalentry.Journalentry.createEntry(newJournalEntry)
        if response[0]:
            return {
                "result": response
            }, 400
        else:
            return {
                "date": date,
                "entry": requestBody['entry'],
                "result": "Journal Entry Successfully Saved"
            }
    
        
def deleteJournalEntry(user_id, date):
    response = journalentryValidator.validateDate(date)
    if response != True:
        return response
    response = journalentry.Journalentry.getEntry(user_id, date)
    if len(response[0]) != 0 and "journalentry_id" in response[0][0]:
        response = journalentry.Journalentry.deleteEntry(user_id, date)
        if response[0]:
            return {
                "result": response
            }, 400
        else:
            return {
                "result": "Journal Entry Successfully Deleted"
            }
    else:
        return {
            "result": "Error: Journal Entry Does Not Exist for Given User and Date Combination"
        }, 400
    
