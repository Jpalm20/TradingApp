import os
import random
import mysql.connector
import logging

logger = logging.getLogger(__name__)

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


def execute_db(query,args):
    logger.info("Entering Execute Database Query Util: " + "(query: {}, args: {})".format(str(query),str(args)))
    connection = None
    try:
        connection = mysql.connector.connect(host=DB_HOST,
                                        port=DB_PORT,
                                        database=DB_NAME,
                                        user=DB_USERNAME,
                                        password=DB_PASSWORD)

        cursor = connection.cursor(dictionary=True)
        cursor.execute(query,args)
        result = cursor.fetchall() 
        id = cursor.lastrowid
        connection.commit()
        response = result,id
        cursor.close()

    except mysql.connector.Error as error:
        response = "Failed: {}".format(error)
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            logger.info("DB Connection Closed")
    logger.info("Leaving Execute Database Query Util: " + str(response))
    return response


def generate_code():
    logger.info("Entering Generate Code Util: ")
    code = ""
    for _ in range(6):
        code += str(random.randint(0, 9))  # Generate a random digit (0-9)
    logger.info("Leaving Generate Code Util: ")
    return code


def add_filters_to_query_sring(query,filters):
    logger.info("Entering Add Filters to Query String Util: " + "(query: {}, filters: {})".format(str(query),str(filters)))
    queryString = query
    if filters:
        queryString += " AND "
        conditions = []
        for key, value in filters.items():
            if key == 'date_range':
                continue
            if value:
                conditions.append(f"{key}='{value}'")
        if 'date_range' in filters: 
            conditions.append(filters['date_range'])
        queryString += " AND ".join(conditions)
    logger.info("Leaving Add Filters to Query String Util: " + str(queryString))
    return queryString


def censor_log(request):
    logger.info("Entering Censor Log Util: ")

    # Check if the request is a dictionary
    if not isinstance(request, dict):
        logger.info("Invalid data type for censoring. Skipping.")
        return request

    # Proceed with copying and censoring
    censoredRequest = request.copy()
    
    # List of keys to censor
    keys_to_censor = ['password', 'curr_pass', 'new_pass_1', 'new_pass_2', 'code']
    
    # Censor specified keys
    for key in keys_to_censor:
        if key in censoredRequest:
            censoredRequest[key] = '********'

    logger.info("Leaving Censor Log Util: ")
    return censoredRequest