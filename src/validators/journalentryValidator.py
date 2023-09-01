import os
import sys
import re
from datetime import date, datetime, timedelta


def validateDate(date):
    if(re.match(r'^\d{4}-\d{2}-\d{2}$', date) is None):
        return {
            "result": "Invalid 'date' format, Please provide the Date in YYYY-MM-DD format"
        }, 400
    if (datetime.strptime(date, '%Y-%m-%d').date() > datetime.now().date() + timedelta(days=1)):
        return {
            "result": "Invalid date. The 'date' provided can't be in the future"
        }, 400
    return True