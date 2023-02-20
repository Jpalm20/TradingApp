import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()
DB_PASSWORD = os.getenv("DBPASSWORD")

def execute_db(query,args):

    try:
            connection = mysql.connector.connect(host='localhost',
                                         port=3306,
                                         database='tradingapp',
                                         user='root',
                                         password='DB PASSWORD ')

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
