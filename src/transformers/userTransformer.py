import os
import sys
from datetime import date, datetime, timedelta
import calendar


script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user

import hashlib

JIRA_PROJECT_ID = os.environ.get('JIRA_PROJECT_ID')


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

def transformReportBug(request, email):
    issueType = ''
    if (request['requestType'] == 'Bug Report'):
        issueType = 'Bug'
    elif (request['requestType'] == 'Feature Request'):
        issueType= 'Story'
    return {
        "fields": {
            "project":
            { 
                "id": str(JIRA_PROJECT_ID)
            },
            "summary": request['page'] + " - " + request['summary'],
            "description": request['description'] + " \n\nSubmitted By: " + email,
            "issuetype": {
                "name": issueType
            }
        }
    }

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

def transformAVtf(today_date,time_frame):
    last_dates = []
    if time_frame == 'Day':
        last_dates = [datetime.strptime(today_date, '%Y-%m-%d').date() - timedelta(days=i) for i in range(6, -1, -1)]
    elif time_frame == 'Week':
        if datetime.strptime(today_date, '%Y-%m-%d').date().weekday() > 0:
            last_dates.append(datetime.strptime(today_date, '%Y-%m-%d').date())
            for i in range(6):
                num_days = datetime.strptime(today_date, '%Y-%m-%d').date().weekday() + (i * 7)
                prev_week_last_day = datetime.strptime(today_date, '%Y-%m-%d').date() - timedelta(days=num_days)
                last_dates.append(prev_week_last_day)
        else:
            for i in range(7):
                num_days = datetime.strptime(today_date, '%Y-%m-%d').date().weekday() + (i * 7)
                prev_week_last_day = datetime.strptime(today_date, '%Y-%m-%d').date() - timedelta(days=num_days)
                last_dates.append(prev_week_last_day)
        last_dates.reverse()
    elif time_frame == 'Month':
        last_dates.append(datetime.strptime(today_date, '%Y-%m-%d').date())
        for i in range(1, 7):
            year = datetime.strptime(today_date, '%Y-%m-%d').date().year
            month = datetime.strptime(today_date, '%Y-%m-%d').date().month - i
            while month <= 0:
                year -= 1
                month += 12
            day = calendar.monthrange(year, month)[1]
            last_dates.append(date(year, month, day))
        last_dates.reverse()
    elif time_frame == 'Year':
        last_dates.append(datetime.strptime(today_date, '%Y-%m-%d').date())
        for i in range(1, 7):
            year = datetime.strptime(today_date, '%Y-%m-%d').date().year - i
            last_day = date(year, 12, 31)
            last_dates.append(last_day)
        last_dates.reverse()
    return last_dates