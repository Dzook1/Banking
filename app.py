from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
import random

app = Flask(__name__)



conn_str = "mysql://root:Dougnang1@localhost/banking"
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
    query = text('Select Balance, First_Name from Information where SSN = :userSSN')
    result = conn.execute(query, {"userSSN": userSSN}).fetchone()
    return render_template('my_account.html', balance=result[0], name=result[1])

@app.route('/transfer.html', methods=['GET'])
def transfer():    
    query = text('Select Balance from information where SSN = :userSSN')
    result = conn.execute(query, {"userSSN": userSSN}).fetchone()
    return render_template('transfer.html', balance=result[0])

@app.route('/transfer.html', methods=['POST'])
def transferGo():
    query = text('Select Balance from information where SSN = :userSSN')
    balanceUser = conn.execute(query, {"userSSN": userSSN}).fetchone()

    amount = request.form['transfer-amount']
    accountTo = request.form['transfer-username']

    query = text("SELECT account_number FROM account_approval WHERE account_number = :accountTo")
    data = conn.execute(query, {'accountTo': accountTo}).fetchone()

    if data:
        query = text('Select information.Balance from information, account_approval where account_approval.account_number = :data and account_approval.SSN = information.SSN;')
        balanceReceiver = conn.execute(query, {'data': data[0]}).fetchone()
        totalBalanceReveiver = float(amount) + float(balanceReceiver[0])

        query = text('Select information.SSN from information, account_approval where account_approval.account_number = :data and account_approval.SSN = information.SSN;')
        receiverSSN = conn.execute(query, {'data': data[0]}).fetchone()

        query = text('Select Balance from information where SSN = :userSSN;')
        balanceUser = conn.execute(query, {'userSSN': userSSN}).fetchone()
        totalBalanceUser = float(balanceUser[0]) - float(amount)

        query = text("UPDATE information SET balance = :totalBalanceReceiver WHERE SSN = :receiverSSN;")
        conn.execute(query, {"totalBalanceReceiver": totalBalanceReveiver, "receiverSSN": receiverSSN[0]})
        
        query2 = text("UPDATE information SET balance = :totalBalanceUser WHERE SSN = :userSSN;")
        conn.execute(query2, {"totalBalanceUser": totalBalanceUser, 'userSSN' : userSSN })

    query = text('Select Balance, First_Name from Information where SSN = :userSSN')
    result = conn.execute(query, {"userSSN": userSSN}).fetchone()
    return render_template('my_account.html', balance=result[0], name=result[1])

@app.route('/adminHome.html')
def adminHome():
    return render_template('adminHome.html')

@app.route('/accounts.html')
def accounts():
    query = text("SELECT information.First_Name, information.Last_Name, information.Username, information.SSN, information.Address, information.Phone_Number, account_approval.account_number, information.Balance FROM information, account_approval WHERE information.SSN = account_approval.SSN AND account_approval.account_number <> '';")
    data = conn.execute(query)
    return render_template('accounts.html', data=data)

@app.route('/approveAccounts.html', methods=['GET'])
def approveAccounts():
    query = text("SELECT information.First_Name, information.Last_Name, information.Username, information.SSN, information.Address, information.Phone_Number FROM information, account_approval WHERE information.SSN = account_approval.SSN AND account_approval.account_number = '';")
    data = conn.execute(query)
    return render_template('approveAccounts.html', data=data)

@app.route('/approveAccounts.html', methods=['POST'])
def approveAccountsGo():
    ssnRequest = request.form['SSN']
    AcctNum = str(random.randint(0, 99999999))

    query = text("SELECT account_number FROM account_approval WHERE SSN = :ssnRequest")
    data = conn.execute(query, {'ssnRequest': ssnRequest}).fetchone()

    if data[0] == "":
        if len(AcctNum) < 8:
            AcctNum =  '0' * (8 - len(AcctNum)) + AcctNum

        if 'submit_button' in request.form and request.form['submit_button'] == 'Approve':
            query = text("UPDATE account_approval SET account_number = :AcctNum WHERE SSN = :ssnRequest")
            conn.execute(query, {'AcctNum': AcctNum, 'ssnRequest': ssnRequest})
            conn.commit()
            pass
        elif 'submit_button' in request.form and request.form['submit_button'] == 'Deny':
            query = text("DELETE FROM account_approval WHERE  SSN = :ssnRequest")
            conn.execute(query, {'ssnRequest': ssnRequest})
            conn.commit()
            query = text("DELETE FROM information WHERE  SSN = :ssnRequest")
            conn.execute(query, {'ssnRequest': ssnRequest})
            conn.commit()
            pass

    query = text("SELECT information.First_Name, information.Last_Name, information.Username, information.SSN, information.Address, information.Phone_Number FROM information, account_approval WHERE information.SSN = account_approval.SSN AND account_approval.account_number = '';")
    data = conn.execute(query)
    return render_template('approveAccounts.html', data=data)

@app.route('/addFunds.html', methods=['GET'])
def addFunds():
    return render_template('addFunds.html')

@app.route('/addFunds.html', methods=['POST'])
def addFundsGo():
    amount1 = request.form['Amount']
    query = text("SELECT Balance FROM information WHERE SSN = :userSSN")
    data =  conn.execute(query, {'userSSN': userSSN}).fetchone()
    amount2 = data[0]
    newAmount = float(amount1) + float(amount2)

    query = text("UPDATE information SET Balance = :newAmount WHERE SSN = :userSSN")
    conn.execute(query, {'newAmount': newAmount , 'userSSN': userSSN})

    query = text('Select Balance, First_Name from Information where SSN = :userSSN')
    result = conn.execute(query, {"userSSN": userSSN}).fetchone()
    return render_template('my_account.html', balance=result[0], name=result[1])

if __name__ == '__main__':
    app.run(debug=True)