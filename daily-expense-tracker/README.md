# Daily Expense Tracker

## Overview
The Daily Expense Tracker is a Kivy-based application designed to help users manage their daily expenses efficiently. The app allows users to add, update, and delete expense entries, providing a simple and intuitive interface for tracking financial activities.

## Features
- Add new expense entries with details such as amount, description, and date.
- Update existing expense records.
- Delete expense entries.
- View a list of all recorded expenses.

## Project Structure
```
daily-expense-tracker
├── src
│   ├── main.py               # Entry point of the application
│   ├── ui
│   │   └── main.kv          # User interface layout
│   ├── models
│   │   └── expense.py        # Expense model definition
│   ├── controllers
│   │   └── expense_controller.py # Logic for managing expenses
│   └── utils
│       └── db.py            # Database utility functions
├── requirements.txt          # Project dependencies
├── buildozer.spec           # Build configuration for APK
└── README.md                 # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd daily-expense-tracker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Building APK
To package the application into an APK, use Buildozer:
1. Install Buildozer:
   ```
   pip install buildozer
   ```

2. Navigate to the project directory and run:
   ```
   buildozer -v android debug
   ```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.