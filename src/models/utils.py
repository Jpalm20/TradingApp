import os
import mysql.connector

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


def execute_db(query,args):

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
        if connection.is_connected():
                connection.close()
        
    return response