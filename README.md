# 💰 CLI Finance Tracker  <a name="top"></a>

> 🐍 *Educational project built during self-learning of Python*  
> 🎯 *Goal — to strengthen understanding of OOP, file handling, logging, and project architecture.*

---

## 📖 **Project Description**

**CLI Finance Tracker** — a simple yet powerful command-line tool for personal finance tracking.  
It allows you to **quickly add income and expenses**, and **view your financial history by period or transaction type** *(income / expense)*.

---

## 📚 Contents
- [Features](#features) 
- [Educational Purpose & Implementation](#educational-purpose--implementation)
- [Applied Techniques & Concepts](#applied-techniques--concepts)
- [Why This Project Matters](#why-this-project-matters)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation & Running](#installation--running)
- [Example Of Saved File](#example-of-saved-file)
- [Error Handling](#error-handling)
- [Example Usage](#example-usage)
- [Modularity](#modularity)
- [License](#license)
- [Author](#author)

---

<h2 id="features">⚙️ Features</h2>

✅ ➕ **Add income and expenses**  
✅ 🗓️ **View transaction history** — filter by date range or type *(income / expense)*  
✅ 📜 **Browse history by categories** *(e.g., salary, groceries, shopping)*  
✅ 💰 **Analyze total income and expenses** for a chosen period  
✅ 💳 **Track your current balance**  
✅ 🧾 **Clean, readable CLI output** with intuitive formatting  
✅ 🗑️ **Delete specific transactions** directly from history  

> 💡 Built for simplicity — manage your finances efficiently, right from the terminal.  
> No heavy UI. Just Python and logic.

---

<h2 id="educational-purpose--implementation">🧠 Educational Purpose & Implementation</h2>

This project was designed and developed as part of my **self-taught Python journey**.  
The main goal was to **gain hands-on experience and strengthen core understanding of OOP, functional programming, and broader Python development concepts.**

---

<h2 id="applied-techniques--concepts">🔧 Applied Techniques & Concepts</h2>

#### 🏗️ 1. **OOP (Object-Oriented Programming)**
Implemented classes:
- `JsonStorage` → handles JSON file operations *(save/load)*  
- `TransactionFactory` → creates transaction objects  
- `TransactionDictManager` → manages transaction dictionary and data processing  

#### 🔒 2. **Encapsulation**
Used to restrict access to class internals and ensure safe object interactions.

#### ⚙️ 3. **Composition**
`TransactionFactory` relies on an instance of `TransactionDictManager`, creating a modular, composable architecture.

#### 📂 4. **Working with JSON**
Supports **persistent storage** of transaction data across sessions.

#### 🔄 5. **Serialization & Deserialization**
- Before saving → **serialization** to JSON  
- After loading → **deserialization** into Python objects  

#### 🧩 6. **Functional Programming**
Applied techniques like `filter()`, `lambda`, and **closures** for clean, flexible data operations.

#### 🧮 7. **List Comprehensions**
Used extensively to make code concise, readable, and expressive.

#### 🚨 8. **Custom Exceptions**
Introduced **custom error classes** for better error handling and maintainability.

#### 🪵 9. **Logging**
Integrated the built-in `logging` module:  
- 🗃️ Logs written to file  
- ⚠️ Console output for `WARNING` level and above  

---

<h2 id="why-this-project-matters">🧑‍💻 Why This Project Matters</h2>

> This is far more than a “Hello, World!” project —  
> it’s built with **real architectural thinking** and clean code practices.

I’m a **self-taught developer**, and this CLI tracker helped me put theory into practice:
- understanding and applying **OOP principles**  
- using **composition** to structure program flow  
- managing **persistent data storage**  
- writing **readable, maintainable code** with real-world structure  

---

<h2 id="project-structure">🗂️ Project Structure</h2>

```text
📂 finance_tracker/
├── app/
│   ├── factories/
│   │   └── transaction_factory.py
│   ├── logs/
│   │   ├── logger.py
│   │   └── app.log
│   └── storage/
│       ├── data.json
│       ├── json_storage.py
│       └── transaction_dict.py
├── utils/
│   ├── cli_menu.py
│   ├── deserializer.py
│   ├── errors.py
│   └── menu.py
├── main.py
└── README.md
```

---

<h2 id="requirements">⚙️ Requirements</h2>

- Python 3.10+
- No external libraries — only Python standard library is used.

---

<h2 id="installation--running">💻 Installation & Running</h2> 

1. Clone the repository:
```bash
git clone https://github.com/ProstoMishutka/finance-tracker.git
cd finance-tracker
```

2. (Optional) Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate.bat  # Windows cmd
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. Run the main program:
```bash
python main.py
```

---

<h2 id="example-of-saved-file">📂 Example of Saved File</h2> 📂 Example of Saved File

Transactions are stored in **JSON** format in the file:
```text
app/storage/data.json
```
This file is automatically created during the first run of the program.

---
<h2 id="error-handling">⚠️ Error Handling</h2>

The program uses a custom exception system:

| Exception                | When it occurs                                                                      |
|--------------------------|-------------------------------------------------------------------------------------|
| FinanceTrackerError      | Base exception class for the Finance Tracker application.                           |
| EmptyInputError          | Exception raised when a required input from the user is empty.                      |
| InvalidInputError        | Raised when user input is incorrect or does not meet the expected format.           |
| TransactionNotFoundError | Raised when a requested transaction doesn’t exist or match the criteria.            |
| CategoryNotFoundError    | Exception raised when no transactions are found for a specified category.           |
| DateNotFoundError        | Raised when no transactions exist for the given date or the date input is invalid.  |

---

<h2 id="example-usage">🧪 Example Usage</h2>

1. Add a Transaction
> Example of adding an income transaction via the CLI:
```text
================================= 
         FINANCE TRACKER         
================================= 
1. Add a transaction 
2. View transactions 
3. Financial summary 
4. Delete a transaction 
0. Exit 
================================= 
Select an option: 1 
Enter transaction type (income/expense): income 
Enter transaction category: salary 
Enter transaction amount: 20000 
Enter transaction date (YYYY-MM-DD, empty = today): 2025-09-30 
Enter transaction description: cashless transfer 
=============================== 
Transaction added successfully! 
- Type: income 
- Category: salary 
- Amount: 20000.0 
- Date: 2025-09-30 
- Description: Cashless transfer
```

> ✅ This transaction will be saved in `app/storage/data.json` as:
```json
{
    "2025-09-30": [
        {
            "t_type": "income",
            "category": "salary",
            "amount": 20000.0,
            "date": "2025-09-30",
            "description": "Cashless transfer"
        }
    ]
}
```

2. View total income by date range
> Example of view total income for a specific period:
```text
=================================
       VIEW FINANCIAL SUMMARY
=================================
1. View total income by date range
2. View total expenses by date range
3. View current balance
0. Back to main menu
=================================
Select an option: 1
Enter the start date in YYYY-MM-DD format. If left empty, all dates up to the specified end date will be considered: 2010-10-10
Enter the end date (YYYY-MM-DD). If left empty, today's date will be used: 2025-10-10
Total income for the specified period — 20000.00.
```

3. Check current balance:
> Example of viewing the user's current balance
```text
=================================
       VIEW FINANCIAL SUMMARY
=================================
1. View total income by date range
2. View total expenses by date range
3. View current balance
0. Back to main menu
=================================
Select an option: 3
Current balance: 20000.00
```

---

<h2 id="modularity">🧩 Modularity</h2>

The program is divided into logical modules:

- **JsonStorage** — handles saving and loading transaction data to/from JSON files.
- **TransactionFactory** — creates transaction objects based on user input.
- **TransactionDictManager** — manages and processes the collection of transactions.

--- 

<h2 id="license">🧾 License</h2>

This project is distributed under the **MIT License**.  
You are free to use, modify, and distribute it.

---

<h2 id="author">🤝 Author</h2>

**Mykhailo Patserkovskyi**  
Beginner Python Developer 🚀

[Back to top](#top)