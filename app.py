from flask import Flask, render_template, redirect, url_for, flash, jsonify, request
from forms import *
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from model import *
from dateutil import parser, tz
from sqlalchemy import extract

app = Flask(__name__)
app.config['SECRET_KEY'] = '27F0812:HKR-THN'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return render_template('index.html')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

            login_user(new_user)

            flash(f'Account created for {form.username.data}!', 'success')
            return render_template("success.html", redirect_url = url_for('setup'))
        
    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter((User.username == form.identifier.data) | (User.email == form.identifier.data)).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return render_template("success.html", redirect_url = url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username/email and password.', 'danger')
    
    return render_template('login.html', form = form)

@app.route('/setup', methods = ['GET', 'POST'])
@login_required
def setup():
    form = IncomeSetupForm()

    if form.validate_on_submit():
        income = Income(salary = form.salary.data, investment = form.investment.data or 0, other_sources = form.other_sources.data or 0,
                        remaining_balance = form.salary.data + (form.investment.data or 0) + (form.other_sources.data or 0),
                        user_id = current_user.id)
        db.session.add(income)
        db.session.commit()

        flash('Income profile saved successfully! Redirecting to dashboard...', 'success')
        return render_template('setup.html', form = form, redirect = True, redirect_url = url_for('dashboard'))
    
    return render_template('setup.html', form = form, redirect = False)

@app.route('/dashboard', methods = ['GET'])
@login_required
def dashboard():

    date_str = request.args.get('date', datetime.today().strftime('%a-%d-%b-%Y'))
    date = datetime.strptime(date_str, '%a-%d-%b-%Y')

    transactions = Transaction.query.filter(Transaction.user_id == current_user.id, 
                                            extract('day', Transaction.date) == date.day,
                                            extract('month', Transaction.date) == date.month,
                                            extract('year', Transaction.date) == date.year).all()

    return render_template('dashboard.html', user = current_user, transactions = transactions, date = date, tz = tz)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out. See you soon!', 'info')
    return redirect(url_for('home'))

@app.route('/add-transaction', methods = ['POST'])
@login_required
def add_transaction():
    amount = float(request.form.get('amount'))
    type = request.form.get('type')
    note = request.form.get('note')
    date_iso = request.form.get('date')
    date = parser.isoparse(date_iso)

    transaction_record = Transaction(amount = amount, type = type, date = date, note = note, user_id = current_user.id)

    db.session.add(transaction_record)
    db.session.commit()

    return jsonify({'message': 'Transaction added'}), 200

if __name__ == '__main__':
    app.run(debug = True)