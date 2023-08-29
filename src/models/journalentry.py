import utils
from datetime import date, datetime, timedelta

class Journalentry:
    
    def __init__(self,journalentryID,userID,journalentry,date):
        self.journalentryID = journalentryID
        self.userID = userID
        self.journalentry = journalentry
        self.date = date
  
    
    def getEntry(userID,date):
            
        Query = """SELECT * FROM Journalentry WHERE user_id = %s and date = %s"""
        Args = (userID,date)
        response = utils.execute_db(Query,Args)
        return response
    
    def createEntry(journalentryInfo):
            
        Query = """INSERT INTO Journalentry VALUES (null,%s,%s,%s)"""
        Args = (journalentryInfo.userID,journalentryInfo.journalentry,journalentryInfo.date)
        response = utils.execute_db(Query,Args)
        return response
    
    def updateEntry(userID,date,entry):
        
        Query = """UPDATE Journalentry SET entrytext = %s WHERE user_id = %s and date = %s"""
        Args = (entry,userID,date)
        response = utils.execute_db(Query,Args)
        return response
    
    def deleteEntry(userID, date):
        
        Query = """DELETE FROM Journalentry WHERE user_id = %s and date = %s"""
        Args = (userID,date)
        response = utils.execute_db(Query,Args)
        return response
    
    def getEntriesForMonth(userID, monthStart, monthEnd):
        
        Query = """SELECT date, entrytext FROM Journalentry WHERE user_id = %s and date >= %s and date <= %s"""
        Args = (userID,monthStart,monthEnd)
        response = utils.execute_db(Query,Args)
        return response
    
    
    
#--------Tests--------# 

#print(response)