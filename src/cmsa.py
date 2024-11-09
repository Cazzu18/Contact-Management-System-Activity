import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Database setup
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS contacts (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT NOT NULL,
   phone TEXT NOT NULL,
   email TEXT NOT NULL
)
''')
conn.commit()

# Main Application Class
class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")

        # Input Fields
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        # GUI Setup
        self.setup_ui()

    def setup_ui(self):
        # Contact Form
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Phone").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(frame, textvariable=self.phone_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Email").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(frame, textvariable=self.email_var).grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(frame, text="Add Contact", command=self.add_contact).grid(row=3, column=0, columnspan=2, pady=10)

        # Contact List
        self.contact_list = ttk.Treeview(self.root, columns=("name", "phone", "email"), show="headings")
        self.contact_list.heading("name", text="Name")
        self.contact_list.heading("phone", text="Phone")
        self.contact_list.heading("email", text="Email")
        self.contact_list.pack(pady=20)

        self.contact_list.bind("<Double-1>", self.load_contact)

        # Update/Delete Buttons
        tk.Button(self.root, text="Update Contact", command=self.update_contact).pack(pady=5)
        tk.Button(self.root, text="Delete Contact", command=self.delete_contact).pack(pady=5)

        # Load contacts
        self.load_contacts()

    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        if not name or not phone or not email:
            messagebox.showerror("Error", "All fields are required!")
            return

        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()

        self.clear_form()
        self.load_contacts()
        messagebox.showinfo("Success", "Contact added successfully!")

    def load_contacts(self):
        # Clear the list
        for row in self.contact_list.get_children():
            self.contact_list.delete(row)

        cursor.execute("SELECT * FROM contacts")
        for row in cursor.fetchall():
            self.contact_list.insert("", "end", iid=row[0], values=(row[1], row[2], row[3]))

    def load_contact(self, event):
        selected_item = self.contact_list.selection()
        if not selected_item:
            return

        contact_id = selected_item[0]
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        contact = cursor.fetchone()

        # Fill the form with the contact's details
        if contact:
            self.name_var.set(contact[1])
            self.phone_var.set(contact[2])
            self.email_var.set(contact[3])
            self.selected_contact_id = contact[0]

    def update_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        if not hasattr(self, "selected_contact_id"):
            messagebox.showerror("Error", "Please select a contact to update!")
            return

        if not name or not phone or not email:
            messagebox.showerror("Error", "All fields are required!")
            return

        cursor.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?", (name, phone, email, self.selected_contact_id))
        conn.commit()

        self.clear_form()
        self.load_contacts()
        messagebox.showinfo("Success", "Contact updated successfully!")

    def delete_contact(self):
        selected_item = self.contact_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a contact to delete!")
            return

        contact_id = selected_item[0]
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()

        self.clear_form()
        self.load_contacts()
        messagebox.showinfo("Success", "Contact deleted successfully!")

    def clear_form(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        if hasattr(self, "selected_contact_id"):
            del self.selected_contact_id

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()

