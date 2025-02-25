import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import pandas as pd

# Initialize main window
root = tk.Tk()
root.title("MySQL Workbench")
root.geometry("800x600")

# Connection Variables
host_var = tk.StringVar(value='localhost')
port_var = tk.StringVar(value='3306')
user_var = tk.StringVar(value='root')
password_var = tk.StringVar()
database_var = tk.StringVar()

# Function to connect to MySQL server
def connect_to_mysql():
    try:
        global conn
        conn = mysql.connector.connect(
            host=host_var.get(),
            user=user_var.get(),
            password=password_var.get(),
            port=port_var.get()
        )
        if conn.is_connected():
            messagebox.showinfo("Success", "Connected to MySQL Server")
            load_databases()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Function to load databases
def load_databases():
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        database_dropdown['values'] = [db[0] for db in databases]
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Function to connect to a database
def connect_to_database():
    try:
        global db_conn
        db_conn = mysql.connector.connect(
            host=host_var.get(),
            user=user_var.get(),
            password=password_var.get(),
            database=database_var.get(),
            port=port_var.get()
        )
        if db_conn.is_connected():
            messagebox.showinfo("Success", f"Connected to database: {database_var.get()}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Function to execute SQL query
def execute_query():
    try:
        cursor = db_conn.cursor()
        query = query_text.get("1.0", tk.END).strip()
        if query.lower().startswith("select"):
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            display_results(results, columns)
        else:
            cursor.execute(query)
            db_conn.commit()
            messagebox.showinfo("Success", "Query executed successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Function to display query results
def display_results(results, columns):
    for item in result_tree.get_children():
        result_tree.delete(item)
    result_tree['columns'] = columns
    result_tree.heading("#0", text="Index")
    for col in columns:
        result_tree.heading(col, text=col)
        result_tree.column(col, anchor="center")
    for i, row in enumerate(results):
        result_tree.insert("", "end", text=str(i + 1), values=row)

# UI Layout
frame = tk.Frame(root)
frame.pack(pady=20)

# Connection form
tk.Label(frame, text="Host:").grid(row=0, column=0)
tk.Entry(frame, textvariable=host_var).grid(row=0, column=1)
tk.Label(frame, text="Port:").grid(row=1, column=0)
tk.Entry(frame, textvariable=port_var).grid(row=1, column=1)
tk.Label(frame, text="User:").grid(row=2, column=0)
tk.Entry(frame, textvariable=user_var).grid(row=2, column=1)
tk.Label(frame, text="Password:").grid(row=3, column=0)
tk.Entry(frame, textvariable=password_var, show='*').grid(row=3, column=1)
tk.Button(frame, text="Connect to MySQL", command=connect_to_mysql).grid(row=4, column=0, columnspan=2, pady=10)

# Database selection
tk.Label(frame, text="Select Database:").grid(row=5, column=0)
database_dropdown = ttk.Combobox(frame, textvariable=database_var)
database_dropdown.grid(row=5, column=1)
tk.Button(frame, text="Connect to Database", command=connect_to_database).grid(row=6, column=0, columnspan=2, pady=10)

# Query execution
tk.Label(root, text="Enter SQL Query:").pack(pady=10)
query_text = tk.Text(root, height=5)
query_text.pack(pady=5)
tk.Button(root, text="Execute Query", command=execute_query).pack(pady=5)

# Query results
result_tree = ttk.Treeview(root)
result_tree.pack(pady=20, fill='both', expand=True)

root.mainloop()