from flask import Flask, render_template, redirect, url_for, flash
from forms import RegistrationForm, LoginForm
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from model import User, db

app = Flask(__name__)
app.config['SECRET_KEY'] = '27F0812:HKR-THN'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        user_same_username = User.query.filter_by(username = form.username.data).first()
        user_same_email = User.query.filter_by(email = form.email.data).first()

        if user_same_username:
            flash('Username is already taken! Please choose a different one.', 'danger')
        elif user_same_email:
            flash('Email is already registered. Please use a different email.', 'danger')

        else:
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(username = form.username.data, email = form.email.data, password = hashed_password)

            db.session.add(new_user)
            db.session.commit()

            flash(f'Account created for {form.username.data}!', 'success')
            return render_template("success.html", redirect_url = url_for('home'))
        
    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter((User.username == form.identifier.data) | (User.email == form.identifier.data)).first()

        if user and check_password_hash(user.password, form.password.data):

            flash(f'Welcome back, {user.username}!', 'success')
            return render_template("success.html", redirect_url = url_for('home'))
        else:
            flash('Login unsuccessful. Please check username/email and password.', 'danger')
    
    return render_template('login.html', form = form)

if __name__ == '__main__':
    app.run(debug = True)