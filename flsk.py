'''
Horizon Hotels Flask app 
***REMOVED***
***REMOVED*** 
'''

from datetime import date, datetime, timedelta
import gc
from locale import currency
from passlib.hash import sha256_crypt
import pandas
import mysql.connector, getConnection
from flask import Flask, jsonify, redirect, render_template, request, url_for, session 

app = Flask(__name__)
app.secret_key = 'SecretString'

@app.route('/searchPage')
def render_searchPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		print('You are not logged in')

	conn = getConnection.getConnection()

	if conn != None:
		print('MySQL Connection is established')
		dbcursor = conn.cursor()
		dbcursor.execute('SELECT DISTINCT CITY FROM HOTEL;')
		rows = dbcursor.fetchall()
		dbcursor.close()
		conn.close()

		locations = []
		for CITY in rows:
			CITY = str(CITY).strip('(')
			CITY = str(CITY).strip(')')
			CITY = str(CITY).strip(',')
			CITY = str(CITY).strip("'")
			locations.append(CITY)

		conn = getConnection.getConnection()

		if conn != None:
			print('MySQL Connection is established')
			dbcursor = conn.cursor()

			# FETCH & CALCULATE TOTAL ROOM CAPACITY, PLUS NUMBER OF DIFFERENT ROOM TYPES

			# Fetch room capacity for selected location
			dbcursor.execute('SELECT ROOM_CAPACITY FROM HOTEL WHERE CITY = %s;', (CITY, ))
			fetched_room_capacity = dbcursor.fetchall() 
			room_capacity = fetched_room_capacity[0][0]

			print(room_capacity)

			# Calculate number of different room types
			# Each hotel has 30% standard room; 50% double rooms and 20% Family rooms.
			num_of_standard = int(0.3 * room_capacity)
			num_of_double = int((0.5 * room_capacity)/2)
			num_of_double2 = int((0.5 * room_capacity)/2)
			num_of_family = int(0.2 * room_capacity)

			dbcursor.close()
			conn.close()
		
		return render_template('searchPage.html', locations=locations, account_type=account_type, num_of_standard=num_of_standard, num_of_double=num_of_double, num_of_double2=num_of_double2, num_of_family=num_of_family)
	else:
		print('DB connection Error')
		return 'DB Connection Error'

@app.route ('/room_capacity', methods = ['POST', 'GET'])
def get_room_capacity():
	
	conn = getConnection.getConnection()

	if conn != None:
		print('MySQL Connection is established')
		dbcursor = conn.cursor()

		# FETCH & CALCULATE TOTAL ROOM CAPACITY, PLUS NUMBER OF DIFFERENT ROOM TYPES

		city = request.args.get('location')

		# Fetch room capacity for selected location
		dbcursor.execute('SELECT ROOM_CAPACITY FROM HOTEL WHERE CITY = %s;', (city, ))
		fetched_room_capacity = dbcursor.fetchall() 
		room_capacity = fetched_room_capacity[0][0]

		# Calculate number of different room types
		# Each hotel has 30% standard room; 50% double rooms and 20% Family rooms.
		num_of_standard = int(0.3 * room_capacity)
		num_of_double = int((0.5 * room_capacity)/2)
		num_of_double2 = int((0.5 * room_capacity)/2)
		num_of_family = int(0.2 * room_capacity)

		dbcursor.close()
		conn.close()

		return jsonify(num_of_standard=num_of_standard, num_of_double=num_of_double, num_of_double2=num_of_double2, num_of_family=num_of_family)
	else:
		print('DB connection Error')
		return 'DB Connection Error'

