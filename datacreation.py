import pymysql

def createdatabase():
    connection = pymysql.connect(host="localhost", user="root", password="")
    currsor = connection.cursor()
    currsor.execute("create database loan_prediction")


def createtablesingin():
    connection = pymysql.connect(host="localhost", user="root", password="",database="loan_prediction")
    currsor = connection.cursor()
    currsor.execute("""CREATE TABLE IF NOT EXISTS USER_DATA ( 
        USER_ID varchar(100) NOT NULL,
        EMAILADDRESS varchar(100) NOT NULL,
        MOBILE_NUMBER varchar(100) NOT NULL,
        FULL_NAME varchar(100) NOT NULL,
        PASSWORD varchar(20) NOT NULL,
        conf_PASSWORD varchar(20) NOT NULL,
        PRIMARY KEY (USER_ID)
    );
       """)
createtablesingin()



