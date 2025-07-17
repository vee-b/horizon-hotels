import mysql.connector, getConnection

# Add a new hotel to the hotel table
def addHotel(): 

    conn = getConnection.getConnection()
    
    DB_NAME = 'HORIZON_HOTELS'             #DB Name
    TABLE_NAME = 'hotel'
    CITY = input('Enter City: ')
    ROOM_CAPACITY = input('Enter Room Capacity: ')
    ON_PEAK_SEASON_PRICE = input('Enter On-peak Season Price: ')
    OFF_PEAK_SEASON_PRICE = input('Enter Off-peak Season Price: ')
    # here you should perform data validation 
    # syntax as well as semantics 

    INSERT_statement = 'INSERT INTO ' + TABLE_NAME + ' (\
        HOTEL_ID, CITY, ROOM_CAPACITY, ON_PEAK_SEASON_PRICE, OFF_PEAK_SEASON_PRICE) VALUES (%s, %s, %s, %s, %s);'    

    if conn != None:    #Checking if connection is None
        if conn.is_connected(): #Checking if connection is established
            print('MySQL Connection is established')                          
            dbcursor = conn.cursor()    #Creating cursor object
            dbcursor.execute('USE {};'.format(DB_NAME)) #use database    

            # Select maximum hotel_ID in current table
            dbcursor.execute('SELECT HOTEL_ID FROM hotel;')
            row = dbcursor.fetchall()
            maxHotelID = max(row)
            # Add 1 to the current max ID & assign it to the hotel_ID to be newly added 
            HOTEL_ID = str(int(maxHotelID[0]) + 1) 

            dataset = (HOTEL_ID, CITY, ROOM_CAPACITY, ON_PEAK_SEASON_PRICE, OFF_PEAK_SEASON_PRICE)        
            dbcursor.execute(INSERT_statement, dataset)   
            conn.commit()              
            print('INSERT query executed successfully.') 
            dbcursor.close()              
            conn.close() #Connection must be closed
        else:
            print('DB connection error')
    else:
        print('DBFunc error')

# Delete a hotel from the hotel table
def deleteHotel():

    conn = getConnection.getConnection()
    
    DB_NAME = 'HORIZON_HOTELS'             #DB Name
    TABLE_NAME = 'hotel'
    HOTEL_ID = input('Enter the Hotel ID of the hotel to be deleted: ') 
    # here you should perform data validation 
    # syntax as well as semantics 

    DELETE_statement = 'DELETE FROM ' + TABLE_NAME + ' \
        WHERE + HOTEL_ID = %s;'    

    if conn != None:    #Checking if connection is None
        if conn.is_connected(): #Checking if connection is established
            print('MySQL Connection is established')                          
            dbcursor = conn.cursor()    #Creating cursor object
            dbcursor.execute('USE {};'.format(DB_NAME)) #use database    
            dataset = (HOTEL_ID,)        
            dbcursor.execute(DELETE_statement, dataset)   
            conn.commit()              
            print('DELETE statement executed successfully.') 
            dbcursor.close()              
            conn.close() #Connection must be closed
        else:
            print('DB connection error')
    else:
        print('DBFunc error')

# Update a hotel from the hotel table
def updateHotel():
    
    conn = getConnection.getConnection()
    
    DB_NAME = 'HORIZON_HOTELS'             #DB Name
    TABLE_NAME = 'hotel'
    HOTEL_ID = input('Enter the Hotel ID of the hotel to be updated: ')
    CITY = input('Enter City: ')
    ROOM_CAPACITY = input('Enter Room Capacity: ')
    ON_PEAK_SEASON_PRICE = input('Enter On-peak Season Price: ')
    OFF_PEAK_SEASON_PRICE = input('Enter Off-peak Season Price: ')
    # here you should perform data validation 
    # syntax as well as semantics 

    UPDATE_statement = 'UPDATE ' + TABLE_NAME + ' SET \
        CITY = %s, \
        ROOM_CAPACITY = %s, \
        ON_PEAK_SEASON_PRICE = %s, \
        OFF_PEAK_SEASON_PRICE = %s \
        WHERE HOTEL_ID = %s;'    

    if conn != None:    #Checking if connection is None
        if conn.is_connected(): #Checking if connection is established
            print('MySQL Connection is established')                          
            dbcursor = conn.cursor()    #Creating cursor object
            dbcursor.execute('USE {};'.format(DB_NAME)) #use database    
            dataset = (CITY, ROOM_CAPACITY, ON_PEAK_SEASON_PRICE, OFF_PEAK_SEASON_PRICE, HOTEL_ID)        
            dbcursor.execute(UPDATE_statement, dataset)   
            conn.commit()              
            print('UPDATE statement executed successfully.') 
            dbcursor.close()              
            conn.close() #Connection must be closed
        else:
            print('DB connection error')
    else:
        print('DBFunc error')

# SELECT queries for hotel table
def selectHotel():
    pass
