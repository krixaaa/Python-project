import tkinter as tk
from tkinter import messagebox, ttk
import os
import csv
from datetime import datetime
from collections import defaultdict

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
        update_summary()
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
        update_summary()
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

def update_summary():
    expenses = [expense_list.get(i).split(" | ") for i in range(expense_list.size())]
    
    category_totals = defaultdict(float)
    highest_expense = ("", 0.0)
    daily_totals = defaultdict(float)
    
    for date, name, category, amount in expenses:
        amount_value = float(amount.replace("$", ""))
        category_totals[category] += amount_value
        daily_totals[date] += amount_value
        if amount_value > highest_expense[1]:
            highest_expense = (name, amount_value)
    
    summary_text = "Total by Category:\n"
    for cat, total in category_totals.items():
        summary_text += f"{cat}: ${total:.2f}\n"
    
    if highest_expense[0]:
        summary_text += f"\nHighest Expense: {highest_expense[0]} - ${highest_expense[1]:.2f}\n"
    
    avg_spending = sum(daily_totals.values()) / len(daily_totals) if daily_totals else 0
    summary_text += f"\nAvg Daily Spending: ${avg_spending:.2f}"
    
    summary_label.config(text=summary_text)

root = tk.Tk()
root.title("Expense Manager")
root.geometry("500x700")
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

tk.Button(button_frame, text="Add Expense", command=add_expense, bg="#1ABC9C", fg="black", font=("Arial", 10), width=15).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Remove Expense", command=remove_expense, bg="#E74C3C", fg="black", font=("Arial", 10), width=15).grid(row=0, column=1, padx=5, pady=5)

total_label = tk.Label(root, text="Total: $0.00", bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
total_label.pack(pady=10)

summary_label = tk.Label(root, text="", bg="#2C3E50", fg="white", font=("Arial", 12), justify="left")
summary_label.pack(pady=10)

update_total()
update_summary()

root.mainloop()
