import hashlib
# import pickle

import logging
import numpy as np
import pandas as pd
from sklearn.svm import SVC

import pymysql
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message

db = pymysql.connect(host='localhost',
                     user='root',
                     password='',
                     database='cardioAly',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
app.secret_key = 'tawanda91'
emailId = 'mailbip14@gmail.com'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=emailId,
    MAIL_PASSWORD='yebankryyxwilflg'
)
mail = Mail(app)

# file = open('C:/xampp/htdocs/HEART-DISEASE-PREDICTION-SYSTEM-main/model.pkl', 'rb')
# clf1 = pickle.load(file)
# file.close()

df = pd.read_csv('C:/xampp/htdocs/HEART-DISEASE-PREDICTION-SYSTEM-main/heart.csv')
x_val = df.iloc[0:, 0:len(df.columns) - 1].values
y_val = df.iloc[0:, -1].values
clf = SVC(kernel='rbf', C=2)
clf.fit(x_val, y_val)

app.secret_key = 'don\'t tell anyone'


@app.route('/', methods=["GET", "POST"])
def main_page():
    return render_template('index.html')


@app.route('/', methods=["GET", "POST"])
def service_page():
    return render_template('service.html')


@app.route('/appointment', methods=["GET", "POST"])
def appointment():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM doctors order by speciality asc")
    # Fetch all records and use a loop to print out
    data = cursor.fetchall()
    if request.method == 'GET':
        return render_template('appointment.html', data=data)
    # if email=="" else email
    elif request.method == 'POST':
        name = request.form['name']
        phnNo = request.form['phnNo']
        email = request.form['email']
        doctorName = request.form['doctorName']
        symptoms = request.form['symptoms']
        date = request.form['date']
        msg = Message('Patient Name: ' + name, sender=email, recipients=[emailId])
        msg.body = "Patient Name: " + name + "\n PhoneNo: " + phnNo + "\n Email: " + email + "\n Appointed Doctor: " + doctorName + "\n Date: " + date + "Symptoms: " + symptoms
        mail.send(msg)
        flash("Appointment Sent for Approval.")
        return render_template('appointment.html', data=data)


@app.route('/test', methods=["GET", "POST"])
def test_page():
    if request.method == "POST":
        myDict = request.form
        while True:
            try:
                age = int(myDict['age'])
                break
            except ValueError:
                render_template('SAT.HTML')
        sex = int(myDict['sex'])
        cp = int(myDict['cp'])
        while True:
            try:
                trestbps = int(myDict['trestbps'])
                break
            except ValueError:
                render_template('SAT.HTML')
        while True:
            try:
                chol = int(myDict['chol'])
                break
            except ValueError:
                render_template('SAT.HTML')
        fbs = int(myDict['fbs'])
        restecg = int(myDict['restecg'])
        while True:
            try:
                thalach = int(myDict['thalach'])
                break
            except ValueError:
                render_template('SAT.HTML')
        exang = int(myDict['exang'])
        while True:
            try:
                oldpeak = int(myDict['oldpeak'])
                break
            except ValueError:
                render_template('SAT.HTML')
        slope = int(myDict['slope'])
        while True:
            try:
                ca = int(myDict['ca'])
                break
            except ValueError:
                render_template('SAT.HTML')
        thal = int(myDict['thal'])
        inputFeatures = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        infProb = clf.predict([inputFeatures])
        logging.info("this is log", infProb)
        if infProb == [1]:
            s = "You may have heart problem! Please Visit the Doctor!"
            return render_template('result.html', inf=s)
        elif infProb == [0]:
            s = "Cogratulations! You don't have any heart problem...\nBut if you feel sick than check out the links below!"
            return render_template('result.html', inf=s)
    return render_template('SAT.html')


