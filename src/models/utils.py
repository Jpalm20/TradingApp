import os
from dotenv import load_dotenv
import random
import mysql.connector
from mysql.connector import pooling, errors
import logging
from PIL import Image
import io
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

ENV = os.environ.get('ENV','prod')
POOL_NAME = os.environ.get('POOL_NAME',"mypool")

if ENV == 'test':
    DB_HOST = os.environ.get('TEST_DB_HOST')
    DB_PORT = os.environ.get('TEST_DB_PORT')
    DB_NAME = os.environ.get('TEST_DB_NAME')
    DB_USERNAME = os.environ.get('TEST_DB_USERNAME')
    DB_PASSWORD = os.environ.get('TEST_DB_PASSWORD')
else:
    if ENV == 'docker':
        DB_HOST = os.environ.get('DB_HOST_DOCKER')
    else:
        DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    

# Database configuration
db_config = {
    "user": DB_USERNAME,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "database": DB_NAME,
    "port": DB_PORT,
}

connection_pool = None

# Set up connection pooling
def get_connection_pool():
    global connection_pool
    if connection_pool is None:
        logger.info("Initializing connection pool")
        connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=POOL_NAME,  # Use a short pool name
            pool_size=10,  # Reasonable default pool size
            pool_reset_session=True,
            **db_config
        )
        logger.info("Connection pool initialized")
    return connection_pool

"""
def get_db_connection():
    logger.info("Getting connection pool")
    pool = get_connection_pool()
    logger.info(f"Connection pool status: {pool.status()}")
    logger.info("Getting database connection")
    connection = pool.get_connection()
    logger.info("Got database connection")
    return connection
"""

def get_db_connection(retry_timeout=30, retry_interval=1):
    """
    Get a database connection from the pool with retry logic.
    :param retry_timeout: Total time to retry before raising an error.
    :param retry_interval: Time to wait between retries.
    :return: A database connection from the pool.
    """
    logger.info("Getting connection pool")
    pool = get_connection_pool()

    start_time = time.time()
    while True:
        try:
            logger.info("Attempting to get a database connection")
            connection = pool.get_connection()
            logger.info("Successfully got a database connection")
            return connection
        except mysql.connector.errors.PoolError as err:
            elapsed_time = time.time() - start_time
            if elapsed_time > retry_timeout:
                logger.error(f"Failed to get a database connection after {retry_timeout} seconds: {err}")
                raise TimeoutError(f"Failed to get a database connection after {retry_timeout} seconds") from err
            logger.warning(f"Connection pool exhausted. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

def close_db_connection(connection):
    if connection is not None and connection.is_connected():
        connection.close()
        logger.info("DB Connection Closed")

def execute_db_old(query,args):
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

def execute_db(query, params=None):
    logger.info("Entering Execute Database Query Util: " + "(query: {}, args: {})".format(str(query),str(params)))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Assuming you want results as dictionaries
    try:
        cursor.execute(query, params)
        """
        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.rowcount
        """
        result = cursor.fetchall() 
        id = cursor.lastrowid
        connection.commit()
        response = result,id
    except mysql.connector.Error as err:
        response = "Failed: {}".format(err)
    finally:
        cursor.close()
        close_db_connection(connection)
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
            if key in ('date_range','from_and_to_date','from_date','to_date'):
                continue
            if value:
                conditions.append(f"{key}='{value}'")
        if 'date_range' in filters: 
            conditions.append(filters['date_range'])
        if 'from_and_to_date' in filters:
            conditions.append(filters['from_and_to_date'])
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


def further_process_image(file, max_width=300, max_height=300):
    image = Image.open(file)
    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS) 
    output = io.BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)
    return output