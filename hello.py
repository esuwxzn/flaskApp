from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    #return "Hello World! with debug flag is true xxxx"
    return render_template('login.html')
    #return render_template('index.html')

# @app.route('/test1')
# def test1():
#     #return "Hello World! with debug flag is true xxxx"
#     return render_template('test1.html')

# @app.route('/test2')
# def test2():
#     #return "Hello World! with debug flag is true xxxx"
#     return render_template('test2.html')

class userFrom(Form):
    username = StringField('Username', [validators.Length(min=1, max=30, message=None)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        #validators.DataRequired(),
        validators.Length(min=6, max=20)])

@app.route('/login')
def register():
    form = RegisterForm(request.form)
    if request.methon == 'POST' and form.validate():
    	
        return




if __name__ == '__main__':
    #app.run(debug = True)
    app.run()




