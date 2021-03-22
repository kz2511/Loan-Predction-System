# -*- coding: utf-8 -*-
import pymysql.connections
from flask import Flask, render_template, request, redirect, session
import os
import pickle
import hashlib
import mysql.connector

# creating the Flask class object
app = Flask(__name__)
model = pickle.load(open('./Model/loanpred.pkl', 'rb'))
app.secret_key = os.urandom(24)
# connection with database
connection = pymysql.connect(host="localhost", user="root", password="", database="loan_prediction")
cursor = connection.cursor()
# decorator defines
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/singin')
def singin():
    return render_template('sing.html')


@app.route('/login_validation', methods=["POST"])
def loginvaldation():
    userid = request.form.get('userid')
    password = request.form.get('password')
    mobile_number = request.form.get('mobile_number')
    val = (userid,)
    val_sql = 'SELECT * FROM USER_DATA WHERE USER_ID = %s'
    cursor.execute(val_sql, val)
    USER_DATA = cursor.fetchall()
    USER_DATA = list(USER_DATA[0])
    print(USER_DATA)

    if password == USER_DATA[-1]:
        return redirect('/home')
    else:
        print("Something went wrong")
        return redirect('/')


@app.route('/add_user', methods=['POST'])
def adduser():
    userid = request.form.get('userid')
    email = request.form.get('email')
    mobile_number = request.form.get('mobile_number')
    fullname = request.form.get('fullname')
    password = request.form.get('password')
    con_password = request.form.get('con_password')

    query = "INSERT INTO USER_DATA (USER_ID, EMAILADDRESS, MOBILE_NUMBER,FULL_NAME,PASSWORD,conf_PASSWORD) " \
            "VALUES('%s','%s','%s','%s','%s','%s')" % (userid, email, mobile_number, fullname, password, con_password)

    val = (userid,)
    val_sql = 'SELECT * FROM USER_DATA WHERE USER_ID = %s'
    if password != con_password:
        return render_template('sing.html', passvali=1)

    cursor.execute(val_sql, val)
    USER_DATA = cursor.fetchall()
    # USER_DATA = list(USER_DATA[0])
    if len(USER_DATA) > 0:
        return render_template('sing.html', status=1)
    else:
        cursor.execute(query)
        connection.commit()
        return redirect('/home')


@app.route("/logout")
def logout():
    return redirect('/')


@app.route("/predction")
def predction():
    return render_template('predction.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.method == 'POST':
            fn = request.form['fn']
            ln = request.form['ln']
            acc = int(request.form['acc'])
            gen = float(request.form['gen'])
            mar = float(request.form['mar'])
            dep = float(request.form['dep'])
            edu = int(request.form['edu'])
            emp = int(request.form['emp'])
            property = int(request.form['property'])
            credit = int(request.form['credit'])
            income = int(request.form['income'])
            caincome = int(request.form['caincome'])
            laamount = int(request.form['laamount'])
            duration = int(request.form['duration'])

            features = [[gen,acc,mar,dep,edu,emp,property,credit,income,caincome,laamount,duration]]
            prediction = model.predict(features)
            lc = [str(i) for i in prediction]
            ans = int("".join(lc))
            print(ans)
            cusname = "Hello Sir "+fn+' '+ln
            acc = "Bank Account Number: " + str(acc)
            if ans == 0:
                mopred = "Sorry! According to Our Calculations you will not get the loan from Bank."
                return render_template('predict.html',cus_name = cusname,acc_no =acc,prediction_text=mopred )
            else:
                print(ans)
                mopred = "Congratulations! According to Our Calculation you will get the loan from Bank."
                return render_template('predict.html', cus_name=cusname, acc_no=acc, prediction_text=mopred)
    except Exception as e:
        print(e)
        return render_template('predict.html',  prediction_text="Something went wrong!!!")


if __name__ == '__main__':
    app.run(debug=True)
# -*- coding: utf-8 -*-
