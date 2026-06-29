import mysql.connector
import csv
import matplotlib.pyplot as plt
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="expense_tracker"
)

cursor = conn.cursor()
class Expenses:
    def __init__(self, id,description, category, expense_date, amount):
        self.id= id
        self.category= category
        self.expense_date= expense_date
        self.amount= amount
        self.description= description
monthly_expenses=30000
def show_row(row):
    print(f"ID: {row[0]} | ₹{row[4]} | Category: {row[1]} | Desc: {row[2]} | Date: {row[3]} | ")
while True:
    print("\n Expense Tracker")
    print("1. Add")
    print("2. View")
    print("3. Search")
    print("4. Delete")
    print("5. Edit expense")
    print("6. Show total spending")
    print("7. Category-wise details")
    print("8. Highest Category Amount")
    print("9. Budget Tracker")
    print("10. Export to CSV")
    print("11. Monthly spending report")
    print("12. Expense Pie Chart")
    print("13. Exit")

    choice= input("Enter your choice: ")
    
    
    if choice == "1":
     
        category=input("Enter category: ")
        expense_date= input("Enter Date: ")
        amount= int(input ("Enter amount: "))
        description= input("Enter description: ")
        cursor.execute(
            "INSERT INTO expenses (description, category, expense_date, amount) VALUES ( %s, %s, %s, %s)",
            (description, category, expense_date, amount)
        )

        conn.commit()
        
        print("Added successfully!")
    elif choice =="2":
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()

        for row in rows:
            show_row(row)
    elif choice =="3":
        category = input("Enter category: ")

        cursor.execute("SELECT id, category, description, expense_date, amount FROM expenses WHERE category = %s", (category,))
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                show_row(row)        
        else:
            print("No expenses found for this category")
    elif choice=="4":
        delete_id = int(input("Enter expense ID: "))
        cursor.execute("DELETE FROM expenses WHERE id = %s", (delete_id,))
        conn.commit()

        print("Deleted successfully!")
    elif choice=="5":

        edit_id = int(input("Enter expense ID: "))
        cursor.execute(
            "SELECT * FROM expenses WHERE id= %s",
            (edit_id,)
        )
        row= cursor.fetchone()
        if row is None:
            print("No expense found with that ID.")
        else:
            category = input("New category: ")
            description = input("New description: ")
            expense_date = input("New date: ")
            amount = int(input("New amount: "))

            cursor.execute("""
                UPDATE expenses
                SET category=%s, description=%s, expense_date=%s, amount=%s
                WHERE id=%s
            """, (category, description, expense_date, amount, edit_id))

            conn.commit()
            print("Updated successfully!")
    elif choice == "6":
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0

        print(f"Total amount: ₹{total}")
    elif choice == "7":
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        rows = cursor.fetchall()

        for row in rows:
            print(f"{row[0]}: ₹{row[1]}")
    elif choice == "8":
        cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
            LIMIT 1
        """)

        row = cursor.fetchone()
        if row:
            print(f"Highest spending category: {row[0]}")
            print(f"Amount: ₹{row[1]}")
        else: print("No data available")
    elif choice=="9":
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0

        remaining_budget = monthly_expenses - total

        if remaining_budget>0:
            print(f"Remaining budget = ₹{remaining_budget}")
        elif remaining_budget<0:
            print(f" Budget Exceeded by ₹{-(remaining_budget)}")
        else:
            print("Budget exactly reached!")  
   
    elif choice == "10":
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()

        if rows:
            with open("expenses.csv", "w", newline="") as file:
                writer = csv.writer(file)

            # header
                writer.writerow(["id", "amount", "category", "description", "expense_date"])

            # data
                for row in rows:
                    writer.writerow(row)

            print("CSV file created successfully: expenses.csv")
        else:
            print("No data to export")

    elif choice == "11":
        cursor.execute("""
            SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month,
                SUM(amount)
            FROM expenses
            GROUP BY month
            ORDER BY month
            """)

        rows = cursor.fetchall()

        for row in rows:
            print(f"Date: {row[0]} | ₹{row[1]} ")
    
    elif choice == "12":
        

        cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        """)

        rows = cursor.fetchall()
        

        categories = []
        amounts = []

        for row in rows:
            categories.append(row[0])
            amounts.append(float(row[1]))

        plt.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%"
        )

        plt.title("Expense Distribution by Category")

        plt.show()
            

    elif choice=="13":
        print("Exit")
        break
    


        