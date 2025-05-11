# print("======== Automatic Admin Log In=======\n")
import os
import random

def user_id():
     if not os.path.exists('user.txt') or os.path.getsize('user.txt') ==0:
         return "U0001"
     
     with open("users.txt", "r") as file:
         return f"U{int(file.readlines()[-1].split(',')[0][1:]) + 1:04}"
    
def customer_user_id():
     if not os.path.exists('customer.txt') or os.path.getsize('customer.txt') ==0:
         return "C0001"
     
     with open("customer.txt", "r") as file:
         return f"U{int(file.readlines()[-1].split(',')[0][1:]) + 1:04}"
customer_user_id()    
     
def create_admin():
    if not os.path.exists('user.txt') or os.path.getsize('user.txt') ==0:
        with open("users.txt", "a") as file:
            admin_id=user_id()
            admin_user_name="Admin"
            admin_password="Admin@123"
            file.write(f"{admin_id},{admin_user_name},{admin_password}\n")
        print("Admin was created successfully, with user name 'Admin' and password 'Admin@123'")
create_admin()



# #==========================create_customer function=========================
def create_customer():
        try:
            # if not os.path.exists('customer.txt') or os.path.getsize('customer.txt') ==0:
            #     with open("customer.txt", "a") as file:
                    new_id = customer_user_id()
                    print("Your new customer ID is:", new_id)
                    password = input("Enter password for new customer: ")
                    with open("users.txt", "a") as file:
                        file.write(f"{new_id},{password}\n")
        
        except FileNotFoundError:
            pass
        print(f"Customer {new_id} created successfully!")
#create_customer()


