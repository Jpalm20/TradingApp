import os
import sys
from datetime import date, datetime, timedelta
import calendar
import logging

logger = logging.getLogger(__name__)

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import user

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'models',)
sys.path.append( mymodule_dir )
import utils

import hashlib

JIRA_PROJECT_ID = os.environ.get('JIRA_PROJECT_ID')


def transformNewUser(request):
    logger.info("Entering Transform New User Transformer: " + "(request: {})".format(str(utils.censor_log(request))))
    hashPass = hashPassword(request['password'])
    request['password'] = hashPass
    if 'first_name' in request and (request['first_name'] != '' or request['first_name'] != None):
        request['first_name'] = request['first_name'].title()
    if 'last_name' in request and (request['last_name'] != '' or request['last_name'] != None):
        request['last_name'] = request['last_name'].title()
    if 'city' in request and (request['city'] != '' or request['city'] != None):
        request['city'] = request['city'].title()
    if 'country' in request and (request['country'] != '' or request['country'] != None):
        request['country'] = request['country'].title()
    if 'state' in request and (request['state'] != '' or request['state'] != None):
        request['state'] = request['state'].upper()
    logger.info("Leaving Transform New User Transformer: " + "(request: {})".format(str(request)))
    return request

def hashPassword(password):
    logger.info("Entering Hash Password: (password: ********)")
    hashPass = hashlib.sha256(password.encode()).hexdigest()
    logger.info("Leaving Hash Password: ")
    return hashPass

def transformEditUser(request):
    logger.info("Entering Transform Edit User Transformer: " + "(request: {})".format(str(request)))
    transformedRequest = {}
    for key in request:
        if request[key] != "" and request[key] != None:
            if key == 'first_name':
                transformedRequest['first_name'] = request['first_name'].title()
            elif key == 'last_name':
                transformedRequest['last_name'] = request['last_name'].title()
            elif key == 'city':
                transformedRequest['city'] = request['city'].title()
            elif key == 'country':
                transformedRequest['country'] = request['country'].title()
            elif key == 'state':
                transformedRequest['state'] = request['state'].upper()
            else: 
                transformedRequest[key] = request[key]
    logger.info("Leaving Transform Edit User Transformer: " + "(request: {})".format(str(request)))
    return transformedRequest