@app.route('/searchResultsPage', methods = ['POST', 'GET'])
def render_searchResultsPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		print('You are not logged in')

	if request.method == 'POST':

		# Fetch currency type from form
		currency = request.form['currency']
		print(currency)

		# Fetch number of selected room types from form
		numStandard = request.form['standard']
		numDouble = request.form['double']
		numDouble2 = request.form['double2']
		numFamily = request.form['family']

		# If no room is selected, then instead of sending the form, redirect back to the search page
		if numStandard == str(0) and numDouble == str(0) and numDouble2 == str(0) and numFamily == str(0):
			return redirect(url_for('render_searchPage'))

		location = request.form['location']
		image_link = "static/css/Images/" + location + ".jpg"

		# Fetch check-in & check-out dates from form
		checkIn = request.form['checkIn']
		checkOut = request.form['checkOut']				

		# Generate list of dates between checkin & checkout dates
		dates_list = pandas.date_range(checkIn,checkOut, freq='D').strftime("%Y-%m-%d").tolist()

		# List on on-peak and off-peak months
		on_peak_months = ['04', '05', '06', '07', '08', '09']
		off_peak_months = ['10', '11', '12', '01', '02', '03']

		# Variables for holding number of on-peak & off-peak days
		on_peak_days = 0
		off_peak_days = 0

		# Loop through dates_list & count how many days are booked during on-peak/off-peak
		# Then add to on_peak_days & off_peak_days variables
		for date in dates_list:
			if date[5:7] in on_peak_months:
				on_peak_days += 1
			elif date[5:7] in off_peak_months:
				off_peak_days += 1

		conn = getConnection.getConnection()
		if conn != None:     
			print('MySQL Connection is established')                          
			dbcursor = conn.cursor()    

			# FETCH & CALCULATE ON-PEAK & OFF-PEAK PRICES
			
			# Fetch off-peak price for selected location
			dbcursor.execute('SELECT ON_PEAK_SEASON_PRICE FROM HOTEL WHERE CITY = %s;', (location, ))   	
			fetched_price = dbcursor.fetchall() 
			on_peak_price = fetched_price[0][0]
             
			# Fetch on-peak price for selected location
			dbcursor.execute('SELECT OFF_PEAK_SEASON_PRICE FROM HOTEL WHERE CITY = %s;', (location, ))           
			fetched_price = dbcursor.fetchall() 
			off_peak_price = fetched_price[0][0]

			# FETCH & CALCULATE TOTAL ROOM CAPACITY, PLUS NUMBER OF DIFFERENT ROOM TYPES

			# Fetch room capacity for selected location
			dbcursor.execute('SELECT ROOM_CAPACITY FROM HOTEL WHERE CITY = %s;', (location, ))
			fetched_room_capacity = dbcursor.fetchall() 
			room_capacity = fetched_room_capacity[0][0]

			# Calculate number of different room types
			# Each hotel has 30% standard room; 50% double rooms and 20% Family rooms.
			num_of_standard = 0.3 * room_capacity
			num_of_double = 0.5 * room_capacity
			num_of_family = 0.2 * room_capacity

			# CALCULATE TOTAL COST OF STAYING IN 1 OF EACH ROOM TYPE FOR SELECTED DATES

			# On-peak & off-peak prices for 1 day in each room type 

			# On-peak & off-peak prices are the same for standard rooms
			standard_on_peak_cost = on_peak_price
			standard_off_peak_cost = off_peak_price
			# Calculate on-peak & off-peak prices for double rooms
			double_on_peak_cost = on_peak_price + (0.2 * on_peak_price) # plus 20%
			double_off_peak_cost = off_peak_price + (0.2 * off_peak_price) 
			# Calculate on-peak & off-peak prices for double2 rooms (with extra guest)
			double2_on_peak_cost = on_peak_price + (0.3 * on_peak_price) # plus 30%
			double2_off_peak_cost = off_peak_price + (0.3 * off_peak_price) 
			# Calculate on-peak & off-peak prices for family rooms
			family_on_peak_cost = on_peak_price + (0.5* on_peak_price) # plus 50%
			family_off_peak_cost = off_peak_price + (0.5* off_peak_price)

			# Total on-peak & off-peak prices for selected dates in each room type 

			# Calculate total cost for selected dates (FOR 1 STANDARD ROOM)
			total_standard_on_peak_cost = standard_on_peak_cost * on_peak_days
			total_standard_off_peak_cost = standard_off_peak_cost * off_peak_days
			total_standard_cost = total_standard_on_peak_cost + total_standard_off_peak_cost

			# Calculate total cost for selected dates (FOR 1 DOUBLE ROOM)
			total_double_on_peak_cost = double_on_peak_cost * on_peak_days
			total_double_off_peak_cost = double_off_peak_cost * off_peak_days
			total_double_cost = total_double_on_peak_cost + total_double_off_peak_cost

			# Calculate total cost for selected dates (FOR 1 DOUBLE2 ROOM)
			total_double2_on_peak_cost = double2_on_peak_cost * on_peak_days
			total_double2_off_peak_cost = double2_off_peak_cost * off_peak_days
			total_double2_cost = total_double2_on_peak_cost + total_double2_off_peak_cost

			# Calculate total cost for selected dates (FOR 1 FAMILY ROOM)
			total_family_on_peak_cost = family_on_peak_cost * on_peak_days
			total_family_off_peak_cost = family_off_peak_cost * off_peak_days
			total_family_cost = total_family_on_peak_cost + total_family_off_peak_cost

			# CALCULATE TOTAL COST OF STAY 

			# Fetch number of selected room types from form
			numStandard = request.form['standard']
			numDouble = request.form['double']
			numDouble2 = request.form['double2']
			numFamily = request.form['family']
			
			# Calulate total stay price (before discount)
			total_price_of_stay_before_discount = (total_standard_cost * int(numStandard)) + (total_double_cost * int(numDouble)) + (total_double2_cost * int(numDouble2)) + (total_family_cost * int(numFamily))

			# CALCULATE & APPLY DISCOUNT TO THE TOTAL PRICE OF STAY 

			# Get current date
			current_date = datetime.today().strftime('%Y-%m-%d')

			# Calculate number of days between check-in & current date
			# Generate list of dates between current date & check-in date
			dates_list = pandas.date_range(current_date,checkIn, freq='D').strftime("%Y-%m-%d").tolist()
			print(dates_list)
			# Variable for counting days between current & check-in date
			days_in_advance = 0
			# Add count to days_in_advance
			for date in dates_list:
				days_in_advance += 1

			# Apply discount to total cost of stay
			if days_in_advance < 45:
				total_price_of_stay_with_discount = total_price_of_stay_before_discount
			elif days_in_advance == 45 or days_in_advance < 60:
				total_price_of_stay_with_discount = total_price_of_stay_before_discount - (0.05 * total_price_of_stay_before_discount)
			elif days_in_advance == 60 or days_in_advance < 80:
				total_price_of_stay_with_discount = total_price_of_stay_before_discount - (0.1 * total_price_of_stay_before_discount)
			elif days_in_advance >= 80:
				total_price_of_stay_with_discount = total_price_of_stay_before_discount - (0.2 * total_price_of_stay_before_discount)

			# Currency conversions
			# 1 GBP = 1.2 Euros, 1 GBP = 1.6 USD
			if currency == 'usd':
				total_price_of_stay_before_discount = format(total_price_of_stay_before_discount * 1.6, '.1f')
				total_price_of_stay_with_discount = format(total_price_of_stay_with_discount * 1.6, '.1f')
			elif currency == 'euro':
				total_price_of_stay_before_discount = format(total_price_of_stay_before_discount * 1.2, '.1f')
				total_price_of_stay_with_discount = format(total_price_of_stay_with_discount * 1.2, '.1f')
			else:
				total_price_of_stay_before_discount = format(total_price_of_stay_before_discount, '.1f')
				total_price_of_stay_with_discount = format(total_price_of_stay_with_discount, '.1f')

			# RECEIPT DETAILS 

			print('\n')
			print('Location: ' + location)
			print('Standard Rooms: ' + str(numStandard))
			print('Double Rooms (1 Guest): ' + str(numDouble))
			print('Double Rooms (2 Guests): ' + str(numDouble2))
			print('Family Rooms: ' + str(numFamily))
			print('Check-in Date: ' + str(checkIn))
			print('Check-out Date: ' + str(checkOut))
			total_days_booked = on_peak_days + off_peak_days
			print('Total Days Booked: ' + str(total_days_booked))
			print('Total Cost (Before Discount): 'u"\xA3" + str(total_price_of_stay_before_discount))
			print('Total Cost (Discount Applied): 'u"\xA3" + str(total_price_of_stay_with_discount))
			print('\n')

			dbcursor.close()              			
			conn.close() 

			# Create session
			session['bookingDetails'] = True
			session['location'] = location
			session['image_link'] = image_link
			session['numStandard'] = numStandard
			session['numDouble'] = numDouble
			session['numDouble2'] = numDouble2
			session['numFamily'] = numFamily
			session['checkIn'] = checkIn
			session['checkOut'] = checkOut
			session['total_days_booked'] = total_days_booked
			session['total_price_of_stay_before_discount'] = total_price_of_stay_before_discount
			session['total_price_of_stay_with_discount'] = total_price_of_stay_with_discount
			session['currency'] = currency

			return render_template('searchResultsPage.html', location=location, image_link=image_link, numStandard=numStandard, numDouble=numDouble, 
			numDouble2=numDouble2, numFamily=numFamily, checkIn=checkIn, checkOut=checkOut, total_days_booked=total_days_booked, 
			total_price_of_stay_before_discount=total_price_of_stay_before_discount, total_price_of_stay_with_discount=total_price_of_stay_with_discount, account_type=account_type, currency=currency)
		else:
			print('DB connection Error')
			return redirect(url_for('searchPage'))

