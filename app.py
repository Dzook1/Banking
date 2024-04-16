from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
app = Flask(__name__)

conn_str = 'mysql://root:9866@localhost/banking'
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/MyAccount')
def Account():    
     return render_template('MyAccount.html')

@app.route('/MyAccount', methods=['GET'])
def Account():
    return render_template('MyAccount.html')


@app.route('/MyAccount', methods=['POST'])
def Accountin():
    conn.execute(text('Select Balance from Information where user'), request.form)
    conn.commit()
    return render_template('MyAccount.html')



@app.route('/Transfer')
def transfer():    
     return render_template('transfer.html')


if __name__ == '__main__':
    app.run(debug=True)
@app.route('/adminLogin.html')
def adminLogin():
    return render_template('adminLogin.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)