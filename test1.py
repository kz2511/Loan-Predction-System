import pymysql
from flask import Flask, render_template, request, redirect,session

connection = pymysql.connect(host="localhost", user="root", password="", database="loan_prediction")
cursor = connection.cursor()

app = Flask(__name__)
@app.route('/admin')
def admin():
    query = "select * from prediction;"
    cursor.execute(query)
    prediction=cursor.fetchall()
    print("User Predictions",prediction)
    return render_template('admin.html',value=prediction)

app.run(debug=True)