@app.route('/loginPage', methods = ['GET', 'POST'])
def render_loginPage():

	if request.method == 'POST':
		email = request.form['email']
		***REMOVED*** = request.form['***REMOVED***']

		# Check database for email

		conn = getConnection.getConnection()   
		DB_NAME = 'HORIZON_HOTELS'             
		TABLE_NAME = 'account_holder'

		if conn != None:    
			if conn.is_connected(): 
				print('MySQL Connection is established')                          
				dbcursor = conn.cursor()    
				dbcursor.execute('USE {};'.format(DB_NAME)) 

				# Check if account (email) is already in the database
				Verify_Query = 'SELECT * FROM ' + TABLE_NAME + ' WHERE EMAIL = %s;'
				dbcursor.execute(Verify_Query,(email,))
				rows = dbcursor.fetchall()      
				# If email is not already in database     
				if dbcursor.rowcount <= 0:  
					email_***REMOVED***_html = 'Incorrect Email/***REMOVED***'
					return render_template("loginPage.html", email_***REMOVED***_html=email_***REMOVED***_html)  
				else:
					# If email is currently in database
					# Check ***REMOVED*** matches email
					# Fetch ***REMOVED*** hash
					Verify_Password_Query = 'SELECT PASSWORD_HASH FROM ' + TABLE_NAME + ' WHERE EMAIL = %s;'
					dbcursor.execute(Verify_Password_Query,(email,))
					fetched_***REMOVED***_hash = dbcursor.fetchall()
					***REMOVED***_hash = str(fetched_***REMOVED***_hash).strip("[(',)]")

					# Fetch account_type
					Fetch_Account_Type_Query = 'SELECT ACCOUNT_TYPE FROM ' + TABLE_NAME + ' WHERE EMAIL = %s;'
					dbcursor.execute(Fetch_Account_Type_Query,(email,))
					fetched_account_type = dbcursor.fetchall()
					account_type = str(fetched_account_type).strip("[(',)]")
					# Fetch account_holder_ID
					Fetch_Account_Type_Query = 'SELECT ACCOUNT_HOLDER_ID FROM ' + TABLE_NAME + ' WHERE EMAIL = %s;'
					dbcursor.execute(Fetch_Account_Type_Query,(email,))
					fetched_account_holder_id = dbcursor.fetchall()
					account_holder_id = str(fetched_account_holder_id).strip("[(',)]")
			
					# Verify hash        
					***REMOVED***_verification = sha256_crypt.verify(***REMOVED***, ***REMOVED***_hash)

					# If ***REMOVED*** doesn't match, display error message 
					if ***REMOVED***_verification == False:
						email_***REMOVED***_html = 'Incorrect Email/***REMOVED***'
						return render_template("loginPage.html", email_***REMOVED***_html=email_***REMOVED***_html)
					else:
						# Create session
						session['logged_in'] = True
						session['account_type'] = account_type
						session['account_email'] = email
						session['account_holder_id'] = account_holder_id

					conn.commit()              
					dbcursor.close()              
					conn.close() 
			else:
				print('DB connection error')
		else:
			print('DBFunc error')

		return redirect('searchPage')
	else:
		return render_template('loginPage.html')

@app.route('/logoutPage')
def logoutUser():  

	# Clear all sessions
    session.clear()    
    print("You have been logged out!")
    gc.collect()
    return redirect('searchPage')

@app.route('/registerPage', methods = ['GET', 'POST'])
def render_registerPage():

	if request.method == 'POST':
		email = request.form['email']
		***REMOVED*** = request.form['***REMOVED***']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		confirm_***REMOVED*** = request.form['confirm_***REMOVED***']

		conn = getConnection.getConnection()  
		DB_NAME = 'HORIZON_HOTELS'             
		TABLE_NAME = 'account_holder'

		INSERT_statement = 'INSERT INTO ' + TABLE_NAME + ' (\
			ACCOUNT_HOLDER_ID, FIRST_NAME, LAST_NAME, EMAIL, PASSWORD_HASH, ACCOUNT_TYPE) VALUES (%s, %s, %s, %s, %s, %s);' 

		if conn != None:   
			if conn.is_connected(): 
				print('MySQL Connection is established')                          
				dbcursor = conn.cursor()    
				dbcursor.execute('USE {};'.format(DB_NAME)) 

				# Check if account (email) is already in the database
				Verify_Query = 'SELECT * FROM ' + TABLE_NAME + ' WHERE EMAIL = %s;'
				dbcursor.execute(Verify_Query,(email,))
				rows = dbcursor.fetchall()           
				# If email already in database
				if dbcursor.rowcount > 0:   			
					email_html = 'An account with that email already exists.'
					return render_template("registerPage.html", email_html=email_html)
				elif ***REMOVED*** != confirm_***REMOVED***:
					***REMOVED***_html = 'The entered ***REMOVED*** fields do not match.'
					return render_template("registerPage.html", ***REMOVED***_html=***REMOVED***_html)
				else:
					# If email is not currently in database, add user account details to database

					# Create ***REMOVED*** hash
					***REMOVED***_hashvalue = sha256_crypt.hash(***REMOVED***) 

					# Select maximum account_holder_ID in current table
					dbcursor.execute('SELECT ACCOUNT_HOLDER_ID FROM ' + TABLE_NAME)
					row = dbcursor.fetchall()
					maxAccountHolderID = max(row)
					# Add 1 to the current max ID & assign it to the hotel_ID to be newly added 
					ACCOUNT_HOLDER_ID = str(int(maxAccountHolderID[0]) + 1) 

					dataset = (ACCOUNT_HOLDER_ID, first_name, last_name, email, ***REMOVED***_hashvalue, 'standard')      
					dbcursor.execute(INSERT_statement, dataset)   

					conn.commit()              
					print('INSERT query executed successfully.') 
					dbcursor.close()              
					conn.close() 
			else:
				print('DB connection error')
		else:
			print('DBFunc error')

	return render_template('registerPage.html')

