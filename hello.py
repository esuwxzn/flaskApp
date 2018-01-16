from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)
app.debug = True

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'USERS'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)



@app.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST': 
        username = request.form['username']
        password_candidate = request.form['password']
        
        # print password_candidate
        
        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM userlist WHERE username = %s", [username])


        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if password == password_candidate:
                # # Passed
                # session['logged_in'] = True
                # session['username'] = username

                # flash('You are now logged in', 'success')
                # return redirect(url_for('dashboard'))
                return 'Success!'

            else:
                return 'Fail!'
                # error = 'Invalid login'
                # return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            return 'Cannot find the user!'
            # error = 'Username not found'"
            # return render_template('login.html', error=error)

        # return result 
    else:
        return render_template('login.html')

    

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/customer/<string:cif>/')
def customer_info(cif):
    return render_template('customer_info.html', CIF = cif)




if __name__ == '__main__':
    #app.run(debug = True)
    app.run()