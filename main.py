# -*- coding: utf-8 -*-
import pymysql.connections
from flask import Flask, render_template, request, redirect, session
import os
import pickle
import hashlib
from sklearn.linear_model import _logistic as logistic


# creating the Flask class object
app = Flask(__name__)
model = pickle.load(open('./Model/loanpred1_tree.pkl', 'rb'))
app.secret_key = os.urandom(24)
# connection with database
connection = pymysql.connect(host="localhost", user="root", password="", database="loan_prediction_system")
cursor = connection.cursor()


# decorator defines
## Admin Code Part is Here
@app.route('/admin')
def admin():
    query = "select * from prediction;"
    cursor.execute(query)
    prediction = cursor.fetchall()
    print("User Predictions", prediction)
    if 'ADMIN_ID' in session:
        print(app.secret_key)
        return render_template('admin.html', value=prediction)
    else:
        return redirect('/')


@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')


@app.route('/adminvaldation', methods=["POST"])
def adminval():
    ADMIN_ID = str(request.form.get('auserid'))
    PASSWORD = str(request.form.get('apassword'))
    MOBILE_NUMBER = request.form.get('amobile_number')
    val = (ADMIN_ID,)
    val_sql = "select * from admin_data where ADMIN_ID=%s;"
    cursor.execute(val_sql, val)

    ADMIN_DATA = cursor.fetchall()
    print(ADMIN_DATA)
    print(len(ADMIN_DATA))
    if len(ADMIN_DATA) > 0:
        session['ADMIN_ID'] = ADMIN_DATA[0][0]
        return redirect('/admin')
    else:
        return redirect('/')

## User Code Start From Here
@app.route('/home')
def home():
    if 'userid' in session:
        print(app.secret_key)
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/singin')
def singin():
    return render_template('sing.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/visualize')

def visu():
    return render_template('visualize.html')


@app.route('/login_validation', methods=["POST"])
def loginvaldation():
    userid = request.form.get('userid')
    password = request.form.get('password')
    mobile_number = request.form.get('mobile_number')
    val = (userid,)
    val_sql = 'SELECT * FROM user_data WHERE USER_ID = %s'
    cursor.execute(val_sql, val)
    USER_DATA = cursor.fetchall()
    USER_DATA = list(USER_DATA[0])
    print(USER_DATA)
    md5 = hashlib.md5()
    md5.update(str(password).encode('utf-8'))
    print(USER_DATA[-1], " ", str(md5.hexdigest()))
    if str(md5.hexdigest()) == USER_DATA[-1]:
        session['userid'] = USER_DATA[0][0]
        return redirect('/home')
    else:
        print("Something went wrong")
        return render_template('login.html',passlo = "FAIL")

@app.route('/add_user', methods=['POST'])
def adduser():
    userid = request.form.get('userid')
    email = request.form.get('email')
    mobile_number = request.form.get('mobile_number')
    fullname = request.form.get('fullname')
    password = request.form.get('password')
    con_password = request.form.get('con_password')

    if password != con_password:
        return render_template('sing.html', passvali=1)

    result = hashlib.md5(str(password).encode('utf-8'))
    md5 = hashlib.md5()
    md5.update(str(password).encode('utf-8'))
    print(str(md5.hexdigest()))
    query = "INSERT INTO USER_DATA (USER_ID, EMAILADDRESS, MOBILE_NUMBER,FULL_NAME,PASSWORD) " \
            "VALUES('%s','%s','%s','%s','%s')" % (userid, email, mobile_number, fullname, md5.hexdigest())

    val = (userid,)
    val_sql = 'SELECT * FROM USER_DATA WHERE USER_ID = %s'

    cursor.execute(val_sql, val)
    USER_DATA = cursor.fetchall()
    # USER_DATA = list(USER_DATA[0])
    if len(USER_DATA) > 0:
        return render_template('sing.html', status=1)
    else:
        cursor.execute(query)
        connection.commit()
        session['userid'] = userid
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
            lamount = int(request.form['lamount'])
            duration = int(request.form['duration'])

            dictPropArea = {0: "Rural", 1: "Semiurban", 2: "urban"}
            dictgender = {1: "Male", 0: "Female"}
            dictmar = {0: "Married", 1: "UnMarried"}
            dictdep = {0: "Zero Dependents", 1: "One Dependents", 2: "two Dependents", 3: "More Than Two Dependents"}
            dictedu = {0: "Graduate", 1: "Not Graduate"}
            dictemp = {0: "Business", 1: "Job"}
            dictcredit = {0: "Between 100 to 300", 1: "Between 300 to 500", 2: "Between 500 to 600", 3: "Above 600"}

            features = [[gen, acc, mar, dep, edu, emp, property, credit, income, caincome, lamount, duration]]

            prediction = model.predict(features)
            print(prediction)
            lc = [str(i) for i in prediction]
            ans = int("".join(lc))
            print(ans)
            cusname = "Hello Sir/Madam " + fn + ' ' + ln
            accr = "Bank Account Number: " + str(acc)
            if ans == 0:
                pred = 'Not Approved'
                mopred = "Sorry! According to Our Calculations you will not get the loan from Bank."
                resp_data = (str(fn), str(ln), str(acc), str(dictgender[gen]), str(dictmar[mar]), str(dictdep[dep]),
                             str(dictedu[edu]), str(dictemp[emp]), str(dictPropArea[property]), str(dictcredit[credit]),
                             str(income), str(caincome), str(lamount), str(duration), str(pred))
                print(len(resp_data))
                print(resp_data)
                resp_query = "INSERT INTO prediction (First_Name,Last_Name,Bank_Account_last_three_digit,Gender,Martial_Status,Number_of_dependents,Education, Employment_status,Property_Area,Credit_Score ,Income,Co_Applicant_Income,Loan_Amount , Loan_Duration,prediction)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(resp_query, resp_data)
                connection.commit()
                return render_template('predict.html', cus_name=cusname, acc_no=accr, prediction_text=mopred)
            else:
                pred = 'Approved'
                resp_data = (str(fn), str(ln), str(acc), str(dictgender[gen]), str(dictmar[mar]), str(dictdep[dep]),
                             str(dictedu[edu]), str(dictemp[emp]), str(dictPropArea[property]), str(dictcredit[credit]),
                             str(income), str(caincome), str(lamount), str(duration), str(pred))
                print(len(resp_data))
                print(resp_data)
                resp_query = "INSERT INTO prediction (First_Name,Last_Name,Bank_Account_last_three_digit,Gender,Martial_Status,Number_of_dependents,Education, Employment_status,Property_Area,Credit_Score ,Income,Co_Applicant_Income,Loan_Amount , Loan_Duration,prediction)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(resp_query, resp_data)
                connection.commit()
                mopred = "Congratulations! According to Our Calculation you will get the loan from Bank."
                return render_template('predict.html', cus_name=cusname, acc_no=accr, prediction_text=mopred)

    except Exception as e:
        print(e)
        return render_template('predict.html', prediction_text="Something went wrong!!!")


if __name__ == '__main__':
    app.run(debug=True)
# -*- coding: utf-8 -*-
