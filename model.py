from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    income = db.relationship('Income', backref = 'user', uselist = False, cascade = "all, delete-orphan") # one-to-one relationship
    transactions = db.relationship('Transaction', backref = 'user', lazy = True, cascade = "all, delete-orphan") # one-to-many relationship with lazy loading

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    

class Income(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    salary = db.Column(db.Float, nullable = False)
    investment = db.Column(db.Float, nullable = True)
    other_sources = db.Column(db.Float, nullable = True)
    remaining_balance = db.Column(db.Float, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Income('{self.salary}', '{self.investment}', '{self.other_sources}', '{self.remaining_balance}')"
    

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float, nullable = False)
    type = db.Column(db.String(6), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    note = db.Column(db.String(255), nullable = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Transaction('{self.amount}', '{self.type}', '{self.date}', '{self.note}')"