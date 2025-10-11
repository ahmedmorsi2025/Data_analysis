import sqlite3
import os

# -------------------------
# DATABASE SETUP (replace old connection)
# -------------------------
home = os.path.expanduser("~")  # user's home folder
db_folder = os.path.join(home, "MyClientApp")
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "clients.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    deposit REAL NOT NULL
)
""")
conn.commit()

# -------------------------
# FUNCTIONS
# -------------------------
def add_client(name, age, deposit):
    cursor.execute("INSERT INTO clients (name, age, deposit) VALUES (?, ?, ?)",
                   (name, age, deposit))
    conn.commit()
    print("✅ Client added!\n")

def list_clients():
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    if not clients:
        print("No clients found.\n")
        return
    print("\nAll saved clients:")
    print("-" * 40)
    for client in clients:
        print(f"ID: {client[0]} | Name: {client[1]} | Age: {client[2]} | Deposit: {client[3]}")
    print("-" * 40 + "\n")

# -------------------------
# MAIN MENU LOOP
# -------------------------
while True:
    choice = input("1. Add client\n2. Show all clients\n3. Exit\nChoose: ")
    if choice == "1":
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        deposit = float(input("Enter deposit: "))
        add_client(name, age, deposit)
    elif choice == "2":
        list_clients()
    elif choice == "3":
        break
    else:
        print("❌ Invalid choice\n")

conn.close()