@app.route('/aboutUsPage')
def render_aboutUsPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		print('You are not logged in')
		
	return render_template('aboutUsPage.html', account_type=account_type)

@app.route('/basketPage')
def render_basketPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	if 'bookingDetails' in session:
		# Retrieve booking details sesssions
		location = session['location'] 
		image_link = session['image_link'] 
		numStandard = session['numStandard']
		numDouble = session['numDouble'] 
		numDouble2 = session['numDouble2'] 
		numFamily = session['numFamily'] 
		checkIn = session['checkIn'] 
		checkOut = session['checkOut'] 
		total_days_booked = session['total_days_booked'] 
		total_price_of_stay_before_discount = session['total_price_of_stay_before_discount']
		total_price_of_stay_with_discount = session['total_price_of_stay_with_discount']
		currency = session['currency']

		return render_template('basketPage.html', location=location, image_link=image_link, numStandard=numStandard, numDouble=numDouble, 
				numDouble2=numDouble2, numFamily=numFamily, checkIn=checkIn, checkOut=checkOut, total_days_booked=total_days_booked, 
				total_price_of_stay_before_discount=total_price_of_stay_before_discount, total_price_of_stay_with_discount=total_price_of_stay_with_discount, account_type=account_type, currency=currency)

	else:

		conn = getConnection.getConnection()

		if conn != None:
			print('MySQL Connection is established')
			dbcursor = conn.cursor()
			dbcursor.execute('SELECT DISTINCT CITY FROM HOTEL;')
			rows = dbcursor.fetchall()
			dbcursor.close()
			conn.close()

			locations = []
			for CITY in rows:
				CITY = str(CITY).strip('(')
				CITY = str(CITY).strip(')')
				CITY = str(CITY).strip(',')
				CITY = str(CITY).strip("'")
				locations.append(CITY)

			conn = getConnection.getConnection()

			if conn != None:
				print('MySQL Connection is established')
				dbcursor = conn.cursor()
				# FETCH & CALCULATE TOTAL ROOM CAPACITY, PLUS NUMBER OF DIFFERENT ROOM TYPES

				# Fetch room capacity for selected location
				dbcursor.execute('SELECT ROOM_CAPACITY FROM HOTEL WHERE CITY = %s;', (CITY, ))
				fetched_room_capacity = dbcursor.fetchall() 
				room_capacity = fetched_room_capacity[0][0]

				# Calculate number of different room types
				# Each hotel has 30% standard room; 50% double rooms and 20% Family rooms.
				num_of_standard = int(0.3 * room_capacity)
				num_of_double = int((0.5 * room_capacity)/2)
				num_of_double2 = int((0.5 * room_capacity)/2)
				num_of_family = int(0.2 * room_capacity)

				dbcursor.close()
				conn.close()
			
			return render_template('emptyBasketPage.html', locations=locations, account_type=account_type, num_of_standard=num_of_standard, num_of_double=num_of_double, num_of_double2=num_of_double2, num_of_family=num_of_family)
		else:
			print('DB connection Error')
			return 'DB Connection Error'

@app.route('/paymentPage')
def render_paymentPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'

	# Retieve booking session details 
	location = session['location']
	image_link = session['image_link']
	numStandard = session['numStandard']
	numDouble = session['numDouble']
	numDouble2 = session['numDouble2']
	numFamily = session['numFamily']
	checkIn = session['checkIn']
	checkOut = session['checkOut']
	total_days_booked = session['total_days_booked']
	total_price_of_stay_before_discount = session['total_price_of_stay_before_discount']
	total_price_of_stay_with_discount = session['total_price_of_stay_with_discount']
	currency = session['currency']

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))

		return render_template('paymentPage.html')
	else:
		account_type = 'guest'
		print('You are not logged in')
	
		login_link_html = 'Login/Register'
		login_error_html = 'Login Required: '
		
		return render_template('searchResultsPage.html', login_link_html=login_link_html, login_error_html=login_error_html, location=location, image_link=image_link, numStandard=numStandard, numDouble=numDouble, 
			numDouble2=numDouble2, numFamily=numFamily, checkIn=checkIn, checkOut=checkOut, total_days_booked=total_days_booked, 
			total_price_of_stay_before_discount=total_price_of_stay_before_discount, total_price_of_stay_with_discount=total_price_of_stay_with_discount, account_type=account_type, currency=currency)

