# ticket.pyw
# Tiketo - A simple ticket management system with email notifications

import tkinter as tk
from tkinter import messagebox
import json
import uuid
from email_sender import send_outlook_email
import os

TICKETS_FILE = "tickets.json"

def load_tickets():
    try:
        with open(TICKETS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_tickets(tickets):
    with open(TICKETS_FILE, "w") as f:
        json.dump(tickets, f, indent=4)

def create_ticket(title, description):
    tickets = load_tickets()
    ticket_id = str(uuid.uuid4())
    tickets[ticket_id] = {
        "title": title,
        "description": description,
        "status": "open"
    }
    save_tickets(tickets)  #  Correct function to save the data
    print(f"New ticket created: {ticket_id}")   
    send_outlook_email()  # Triggers email + logging
    messagebox.showinfo("Email sent", "tickets.json have been sent!")
    return ticket_id

def submit_ticket():
    title = title_entry.get()
    desc = desc_entry.get("1.0", tk.END).strip()
    print("Path to log file:", os.path.abspath("email_log.txt"))
    if title and desc:
        tid = create_ticket(title, desc)
        messagebox.showinfo("Ticket created", f"New ID: {tid}")
        title_entry.delete(0, tk.END)
        desc_entry.delete("1.0", tk.END)
        refresh_list()
        update_email_status()  #  Now it refreshes the email status label
    else:
        messagebox.showwarning("Error", "You must fill in both title and description.")

def list_tickets():
    tickets = load_tickets()
    return [f"{tid}: {data['title']} ({data['status']})" for tid, data in tickets.items()]

def refresh_list():
    ticket_list.delete(0, tk.END)
    for item in list_tickets():
        ticket_list.insert(tk.END, item)

def delete_ticket():
    selection = ticket_list.curselection()
    if selection:
        selected = ticket_list.get(selection[0])
        ticket_id = selected.split(":")[0]
        tickets = load_tickets()
        if ticket_id in tickets:
            del tickets[ticket_id]
            save_tickets(tickets)
            refresh_list()            
    else:
        messagebox.showwarning("No selection", "Remove ticket.")

def refresh_list():
    ticket_list.delete(0, tk.END)
    for item in list_tickets():
        ticket_list.insert(tk.END, item)

def update_email_status():
    try:
        with open("email_log.txt", "r") as f:
            last_line = f.readlines()[-1].strip()
            email_status_label.config(text=f"Latest emailstatus: {last_line}", fg="green" if "✅" in last_line else "red")
    except:
        email_status_label.config(text="Latest emailstatus: Not available", fg="gray")

# GUI (Tkinter)
root = tk.Tk()
root.title("Tiketo")

tk.Label(root, text="Title:").pack()
title_entry = tk.Entry(root, width=40)
title_entry.pack()

tk.Label(root, text="Description:").pack()
desc_entry = tk.Text(root, height=5, width=40)
desc_entry.pack()
tk.Button(root, text="Refresh", command=refresh_list).pack(pady=5)
tk.Button(root, text="Create ticket", command=submit_ticket).pack(pady=5)
tk.Button(root, text="Remove ticket", command=delete_ticket).pack(pady=5)
tk.Label(root, text="All tickets:").pack()
ticket_list = tk.Listbox(root, width=60)
ticket_list.pack()
email_status_label = tk.Label(root, text="Latest emailstatus: Unknown", fg="gray")
email_status_label.pack()

refresh_list()
update_email_status()
root.mainloop()
