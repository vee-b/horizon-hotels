from datetime import datetime
import mysql.connector, getConnection
from passlib.hash import sha256_crypt

def account_holder_table():
    conn = getConnection.getConnection()   #connection to DB
    DB_NAME = 'HORIZON_HOTELS'             #DB Name
    TABLE_NAME = 'account_holder'
    INSERT_statement = 'INSERT INTO ' + TABLE_NAME + ' (\
        ACCOUNT_HOLDER_ID, FIRST_NAME, LAST_NAME, EMAIL, PASSWORD_HASH, ACCOUNT_TYPE) VALUES (%s, %s, %s, %s, %s, %s);'    
    if conn != None:    #Checking if connection is None
        if conn.is_connected(): #Checking if connection is established
            print('MySQL Connection is established')                          
            dbcursor = conn.cursor()    #Creating cursor object
            dbcursor.execute('USE {};'.format(DB_NAME)) #use database       
            ***REMOVED*** = 'admin'
            ***REMOVED***_hashvalue = sha256_crypt.hash(***REMOVED***) 
            dataset = [ (1000, 'Alice', 'Liddle', 'admin@hotmail.co.uk', ***REMOVED***_hashvalue, 'admin') ] 
            dbcursor.executemany(INSERT_statement, dataset) #multiple datasets  
            conn.commit()              
            print('INSERT query executed successfully.') 
            dbcursor.close()              
            conn.close() #Connection must be closed
        else:
            print('DB connection error')
    else:
        print('DBFunc error')

def hotel_table():
    conn = getConnection.getConnection()   #connection to DB
    DB_NAME = 'HORIZON_HOTELS'             #DB Name
    TABLE_NAME = 'hotel'
    INSERT_statement = 'INSERT INTO ' + TABLE_NAME + ' (\
        HOTEL_ID, CITY, ROOM_CAPACITY, ON_PEAK_SEASON_PRICE, OFF_PEAK_SEASON_PRICE) VALUES (%s, %s, %s, %s, %s);'    
    if conn != None:    #Checking if connection is None
        if conn.is_connected(): #Checking if connection is established
            print('MySQL Connection is established')                          
            dbcursor = conn.cursor()    #Creating cursor object
            dbcursor.execute('USE {};'.format(DB_NAME)) #use database        
            dataset = [ (1000,'Aberdeen', '80','140', '60'),
                (1001,'Belfast', '80','140','60'),
                (1002,'Birmingham', '90','150','70'),
                (1003,'Bristol', '90','140','70'),
                (1004,'Cardiff', '80','120','60'),
                (1005,'Edinburgh', '90','160','70'),
                (1006,'Glasgow', '100','150','70'),
                (1007,'London', '120','200','80'),
                (1008,'Manchester', '110','180','80'),
                (1009,'New Castle', '80','100','60'),
                (1010,'Norwich', '80','100','60'),
                (1011,'Nottingham', '100','120','70'),
                (1012,'Oxford', '80','180','70'),
                (1013,'Plymouth', '80','180','50'),
                (1014,'Swansea', '80','120','50') ]        
            dbcursor.executemany(INSERT_statement, dataset) #multiple datasets  
            conn.commit()              
            print('INSERT query executed successfully.') 
            dbcursor.close()              
            conn.close() #Connection must be closed
        else:
            print('DB connection error')
    else:
        print('DBFunc error')

#hotel_table()
account_holder_table()