@app.route('/paymentConfirmation', methods = ['GET', 'POST'])
def render_paymentConfirmation():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	# Store booking details in database booking table
	# Retieve booking session details 
	location = session['location']
	image_link = session['image_link']
	numStandard = session['numStandard']
	numDouble = session['numDouble']
	numDouble2 = session['numDouble2']
	numFamily = session['numFamily']
	checkIn = session['checkIn']
	checkOut = session['checkOut']
	total_days_booked = session['total_days_booked']
	total_price_of_stay_before_discount = session['total_price_of_stay_before_discount']
	total_price_of_stay_with_discount = session['total_price_of_stay_with_discount']
	currency = session['currency']

	# Retrieve logged in email via session
	email = session['account_email']

	if request.method == 'POST':

		# Check database for email

		conn = getConnection.getConnection()  
		DB_NAME = 'HORIZON_HOTELS'           
		TABLE_NAME = 'account_holder'

		if conn != None:   
			if conn.is_connected():
				print('MySQL Connection is established')                          
				dbcursor = conn.cursor()   
				dbcursor.execute('USE {};'.format(DB_NAME))    

				# Use email to retrieve account holder ID from account_holder table
				Verify_Query = 'SELECT ACCOUNT_HOLDER_ID FROM ' + TABLE_NAME + ' WHERE EMAIL = %s;'
				dbcursor.execute(Verify_Query,(email,))
				fetched_account_holder_ID = str(dbcursor.fetchall())
				account_holder_ID = fetched_account_holder_ID.strip("[(),]''")

				# Use location to retrieve hotel ID from hotel table
				TABLE_NAME = 'hotel'
				Verify_Query = 'SELECT HOTEL_ID FROM ' + TABLE_NAME + ' WHERE CITY = %s;'
				dbcursor.execute(Verify_Query,(location,))
				fetched_hotel_ID = str(dbcursor.fetchall())
				hotel_ID = fetched_hotel_ID.strip("[(),]''")

				# Select booking table for storing data
				TABLE_NAME = 'booking'

				INSERT_statement = 'INSERT INTO ' + TABLE_NAME + ' (\
			BOOKING_ID, STANDARD_ROOMS, DOUBLE_ROOMS, DOUBLE2_ROOMS, FAMILY_ROOMS, RESERVATION_DATE, CHECK_IN_DATE, CHECK_OUT_DATE, TOTAL_NIGHTS_BOOKED, TOTAL_COST_NO_DISCOUNT, TOTAL_COST_DISCOUNTED, ACCOUNT_HOLDER_ID, HOTEL_ID, CURRENCY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

				# Select maximum booking_ID in current table
				dbcursor.execute('SELECT BOOKING_ID FROM ' + TABLE_NAME)
				row = dbcursor.fetchall()
				maxBookingID = max(row)
				# Add 1 to the current max ID & assign it to the booking_ID to be newly added 
				BOOKING_ID = str(int(maxBookingID[0]) + 1)

				# Retrieve the current date for reservationDate
				reservationDate = date.today()

				dataset = (BOOKING_ID, numStandard, numDouble, numDouble2, numFamily, reservationDate, checkIn, checkOut, total_days_booked, total_price_of_stay_before_discount, total_price_of_stay_with_discount, account_holder_ID, hotel_ID, currency)      
				dbcursor.execute(INSERT_statement, dataset)   

				conn.commit()              
				dbcursor.close()              
				conn.close() 

				# Generate and store receipt as txt file

				with open(BOOKING_ID + '_receipt.txt', 'w') as file:
					file.write(
						'Booking ID: ' + str(BOOKING_ID) + '\n' +
						'Location: ' + location + '\n' +
						'Standard Rooms: ' + str(numStandard) + '\n' +
						'Double Rooms: ' + str(numDouble) + '\n' +
						'Double2 Rooms: ' + str(numDouble2) + '\n' +
						'Family Rooms: ' + str(numFamily) + '\n' +
						'Check-in Date: ' + str(checkIn) + '\n' +
						'Check-out Date: ' + str(checkOut) + '\n' +
						'Total Nights Booked: ' + str(total_days_booked) + '\n' +
						'Total Price (without discount): ' + str(total_price_of_stay_before_discount) + '0\n' +
						'Total Price (discounted): ' + str(total_price_of_stay_with_discount) + '0\n' +
						'Currency: ' + str(currency)
					)

					location = session['location']
					image_link = session['image_link']
					numStandard = session['numStandard']
					numDouble = session['numDouble']
					numDouble2 = session['numDouble2']
					numFamily = session['numFamily']
					checkIn = session['checkIn']
					checkOut = session['checkOut']
					total_days_booked = session['total_days_booked']
					total_price_of_stay_before_discount = session['total_price_of_stay_before_discount']
					total_price_of_stay_with_discount
					currency = session['currency']

				# Clear basket/booking details sessions
				session.pop('bookingDetails')    
				image_link = session['image_link']
				gc.collect()
				return render_template('paymentConfirmationPage.html', image_link=image_link)
			else:
				print('DB connection error')
		else:
			print('DBFunc error')

@app.route('/userAccountPage')
def render_userAccountPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	conn = getConnection.getConnection()   
	DB_NAME = 'HORIZON_HOTELS'             
	TABLE_NAME = 'booking'

	if conn != None:    
		if conn.is_connected(): 
			print('MySQL Connection is established')                          
			dbcursor = conn.cursor()    
			dbcursor.execute('USE {};'.format(DB_NAME))    

			# Retrieve booking_ids using user account_holder_id
			account_holder_id = session['account_holder_id'] 
			Verify_Query = 'SELECT BOOKING_ID FROM ' + TABLE_NAME + ' WHERE ACCOUNT_HOLDER_ID = %s;'
			dbcursor.execute(Verify_Query,(account_holder_id,))
			fetched_booking_id = list(dbcursor.fetchall())

			bookings = []
			for BOOKING_ID in fetched_booking_id:
				BOOKING_ID = str(BOOKING_ID).strip('(')
				BOOKING_ID = str(BOOKING_ID).strip(')')
				BOOKING_ID = str(BOOKING_ID).strip(',')
				BOOKING_ID = str(BOOKING_ID).strip("'")
				bookings.append(BOOKING_ID)

			# Create bookings session for if statement for front end display
			if bookings == []:
				session['bookings'] = 'false'
			else:
				session['bookings'] = 'true'
			are_there_bookings = session['bookings']
		
			# Use hotel_id to retrieve location from hotel table
			TABLE_NAME = 'hotel'

			# Retrieve user account email from sessions
			email = session['account_email']
			# Use user email to retrieve first and last name from account_holder table
			TABLE_NAME = 'account_holder'
			Verify_Query = 'SELECT FIRST_NAME FROM ' + TABLE_NAME + ' WHERE EMAIL = %s;'
			dbcursor.execute(Verify_Query,(email,))
			fetched_first_name = str(dbcursor.fetchall())
			first_name = fetched_first_name.strip("[(),]''")
			Verify_Query = 'SELECT LAST_NAME FROM ' + TABLE_NAME + ' WHERE EMAIL = %s;'
			dbcursor.execute(Verify_Query,(email,))
			fetched_last_name= str(dbcursor.fetchall())
			last_name = fetched_last_name.strip("[(),]''")

			conn.commit()              
			dbcursor.close()              
			conn.close() 

			return render_template('userAccountPage.html', are_there_bookings=are_there_bookings, bookings=bookings, first_name=first_name, last_name=last_name, email=email)
		else:
			print('DB connection error')
	else:
		print('DBFunc error')

