menu = '''
Welcome to Awesome Bank! What would you like to do?

    ------Transactions------
    [1] - Deposit
    [2] - Withdraw
    [3] - Check Extract
    [4] - Leave
    ------------------------

    ----------User----------
    [5] - Create User
    [6] - Create Account
    [7] - List Accounts
    ------------------------
'''

balance = 0
withdraw_limit = 500
extract = ""
number_of_withdraws = 0
NUMBER_WITHDRAW_LIMIT = 3

USERS_LIST = []
ACCOUNTS_LIST = []
account_number = 0
agency_number = "0001"


def deposit (balance, extract, /):
    while True:
        deposit_value = input("Enter the amount to be deposited: ")
        if "-" in deposit_value:
            print("Enter a positive number!")  
            continue
        else:
            if deposit_value.isnumeric():
                break
            else:
                print("Enter a number!!")
                continue
    deposit_value = float(deposit_value)
    balance += deposit_value
    extract += f"\nDeposit of R${deposit_value}"
    return balance, extract
    
def withdraw (*, balance, extract, value, number_withdraws, withdraw_limit, number_withdraw_limit):
    not_enough_balance = value < balance
    passed_withdraw_limit = value > withdraw_limit
    passed_number_withdraws_limit = number_of_withdraws >= number_withdraw_limit
    
    
    if passed_number_withdraws_limit:
        print("You can't make any more withdrawals! The daily withdraw limit has been exceeded!")
    else:
        while True:
            withdraw_value = input("Enter the amount to be withdrawn: ")
            if "-" in withdraw_value:
                print("Enter a positive number!")  
                continue
            else:
                if withdraw_value.isnumeric():
                    break
                else:
                    print("Enter a number!!")
                    continue
        withdraw_value = float(withdraw_value)
        if not_enough_balance:
            print("You don't have enough balance!")
        else:
            if passed_withdraw_limit:
                print("The withdraw limit is $500!")
            else:
                balance -= withdraw_value
                number_withdraws += 1
                print(f"Daily withdraws left: {3 - number_withdraws}")
                extract += f"\nWithdraw of R${withdraw_value}"
    return balance, extract, number_withdraws

def show_extract(extract, /, *, balance):
    print(f"Your extract: {extract}"
          f"Balance: {balance}")

def filter_user (SSN, users):
    for user in users:
        if user["SSN"] == SSN:
            return True
    return False

def create_user (user_list):
    while True:
        SSN = input("Enter your SSN: ")
        if SSN.isnumeric():
            break
        else:
            print("Invalid value! Enter your SSN!")
            continue
    
    if filter_user(SSN, user_list):
        print("This user already exists!")

    else:    
        while True:
            name = input("Enter your name: ")
            if name.isnumeric():
                print("Invalid value! Enter your name!")
                continue
            else:
                break
                
        birth = input("Enter your birth date (mm/dd/yyyy): ")
        adress = input("Enter your adress (Number, District, City/State): ")
        
        user_list.append({"Name": name, "SSN": SSN, "Birth": birth, "Adress": adress})
        print("User created!")

def create_account (account_list, account_number, agency):
    account_number += 1
    user = input("Enter your SSN to validate your user: ")
    if filter_user(user, USERS_LIST):
        account_list.append({"Agency": agency, "Account Number": account_number, "User": user})
        print("Account created!")
    else:
        print("This user doesn't exist!")
    return account_number

def list_users(accounts_list):
    for account in accounts_list:
        print(f'''
    ===========================
    Agency: {account["Agency"]}
    Account Number: {account["Account Number"]}
    User: {account["User"]}
            ''')

while True: 
    option = input(menu)

    if option == "1":
        balance, extract = deposit(balance, extract)

    elif option == "2":
        balance, extract, number_of_withdraws = withdraw (
            balance = balance, 
            extract = extract, 
            number_withdraws = number_of_withdraws, 
            withdraw_limit = withdraw_limit, 
            number_withdraw_limit = NUMBER_WITHDRAW_LIMIT
        )

    elif option == "3":
        show_extract(extract, balance = balance)
    
    elif option == "4":
        break

    elif option == "5":
        create_user(USERS_LIST)

    elif option == "6":
        account_number = create_account(ACCOUNTS_LIST, account_number, agency_number)

    elif option == "7":
        list_users(ACCOUNTS_LIST)

    else:
        print("This isn't a valid option!")


