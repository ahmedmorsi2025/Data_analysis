import tkinter as tk
from tkinter import messagebox
import psycopg


# Function to insert data
def insert_data():
    name = name_entry.get()
    email = email_entry.get()

    if not name or not email:
        messagebox.showerror("Error", "Please enter both name and email")
        return

    try:
        conn = psycopg.connect(
            host="localhost",
            dbname="postgres",  # your database
            user="postgres",
            password="1234",
            port=5432
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO Users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("Success", "Data inserted successfully!")
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI window
root = tk.Tk()
root.title("Insert Users Data")

# Name field
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

# Email field
tk.Label(root, text="Email:").grid(row=1, column=0, padx=10, pady=5)
email_entry = tk.Entry(root)
email_entry.grid(row=1, column=1, padx=10, pady=5)

# Submit button
submit_btn = tk.Button(root, text="Insert Data", command=insert_data)
submit_btn.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
