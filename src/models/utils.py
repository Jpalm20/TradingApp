import mysql.connector

def execute_db(query,args):

    try:
            connection = mysql.connector.connect(host='docker.for.mac.localhost',
                                         port=3306,
                                         database='TradingApp',
                                         user='jp',
                                         password={DB_PASSWORD})

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