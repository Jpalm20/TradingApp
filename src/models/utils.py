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
    try:
        connection = mysql.connector.connect(host='localhost',
                                        port=3306,
                                        database='TradingApp',
                                        user='jp',
                                        password='Jpalmieri20!')

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
        if connection.is_connected():
                connection.close()
    logger.info("Leaving Execute Database Query Util: " + str(response))
    return response


def generate_code():
    logger.info("Entering Generate Code Util: ")
    code = ""
    for _ in range(6):
        code += str(random.randint(0, 9))  # Generate a random digit (0-9)
    logger.info("Leaving Generate Code Util: " + str(code))
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

        