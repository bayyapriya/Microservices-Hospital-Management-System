from atexit import register
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__, template_folder="templates")
app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Govinda1@'
app.config['MYSQL_DB'] = 'newmicro'
 
mysql = MySQL(app)
 
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/login', methods = ['POST', 'GET'])

def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        Username = request.form['Username']
        Password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE Username = % s AND Password = % s', (Username, Password, ))
        login = cursor.fetchone()
        if login:
            session['loggedin'] = True
            session['Username'] = login['Username']
            session['Password'] = login['Password']
            cursor.execute("INSERT INTO login(Username,Password)VALUES(%s,  %s)",(Username,Password))
            mysql.connection.commit()
            msg = 'Logged in successfully !'
        else:
            msg = 'Incorrect Username / Password !'
    return msg
 
        

@app.route('/register',methods = ['POST', 'GET'])
def r():
    if request.method == 'GET':
        return render_template('register.html')
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form and 'Email' in request.form :
        Username = request.form['Username']
        Password = request.form['Password']
        Email = request.form['Email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE username = % s', (Username, ))
        register = cursor.fetchone()
        if register:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', Username):
            msg = 'Username must contain only characters and numbers !'
        elif not Username or not Password or not Email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO register VALUES (% s, % s, % s)', (Username, Password, Email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return msg

@app.route('/list')
def lis():
    return render_template('List.html')

@app.route('/appointment',methods = ['POST', 'GET'])
def appo():
    if request.method == 'GET':
        return render_template('appointment.html')
    if request.method == 'POST':
        PATIENTNAME = request.form['PATIENTNAME']
        PATIENTAGE = request.form['PATIENTAGE']
        BOOKDATE = request.form['BOOKDATE']
        BOOKTIME = request.form['BOOKTIME']
        DOCTORNAME = request.form['DOCTORNAME']
        SPECIALITY = request.form['SPECIALITY']
        FEES = request.form['FEES']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO appointment VALUES(%s, %s, %s, %s, %s, %s, %s)',(PATIENTNAME, PATIENTAGE, BOOKDATE, BOOKTIME, DOCTORNAME, SPECIALITY, FEES))
        mysql.connection.commit()
        return "Your appointment is booked successfully!!"

@app.route('/payment',methods = ['POST', 'GET'])
def pay():
    if request.method == 'GET':
        return render_template('payment.html')
    if request.method == 'POST':
        Fullname = request.form['Fullname']
        Nickname = request.form['Nickname']
        Email = request.form['Email']
        DOB =request.form['DOB']
        Gender = request.form['Gender']
        Cardnumber = request.form['Cardnumber']
        Cvv = request.form['Cvv']
        Expdate = request.form['Expdate']
        Amount = request.form['Amount']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO payment VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)',(Fullname, Nickname, Email, DOB, Gender, Cardnumber, Cvv, Expdate, Amount ))
        mysql.connection.commit()
        return "done!!"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