@app.route('/bookingDetailsPage', methods = ['GET', 'POST'])
def render_bookingDetailsPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	conn = getConnection.getConnection()   
	DB_NAME = 'HORIZON_HOTELS'             
	TABLE_NAME = 'booking'

	if conn != None:   
		if conn.is_connected(): 
			print('MySQL Connection is established')                          
			dbcursor = conn.cursor()   
			dbcursor.execute('USE {};'.format(DB_NAME)) 

			booking_id = request.form['booking_id']

			# Use booking_id to retrieve booking details from booking table
			Verify_Query = 'SELECT * FROM ' + TABLE_NAME + ' WHERE BOOKING_ID = %s;'
			dbcursor.execute(Verify_Query,(booking_id,))
			fetched_booking_details = dbcursor.fetchall()
			booking_details = list(fetched_booking_details)

			numStandard = booking_details[0][1]
			numDouble = booking_details[0][2]
			numDouble2 = booking_details[0][3]
			numFamily = booking_details[0][4]
			checkIn = booking_details[0][6]
			checkOut = booking_details[0][7]
			total_days_booked = booking_details[0][8]
			total_price_of_stay_before_discount = booking_details[0][9]
			total_price_of_stay_with_discount = booking_details[0][10]
			currency = booking_details[0][13]

			# Use hotel_id to retrieve location from hotel table
			TABLE_NAME = 'hotel'
			Verify_Query = 'SELECT CITY FROM ' + TABLE_NAME + ' WHERE HOTEL_ID = %s;'
			dbcursor.execute(Verify_Query,(booking_details[0][12],))
			fetched_location = str(dbcursor.fetchall())
			location = fetched_location.strip("[(),]''")

			conn.commit()              
			dbcursor.close()              
			conn.close()

			return render_template('bookingDetailsPage.html', booking_id=booking_id, location=location, numStandard=numStandard, numDouble=numDouble, numDouble2=numDouble2, numFamily=numFamily, checkIn=checkIn, checkOut=checkOut, total_days_booked=total_days_booked, total_price_of_stay_before_discount=total_price_of_stay_before_discount, total_price_of_stay_with_discount=total_price_of_stay_with_discount, currency=currency)
		else:
			print('DB connection error')
	else:
		print('DBFunc error')

@app.route('/bookingCancellationConfirmationPage', methods = ['GET', 'POST'])
def render_bookingCancellationConfirmationPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	conn = getConnection.getConnection()  
	DB_NAME = 'HORIZON_HOTELS'             
	TABLE_NAME = 'booking'

	if conn != None:   
		if conn.is_connected():
			print('MySQL Connection is established')                          
			dbcursor = conn.cursor()    
			dbcursor.execute('USE {};'.format(DB_NAME))  

			booking_id = request.form['booking_id']

			# Use booking_id to retrieve booking details from booking table
			Verify_Query = 'SELECT * FROM ' + TABLE_NAME + ' WHERE BOOKING_ID = %s;'
			dbcursor.execute(Verify_Query,(booking_id,))
			fetched_booking_details = dbcursor.fetchall()
			booking_details = list(fetched_booking_details)

			numStandard = booking_details[0][1]
			numDouble = booking_details[0][2]
			numDouble2 = booking_details[0][3]
			numFamily = booking_details[0][4]
			checkIn = booking_details[0][6]
			checkOut = booking_details[0][7]
			total_days_booked = booking_details[0][8]
			total_price_of_stay_before_discount = booking_details[0][9]
			total_price_of_stay_with_discount = booking_details[0][10]
			reservation_date = booking_details[0][5]
			currency = booking_details[0][13]

			# Use hotel_id to retrieve location from hotel table
			TABLE_NAME = 'hotel'
			Verify_Query = 'SELECT CITY FROM ' + TABLE_NAME + ' WHERE HOTEL_ID = %s;'
			dbcursor.execute(Verify_Query,(booking_details[0][12],))
			fetched_location = str(dbcursor.fetchall())
			location = fetched_location.strip("[(),]''")

			cancellation_date = date.today()
			days_from_booking_list = pandas.date_range(reservation_date,checkIn, freq='D').strftime("%Y-%m-%d").tolist()
	
			# Variable for counting days between current & check-in date
			days_from_booking = 0
			# Add count to days_in_advance
			for day in days_from_booking_list:
				days_from_booking += 1

			# Calculate cancellation charges incurred
			if days_from_booking >= 60:
				# Zero charges incurred
				cancellation_charge = 0.0
			elif days_from_booking < 60 and days_from_booking > 30:
				# 50% of total is charged
				cancellation_charge = total_price_of_stay_with_discount - (0.5 * total_price_of_stay_with_discount)
			else:
				# Cancel date is within 30 days and 100% of total is charged
				cancellation_charge = total_price_of_stay_with_discount 

			# Calculate total refund
			refund_charges_with_applied = total_price_of_stay_with_discount - cancellation_charge

			# Use booking_id to delete booking from database
			TABLE_NAME = 'booking'
			DELETE_statement = 'DELETE FROM ' + TABLE_NAME + ' WHERE + BOOKING_ID = %s;'
			dbcursor.execute(DELETE_statement, (booking_id,)) 

			conn.commit()              
			dbcursor.close()              
			conn.close() 

			return render_template('bookingCancellationConfirmationPage.html', booking_id=booking_id, location=location, numStandard=numStandard, numDouble=numDouble, numDouble2=numDouble2, numFamily=numFamily, checkIn=checkIn, checkOut=checkOut, total_days_booked=total_days_booked, total_price_of_stay_before_discount=total_price_of_stay_before_discount, total_price_of_stay_with_discount=total_price_of_stay_with_discount, reservation_date=reservation_date, cancellation_date=cancellation_date, cancellation_charge=cancellation_charge, refund_charges_with_applied=refund_charges_with_applied, currency=currency)
		else:
			print('DB connection error')
	else:
		print('DBFunc error')

