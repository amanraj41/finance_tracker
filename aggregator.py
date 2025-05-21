from datetime import timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import func, extract
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import Transaction, Income

def get_visualization_data(db: SQLAlchemy, date: datetime, user_id):
    month_first_day = date.replace(day = 1)
    month_last_day = (month_first_day + relativedelta(months = 1)) - timedelta(days = 1)

    monthly_data = db.session.query(
        Transaction.date,
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == 'debit',
        Transaction.date >= month_first_day,
        Transaction.date <= month_last_day,
    ).group_by(
        extract('day', Transaction.date)
    ).all()

    week_first_day = date - timedelta(days = date.weekday())
    week_last_day = week_first_day + timedelta(days = 7)

    weekly_data = db.session.query(
        Transaction.date,
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == 'debit',
        Transaction.date >= week_first_day,
        Transaction.date <= week_last_day
    ).group_by(
        extract('day', Transaction.date)
    ).all()

    monthly_income = db.session.query(
        func.sum(Income.salary + Income.investment + Income.other_sources)
    ).filter(
        Income.user_id == user_id
    ).scalar()

    weekly_expenditure = {}
    for daily_expense in monthly_data:
        week_number = daily_expense.date.isocalendar()[1]

        if week_number not in weekly_expenditure:
            weekly_expenditure[week_number] = 0

        weekly_expenditure[week_number] += daily_expense.total

    month_total_expense = sum(week for week in weekly_expenditure.values())

    monthly_balance = monthly_income - month_total_expense

    return monthly_data, weekly_data, weekly_expenditure, month_total_expense, monthly_balance

"""
def print_aggregations(db: SQLAlchemy, date: datetime, user_id):

    monthly_data, weekly_data, weekly_expenditure, month_total_expense, monthly_balance = get_visualization_data(db, date, user_id)

    print(f"\n\nDate-wise total expenses for the month of {date.strftime('%B, %Y')}:\n")
    for day in monthly_data:
        print(f"Date: {day.date.strftime('%d-%b-%Y')}\tTotal expense: {day.total}\n")

    print(f"\n\nDate-wise total expenses for the week number {date.isocalendar()[1]} of year {date.year}:\n")

    for day in weekly_data:
        print(f"Date: {day.date.strftime('%d-%b-%Y')}\tTotal expense: {day.total}\n")

    print(f"\n\nWeek-wise total expenses for the month of {date.strftime('%B, %Y')}:\n")
    for week in weekly_expenditure:
        print(f"Week number: {week}\tTotal expenditure: {weekly_expenditure[week]}\n")

    print(f"\n\nTotal expense for the month of {date.strftime('%B, %Y')}: {month_total_expense}\n")
    
    print(f"\nBalance amount for the month of {date.strftime('%B, %Y')}: {monthly_balance}\n")
"""