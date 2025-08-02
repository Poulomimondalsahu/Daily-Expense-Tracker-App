from sqlalchemy import create_engine, Column, Integer, String, Date, func
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow)

engine = create_engine('sqlite:///expenses.db', echo=True)
Base.metadata.create_all(engine)

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

def add_expense(amount, description, date):
    session = get_session()
    new_expense = Expense(amount=amount, description=description, date=date)
    session.add(new_expense)
    session.commit()
    session.close()

def get_expenses():
    session = get_session()
    expenses = session.query(Expense).all()
    session.close()
    return expenses

def remove_expense(expense_id):
    session = get_session()
    expense = session.query(Expense).filter_by(id=expense_id).first()
    if expense:
        session.delete(expense)
        session.commit()
    session.close()

if __name__ == "__main__":
    # Clear all expenses for testing (optional)
    session = get_session()
    session.query(Expense).delete()
    session.commit()
    session.close()

    # Add a test expense
    add_expense(100, "Test Entry", datetime.date.today())
    # Print all expenses
    expenses = get_expenses()
    for exp in expenses:
        print(f"ID: {exp.id}, Amount: {exp.amount}, Desc: {exp.description}, Date: {exp.date}")

    # --- New code for today's history and summary ---
    today = datetime.date.today()
    session = get_session()
    # Today's expenses
    todays_expenses = session.query(Expense).filter(Expense.date == today).all()
    print(f"\nToday's Expenses ({today}):")
    for exp in todays_expenses:
        print(f"  ID: {exp.id}, Amount: {exp.amount}, Desc: {exp.description}")

    # Total amount spent today
    total_today = sum(exp.amount for exp in todays_expenses)
    print(f"Total amount spent today: {total_today}")

    # Summary: date-wise count of expenses
    date_counts = session.query(Expense.date, func.count(Expense.id)).group_by(Expense.date).all()
    print("\nExpenses count by date:")
    for date, count in date_counts:
        print(f"  {date}: {count} expense(s)")
    session.close()
    # --- End new code ---

    # Keep the console window open
    input("Press Enter to continue...")