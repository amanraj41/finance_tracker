from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from sqlalchemy import func, extract
from flask_sqlalchemy import SQLAlchemy
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

    return monthly_data, weekly_data, weekly_expenditure, month_total_expense, monthly_income, monthly_balance

def partition_month(year, month):
    month_start = date(year, month, 1)
    month_end = date(year, month, monthrange(year, month)[1])

    partition = {}

    week_start = month_start
    if week_start.weekday() != 0:
        week_start += timedelta(days = (7 - week_start.weekday()))

    while(week_start <= month_end):
        week_end = week_start + timedelta(days = 6)

        if week_end > month_end:
            week_end = month_end
        
        partition[week_start.isocalendar()[1]] = (week_start, week_end)
        week_start += timedelta(weeks = 1)

    if month_start < partition[next(iter(partition))][0]:
        
        partition[month_start.isocalendar()[1]] = (month_start, (partition[next(iter(partition))][0] - timedelta(days = 1)))

    return partition

def monthly_plot(monthly_data, month, year):
    _, num_days = monthrange(year, month)

    daily_expenses = {date(year, month, day): 0 for day in range(1, num_days + 1)}

    for available_data in monthly_data:
        daily_expenses[available_data.date.date()] = available_data.total
    
    return [date.strftime('%d-%m-%Y') for date in daily_expenses.keys()], [expense for expense in daily_expenses.values()]

def print_aggregations(db: SQLAlchemy, date: datetime, user_id):

    monthly_data, weekly_data, weekly_expenditure, month_total_expense, monthly_income, monthly_balance = get_visualization_data(db, date, user_id)

    print(f"\n\nDate-wise total expenses for the month of {date.strftime('%B, %Y')}:\n")
    for day in monthly_data:
        print(f"Date: {day.date.strftime('%d-%b-%Y')}\tTotal expense: {day.total}\n")

    print(f"\n\nDate-wise total expenses for the week number {date.isocalendar()[1]} of year {date.year}:\n")

    for day in weekly_data:
        print(f"Date: {day.date.strftime('%d-%b-%Y')}\tTotal expense: {day.total}\n")

    print(f"\n\nWeek-wise total expenses for the month of {date.strftime('%B, %Y')}:\n")
    date_ranges = partition_month(date.year, date.month)

    for week in weekly_expenditure:
        
        print(f"Week number: {week}\t\tStart date: {date_ranges[week][0]}\tEnd date: {date_ranges[week][1]}\tTotal expenditure: {weekly_expenditure[week]}\n")

    print(f"\n\nTotal expense for the month of {date.strftime('%B, %Y')}: {month_total_expense}\n")
    
    print(f"\nBalance amount for the month of {date.strftime('%B, %Y')}: {monthly_balance}\n")

if __name__ == '__main__':
    ranges = partition_month(2025, 12)
    print(f"\n\nPartition for December, 2025:\n")
    for wnum, range in ranges.items():
        print(f"\nWeek number: {wnum}\tStart date: {range[0]}\tEnd date: {range[1]}")

    ranges = partition_month(2026, 1)
    print(f"\n\nPartition for January, 2026:\n")
    for wnum, range in ranges.items():
        print(f"\nWeek number: {wnum}\tStart date: {range[0]}\tEnd date: {range[1]}")