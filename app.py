from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

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
        return render_template('signup.html')
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
        return render_template('signup.html')
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

if __name__ == '__main__':
    app.run(debug=True)