@app.route('/changePersonalDetailsPage', methods = ['GET', 'POST'])
def render_changePersonalDetailsPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	# Retrieve personal details
	email = request.form['email']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	account_holder_id = session['account_holder_id']

	if request.method == 'POST':

		conn = getConnection.getConnection()  
		DB_NAME = 'HORIZON_HOTELS'             
		TABLE_NAME = 'account_holder'

		if conn != None:    
			if conn.is_connected(): 
				print('MySQL Connection is established')                          
				dbcursor = conn.cursor()    
				dbcursor.execute('USE {};'.format(DB_NAME)) 

				UPDATE_statement = 'UPDATE ' + TABLE_NAME + ' SET \
				FIRST_NAME = %s, \
				LAST_NAME = %s, \
				EMAIL = %s \
				WHERE ACCOUNT_HOLDER_ID = %s;'    

				dataset = (first_name, last_name, email, account_holder_id)
				dbcursor.execute(UPDATE_statement, dataset)

				# Recreate session
				session['account_email'] = email

				conn.commit()              
				dbcursor.close()              
				conn.close()            
			else:
				print('DB connection error')
		else:
			print('DBFunc error')

		return render_template('changePersonalDetailsPage.html', email=email, first_name=first_name, last_name=last_name)

@app.route('/adminAccountPage', methods = ['GET', 'POST'])
def render_adminAccountPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	conn = getConnection.getConnection()
	DB_NAME = 'HORIZON_HOTELS'             
	TABLE_NAME = 'hotel'

	if conn != None:
		print('MySQL Connection is established')
		dbcursor = conn.cursor()

		dbcursor.execute('USE {};'.format(DB_NAME))  
		Verify_Query = 'SELECT HOTEL_ID, CITY FROM ' + TABLE_NAME + ';'
		dbcursor.execute(Verify_Query)
		
		desc = dbcursor.description
		column_names = [col[0] for col in desc]
		hotels = [dict(zip(column_names, row))  
				for row in dbcursor.fetchall()]

		dbcursor.close()
		conn.close()

	else:
		print('DB connection Error')
		return 'DB Connection Error'

	return render_template('adminAccountPage.html', hotels=hotels)

@app.route('/adminHotelDetailsPage', methods = ['GET', 'POST'])
def render_adminHotelDetailsPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	hotel_id = request.form['hotel_id']

	conn = getConnection.getConnection()
	DB_NAME = 'HORIZON_HOTELS'             
	TABLE_NAME = 'hotel'

	if conn != None:
		print('MySQL Connection is established')
		dbcursor = conn.cursor()

		dbcursor.execute('USE {};'.format(DB_NAME)) 
		Verify_Query = 'SELECT CITY, ROOM_CAPACITY, ON_PEAK_SEASON_PRICE, OFF_PEAK_SEASON_PRICE FROM ' + TABLE_NAME + ' WHERE HOTEL_ID = ' + hotel_id + ';'
		dbcursor.execute(Verify_Query)
		hotel_details = dbcursor.fetchall()
		
		location = hotel_details[0][0]
		room_capacity = hotel_details[0][1]
		on_peak = hotel_details[0][2]
		off_peak = hotel_details[0][3]

		dbcursor.close()
		conn.close()

	else:
		print('DB connection Error')
		return 'DB Connection Error'

	return render_template('adminHotelDetailsPage.html', hotel_id=hotel_id, location=location, room_capacity=room_capacity, on_peak=on_peak, off_peak=off_peak)

@app.route('/changeHotelDetailsPage', methods = ['GET', 'POST'])
def render_changeHotelDetailsPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	# Retrieve personal details
	location = request.form['location']
	room_capacity = request.form['room_capacity']
	on_peak = request.form['on_peak']
	off_peak = request.form['off_peak']
	hotel_id = request.form['hotel_id']

	if request.method == 'POST':

		conn = getConnection.getConnection()   
		DB_NAME = 'HORIZON_HOTELS'            
		TABLE_NAME = 'hotel'

		if conn != None:   
			if conn.is_connected(): 
				print('MySQL Connection is established')                          
				dbcursor = conn.cursor()    
				dbcursor.execute('USE {};'.format(DB_NAME))

				UPDATE_statement = 'UPDATE ' + TABLE_NAME + ' SET \
				CITY = %s, \
				ROOM_CAPACITY = %s, \
				ON_PEAK_SEASON_PRICE = %s, \
				OFF_PEAK_SEASON_PRICE = %s \
				WHERE HOTEL_ID = %s;'    

				dataset = (location, room_capacity, on_peak, off_peak, hotel_id)
				dbcursor.execute(UPDATE_statement, dataset)

				conn.commit()              
				dbcursor.close()              
				conn.close() #Connection must be closed             
			else:
				print('DB connection error')
		else:
			print('DBFunc error')

		return render_template('adminHotelDetailsPage.html', hotel_id=hotel_id, location=location, room_capacity=room_capacity, on_peak=on_peak, off_peak=off_peak)

@app.route('/adminDeleteHotelPage', methods = ['GET', 'POST'])
def render_adminDeleteHotelPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	hotel_id = request.form['hotel_id']

	conn = getConnection.getConnection()   
	DB_NAME = 'HORIZON_HOTELS'            
	TABLE_NAME = 'hotel'
    
	DELETE_statement = 'DELETE FROM ' + TABLE_NAME + ' WHERE HOTEL_ID = %s;'    

	if conn != None:    
		if conn.is_connected(): 
			print('MySQL Connection is established')
			dbcursor = conn.cursor()    
			dbcursor.execute('USE {};'.format(DB_NAME)) 
			dbcursor.execute(DELETE_statement, (hotel_id,))
			
			conn.commit()
			print('DELETE statement executed successfully.')
			dbcursor.close()
			conn.close() 
		else:
			print('DB connection error')
	else:
		print('DBFunc error')

	return redirect(url_for('render_adminAccountPage', hotel_id=hotel_id))

@app.route('/adminAddHotelPage', methods = ['GET', 'POST'])
def render_adminAddHotelPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	conn = getConnection.getConnection()
	DB_NAME = 'HORIZON_HOTELS'            
	TABLE_NAME = 'hotel'

	if conn != None:    
		if conn.is_connected(): 
			print('MySQL Connection is established')
			dbcursor = conn.cursor()    
			dbcursor.execute('USE {};'.format(DB_NAME)) 

            # Select maximum hotel_ID in current table
			dbcursor.execute('SELECT HOTEL_ID FROM hotel;')
			row = dbcursor.fetchall()
			maxHotelID = max(row)
            # Add 1 to the current max ID & assign it to the hotel_ID to be newly added 
			hotel_id = str(int(maxHotelID[0]) + 1) 
			print(hotel_id)

			conn.commit()
			print('INSERT query executed successfully.')
			dbcursor.close()
			conn.close()
		else:
			print('DB connection error')
	else:
		print('DBFunc error')

	return render_template('adminAddHotelPage.html', hotel_id=hotel_id)

