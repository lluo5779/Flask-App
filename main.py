from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)

#CONFIG MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '243589624@Louis'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#Initialize MySQL
mysql = MySQL(app)

Articles = Articles()

@app.route('/')
def hello():
	return render_template('home.html')

# @app.route('/<name>')
# def hello_name(name):
# 	return 'Hello {}!'.format(name)

@app.route('/about.html')
def about():
	return render_template('about.html')

@app.route('/articles.html')
def articles():
	return render_template('articles.html', articles=Articles)

@app.route('/articles/<string:id>/')
def article(id):
	return render_template('article.html', id=id)

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate(): 
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		#Create cursor
		cur = mysql.connection.cursor()

		cur.execute('INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)', (name, email, username, password))

		#Commmit to DB
		mysql.connection.commit()

		#Close connection
		cur.close()

		flash('You are now registered and can log in!', 'success')

		redirect(url_for('index'))

		return render_template('register.html', form=form)
	return render_template('register.html', form=form)



if __name__=='__main__':
	app.secret_key='secret123'
	app.run(debug=True)