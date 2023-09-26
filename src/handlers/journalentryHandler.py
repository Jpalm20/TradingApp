import os
import sys
from datetime import date, datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import journalentry

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'validators',)
sys.path.append( mymodule_dir )
import journalentryValidator


def getJournalEntries(user_id, date):
    logger.info("Entering Get Journal Entries Handler: " + "(user_id: {}, date: {})".format(str(user_id), str(date)))
    response = journalentryValidator.validateDate(date)
    if response != True:
        logger.warning("Leaving Get Journal Entries Handler: " + str(response))
        return response
    date_object = datetime.strptime(date, '%Y-%m-%d')
    first_day = date_object.replace(day=1)
    next_month = first_day.replace(month=first_day.month + 1)
    last_day = next_month - timedelta(days=1)
    response = journalentry.Journalentry.getEntriesForMonth(user_id, first_day, last_day)
    if len(response[0]) != 0 and "date" in response[0][0]:
        entries = [{'date': entry['date'].strftime('%Y-%m-%d'), 'entrytext': entry['entrytext']} for entry in response[0]]
        logger.info("Leaving Get Journal Entries Handler: " + str(entries))
        return {
            "entries": entries
        }
    else:
        logger.info("Leaving Get Journal Entries Handler: []")
        return {
            "entries": []
        }
    
def postJournalEntry(user_id, date, requestBody):
    logger.info("Entering Post Journal Entry Handler: " + "(user_id: {}, date: {}, request: {})".format(str(user_id), str(date), str(requestBody)))
    response = journalentryValidator.validateDate(date)
    if response != True:
        logger.warning("Leaving Post Journal Entry Handler: " + str(response))
        return response
    response = journalentry.Journalentry.getEntry(user_id, date)
    if len(response[0]) != 0 and "journalentry_id" in response[0][0]:
        response = journalentry.Journalentry.updateEntry(user_id, date, requestBody['entry'])
        if response[0]:
            logger.warning("Leaving Post Journal Entry Handler: " + str(response))
            return {
                "result": response
            }, 400
        else:
            response = {
                "date": date,
                "entry": requestBody['entry'],
                "result": "Journal Entry Successfully Updated"
            }
            logger.info("Leaving Post Journal Entry Handler: " + str(response))
            return response
    else:
        newJournalEntry = journalentry.Journalentry(None,user_id,requestBody['entry'],date)
        response = journalentry.Journalentry.createEntry(newJournalEntry)
        if response[0]:
            logger.warning("Leaving Post Journal Entry Handler: " + str(response))
            return {
                "result": response
            }, 400
        else:
            response = {
                "date": date,
                "entry": requestBody['entry'],
                "result": "Journal Entry Successfully Saved"
            }
            logger.info("Leaving Post Journal Entry Handler: " + str(response))
            return response
    
        
def deleteJournalEntry(user_id, date):
    logger.info("Entering Delete Journal Entry Handler: " + "(user_id: {}, date: {})".format(str(user_id), str(date)))
    response = journalentryValidator.validateDate(date)
    if response != True:
        logger.warning("Leaving Delete Journal Entry Handler: " + str(response))
        return response
    response = journalentry.Journalentry.getEntry(user_id, date)
    if len(response[0]) != 0 and "journalentry_id" in response[0][0]:
        response = journalentry.Journalentry.deleteEntry(user_id, date)
        if response[0]:
            logger.warning("Leaving Delete Journal Entry Handler: " + str(response))
            return {
                "result": response
            }, 400
        else:
            response = "Journal Entry Successfully Deleted"
            logger.info("Leaving Delete Journal Entry Handler: " + response)
            return {
                "result": response
            }
    else:
        response = "Error: Journal Entry Does Not Exist for Given User and Date Combination"
        logger.warning("Leaving Delete Journal Entry Handler: " + response)
        return {
            "result": response
        }, 400
    
