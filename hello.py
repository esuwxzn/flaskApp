from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

from wtforms.fields import (StringField, PasswordField, DateField, BooleanField,
                            SelectField, SelectMultipleField, TextAreaField,
                            RadioField, IntegerField, DecimalField, SubmitField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Regexp


from taxReportStatistic import taxReportStatistic

from taxReportStatistic import taxReportStatistic



#Test ssh

# from requestHandler import requestHandler



# requestHandler = requestHandler()

app = Flask(__name__)
app.debug = True

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'TEST'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# class searchForm(Form):
#     CIF = StringField('CIF', [validators.Length(min=10, max=10)])
#     CustomerName = StringField('Customer Name', [validators.Length(min=1, max=50)])
#     AccountNumber = StringField('Account Number', [validators.Length(min=14, max=14)])
#     TaxNumber = StringField('Tax Number', [validators.Length(min=1, max=10)])
    

# class retrieveData(object):
    # def __init__(self, arg):
    #     super(data, self).__init__()
    #     self.arg = arg



        

class searchForm(Form):

    infoType = SelectField('infoType', choices=[
        ('cif', 'CIF'),
        ('accountNumber', 'Account Number'),
        ('customerName', 'Customer Name'),
        ('taxNumber', 'Tax Number')],
        render_kw = {"class": "form-control"})
    
    keyword = StringField('Keyword', validators=[DataRequired()], render_kw = {"class": "form-control" , "placeholder" : "Please input keywords..."})



class timeForm(Form):
    startTime = StringField('From', validators=[DataRequired()], render_kw = {"class": "form-control" , "placeholder" : "Start Date..."})
    endTime = StringField('To', validators=[DataRequired()], render_kw = {"class": "form-control" , "placeholder" : "End Date..."})


class loginForm(Form):
    username = StringField('Username', validators=[DataRequired()], render_kw = {"class": "form-control" , "placeholder" : "Username..."})
    password = StringField('Password', validators=[DataRequired()], render_kw = {"class": "form-control" , "placeholder" : "Password..."})    






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
# requestHandler.home()



@app.route('/customer', methods=['GET', 'POST'])
def customer():
    form = searchForm(request.form)
    if request.method == 'POST' and form.validate():
        infoType = form.infoType.data
        keyword = form.keyword.data

                # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        # cur.execute("SELECT * FROM TEST_FLASK WHERE ID = %s", keyword)
        cur.execute("SELECT * FROM TEST_FLASK")        
        data = cur.fetchall()
        # print data['DESCRIPTION']
        print data[0];
        print data[1];
        print data[2];
        # print data[3];
        # print data[4];
        # print len(data)




        # Commit to DB
        # mysql.connection.commit()

        # Close connection
        cur.close()

        # flash('You are now registered and can log in', 'success')

        return render_template('customer_info.html', data = data)






    return render_template('customer.html', form = form)



@app.route('/tax-report', methods=('GET', 'POST'))
def generateTaxReport():
    # form = timeForm(request.form)
    # print request.form.get('Remittance')
    # print request.form.get('startTime')
    # print request.form.get('endTime')    
    
    # print request.form['Remittance']
    dataToReport = []
    
    if request.method == 'POST':# and form.validate():
        startTime = request.form.get('startTime')
        endTime = request.form.get('endTime')
        remittance = request.form.get('Remittance')

        print startTime
        print endTime
        print remittance

        report = taxReportStatistic(startTime, endTime, remittance)
        data = report.run()
        # print data.keys()

        keys = data.dataToReport.keys()
        # print keys

        for key in keys:
            for row in data.dataToReport[key]:
                dataToReport.append(row)
                # print row

        # Commit to DB
        # mysql.connection.commit()

        # Close connection
        # cur.close()

        if remittance == 'outward':
            return render_template('tax-report-outward.html', data=dataToReport)

        if remittance == 'inward':
            return render_template('tax-report-inward.html', data=dataToReport)


    # return render_template('tax-report.html', form=form)
    return render_template('tax-report.html')



@app.route('/test', methods=('GET', 'POST'))
def test():
    form = timeForm(request.form)
    
    if request.method == 'POST' and form.validate():
        startTime = form.startTime.data
        endTime = form.endTime.data

        print startTime
        print endTime

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM TEST_FLASK")        
        data = cur.fetchall()
        # print data['DESCRIPTION']
        print data[0];
        print data[1];
        print data[2];

        # Commit to DB
        # mysql.connection.commit()

        # Close connection
        cur.close()

        return render_template('tax.html', data=data)


    return render_template('test.html', form=form)



# @app.route('/customer/<string:cif>/')
# def customer_info(cif):
#     return render_template('customer_info.html', CIF = cif)

# @app.route('/test')
# def test():
#     return render_template('test.html')


if __name__ == '__main__':
    #app.run(debug = True)
    app.secret_key='secret123'
    app.run()
