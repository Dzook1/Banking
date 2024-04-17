from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)


conn_str = "mysql://root:cset155@localhost/banking"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def homeGo():
    username = request.form['Username']
    password = request.form['Password']

    query = text("SELECT information.SSN FROM information, account_approval WHERE information.Username = :username AND information.Password = :password AND account_approval.account_number <> '' AND account_approval.SSN = information.SSN")
    result = conn.execute(query, {'username': username, 'password': password}).fetchone()

    if result:
        global userSSN
        userSSN = result[0]

        query = text('Select Balance, First_Name from Information where SSN = :userSSN')
        result = conn.execute(query, {"userSSN": userSSN}).fetchone()

        return render_template('my_account.html', balance=result[0], name=result[1])

    else:
        return render_template('index.html')
    

@app.route('/adminLogin.html', methods=['GET'])
def adminLogin():
    return render_template('adminLogin.html')

@app.route('/adminLogin.html', methods=['POST'])
def adminLoginGo():
    username = request.form['Username']
    password = request.form['Password']

    query = text("SELECT First_Name from information WHERE Username = :username AND Password = :password AND Type = 'Admin';")
    result = conn.execute(query, {'username': username, 'password': password}).fetchone()

    if result:
        return render_template('adminHome.html')
    else:
        return render_template('index.html')

@app.route('/signup.html', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup.html', methods=['POST'])
def signupGo():
    conn.execute(text("INSERT INTO information VALUES (:First_Name, :Last_Name, :Username, :Password, :Address, :Phone_Number, :SSN, 0, 'User')"), request.form)
    conn.commit()
    conn.execute(text("INSERT INTO account_approval VALUES (:SSN, '')"), request.form)
    conn.commit()

    return render_template('index.html')

@app.route('/my_account.html')
def Account():
    query = text('Select Balance from Information where SSN = :userSSN')
    result = conn.execute(query, {"userSSN": userSSN}).fetchone()
    return render_template('my_account.html', balance=result[0])

@app.route('/transfer.html')
def transfer():    
     return render_template('transfer.html')

@app.route('/adminHome.html')
def adminHome():
    return render_template('adminHome.html')

@app.route('/accounts.html')
def accounts():
    query = text("SELECT information.First_Name, information.Last_Name, information.Username, information.SSN, information.Address, information.Phone_Number, account_approval.account_number FROM information, account_approval WHERE information.SSN = account_approval.SSN AND account_approval.account_number <> '';")
    data = conn.execute(query)
    return render_template('accounts.html', data=data)

@app.route('/approveAccounts.html')
def approveAccounts():
    return render_template('approveAccounts.html')

@app.route('/addFunds.html', methods=['GET'])
def addFunds():
    return render_template('addFunds.html')


if __name__ == '__main__':
    app.run(debug=True)