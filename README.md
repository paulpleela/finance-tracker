# Expense Manager

The Expense Manager is a desktop application designed to easily and effectively manage and track financial transactions. This project provides a platform for users to log their income and expenses. Additionally, it offers an Analytics feature for viewing charts by category and timeframe.

- [Features](#features)
  - [User Authentication](#user-authentication)
  - [Main Dashboard](#main-dashboard)
  - [Edit Transactions](#edit-transactions)
  - [View Analytics](#view-analytics)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation and Running the Application](#installation-and-running-the-application)
- [License](#license)


## Features

### User Authentication

* **User Accounts:** Users can register and log in with their username and password.
* **Secure Data:** User passwords and private financial transactions are encrypted and stored safely.
![login page and register page](https://i.imgur.com/OmfLPpg.png)

### Main Dashboard

* **Navigation Buttons:** Easily navigate to the transactions and analytics pages.
* **Daily Summary:** Displays a quick summary of all income and expense transactions made on the current day.
* **Monthly Budget Tracker:** Displays remaining amount from the chosen monthly budget. The budget page helps users calculate and set their budget based on the desired savings amount or percentage of monthly income.
![main dashboard](https://i.imgur.com/p29F68h.png)

### Edit Transactions

* **Income/Expense Table:** Displays a table showing rows of transactions sorted by the most recent date.
* **Adding/Removing Logs:** Simple interface for adding new transactions. Users can easily input details with the category dropdown menu and calendar date selector. Users can delete logs by selecting rows from the table.
* **Filter by Date Range:** Use calendar date selectors to select a start and end date for filtering transactions.
![edit expenses page](https://i.imgur.com/CYI8cZE.png)

### View Analytics

* **Overview Summary:** Displays a bar chart of total income and total expenses from the past few days, months, or years.
* **Expenses Summary:** Displays a pie chart of total expenses made in each category in the current day, month, or year.
![analytics page](https://i.imgur.com/JoXxk7M.png)


## Technologies Used

* **Python:** Program functionality and logic
* **Tkinter:** Graphical user interface
* **SQLite:** Database (for storing login data and transactions)
* **Matplotlib:** Dynamic bar and pie chart generation


## Getting Started

Follow these steps to set up and run the Expense Manager application on your local machine:

### Prerequisites

- [Python](https://www.python.org/) (version 3.7 or higher)
- [Pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)

### Installation and Running the Application

1. Clone this repository:

    ```bash
    git clone https://github.com/paulpleela/expense-manager.git
    ```

2. Navigate to the project directory:

    ```bash
    cd expense-manager
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the program:

    ```bash
    python main.py
    ```  


## License

[MIT](https://choosealicense.com/licenses/mit/)