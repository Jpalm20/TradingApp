import os
import sys
import re
from datetime import date, datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def validateDate(date):
    logger.info("Entering Validate Journal Entry Date Validator: " + "(date: {})".format(str(date)))
    if(re.match(r'^\d{4}-\d{2}-\d{2}$', date) is None):
        response = "Invalid 'date' format, Please provide the Date in YYYY-MM-DD format"
        logger.warning("Leaving Validate Journal Entry Date Validator: " + response)
        return {
            "result": response
        }, 400
    if (datetime.strptime(date, '%Y-%m-%d').date() > datetime.now().date() + timedelta(days=1)):
        response = "Invalid date. The 'date' provided can't be in the future"
        logger.warning("Leaving Validate Journal Entry Date Validator: " + response)
        return {
            "result": response
        }, 400
    logger.info("Leaving Validate Journal Entry Date Validator: ")
    return True