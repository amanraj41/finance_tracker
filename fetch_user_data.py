from app import app, db
from model import User, Transaction, Income
from dateutil import tz

def fetch_user_data(username):
    with app.app_context():
        user = User.query.filter_by(username = username).first()

        if not user:
            print(f"No user found with username: {username}")
            return
        
        income = Income.query.filter_by(user_id = user.id).first()
        userName = user.username
        email = user.email

        if income:
            print(f"\nUserID: {income.user_id}\tUsername: {userName}\tEmail: {email}\nSalary: {income.salary}\tInvestments: {income.investment}\tOther Sources: {income.other_sources}\tRemaining Balance: {income.remaining_balance}\t")
        
        transactions = Transaction.query.filter_by(user_id = user.id).all()

        from_zone = tz.tzutc()
        to_zone = tz.gettz('Asia/Kolkata')

        if transactions:
            print(f"\nTransaction records for user: {username}:\n")
            for transaction in transactions:
                print(f"ID: {transaction.id}\tAmount: {transaction.amount}\tType: {transaction.type}\tDate: {transaction.date.replace(tzinfo = from_zone).astimezone(to_zone)}\tNote: {transaction.note}\tUserID: {transaction.user_id}\n")
        else:
            print(f"No transactions found for user '{username}'")
        
if __name__ == '__main__':
    fetch_user_data('amanraj')