@app.route('/adminHotelAdded', methods = ['GET', 'POST'])
def render_adminHotelAdded():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	conn = getConnection.getConnection()
	DB_NAME = 'HORIZON_HOTELS'             
	TABLE_NAME = 'hotel'

	INSERT_statement = 'INSERT INTO ' + TABLE_NAME + ' (\
        HOTEL_ID, CITY, ROOM_CAPACITY, ON_PEAK_SEASON_PRICE, OFF_PEAK_SEASON_PRICE) VALUES (%s, %s, %s, %s, %s);'    

	if conn != None:    
		if conn.is_connected(): 
			print('MySQL Connection is established')
			dbcursor = conn.cursor()   
			dbcursor.execute('USE {};'.format(DB_NAME))

			if request.method == 'POST':
				hotel_id = request.form['hotel_id']
				location = request.form['location']
				room_capacity = request.form['room_capacity']
				on_peak = request.form['on_peak']
				off_peak = request.form['off_peak'] 
			
				dataset = (hotel_id, location, room_capacity, on_peak, off_peak)
				dbcursor.execute(INSERT_statement, dataset)

			conn.commit()
			print('INSERT query executed successfully.')
			dbcursor.close()
			conn.close() 
		else:
			print('DB connection error')
	else:
		print('DBFunc error')

	return redirect(url_for('render_adminAddHotelPage', hotel_id=hotel_id, location=location, room_capacity=room_capacity, on_peak=on_peak, off_peak=off_peak))

@app.route('/adminBookingsPage', methods = ['GET', 'POST'])
def render_adminBookingsPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	conn = getConnection.getConnection()
	DB_NAME = 'HORIZON_HOTELS'            
	TABLE_NAME = 'booking'

	if conn != None:
		print('MySQL Connection is established')
		dbcursor = conn.cursor()

		hotel_id = request.form['hotel_id']

		dbcursor.execute('USE {};'.format(DB_NAME)) 
		Verify_Query = 'SELECT BOOKING_ID, CHECK_IN_DATE, CHECK_OUT_DATE FROM ' + TABLE_NAME + ' WHERE HOTEL_ID = ' + hotel_id + ' AND ACCOUNT_HOLDER_ID NOT IN (1000);'
		dbcursor.execute(Verify_Query)
		
		desc = dbcursor.description
		column_names = [col[0] for col in desc]
		bookings = [dict(zip(column_names, row))  
				for row in dbcursor.fetchall()]

		dbcursor.close()
		conn.close()

	else:
		print('DB connection Error')
		return 'DB Connection Error'

	return render_template('adminBookingsPage.html', bookings=bookings)

@app.route('/adminBookingDetailsPage', methods = ['GET', 'POST'])
def render_adminBookingDetailsPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	booking_id = request.form['booking_id']

	conn = getConnection.getConnection()
	DB_NAME = 'HORIZON_HOTELS'             
	TABLE_NAME = 'booking'

	if conn != None:
		print('MySQL Connection is established')
		dbcursor = conn.cursor()

		dbcursor.execute('USE {};'.format(DB_NAME)) 
		Verify_Query = 'SELECT STANDARD_ROOMS, DOUBLE_ROOMS, DOUBLE2_ROOMS, FAMILY_ROOMS, RESERVATION_DATE, CHECK_IN_DATE, CHECK_OUT_DATE, TOTAL_NIGHTS_BOOKED, TOTAL_COST_NO_DISCOUNT, TOTAL_COST_DISCOUNTED, ACCOUNT_HOLDER_ID, HOTEL_ID, CURRENCY FROM ' + TABLE_NAME + ' WHERE BOOKING_ID = ' + booking_id + ';'
		dbcursor.execute(Verify_Query)
		booking_details = dbcursor.fetchall()
		
		standard = booking_details[0][0]
		double = booking_details[0][1]
		double2 = booking_details[0][2]
		family = booking_details[0][3]
		reservation_date = booking_details[0][4]
		check_in = booking_details[0][5]
		check_out = booking_details[0][6]
		total_nights = booking_details[0][7]
		total_cost_no_discount = booking_details[0][8]
		total_cost_discounted = booking_details[0][9]
		account_holder_id = booking_details[0][10]
		hotel_id = booking_details[0][11]
		currency = booking_details[0][12]

		dbcursor.close()
		conn.close()

	else:
		print('DB connection Error')
		return 'DB Connection Error'

	return render_template('adminBookingDetailsPage.html', booking_id=booking_id, standard=standard, double=double, double2=double2, family=family, reservation_date=reservation_date, check_in=check_in, check_out=check_out, total_nights=total_nights, total_cost_no_discount=total_cost_no_discount, total_cost_discounted=total_cost_discounted, account_holder_id=account_holder_id, hotel_id=hotel_id, currency=currency)

@app.route('/adminDeleteBookingPage', methods = ['GET', 'POST'])
def render_adminDeleteBookingPage():

	if 'logged_in' in session:
		logged_in = session['logged_in']
		print(session)
		print('Logged in as ' + str(logged_in))
		if 'account_type' in session:
			account_type = session['account_type']
			print('Account type is ' + str(account_type))
	else:
		account_type = 'guest'
		return redirect('loginPage')

	conn = getConnection.getConnection()   
	DB_NAME = 'HORIZON_HOTELS'            
	TABLE_NAME = 'booking'

	if conn != None:    
		if conn.is_connected(): 
			print('MySQL Connection is established')                          
			dbcursor = conn.cursor()   
			dbcursor.execute('USE {};'.format(DB_NAME)) 

			booking_id = request.form['booking_id']

			# Use booking_id to delete booking from database
			DELETE_statement = 'DELETE FROM ' + TABLE_NAME + ' WHERE + BOOKING_ID = %s;'
			dbcursor.execute(DELETE_statement, (booking_id,)) 

			conn.commit()              
			dbcursor.close()              
			conn.close() 

			return render_template('adminDeleteBookingPage.html', booking_id=booking_id)
		else:
			print('DB connection error')
	else:
		print('DBFunc error')



if __name__ == '__main__':
    app.run(debug=True)