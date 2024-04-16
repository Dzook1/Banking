from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/base')
def test():
    return render_template('base.html')

@app.route('/MyAccount')
def Account():    
     return render_template('MyAccount.html')

if __name__ == '__main__':
    app.run(debug=True)

    