#===============================Transaction_History======================================================
import os
from datetime import datetime
def record_transaction(transaction_type, account_number, amount, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("transaction_history.txt", "a") as file:
        file.write(f"{timestamp} | {transaction_type} | Account: {account_number} | Amount: {amount} | {details}\n")

#=================================================================================
accounts = []
next_account_number = 1001
active_account_number = None

 #=========================create_account====================================
def create_account():
    global next_account_number, active_account_number
    name = input("Enter account holder name: ").strip()
    address = input("Enter account holder address: ").strip()
    date_of_birth = input("Enter account holder D.O.B (DD/MM/YYYY): ").strip()

    try:
        new_id = input("Enter customer_id: ").strip()  
        age = int(input("Enter account holder age: "))
        initial_balance = float(input("Enter initial balance: "))
        if initial_balance < 0:
            print("Initial balance cannot be negative.")
            return None
    except ValueError:
        print("Invalid input for age or balance.")
        return None

    account_details = [
        next_account_number,
        new_id,
        name,
        address,
        date_of_birth,
        age,
        initial_balance
    ]
    record_transaction("Account Creation", next_account_number, initial_balance, "Initial deposit")
    
    active_account_number=next_account_number
    next_account_number += 1
    accounts.append(account_details)

    return account_details

account_details = create_account()

if account_details:
    with open("customers.txt", "a") as file:
        file.write(f"({account_details[0]}, {account_details[1]}, {account_details[2]})\n")

    with open("userdetails.txt", "a") as file:
        file.write(f"({account_details[0]},{account_details[2]}, {account_details[3]}, {account_details[4]}, {account_details[5]})\n")

if account_details:
    print("Account created successfully!")
    print(f"Account Number: {account_details[0]}")
    print(f"Customer_ID: {account_details[1]}")
    print(f"Name: {account_details[2]}")
    print(f"Address: {account_details[3]}")
    print(f"D.O.B: {account_details[4]}")
    print(f"Age: {account_details[5]}")
    print(f"Balance: {account_details[6]}")
else:
    print("Account creation failed. Please try again with valid inputs.")

#=============================Admin_Login==============================
def admin_login():
    print("===<<<Admin Login ===>>>")
    admin_username = input("Enter admin username: ").strip()
    admin_password = input("Enter admin password: ").strip()
    if admin_username == "Admin" and admin_password == "Admin@123":
        print("Admin login successful!")
        return True
    else:
        print("Invalid admin credentials.")
        return False

#=========================Customer_Login===============================
def customer_login():
    print("<<<=== Customer Login ===>>>")
    input_customer_id = input("Enter your customer ID: ").strip()
    input_password = input("Enter your password: ").strip()
    
    try:
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(',')
        if len(parts) >= 2 and parts[0] == input_customer_id and parts[1] == input_password:
            print("Login successful!")
            return input_customer_id

                    
        print("Invalid credentials. Please try again.")
        return None
    except FileNotFoundError:
        print("User database not found. Please contact the administrator.")
        return None

#=============================Deposit_function============================
accounts = []
next_account_number = 1001
def deposit():
    global active_account_number
    if active_account_number is None:
        print("No active account. Please create an account first.")
        return

    try:
        deposit_amount = float(input("Enter deposit amount: "))
        if deposit_amount <= 0:
            print("deposit amount must be positive.")
            return
    except ValueError:
        print("Invalid input for deposit amount.")
        return
    account = next((acc for acc in accounts if acc[0] == active_account_number), None)
    if account is None:
        print("Account not found.")
        return
    
    account[6] += deposit_amount
    print("deposit successful!")
    print(f"Account Number: {account[0]}")
    print(f"New Balance: {account[6]}")
    record_transaction("Deposit", account[0], deposit_amount, f"New balance: {account[6]}")


#======================Withdraw_function====================================================
accounts = []
next_account_number = 1001
active_account_number = None
def withdraw():
    global active_account_number
    if active_account_number is None:
        print("No active account. Please create an account first.")
        return

    try:
        withdrawal_amount = float(input("Enter withdrawal amount: "))
        if withdrawal_amount <= 0:
            print("Withdrawal amount must be positive.")
            return
    except ValueError:
        print("Invalid input for withdrawal amount.")
        return
    account = next((acc for acc in accounts if acc[0] == active_account_number), None)
    if account is None:
        print("Account not found.")
        return

    if account[6] < withdrawal_amount:
        print("Insufficient funds.")
        return

    account[6] -= withdrawal_amount
    print("Withdrawal successful!")
    print(f"Account Number: {account[0]}")
    print(f"New Balance: {account[6]}")
    record_transaction("Withdraw", account[0], withdrawal_amount, f"New balance: {account[6]}")


# #=======================Money_transfer_function==============================
accounts = []
next_account_number = 1001
active_account_number = None
def transfer_money():
    global active_account_number
    if active_account_number is None:
        print("No active source account. Please create an account first.")
        return
    try:
        from_account_number = int(input("Enter from account number: "))
        destination_account_number = int(input("Enter destination account number: "))
        transfer_amount = float(input("Enter transfer amount: "))
        if transfer_amount <= 0:
            print("Transfer amount must be positive.")
            return
    except ValueError:
        print("Invalid input. Please enter valid numbers for destination account and transfer amount.")
        return
    from_account = next((acc for acc in accounts if acc[0] == active_account_number), None)
    destination_account = next((acc for acc in accounts if acc[0] == destination_account_number), None)

    if from_account is None:
        print("From account not found. Please check the active account.")
        return
    if destination_account is None:
        print("Destination account not found.")
        return
    if from_account[6] < transfer_amount:
        print("Insufficient funds in the source account.")
        return
    from_account[6] -= transfer_amount
    destination_account[6] += transfer_amount

    print("Transfer successful!")
    print(f"From Account ({from_account[0]}) new balance: {from_account[6]}")
    print(f"Destination Account ({destination_account[0]}) new balance: {destination_account[6]}")

    record_transaction("Transfer Debit", from_account_number, transfer_amount, f"Money Transferred to account {destination_account_number}. New balance: {from_account[6]}")
    record_transaction("Transfer Credit", destination_account_number, transfer_amount, f"Money Received from account {from_account_number}. New balance: {destination_account[6]}")


#=========================Check_Balance_function======================================================================
def check_balance():
    global active_account_number
    if active_account_number is None:
        print("No active account. Please create an account first.")
        return
    account = next((acc for acc in accounts if acc[0] == active_account_number), None)
    if account is None:
        print("Account not found.")
        return
    
    print(f"Account Number: {account[0]}")
    print(f"Your Balance: {account[6]}")
#==================================================================================

#=============================update account details=============================
def update_account_details():
    try:
        acc_num=int(input("Enter the account number to update"))
    except ValueError:
        print("Invalid account number.Enter a valid account number.")
        return
    account=next((acc for acc in accounts if acc[0] == acc_num), None)
    if account is None:
        print("Account not found.")
        return

    print("Enter the new details.")
    new_name        = input(f"Current Name ({account[2]}): ").strip()
    new_address     = input(f"Current Address ({account[3]}): ").strip()
    new_dob         = input(f"Current D.O.B ({account[4]}): ").strip()
    new_age         = input(f"Current Age ({account[5]}): ").strip()
    
    if new_name:
        account[2] = new_name
    if new_address:
        account[3] = new_address
    if new_dob:
        account[4] = new_dob
    if new_age:
        try:
            account[5] = int(new_age)
        except ValueError:
            print("Invalid age provided; keeping current age.")

    print("Account details updated successfully!")
    print("Updated Details:", account)

#=========================Transaction_History_Function==============


# #=======================================================================
def admin_menu():
    while True:
        print("========Admin Menu========")
        print("1. Create Customer")
        print("2. Create Account")
        print("3.Deposit")
        print("4. Withdraw")
        print("5.Check Balance")
        print("6. Transfer Money")
        print("7. Transaction History")
        ## print("8. Change Intrest rate")(working on it update on future)
        print(".8 Update Accounts Details")
        print("9. Logout")

        try:
            choice = int(input("Enter a number from 1 to 9: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if choice==1:
            print(">~~~=====Create_Customer=====~~~<")
            create_customer()
        elif choice==2:
            print(">~~~=====Create_Account=====~~~<")
            create_account()
        elif choice==3:
            print(">~~~=====Deposit_Money=====~~~<")
            deposit()
        elif choice==4:
            print(">~~~=====Withdraw_Money=====~~~<")
            withdraw()        
        elif choice==5:
            print(">~~~=====Check_Balance=====~~~<")
            check_balance()        
        elif choice==6:
            print(">~~~=====Transfer_Money=====~~~<")
            transfer_money()       
        elif choice==7:
            print(">~~~=====Transaction_History=====~~~<")
            record_transaction()
        elif choice==8:
            print(">~~~=====Update_Account_Details=====~~~<")
            update_account_details()
        elif choice==9:
            print("Thanks for using the service.")
            break
        else:
            print("Invalid choice.")

# #====================================================================
def customer_menu(customer_id):
    while True:
        print("========Customer Menu========")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer Money")
        print("4. Transaction History")
        print("5.Check Balance")
        #### print("6. View Interest rate")
        ##### print("7. View All Accounts")
        print("6. Logout")

        try:
            choice = int(input("Enter a number from 1 to 8: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if choice==1:
            print(">~~~=====Deposit_Money=====~~~<")
            deposit()
        elif choice==2:
            print(">~~~=====Withdraw_Money=====~~~<")
            withdraw()
        elif choice==3:
            print(">~~~=====Transfer_Money=====~~~<")
            transfer_money()
        elif choice==4:
            print(">~~~=====Transaction_History=====~~~<")
            record_transaction()
        elif choice==5:
            print(">~~~=====Check_Balance=====~~~<")
            check_balance()
        elif choice==6:
            print("Thanks for using the service.")
            break
        else:
            print("Invalid choice.")



#======================Main_menu===================================
def main():
    print("Welcome to the Banking App")
    role = input("Login as (admin/customer): ").strip()
    
    if role == "admin":
        if admin_login():
            admin_menu()
    elif role == "customer":
        logged_in_customer = customer_login()
        if logged_in_customer:
            customer_menu(logged_in_customer)
        else:
            print("Customer login failed.")
    else:
        print("Invalid role selected.")

if __name__ == "__main__":
    main()
 