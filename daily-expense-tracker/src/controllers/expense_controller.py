class ExpenseController:
    def __init__(self, db):
        self.db = db

    def add_expense(self, amount, description, date):
        self.db.add_expense(amount, description, date)

    def get_expenses(self):
        return self.db.get_expenses()

    def remove_expense(self, expense_id):
        self.db.remove_expense(expense_id)