from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.metrics import dp
from kivy.properties import StringProperty
import datetime

from controllers.expense_controller import ExpenseController
from utils import db

class MainApp(App):
    def build(self):
        self.title = "Daily Expense Tracker"
        self.manager = ScreenManager()
        self.manager.add_widget(MainScreen(name='main'))
        return self.manager

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.controller = ExpenseController(db)
        self.filter_date = None

    def on_enter(self):
        self.update_expense_list()

    def update_expense_list(self):
        expenses = self.controller.get_expenses()
        today = datetime.date.today()
        today_total = 0
        if self.filter_date:
            filtered = []
            for expense in expenses:
                exp_date = expense.date
                if isinstance(exp_date, str):
                    try:
                        exp_date = datetime.datetime.strptime(exp_date, "%Y-%m-%d").date()
                    except Exception:
                        continue
                elif isinstance(exp_date, datetime.datetime):
                    exp_date = exp_date.date()
                if exp_date == self.filter_date:
                    filtered.append(expense)
                if exp_date == today:
                    today_total += expense.amount
            expenses = filtered
        else:
            for expense in expenses:
                exp_date = expense.date
                if isinstance(exp_date, str):
                    try:
                        exp_date = datetime.datetime.strptime(exp_date, "%Y-%m-%d").date()
                    except Exception:
                        continue
                elif isinstance(exp_date, datetime.datetime):
                    exp_date = exp_date.date()
                if exp_date == today:
                    today_total += expense.amount
        self.ids.expense_list.data = [
            {
                'text': f"{expense.date} | ₹{expense.amount} | {expense.description}",
                'expense_id': str(expense.id)
            }
            for expense in expenses
        ]
        self.ids.today_total_label.text = f"Today's Total: ₹{today_total}"

    def add_expense(self):
        amount = self.ids.amount_input.text
        description = self.ids.description_input.text
        if amount and description:
            try:
                today = datetime.date.today()
                self.controller.add_expense(int(amount), description, today)
                self.ids.amount_input.text = ""
                self.ids.description_input.text = ""
                self.update_expense_list()
            except Exception as e:
                print("Error adding expense:", e)

    def remove_expense(self, expense_id):
        try:
            self.controller.remove_expense(expense_id)
            self.update_expense_list()
        except Exception as e:
            print("Error removing expense:", e)

    def filter_by_date(self):
        date_str = self.ids.filter_date_input.text.strip()
        try:
            self.filter_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            self.filter_date = None
        self.update_expense_list()

class ExpenseLabel(Label):
    text = StringProperty("")

Builder.load_string('''
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            spacing: 10
            TextInput:
                id: amount_input
                hint_text: "Amount"
                input_filter: 'int'
            TextInput:
                id: description_input
                hint_text: "Description"
            Button:
                text: "Add"
                size_hint_x: None
                width: dp(80)
                on_press: root.add_expense()

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            spacing: 10
            TextInput:
                id: filter_date_input
                hint_text: "Filter by date (YYYY-MM-DD)"
            Button:
                text: "Apply"
                size_hint_x: None
                width: dp(80)
                on_press: root.filter_by_date()

        Label:
            id: today_total_label
            text: "Today's Total: ₹0"
            size_hint_y: None
            height: dp(30)
            font_size: 18

        RecycleView:
            id: expense_list
            viewclass: 'ExpenseRow'
            RecycleBoxLayout:
                default_size: None, dp(40)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'

<ExpenseRow@BoxLayout>:
    text: ''
    expense_id: ''
    size_hint_y: None
    height: dp(40)
    Label:
        text: root.text
        font_size: 18
    Button:
        text: "Remove"
        size_hint_x: None
        width: dp(80)
        on_press: app.root.get_screen('main').remove_expense(root.expense_id)
''')

if __name__ == '__main__':
    MainApp().run()