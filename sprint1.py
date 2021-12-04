
import flask  #install flask
from flask import jsonify #install jsonify from flask
from flask import request, make_response 
import mysql.connector  #imports the connector for mysql
from mysql.connector import Error  
from sql1 import create_connection   #grabs create connection function from sql1 file
from sql1 import execute_query       #grabs execute query function from sql1 file
from sql1 import execute_read_query    #grabs execute read query from sql1 file
import random
from flask_cors import CORS

#creates a connect to the AWS database for user1 table
conn = create_connection("cis3368fall2021.cx2um3wbtrjd.us-east-2.rds.amazonaws.com", "admin","Talon4873!", "cis3368fall21") 
cursor = conn.cursor(dictionary=True)
sql = "SELECT * FROM users1"
cursor.execute(sql)
rows = cursor.fetchall()

#application name
app = flask.Flask(__name__) 
CORS(app)
app.config["DEBUG"] = True #allows application to show errors

#GET Method to show connectivity between python and the API files
@app.route('/', methods=['GET'])  
def home(): 
    return "Welcome"

@app.route('/api/createUser', methods=['POST'])
def createUser():
    request_data = request.get_json()   #requests data is json format
    request_data = request_data['body']
    newfirstname = request_data['firstname']       #grabs name from json format and turns it into a variable
    newlastname = request_data['lastname']   #grabs distance from json format and turns it into a variable
    newbirthdate = request_data['birthdate']
    rows.append({'firstname': newfirstname, 'lastname': newlastname, 'birthdate': newbirthdate})
    #statement to insert data into the AWS database in the users1 table
    insert_statement = "INSERT INTO users1 (firstname, lastname, birthdate) VALUES ('%s','%s','%s')" % (newfirstname, newlastname, newbirthdate)
    #executes
    execute_query(conn, insert_statement)

    queryByName = "SELECT * FROM users1 WHERE firstname = '%s'" % (newfirstname)
    res = execute_read_query(conn, queryByName)
    userid = res[0]['id']

    return jsonify({
    	"success": 'true',
    	"userid": userid
    })


@app.route('/api/deleteUser', methods=['POST']) #api files using POST method
def deleteUser():
        request_data = request.get_json() #request data in json format
        request_data = request_data['body']
        delete_first = request_data['firstname']       #grabs name from json format and turns it into a variable
        delete_last = request_data['lastname']   #grabs distance from json format and turns it into a variable
        delete_bday = request_data['birthdate']
        delete_statement = "DELETE FROM users1 WHERE firstname = '%s' AND lastname = '%s' AND birthdate= '%s'" % (delete_first, delete_last, delete_bday) #delete statement that deletes user from AWS database
        #executes
        execute_query(conn, delete_statement)

        #returns message if delete request was sent
        return 'DELETE REQUEST SENT'

@app.route('/api/updateLast', methods=['POST'])#api files using POST method
def updateLast():
    request_data = request.get_json()   #requests data is json format
    request_data = request_data['body']
    existing_first = request_data['firstname']  #grabs name from json format and turns it into a variable
    updated_last = request_data['lastname']  #grabs name from json format and turns it into a variable
    user_bday = request_data['birthdate']
    update_lastname_statement = "UPDATE users1 SET lastname = '%s' WHERE firstname ='%s' AND birthdate ='%s'" % (updated_last,existing_first,user_bday)
    #update statement that updates users last name
    execute_query(conn, update_lastname_statement)

    return jsonify({'response': 'User last name has been updated'})

@app.route('/api/updateFirst', methods=['POST'])#api files using POST method
def updateFirst():
    request_data = request.get_json()   #requests data is json format
    print(request_data)
    request_data = request_data['body']
    existing_last = request_data['lastname']  #grabs name from json format and turns it into a variable
    updated_first = request_data['firstname']  #grabs name from json format and turns it into a variable
    user_bday = request_data['birthdate']
    update_firstname_statement = "UPDATE users1 SET firstname = '%s' WHERE lastname ='%s' AND birthdate ='%s'" % (updated_first,existing_last,user_bday)
    #updates first name based on input from lastname and birthdate
    execute_query(conn, update_firstname_statement)

    return jsonify({'response': 'User first name has been updated'})

@app.route('/api/userlist', methods=['GET']) #api files using GET method
def userList():
    conn = create_connection("cis3368fall2021.cx2um3wbtrjd.us-east-2.rds.amazonaws.com", "admin","Talon4873!", "cis3368fall21") 
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM users1"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return jsonify(rows)

#creates a connect to the AWS database to the restaurants table
conn = create_connection("cis3368fall2021.cx2um3wbtrjd.us-east-2.rds.amazonaws.com", "admin","Talon4873!", "cis3368fall21") 
cursor2 = conn.cursor(dictionary=True)
sql1 = "SELECT * FROM restaurants"
cursor2.execute(sql1)
rows2= cursor2.fetchall()

#API for adding a restauraunt 
@app.route('/api/createRestaurant', methods=['POST'])
def createRestaurant():
    request_data = request.get_json()  
    request_data = request_data['body']
    restaurant_name= request_data['restaurantname']  
    userid= request_data['userid']  
    rows2.append({'restaurantname': restaurant_name})     
    rows2.append({'userid': userid})     
    #statement to insert 
    insert_statement = "INSERT INTO restaurants (restaurantname, userid) VALUES ('%s', '%d')" % (restaurant_name, userid)
    #executes
    execute_query(conn, insert_statement)

    return 'restaurant created!'

#for the UPDATE portion of the restaurant, just delete the restaurant and create a new one.

#API to show restauraunt list
@app.route('/api/restaurantList', methods=['GET'])
def restaurantList():
    cursor2.execute(sql1)
    rows2= cursor2.fetchall()
    return jsonify(rows2)

#API to select restauraunt
@app.route('/api/selectRestaurant', methods=['POST'])
def selectRestaurant():
    try:
        request_data = request.get_json()  
        request_data = request_data['body']
        userid = request_data['userid']  
        rows2.append({'userid': userid}) 
        select_statement = "SELECT * FROM restaurants WHERE userid = '%d'" % (userid)      
        random_restaurant = execute_read_query(conn, select_statement)   #reads sorted data
        res = random_restaurant[random.randint(0, len(random_restaurant)-1)]
    except:
        select_statement = "SELECT * FROM restaurants"
        random_restaurant = execute_read_query(conn, select_statement)   #reads sorted data
        res = random_restaurant[random.randint(0, len(random_restaurant)-1)]
        
    return jsonify({'response': res})
# used random int and length of table to pick random restaurant

@app.route('/api/deleteRestaurant', methods=['POST']) #api files using POST method
#function to delete object from AWS database
def deleteRestaurant():
        request_data = request.get_json() #request data in json format
        request_data = request_data['body']
        delete_restaurant = request_data['restaurantname'] #grabs id from json format and turns into a variable
        delete_statement = "DELETE FROM restaurants WHERE restaurantname = '%s'" % (delete_restaurant) #delete statement that deletes ID from AWS database
        #execut
        execute_query(conn, delete_statement)

        #returns message if delete request was sent
        return 'DELETE REQUEST SENT'
        
app.run() #runs app until prompted to quit

#citations : https://www.geeksforgeeks.org/get-post-requests-using-python/
#crudops.py  https://www.quackit.com/mysql/workbench/create_a_table.cfm
#restapi.py  https://www.w3schools.com/sql/sql_datatypes.asp
#sql.py      http://www.edu4java.com/en/sql/sql6.html
#HW1         https://stackoverflow.com/questions/3090175/find-the-greatest-number-in-a-list-of-numbers

