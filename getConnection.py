import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os
 
# Load variables from .env file
load_dotenv()

# MYSQL CONFIG VARIABLES
hostname = os.getenv("DB_HOST")
username = os.getenv("DB_USER")
***REMOVED*** = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

def getConnection():    
    try:
        conn = mysql.connector.connect(
            host=hostname,                              
            user=username,
            ***REMOVED***=***REMOVED***,
            database=database
            )  
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User name or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)                        
    else:  #will execute if there is no exception raised in try block
        return conn   
                
