import mysql.connector

def execute_db(query,args):
    
    try:
            connection = mysql.connector.connect(host='docker.for.mac.localhost',
                                         port=3306,
                                         database='TradingApp',
                                         user='jp',
                                         password='LOCAL.MYSQL.PASSWORD')

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,args)
            result = cursor.fetchall() 
            connection.commit()
            
            for x in result:
                print(x)
            
            print(cursor.rowcount, "Success")
            response = "Success"
            cursor.close()

    except mysql.connector.Error as error:
            print("Failed: {}".format(error))
            response = "Failed: {}".format(error)
    finally:
        if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")
        
    return response