# Python Bank System 🏛️

A Python-based bank system that allows users to create accounts, deposit and withdraw money, and view account statements.
<br>
The project was created as part of a Digital Innovation One (DIO) project.

## Table of Contents 📋

- [Overview](#overview-)
- [Classes and Methods](#classes-and-methods-)
  - [Customer](#customer)
  - [Individual](#individual)
  - [Account](#account)
  - [CheckingAccount](#checkingaccount)
  - [History](#history)
  - [Transaction](#transaction)
  - [Withdrawal](#withdrawal)
  - [Deposit](#deposit)
- [Functions](#functions-)
  - [deposit](#deposit-1)
  - [withdraw](#withdraw)
  - [display_statement](#display_statement)
  - [create_account](#create_account)
  - [create_customer](#create_customer)
  - [filter_customer](#filter_customer)
  - [retrieve_customer_account](#retrieve_customer_account)
  - [list_accounts](#list_accounts)
- [Menu](#menu)
- [Main](#main)
- [License](#license-)
- [Contact](#contact-)

## Overview 🔎

This project implements a simple bank system with classes to represent customers, accounts, transactions, and transaction histories. The main functionality includes creating users, creating accounts, performing deposits and withdrawals, and displaying account statements.

## Classes and Methods 📜

### Customer

```python
class Customer:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        transaction.record(account)

    def add_account(self, account):
        self.accounts.append(account)
```

- **Customer**: Base class representing a customer.
  - **address**: The address of the customer.
  - **accounts**: List of the customer's accounts.
  - **perform_transaction**: Executes a transaction on a given account.
  - **add_account**: Adds a new account to the customer's list of accounts.

### Individual

```python
class Individual(Customer):
    def __init__(self, address, name, birth_date, id):
        self.name = name
        self.birth_date = birth_date
        self.id = id
        super().__init__(address)
```

- **Individual**: Subclass of `Customer` representing an individual customer.
  - **name**: The name of the individual.
  - **birth_date**: The birth date of the individual.
  - **id**: The identification number of the individual.

### Account

```python
class Account:
    def __init__(self, number, customer):
        self._balance = 0
        self._number = number
        self._branch = "0001"
        self._customer = customer
        self._history = History()

    @classmethod
    def new_account(cls, customer, number):
       return cls(number, customer) 

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number
    
    @property
    def branch(self):
        return self._branch
    
    @property
    def customer(self):
        return self._customer
    
    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        balance = self.balance
        exceeded_balance = balance < amount

        if exceeded_balance:
            print("\nOperation failed! Insufficient balance!")

        elif amount > 0:
            self._balance -= amount
            print("\nWithdrawal successful!")
            return True
        
        else:
            print("\nOperation failed! Invalid amount!")
        
        return False
        
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\nDeposit successful!")
            
        else:
            print("\nOperation failed! Invalid amount!")
            return False
        
        return True
```

- **Account**: Represents a bank account.
  - **_balance**: The balance of the account.
  - **_number**: The account number.
  - **_branch**: The branch code.
  - **_customer**: The customer who owns the account.
  - **_history**: The transaction history of the account.
  - **new_account**: Class method to create a new account.
  - **withdraw**: Withdraws an amount from the account if sufficient balance is available.
  - **deposit**: Deposits an amount into the account.

### CheckingAccount

```python
class CheckingAccount(Account):
    def __init__(self, number, customer, limit=500, withdrawal_limit=3):
        self.limit = limit
        self.withdrawal_limit = withdrawal_limit
        super().__init__(number, customer)

    def withdraw(self, amount):
        withdrawal_count = len([transaction for transaction in self.history.transactions if transaction["type"] == "Withdrawal"])

        exceeded_limit = amount > self.limit
        exceeded_withdrawals = withdrawal_count >= self.withdrawal_limit

        if exceeded_limit:
            print("Operation failed! Withdrawal amount exceeded the limit!")

        elif exceeded_withdrawals:
            print("Operation failed! Maximum number of withdrawals exceeded.")

        else:
            return super().withdraw(amount)

    def __str__(self):
        return f"""
                Branch:\t{self.branch}
                Account Number:\t{self.number}
                Holder:\t{self.customer.name}
        """
```

- **CheckingAccount**: Represents a checking account with limits on withdrawal amounts and the number of withdrawals.
  - **limit**: Maximum withdrawal amount.
  - **withdrawal_limit**: Maximum number of withdrawals allowed.
  - **withdraw**: Overrides the `withdraw` method to include additional checks for withdrawal limits.
  - **__str__**: Returns a string representation of the account details.

### History

```python
class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
            }
        )
```

- **History**: Keeps track of all transactions for an account.
  - **_transactions**: List of transactions.
  - **add_transaction**: Adds a transaction to the history.

### Transaction

```python
class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @classmethod
    @abstractmethod
    def record(self, account):
        pass
```

- **Transaction**: Abstract base class for transactions.
  - **amount**: Abstract property to get the transaction amount.
  - **record**: Abstract method to record the transaction in an account.

### Withdrawal

```python
class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount
    
    def record(self, account):
        transaction_successful = account.withdraw(self.amount)

        if transaction_successful:
            account.history.add_transaction(self)
```

- **Withdrawal**: Represents a withdrawal transaction.
  - **_amount**: The amount to withdraw.
  - **record**: Executes the withdrawal and records it in the account's history if successful.

### Deposit

```python
class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount
    
    def record(self, account):
        transaction_successful = account.deposit(self.amount)

        if transaction_successful:
            account.history.add_transaction(self)
```

- **Deposit**: Represents a deposit transaction.
  - **_amount**: The amount to deposit.
  - **record**: Executes the deposit and records it in the account's history if successful.

## Functions 🔧

### deposit

```python
def deposit(customers):
    id = input("Enter the customer's id: ")
    customer = filter_customer(id, customers)

    if not customer:
        print("\nCustomer not found!")
        return
    
    amount = float(input("Enter the deposit amount: "))
    transaction = Deposit(amount)

    account = retrieve_customer_account(customer)
    if not account:
        return
    
    customer.perform_transaction(account, transaction)
```

- Prompts the user for a customer ID and deposit amount, performs the deposit transaction, and records it.

### withdraw

```python
def withdraw(customers):
    id = input("Enter the customer's id: ")
    customer = filter_customer(id, customers)

    if not customer:
        print("\nCustomer not found!")
        return
    
    amount = float(input("Enter the withdrawal amount: "))
    transaction = Withdrawal(amount)

    account = retrieve_customer_account(customer)
    if not account:
        return
    
    customer.perform_transaction(account, transaction)
```

- Prompts the user for a customer ID and withdrawal amount, performs the withdrawal transaction, and records it.

### display_statement

```python
def display_statement(customers):
    id = input("Enter the customer's id: ")
    customer = filter_customer(id, customers)

    if not customer:
        print("\nCustomer not found!")
        return
    
    account = retrieve_customer_account(customer)
    if not account:
        return
    
    print("\nSTATEMENT:")
    transactions = account.history.transactions

    statement = ""
    if not transactions:
        statement = "No transactions were made."

    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']}: \n\tR${transaction['amount']:.2f}"

    print(statement)
```

- Prompts the user for a customer ID and displays the account statement

Here's the continuation and completion of the README content:

### create_account

```python
def create_account(account_number, customers, accounts):
    id = input("Enter the customer's id: ")
    customer = filter_customer(id, customers)

    if not customer:
        print("Customer not found! Account creation terminated!")
        return
    
    account = CheckingAccount.new_account(customer=customer, number=account_number)
    accounts.append(account)
    customer.accounts.append(account)

    print("\nAccount successfully created!")
```

- Prompts the user for a customer ID, creates a new checking account for the customer, and adds it to the accounts list.

### create_customer

```python
def create_customer(customers):
    id = input("Enter the id (numbers only): ")
    customer = filter_customer(id, customers)

    if customer:
        print("\nA customer with this id already exists!")
        return
    
    name = input("Enter the full name: ")
    birth_date = input("Enter the birth date: ")
    address = input("Enter the address: ")

    customer = Individual(address, name, birth_date, id)

    customers.append(customer)

    print("\nCustomer successfully created!")
```

- Prompts the user for customer details and creates a new individual customer.

### filter_customer

```python
def filter_customer(id, customers):
    filtered_customers = [customer for customer in customers if customer.id == id]
    return filtered_customers[0] if filtered_customers else None
```

- Filters the list of customers by ID and returns the matching customer.

### retrieve_customer_account

```python
def retrieve_customer_account(customer):
    if not customer.accounts:
        print("\nCustomer has no account!")
        return
    
    return customer.accounts[0]
```

- Retrieves the first account of a given customer.

### list_accounts

```python
def list_accounts(accounts):
    for account in accounts:
        print(str(account))
```

- Lists all accounts and prints their details.

## Menu 

```python
menu = '''
Welcome to Awesome Bank, what would you like to do?

    ------Transactions------
    [1] - Deposit
    [2] - Withdraw
    [3] - Check Statement
    [4] - Exit
    ------------------------

    ----------User----------
    [5] - Create User
    [6] - Create Account
    [7] - List Accounts
    ------------------------
'''
```

- Defines the menu options for the bank system.

## Main

```python
def main():
    customers = []
    accounts = []
    
    while True: 
        option = input(menu)

        if option == "1":
            deposit(customers)

        elif option == "2":
            withdraw(customers)

        elif option == "3":
            display_statement(customers)
        
        elif option == "4":
            break

        elif option == "5":
            create_customer(customers)

        elif option == "6":
            account_number = len(accounts) + 1
            create_account(account_number, customers, accounts)

        elif option == "7":
            list_accounts(accounts)

        else:
            print("This is not a valid option!")

main()
```

- The main function initializes lists of customers and accounts and handles user interactions based on menu choices.

## License 🧾

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contact 📩

André Nakamatsu Rocha - [GitHub Profile](https://github.com/andrenakarocha)
LinkedIn - [LinkedIn Profile](https://www.linkedin.com/in/andrenakarocha/)
