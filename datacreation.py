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
#createtablesingin()

def createtablepredction():
    connection = pymysql.connect(host="localhost", user="root", password="",database="loan_prediction")
    currsor = connection.cursor()
    currsor.execute("""CREATE TABLE IF NOT EXISTS prediction( 
        First_Name varchar(100) NOT NULL,
        Last_Name varchar(100) NOT NULL,
        Bank_Account_last_three_digit varchar(100) NOT NULL,
        Gender varchar(100) NOT NULL,
        Martial_Status varchar(20) NOT NULL,
        Number_of_dependents varchar(20) NOT NULL,
        Education varchar(20) NOT NULL,
        Employment_status varchar(20) NOT NULL,
        Property_Area varchar(20) NOT NULL,
        Credit_Score varchar(20) NOT NULL,
        Income varchar(20) NOT NULL,
        Co_Applicant_Income varchar(20) NOT NULL,
        Loan_Amount varchar(20) NOT NULL,
        Loan_Duration varchar(20) NOT NULL  ,
        prediction varchar(20) NOT NULL
    );
       """)
createtablepredction()




