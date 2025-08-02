class Expense:
    def __init__(self, amount, description, date):
        self.amount = amount
        self.description = description
        self.date = date

    def __repr__(self):
        return f"Expense(amount={self.amount}, description='{self.description}', date='{self.date}')"

    def to_dict(self):
        return {
            'amount': self.amount,
            'description': self.description,
            'date': self.date
        }