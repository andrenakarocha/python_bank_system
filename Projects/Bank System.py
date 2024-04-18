menu = '''
Welcome to Awesome Bank! What would you like to do?

    ----------Menu----------
    [1] - Deposit
    [2] - Withdraw
    [3] - Check Extract
    [4] - Leave
    ------------------------
'''

balance = 0
withdraw_limit = 500
extract = ""
number_of_withdraws = 0
NUMBER_WITHDRAW_LIMIT = 3

while True: 
    option = input(menu)

    if option == "1":
        deposit_value = input("Enter the amount to be deposited: ")
        while not deposit_value.isnumeric:
            print("Enter a number!!")
        deposit_value = float(deposit_value)
        balance += deposit_value
        extract += f"\nDeposit of R${deposit_value}"

    elif option == "2":
        if number_of_withdraws >= 3:
            print("You can't make any more withdrawals! The daily withdraw limit has been exceeded!")
        else: 
            withdraw_value = input("Enter the amount to be withdrawn: ")
            while not withdraw_value.isnumeric:
                print("Enter a number!!")
            withdraw_value = float(withdraw_value)
            if withdraw_value > 500: 
                print("It isn't possible to withdraw an amount above R$500!!")
            else:
                balance -= withdraw_value
                number_of_withdraws += 1
                print(f"Daily withdraws left: {3 - number_of_withdraws}")
                extract += f"\nWithdraw of R${withdraw_value}"

    elif option == "3":
        print(f"Your extract: {extract}")
    
    elif option == "4":
        break

    else:
        print("This isn't a valid option!")