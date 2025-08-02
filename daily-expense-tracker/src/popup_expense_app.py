from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import datetime

from utils import db

class ExpensePopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Add Today's Expense"
        self.size_hint = (0.8, 0.5)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        self.amount_input = TextInput(hint_text="Amount spent", input_filter='int', multiline=False)
        self.item_input = TextInput(hint_text="Item/Product", multiline=False)
        
        submit_btn = Button(text="Submit", size_hint_y=None, height=40)
        submit_btn.bind(on_press=self.submit_expense)
        
        self.msg_label = Label(text="")
        
        layout.add_widget(Label(text="How much did you spend today?"))
        layout.add_widget(self.amount_input)
        layout.add_widget(Label(text="On which item/product?"))
        layout.add_widget(self.item_input)
        layout.add_widget(submit_btn)
        layout.add_widget(self.msg_label)
        
        self.content = layout

    def submit_expense(self, instance):
        amount = self.amount_input.text.strip()
        item = self.item_input.text.strip()
        if amount and item:
            try:
                db.add_expense(int(amount), item, datetime.date.today())
                self.msg_label.text = "Expense saved!"
                self.amount_input.text = ""
                self.item_input.text = ""
            except Exception as e:
                self.msg_label.text = f"Error: {e}"
        else:
            self.msg_label.text = "Please fill all fields."

class HistoryPopup(Popup):
    def __init__(self, date=None, **kwargs):
        super().__init__(**kwargs)
        self.title = "Expense History"
        self.size_hint = (0.95, 0.85)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Date filter
        filter_layout = BoxLayout(size_hint_y=None, height=40, spacing=5)
        self.date_input = TextInput(hint_text="YYYY-MM-DD", multiline=False, size_hint_x=0.7)
        filter_btn = Button(text="Filter", size_hint_x=0.3)
        filter_btn.bind(on_press=self.filter_by_date)
        filter_layout.add_widget(self.date_input)
        filter_layout.add_widget(filter_btn)
        layout.add_widget(filter_layout)

        # Totals
        self.day_total_label = Label(text="Day Total: ₹0", size_hint_y=None, height=30)
        self.week_total_label = Label(text="Week Total: ₹0", size_hint_y=None, height=30)
        layout.add_widget(self.day_total_label)
        layout.add_widget(self.week_total_label)

        # Scrollable list
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        layout.add_widget(self.scroll)

        self.msg_label = Label(text="")
        layout.add_widget(self.msg_label)
        self.content = layout

        # Load today's or selected date's expenses
        if date:
            self.date_input.text = date.strftime("%Y-%m-%d")
            self.load_expenses(date)
        else:
            self.load_expenses(datetime.date.today())

    def filter_by_date(self, instance):
        date_str = self.date_input.text.strip()
        for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
            try:
                date = datetime.datetime.strptime(date_str, fmt).date()
                self.load_expenses(date)
                self.msg_label.text = ""
                return
            except ValueError:
                continue
        self.msg_label.text = "Invalid date format. Use YYYY-MM-DD."

    def load_expenses(self, date):
        self.grid.clear_widgets()
        expenses = db.get_expenses()
        # Convert all dates to date objects for comparison
        filtered = []
        for e in expenses:
            exp_date = e.date
            if isinstance(exp_date, str):
                try:
                    exp_date = datetime.datetime.strptime(exp_date, "%Y-%m-%d").date()
                except Exception:
                    continue
            elif isinstance(exp_date, datetime.datetime):
                exp_date = exp_date.date()
            if exp_date == date:
                filtered.append(e)
        day_total = sum(e.amount for e in filtered)
        self.day_total_label.text = f"Day Total: ₹{day_total}"

        # Week total (Monday to Sunday)
        week_start = date - datetime.timedelta(days=date.weekday())
        week_end = week_start + datetime.timedelta(days=6)
        week_expenses = []
        for e in expenses:
            exp_date = e.date
            if isinstance(exp_date, str):
                try:
                    exp_date = datetime.datetime.strptime(exp_date, "%Y-%m-%d").date()
                except Exception:
                    continue
            elif isinstance(exp_date, datetime.datetime):
                exp_date = exp_date.date()
            if week_start <= exp_date <= week_end:
                week_expenses.append(e)
        week_total = sum(e.amount for e in week_expenses)
        self.week_total_label.text = f"Week Total: ₹{week_total}"

        if not filtered:
            self.grid.add_widget(Label(text="No expenses found for this date."))
        for exp in filtered:
            row = BoxLayout(size_hint_y=None, height=40)
            row.add_widget(Label(text=f"₹{exp.amount} | {exp.description} | {exp.date}", size_hint_x=0.8))
            rm_btn = Button(text="Remove", size_hint_x=0.2)
            rm_btn.bind(on_press=lambda btn, eid=exp.id: self.remove_expense(eid, date))
            row.add_widget(rm_btn)
            self.grid.add_widget(row)

    def remove_expense(self, expense_id, date):
        db.remove_expense(expense_id)
        self.load_expenses(date)
        self.msg_label.text = "Expense removed."

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        btn_add = Button(text="Add Today's Expense", size_hint=(1, 0.2))
        btn_add.bind(on_press=self.open_popup)
        btn_history = Button(text="View Expense History", size_hint=(1, 0.2))
        btn_history.bind(on_press=self.open_history)
        self.add_widget(btn_add)
        self.add_widget(btn_history)

    def open_popup(self, instance):
        ExpensePopup().open()

    def open_history(self, instance):
        HistoryPopup().open()

class ExpenseApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    ExpenseApp().run()