@app.route('/about', methods=["GET", "POST"])
def about_page():
    return render_template('about.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'GET':
        flash("Wellcome to signIn")
        return render_template('signin.html')
    else:
        form_secure = 'This$#is#$my#$Secret@#Key!@#'
        form_key = request.form['form_secure']
        # check if form security key is present
        if form_key and form_key == form_secure:
            # collect login-form inputs
            username = request.form['username']
            password = request.form['password']
            h = hashlib.md5(password.encode())
            password = h.hexdigest()
            # user_group from database
            if request.method == 'POST' and username and password:
                # Check if account exists using MySQL
                cursor = db.cursor()
                sql = 'SELECT * FROM usersTable WHERE username = %s'
                cursor.execute(sql, username)
                # Fetch one record and return result
                account = cursor.fetchone()
                # If account exists in usersTable table in out database
                if username == account['username'] and password == account['password']:
                    session['signin'] = True
                    session['username'] = username
                    session['sessionkey'] = password
                    flash('Welcome, ' + username + ' to Cardio-Aly')
                    return render_template('index.html')
                else:
                    flash("Username/Password combination wrong!")
                    return render_template('signin.html')
            else:
                flash("Something went wrong!")
                return render_template('signin.html')
        else:
            flash("Something went wrong!")
            return render_template('signin.html')


@app.route('/signup')
def signup():
    flash("Welcome to SignUp Form!")
    return render_template('signup.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    # adding a key to secure form against injection
    # can further encrypt this key
    form_secure = 'This$#is#$my#$Secret@#Key!@#'
    form_key = request.form['form_secure']
    # check if form security key is present
    if form_key and form_key == form_secure:
        username = request.form['username']
        password = request.form['password']
        # encode our user submitted password
        h = hashlib.md5(password.encode())
        password = h.hexdigest()

        email = request.form['email']
        password2 = request.form['password2']
        if password != password2:
            flash('Error! User Password Mismatched')
            return render_template('signup.html')

        # check that all fields have been submitted
        if request.method == 'POST' and username and password and email:

            # Check if account exists using MySQL
            cursor = db.cursor()
            sql = 'SELECT * FROM usersTable WHERE username = %s'
            cursor.execute(sql, username)
            # Fetch one record and return result
            account = cursor.fetchone()
            # If account exists in usersTable table in out database
            if account:
                flash('Error! User account or email already exists!')
                return render_template('signup.html')
            else:
                cursor.execute('INSERT INTO usersTable VALUES (NULL, %s, %s, %s)', (username, email, password))
                # the connection is not autocommited by default. So we must commit to save our changes.
                db.commit()
                flash('successfully registered! Continue to Login.')
                return render_template('signin.html')
        else:
            flash('something went wrong')
            return render_template('signup.html')

    # return 'successfully regestered user: '+ username
    else:
        flash('something went wrong')
        return render_template('signup.html')


@app.route('/signout')
def signout():
    session.pop('signin', None)
    session.pop('username', None)
    session.pop('sessionkey', None)
    return redirect(url_for('signin'))


@app.route('/profile')
def profile():
    username = session['username']
    sessionkey = session['sessionkey']
    # Check if account exists using MySQL
    cursor = db.cursor()
    sql = 'SELECT * FROM usersTable WHERE username = %s'
    cursor.execute(sql, username)
    # Fetch one record and return result
    account = cursor.fetchone()
    # If account exists in usersTable table in out database
    if username == account['username']:
        return render_template('profile.html', userid=account['id'], username=account['username'],
                               email=account['email'])

    else:
        return 'No matching record found!'


# doctor_part
@app.route('/doctors')
def doctors():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM doctors")
    # Fetch all records and use a loop to print out
    data = cursor.fetchall()
    return render_template('doctors.html', data=data)


@app.route('/addDoctors', methods=['POST', 'GET'])
def addDoctors():
    if request.method == 'GET':
        return render_template('addDoctors.html')

    elif request.method == 'POST':
        name = request.form['name']
        speciality = request.form['speciality']
        NMCnumber = request.form['NMCnumber']
        contacts = request.form['contacts']
        mailId = request.form['mailId']
        workSpace = request.form['workSpace']
        if name and mailId:
            cursor = db.cursor()
            sql = 'SELECT * FROM doctors WHERE name = %s and NMCnumber=%s'
            cursor.execute(sql, (name, int(NMCnumber)))
            # Fetch one record and return result
            account = cursor.fetchone()
            if account:
                flash('Error! Doctor already exists!')
                return render_template('addDoctors.html')
            else:
                try:
                    cursor.execute('INSERT INTO doctors VALUES (NULL, %s, %s, %s, %s, %s, %s)',
                                   (name, speciality, NMCnumber, contacts, mailId, workSpace))
                    # the connection is not autocommited by default. So we must commit to save our changes.
                    db.commit()
                    flash('successfully registered Doctor ' + str(name) + ' Info.')
                except:
                    db.rollback()
                    flash('Cannot registered Doctor ' + str(name) + ' Info.')
                return redirect(url_for('doctors'))
        else:
            flash('Name and MailId is required')
            return render_template('addDoctors.html')
    else:
        flash('something went wrong')
        return render_template('doctors.html')


# upate doctor
# get
@app.route('/updateD/<int:id>/')
def updateD(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM doctors where id = %s order by name asc", (id,))
    # Fetch one record and return result
    data = cursor.fetchone()
    if len(data) == 0:
        flash('not found record in database')
        return redirect(url_for('doctors'))
    else:
        session['updateDoc'] = id
        return render_template('updateD.html', data=data)


# post
@app.route('/updateDoctor', methods=['POST'])
def updateDoctor():
    if request.method == 'POST':
        cursor = db.cursor()
        name = request.form['name']
        speciality = request.form['speciality']
        NMCnumber = request.form['NMCnumber']
        contacts = request.form['contacts']
        mailId = request.form['mailId']
        workSpace = request.form['workSpace']
        if name and mailId:
            try:
                cursor.execute(
                    "UPDATE doctors set name = %s, speciality = %s, NMCnumber = %s, contacts = %s, mailId = %s, workSpace = %s where id = %s",
                    (name, speciality, int(NMCnumber), contacts, mailId, workSpace, int(session['updateDoc'])))
                db.commit()
                flash('A Doctore ' + str(name) + ' Info has been updated')
            except:
                db.rollback()
                flash('A Doctore Info can not be updated')

        else:
            flash('Name and mailId is required')

    session.pop('updateDoc', None)
    return redirect(url_for('doctors'))


# delete Doctor
@app.route('/deleteD/<int:id>/')
def deleteD(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM doctors where id = %s order by name asc", (id,))
    # Fetch one record and return result
    data = cursor.fetchone()
    if len(data) == 0:
        flash('not found record in database')
        return redirect(url_for('doctors'))
    else:
        session['deleteDoc'] = id
        return render_template('deleteD.html', data=data)


@app.route('/deleteDoctor', methods=['POST'])
def deleteDoctor():
    if request.method == 'POST':
        cursor = db.cursor()
        docId = session['deleteDoc']
        if docId:
            try:
                cursor.execute("DELETE FROM doctors where id = %s", (docId,))
                db.commit()
                flash('A Doctore Info has been deleted')
            except:
                db.rollback()
                flash('A Doctore Info can not be deleted')

        else:
            flash('Doctore Id is required')

    session.pop('deleteDoc', None)
    return redirect(url_for('doctors'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True)
