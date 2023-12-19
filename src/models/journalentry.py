import models.utils as utils
from datetime import date, datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Journalentry:
    
    def __init__(self,journalentryID,userID,journalentry,date):
        self.journalentryID = journalentryID
        self.userID = userID
        self.journalentry = journalentry
        self.date = date
  
    
    def getEntry(userID,date):
            
        logger.info("Entering Get Journal Entry Model Function: " + "(user_id: {}, date: {})".format(str(userID),str(date)))
        Query = """SELECT * FROM Journalentry WHERE user_id = %s and date = %s"""
        Args = (userID,date)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Journal Entry Model Function: " + str(response))
        return response
    
    def createEntry(journalentryInfo):
            
        logger.info("Entering Create Journal Entry Model Function: " + "(journalentry_info: {})".format(str(journalentryInfo)))
        Query = """INSERT INTO Journalentry VALUES (null,%s,%s,%s)"""
        Args = (journalentryInfo.userID,journalentryInfo.journalentry,journalentryInfo.date)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Create Journal Entry Model Function: " + str(response))
        return response
    
    def updateEntry(userID,date,entry):
        
        logger.info("Entering Update Journal Entry Model Function: " + "(user_id: {}, date: {}, entry: {})".format(str(userID),str(date),str(entry)))
        Query = """UPDATE Journalentry SET entrytext = %s WHERE user_id = %s and date = %s"""
        Args = (entry,userID,date)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Update Journal Entry Model Function: " + str(response))
        return response
    
    def deleteEntry(userID, date):
        
        logger.info("Entering Delete Journal Entry Model Function: " + "(user_id: {}, date: {})".format(str(userID),str(date)))
        Query = """DELETE FROM Journalentry WHERE user_id = %s and date = %s"""
        Args = (userID,date)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Delete Journal Entry Model Function: " + str(response))
        return response
    
    def getEntriesForMonth(userID, monthStart, monthEnd):
        
        logger.info("Entering Get Entries for Month Model Function: " + "(user_id: {}, month_start: {}, month_end: {})".format(str(userID),str(monthStart),str(monthEnd)))
        Query = """SELECT date, entrytext FROM Journalentry WHERE user_id = %s and date >= %s and date <= %s"""
        Args = (userID,monthStart,monthEnd)
        response = utils.execute_db(Query,Args)
        logger.info("Leaving Get Entries for Month Model Function: " + str(response))
        return response
    
    
    
#--------Tests--------# 

#print(response)