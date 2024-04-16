from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/MyAccount')
def Account():    
     return render_template('MyAccount.html')

@app.route('/adminLogin.html')
def adminLogin():
    return render_template('adminLogin.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)