from abc import ABC, abstractmethod

class Customer:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        transaction.record(account)

    def add_account(self, account):
        self.accounts.append(account)

class Individual(Customer):
    def __init__(self, address, name, birth_date, id):
        self.name = name
        self.birth_date = birth_date
        self.id = id
        super().__init__(address)

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

class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @classmethod
    @abstractmethod
    def record(self, account):
        pass

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
    transactions =  account.history.transactions

    statement = ""
    if not transactions:
        statement = "No transactions were made."

    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']}: \n\tR${transaction['amount']:.2f}"

    print(statement)

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

def filter_customer(id, customers):
    filtered_customers = [customer for customer in customers if customer.id == id]
    return filtered_customers[0] if filtered_customers else None

def retrieve_customer_account(customer):
    if not customer.accounts:
        print("\nCustomer has no account!")
        return
    
    return customer.accounts[0]

def list_accounts(accounts):
    for account in accounts:
        print(str(account))

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