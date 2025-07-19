import mysql.connector, getConnection

# Connect to DB function
conn = getConnection.getConnection()  
# Name of DB
DB_NAME = 'HORIZON_HOTELS'             
# SQL
DBStatement = 'CREATE DATABASE ' + DB_NAME + ';'    
# If the connection is None
if conn != None:   
    # If there is a connection
    if conn.is_connected():
        print('MySQL Connection is established')             
        # Create a cursor object             
        dbcursor = conn.cursor()    
        # CREATE the database  
        dbcursor.execute(DBStatement)
        print("Database {} created successfully.".format(DB_NAME))     
        dbcursor.close()                   
        # Close the connection            
        conn.close() 
    else:
        print('DB connection error')
else:
    print('DBFunc error')
