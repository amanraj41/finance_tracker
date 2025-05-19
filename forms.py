from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 4, max = 20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    identifier = StringField('Username or Email', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class IncomeSetupForm(FlaskForm):
    salary = FloatField('Salary', validators = [DataRequired(), NumberRange(min = 10000, message = 'Salary must be atleast 10,000.')])
    investment = FloatField('Investments', validators = [Optional(), NumberRange(min = 0, message = 'Amount must be non-negative')])
    other_sources = FloatField('Other Sources', validators = [Optional(), NumberRange(min = 0, message = 'Amount must be non-negative')])
    submit = SubmitField('Save')