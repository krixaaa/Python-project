import tkinter as tk
from tkinter import messagebox, ttk
import os
import csv
from datetime import datetime

EXPENSE_FILE = "expenses.csv"

def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as file:
            reader = csv.reader(file)
            return list(reader)
    return []

def save_expenses():
    with open(EXPENSE_FILE, "w", newline='') as file:
        writer = csv.writer(file)
        for i in range(expense_list.size()):
            writer.writerow(expense_list.get(i).split(" | "))

def add_expense():
    expense = expense_entry.get()
    amount = amount_entry.get()
    category = category_var.get()
    date = date_entry.get()
    if expense and amount and category and date:
        entry = f"{date} | {expense} | {category} | ${amount}"
        expense_list.insert(tk.END, entry)
        update_total()
        expense_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        save_expenses()
    else:
        messagebox.showwarning("Warning", "All fields must be filled!")

def remove_expense():
    try:
        selected_expense_index = expense_list.curselection()[0]
        expense_list.delete(selected_expense_index)
        update_total()
        save_expenses()
    except IndexError:
        messagebox.showwarning("Warning", "Select an expense to remove!")

def update_total():
    total = 0.0
    for i in range(expense_list.size()):
        try:
            amount = float(expense_list.get(i).split(" | ")[-1].replace("$", ""))
            total += amount
        except ValueError:
            pass
    total_label.config(text=f"Total: ${total:.2f}")

def export_csv():
    with open("exported_expenses.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Expense", "Category", "Amount"])
        for i in range(expense_list.size()):
            writer.writerow(expense_list.get(i).split(" | "))
    messagebox.showinfo("Success", "Expenses exported successfully!")

root = tk.Tk()
root.title("Expense Manager")
root.geometry("500x600")
root.configure(bg="#2C3E50")

frame = tk.Frame(root, bg="#2C3E50")
frame.pack(pady=10)

tk.Label(frame, text="Expense Name:", bg="#2C3E50", fg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
expense_entry = tk.Entry(frame, width=20, font=("Arial", 12), bg="#34495E", fg="white", insertbackground="white")
expense_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Amount:", bg="#2C3E50", fg="white", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(frame, width=20, font=("Arial", 12), bg="#34495E", fg="white", insertbackground="white")
amount_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Category:", bg="#2C3E50", fg="white", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5)
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(frame, textvariable=category_var, values=["Food", "Transport", "Bills", "Entertainment", "Others"], state="readonly", width=18)
category_dropdown.grid(row=2, column=1, padx=5, pady=5)
category_dropdown.current(0)

tk.Label(frame, text="Date (YYYY-MM-DD):", bg="#2C3E50", fg="white", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=5)
date_entry = tk.Entry(frame, width=20, font=("Arial", 12), bg="#34495E", fg="white", insertbackground="white")
date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
date_entry.grid(row=3, column=1, padx=5, pady=5)

expense_list = tk.Listbox(root, width=60, height=12, font=("Arial", 12), bg="#34495E", fg="white", selectbackground="#1ABC9C")
expense_list.pack(pady=10)

expenses = load_expenses()
for expense in expenses:
    expense_list.insert(tk.END, " | ".join(expense))

button_frame = tk.Frame(root, bg="#2C3E50")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Expense", command=add_expense, bg="#1ABC9C", fg="black", font=("Arial", 10), width=12).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Remove Expense", command=remove_expense, bg="#E74C3C", fg="black", font=("Arial", 10), width=12).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Export CSV", command=export_csv, bg="#F1C40F", fg="black", font=("Arial", 10), width=12).grid(row=0, column=2, padx=5, pady=5)

total_label = tk.Label(root, text="Total: $0.00", bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
total_label.pack(pady=10)
update_total()

root.mainloop()
