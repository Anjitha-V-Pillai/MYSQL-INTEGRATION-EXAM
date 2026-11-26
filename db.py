import mysql.connector

class Bank_db:

    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                user="root",
                password="root",
                host="localhost",
                database="bank_management"
            )
            print("Database Connected Successfully")
        except:
            self.con = None
            print("Connection Failed")

    def create(self, name, account_type, phone, balance):
        try:
            if balance < 0:
                print("Balance cannot be negative")
                return

            cursor = self.con.cursor()
            query = "insert into accounts(customer_name,account_type,phone,balance) values(%s,%s,%s,%s)"
            data = (name, account_type, phone, balance)

            cursor.execute(query, data)
            self.con.commit()

            print("Account Created Successfully")

        except:
            print("Failed to Create Account")

    def read(self, min_balance=None):
        try:
            cursor = self.con.cursor()

            if min_balance is not None:
                query = "select * from accounts where balance >= %s order by balance desc"
                data = (min_balance,)
                cursor.execute(query, data)
            else:
                query = "select * from accounts order by balance desc"
                cursor.execute(query)

            records = cursor.fetchall()

            if records:
                for row in records:
                    print(row)
            else:
                print("No Records Found")

        except:
            print("Failed to Read")

    def retrieve(self, keyword):
        try:
            cursor = self.con.cursor()

            if keyword.isdigit():
                query = "select * from accounts where account_id=%s"
                data = (int(keyword),)
            else:
                query = "select * from accounts where customer_name like %s"
                data = ("%" + keyword + "%",)

            cursor.execute(query, data)
            records = cursor.fetchall()

            if records:
                for row in records:
                    print(row)
            else:
                print("No Records Found")

        except:
            print("Failed to Search")

    def deposit(self, account_id, amount):
        try:
            if amount <= 0:
                print("Amount must be positive")
                return

            cursor = self.con.cursor()
            query = "update accounts set balance=balance+%s where account_id=%s"
            data = (amount, account_id)

            cursor.execute(query, data)
            self.con.commit()

            if cursor.rowcount > 0:
                print("Deposited Successfully")
            else:
                print("No Record Found")

        except:
            print("Failed to Deposit")

    def withdraw(self, account_id, amount):
        try:
            if amount <= 0:
                print("Amount must be positive")
                return

            cursor = self.con.cursor()
            query = "update accounts set balance=balance-%s where account_id=%s and balance >= %s"
            data = (amount, account_id, amount)

            cursor.execute(query, data)
            self.con.commit()

            if cursor.rowcount > 0:
                print("Withdrawn Successfully")
            else:
                print("Insufficient Balance or Invalid Account ID")

        except:
            print("Failed to Withdraw")

    def delete(self, account_id):
        try:
            cursor = self.con.cursor()
            query = "delete from accounts where account_id=%s"
            data = (account_id,)

            cursor.execute(query, data)
            self.con.commit()

            if cursor.rowcount > 0:
                print("Account Deleted Successfully")
            else:
                print("No Record Found")

        except:
            print("Failed to Delete")

    def summary(self):
        try:
            cursor = self.con.cursor()
            query = "select count(*),sum(balance),avg(balance) from accounts"
            cursor.execute(query)

            total_acc, total_bal, avg_bal = cursor.fetchone()

            print("Total Accounts:", total_acc)
            print("Total Balance:", total_bal)
            print("Average Balance:", avg_bal)

            query = "select account_type, count(*) from accounts group by account_type"
            cursor.execute(query)
            type_records = cursor.fetchall()
            print("Accounts by Type:")
            for row in type_records:
                print(row)

        except:
            print("Failed to get summary")


b = Bank_db()

while(1):

    print("1. Create Account")
    print("2. View All Accounts")
    print("3. Search Account")
    print("4. Deposit Amount")
    print("5. Withdraw Amount")
    print("6. Delete Account")
    print("7. Account Summary")
    print("8. Exit")

    try:
        ch = int(input("Enter your choice:"))
    except ValueError:
        print("Invalid Input")
        continue

    if ch == 1:
        n = input("Enter customer name:")
        t = input("Enter account type:")
        p = input("Enter phone:")
        bal = int(input("Enter opening balance:"))
        b.create(n, t, p, bal)

    elif ch == 2:
        opt = input("Filter by minimum balance? (y/n):")
        if opt == "y":
            min_b = int(input("Enter minimum balance:"))
            b.read(min_b)
        else:
            b.read()

    elif ch == 3:
        key = input("Enter account ID or customer name:")
        b.retrieve(key)

    elif ch == 4:
        acc_id = int(input("Enter account ID:"))
        amt = int(input("Enter deposit amount:"))
        b.deposit(acc_id, amt)

    elif ch == 5:
        acc_id = int(input("Enter account ID:"))
        amt = int(input("Enter withdrawal amount:"))
        b.withdraw(acc_id, amt)

    elif ch == 6:
        acc_id = int(input("Enter account ID:"))
        confirm = input("Confirm delete? (y/n):")

        if confirm == "y":
            b.delete(acc_id)
        else:
            print("Cancelled")

    elif ch == 7:
        b.summary()

    elif ch == 8:
        if b.con:
            b.con.close()
        print("Database Connection Closed")
        break

    else:
        print("Invalid Input")
