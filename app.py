from flask import Flask,render_template,flash,redirect,url_for,logging,session,request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_ngrok import run_with_ngrok
app = Flask(__name__)
#run_with_ngrok(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT']=4000
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'feedback'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

'''@app.route('/')

def index():
	return render_template("home.html")'''



# User login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM student WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if password==password_candidate:
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return render_template('dashboard.html')
            else:
                error = 'Invalid login'
                return render_template('home.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('home.html', error=error)

    return render_template('home.html')



if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)
	