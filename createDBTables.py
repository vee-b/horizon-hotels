import mysql.connector, getConnection
from mysql.connector import Error, errorcode

# Connect to DB Function
conn = getConnection.getConnection() 
# DB Name 
DB_NAME = 'HORIZON_HOTELS'             
TABLES = {}

TABLES['HOTEL'] = 'CREATE TABLE HOTEL (\
  HOTEL_ID VARCHAR(10) NOT NULL, \
  CITY VARCHAR(45) NOT NULL, \
  ROOM_CAPACITY INT, \
  ON_PEAK_SEASON_PRICE DOUBLE NOT NULL, \
  OFF_PEAK_SEASON_PRICE DOUBLE NOT NULL, \
  PRIMARY KEY (HOTEL_ID));'

TABLES['BOOKING'] = 'CREATE TABLE BOOKING(\
BOOKING_ID VARCHAR(15) NOT NULL, \
PRIMARY KEY (BOOKING_ID), \
STANDARD_ROOMS INT NOT NULL, \
DOUBLE_ROOMS INT NOT NULL, \
DOUBLE2_ROOMS INT NOT NULL, \
FAMILY_ROOMS INT NOT NULL, \
RESERVATION_DATE DATE NOT NULL, \
CHECK_IN_DATE DATE NOT NULL, \
CHECK_OUT_DATE DATE NOT NULL, \
TOTAL_NIGHTS_BOOKED INT NOT NULL, \
TOTAL_COST_NO_DISCOUNT DOUBLE NOT NULL, \
TOTAL_COST_DISCOUNTED DOUBLE NOT NULL, \
ACCOUNT_HOLDER_ID VARCHAR(10), \
FOREIGN KEY (ACCOUNT_HOLDER_ID) \
  REFERENCES ACCOUNT_HOLDER (ACCOUNT_HOLDER_ID) \
  ON DELETE CASCADE \
  ON UPDATE CASCADE, \
HOTEL_ID VARCHAR(10), \
FOREIGN KEY (HOTEL_ID) \
  REFERENCES HOTEL (HOTEL_ID) \
  ON DELETE CASCADE \
  ON UPDATE CASCADE );'

TABLES['ACCOUNT_HOLDER'] = 'CREATE TABLE ACCOUNT_HOLDER (\
ACCOUNT_HOLDER_ID VARCHAR(10) NOT NULL, \
PRIMARY KEY (ACCOUNT_HOLDER_ID), \
FIRST_NAME VARCHAR(20) NOT NULL, \
LAST_NAME VARCHAR(20) NOT NULL, \
EMAIL VARCHAR(20) NOT NULL, \
PASSWORD_HASH VARCHAR(128) NOT NULL, \
ACCOUNT_TYPE VARCHAR(20) NOT NULL );'


# If the connection is None
if conn != None:    
    # If there is a connection
    if conn.is_connected(): 
        print('MySQL Connection is established')  
        # Create a cursor object                              
        dbcursor = conn.cursor()   
        # Use the database
        dbcursor.execute('USE {};'.format(DB_NAME)) 

        # Loop through the TABLES
        for table_name in TABLES:   
            table_description = TABLES[table_name]
            try:
                print('Creating table {}:'.format(table_name), end='')
                dbcursor.execute(table_description)
            except mysql.connector.Error as e:
                if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('Table {} already exists.'.format(table_name))
                else:
                    print(e.msg)
            else:
                print('Table {} successfully created.'.format(table_name))       
        
        dbcursor.close()     
        # Close the connection     
        conn.close()
    else:
        print('DB connection error')
else:
    print('DBFunc error')