def transformReportBug(request, email):
    logger.info("Entering Transform Bug Report Transformer: " + "(email: {}, request: {})".format(str(email),str(request)))
    issueType = ''
    if (request['requestType'] == 'Bug Report'):
        issueType = 'Bug'
    elif (request['requestType'] == 'Feature Request'):
        issueType= 'Story'
    response = {
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
    logger.info("Leaving Transform Bug Report Transformer: " + str(response))
    return response

def transformDateRange(date_range):
    logger.info("Entering Transform Date Range Transformer: " + "(date_range: {})".format(str(date_range)))
    query = "trade_date >= "
    if date_range == "Year":
        query += "DATE_ADD(NOW(), INTERVAL -1 YEAR)"
    elif date_range == "Month":
        query += "DATE_ADD(NOW(), INTERVAL -1 MONTH)"
    elif date_range == "Week":
        query += "DATE_ADD(NOW(), INTERVAL -1 WEEK)"
    elif date_range == "Day":
        query += "DATE_ADD(NOW(), INTERVAL -1 DAY)"
    logger.info("Leaving Transform Date Range Transformer: " + str(query))
    return query

def transformFromAndToDate(from_date,to_date):
    logger.info("Entering Transform From and To Date Transformer: " + "(date_range: {})".format(str(from_date),str(to_date)))
    query = "trade_date >= '{}' AND trade_date <= '{}'".format(str(from_date),str(to_date))
    logger.info("Leaving Transform From and To Date Transformer: " + str(query))
    return query

def transformAVtf(today_date,time_frame):
    logger.info("Entering Transform Account Value Timeframe Transformer: " + "(today_date: {}, time_frame: {})".format(str(today_date),str(time_frame)))
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
    logger.info("Leaving Transform Account Value Timeframe Transformer: " + str(last_dates))
    return last_dates

def transformLeaderboardTimeFilter(time_filter):
    logger.info("Entering Transform Leaderboard Time Filter Transformer: " + "(time_filter: {})".format(str(time_filter)))
    time_filter_query = ""
    if time_filter == 'All Time':
        time_filter_query = "t.trade_date is not NULL"
        #pass
    elif time_filter == "YTD":
        current_year = date.today().year
        ytd_start_date = date(current_year, 1, 1)
        time_filter_query = "t.trade_date >= '{}'".format(str(ytd_start_date))
    elif time_filter == "Quarter":
        # Get today's date
        today = date.today()
        # Determine the start of the current quarter
        current_month = today.month
        current_year = today.year
        # Map the month to the quarter's start month
        if current_month in [1, 2, 3]:  # Q1
            quarter_start_date = date(current_year, 1, 1)
        elif current_month in [4, 5, 6]:  # Q2
            quarter_start_date = date(current_year, 4, 1)
        elif current_month in [7, 8, 9]:  # Q3
            quarter_start_date = date(current_year, 7, 1)
        else:  # Q4
            quarter_start_date = date(current_year, 10, 1)
        time_filter_query = "t.trade_date >= '{}'".format(str(quarter_start_date))
    elif time_filter == "Month":
        today = date.today()
        month_start_date = date(today.year, today.month, 1)
        time_filter_query = "t.trade_date >= '{}'".format(str(month_start_date))
    elif time_filter == "Week":
        # Get today's date
        today = date.today()
        # Calculate WTD start date (assuming week starts on Sunday)
        days_since_sunday = today.weekday() + 1 if today.weekday() < 6 else 0
        week_start_date = today - timedelta(days=days_since_sunday)
        time_filter_query = "t.trade_date >= '{}'".format(str(week_start_date))
    elif time_filter == "Today":
        today = date.today()
        time_filter_query = "t.trade_date >= '{}'".format(str(today))
    logger.info("Leaving Transform Leaderboard Time Filter Transformer: " + "(time_filter_query: {})".format(str(time_filter_query)))
    return time_filter_query

def transformLeaderboardValueFilter(value_filter):
    logger.info("Entering Transform Leaderboard Value Filter Transformer: " + "(value_filter: {})".format(str(value_filter)))
    value_filter_query = []
    if value_filter == "Total PNL":
        value_filter_query = ["SUM(COALESCE(t.pnl, 0))","COUNT(t.trade_id) > 0","DESC"]
    elif value_filter == "Avg PNL":
        value_filter_query = ["SUM(COALESCE(t.pnl, 0)) / COUNT(t.trade_id)","COUNT(t.trade_id) > 0","DESC"]
    elif value_filter == "Win %":
        value_filter_query = ["COUNT(CASE WHEN t.pnl > 0 THEN 1 END) * 100.0 / COUNT(t.trade_id)","COUNT(t.trade_id) > 0","DESC"]
    elif value_filter == "Largest Win":
        value_filter_query = ["MAX(CASE WHEN t.pnl > 0 THEN t.pnl ELSE NULL END)","MAX(CASE WHEN t.pnl > 0 THEN t.pnl ELSE NULL END) IS NOT NULL","DESC"]   
    elif value_filter == "Avg Win":
        value_filter_query = ["AVG(CASE WHEN t.pnl > 0 THEN t.pnl ELSE NULL END)","AVG(CASE WHEN t.pnl > 0 THEN t.pnl ELSE NULL END) IS NOT NULL","DESC"]
    elif value_filter == "Avg Loss":
        value_filter_query = ["AVG(CASE WHEN t.pnl < 0 THEN t.pnl ELSE NULL END)","AVG(CASE WHEN t.pnl < 0 THEN t.pnl ELSE NULL END) IS NOT NULL","ASC"]
    logger.info("Leaving Transform Leaderboard Value Filter Transformer: " + "(value_filter_query: {})".format(str(value_filter_query)))
    return value_filter_query