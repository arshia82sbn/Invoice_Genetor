import os
import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox  # Importing ctkmessagebox for notifications
from docxtpl import DocxTemplate
import datetime as dt

# Initial window setup
window = ctk.CTk()
window.title("Invoice Generator Form")
window.geometry("1000x800")
window._set_appearance_mode("dark")

# Variables for quantities and prices
qty_num = ctk.IntVar(value=0)
price_num = ctk.DoubleVar(value=0.0)
entry_var = ctk.StringVar(value="0")  

def validate_input(var, index, mode):
    value = entry_var.get()
    try:
        float(value)  # If the value is not a valid number, an exception will be raised
    except ValueError:
        entry_var.set("0")  # Reset invalid input to "0"


entry_var.trace_add("write", validate_input)


def limit_phone_entry(*args):
    value = phone_entry.get()
    if len(value) > 10:  # Limit to 10 digits
        phone_entry.delete(10, ctk.END)

    phone_entry.bind("<KeyRelease>", limit_phone_entry)


#make generate_invoice
def generate_invoice():
    doc = DocxTemplate(r"C:\Users\Arshia\OneDrive\Documents\programming\python trian\trading app\invoice_template.docx")
    if not os.path.exists(r"C:\Users\Arshia\OneDrive\Documents\programming\python trian\trading app\invoice_template.docx"):
        CTkMessagebox(title="Error", message="Template file not found!", icon="cancel")
        return
    # Get the values from the entry fields
    name = f"{first_name_entry.get()} {last_name_entry.get()}"
    phone = phone_entry.get()
    limit_phone_entry()
    try:
        salestax = float(tax_entry.get()) / 100
    except ValueError:
        salestax = 0.1
    subtotal = round(sum(item[3] for item in invoice_list), 2)
    total = round(subtotal * (1 - salestax), 2)

    total = subtotal*(1-salestax)
    if not invoice_list:
        CTkMessagebox(title="Error", message="Invoice list is empty!", icon="cancel")
        return

        
    doc.render({"name":name,
            "phone":phone,
            "invoice_list":invoice_list,
            "subtotal":subtotal,
            "salestax":str(salestax*100)+"%",
            "total":total})
    doc_name = "new_inovice" + name + dt.datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".docx"
    doc.save(doc_name)
    CTkMessagebox(title="Success", message=f"Invoice saved as {doc_name}", icon="check")

    
def new_invoice():
    # Clear the entry fields
    first_name_entry.delete(0, ctk.END)
    last_name_entry.delete(0, ctk.END)
    phone_entry.delete(0,ctk.END)
    tax_entry.delete(0,ctk.END)
    clear_item()
    delete_all_row()
    invoice_list.clear()
    
# Function to clear input fields
def clear_item():
    qty_entry.delete(0, ctk.END)
    desc_entry.delete(0, ctk.END)
    price_entry.delete(0, ctk.END)
    qty_num.set(0)
    price_num.set(0.0)

invoice_list = []
# Function to add item to the invoice
def add_item():
    try:
        qty = int(qty_entry.get())
        desc = desc_entry.get()
        price = float(price_entry.get())
        
        # Ensure input values are valid
        if qty <= 0 or price <= 0 or not desc.strip():
            CTkMessagebox(title="Error", message="Please enter valid Quantity, Description, and Price!", icon="cancel")
            return
        
        line_total = qty * price
        invoice_item = [qty, desc, price, line_total]
        
        invoice_list.append(invoice_item)
        
        # Add item to the invoice table
        add_row(invoice_item)
        clear_item()
        CTkMessagebox(title="Success", message="Item added successfully!", icon="check")
    except ValueError:
        CTkMessagebox(title="Error", message="Please enter valid numbers for Quantity and Price!", icon="cancel")

# Functions to increase or decrease Quantity
def increase_qty():
    qty_num.set(qty_num.get() + 1)

def decrease_qty():
    if qty_num.get() > 0:  # Prevent negative values
        qty_num.set(qty_num.get() - 1)

# Functions to increase or decrease Price
def increase_price():
    if price_num.get() < 500:  # Limit to 500
        price_num.set(round(price_num.get() + 0.5, 2))

def decrease_price():
    if price_num.get() > 0:  # Prevent negative values
        price_num.set(round(price_num.get() - 0.5, 2))

# Main frame for input fields
frame = ctk.CTkFrame(window, width=1000, height=600)
frame.pack(pady=20, padx=20)

# First and Last Name Labels and Entries
first_name_label = ctk.CTkLabel(frame, text="First Name")
first_name_label.grid(row=0, column=0, padx=10, pady=10)
first_name_entry = ctk.CTkEntry(frame)
first_name_entry.grid(row=1, column=0, padx=10, pady=10)

last_name_label = ctk.CTkLabel(frame, text="Last Name")
last_name_label.grid(row=0, column=1, padx=10, pady=10)
last_name_entry = ctk.CTkEntry(frame)
last_name_entry.grid(row=1, column=1, padx=10, pady=10)

# Phone Label and Entry
phone_label = ctk.CTkLabel(frame, text="Phone")
phone_label.grid(row=0, column=2, padx=10, pady=10)
phone_entry = ctk.CTkEntry(frame)
phone_entry.grid(row=1, column=2, padx=10, pady=10)

# Quantity Section
qty_label = ctk.CTkLabel(frame, text="Quantity")
qty_label.grid(row=2, column=0, padx=10, pady=10)
qty_entry = ctk.CTkEntry(frame, textvariable=qty_num, justify="center", font=("Arial", 16), width=100)
qty_entry.grid(row=2, column=1, padx=10, pady=10)
qty_increase = ctk.CTkButton(frame, text="+", width=40, command=increase_qty)
qty_increase.grid(row=2, column=2, padx=5, pady=5)
qty_decrease = ctk.CTkButton(frame, text="-", width=40, command=decrease_qty)
qty_decrease.grid(row=2, column=3, padx=5, pady=5)

# Description Section
desc_label = ctk.CTkLabel(frame, text="Description")
desc_label.grid(row=2, column=4, padx=10, pady=10)
desc_entry = ctk.CTkEntry(frame)
desc_entry.grid(row=2, column=5, padx=10, pady=10)

#taxlabel
tax_label = ctk.CTkLabel(frame, text="Sales Tax (%)")
tax_label.grid(row=4, column=0, padx=10, pady=10)
tax_entry = ctk.CTkEntry(frame, justify="center", font=("Arial", 16), width=100)
tax_entry.grid(row=4, column=1, padx=10, pady=10)


# Unit Price Section
price_label = ctk.CTkLabel(frame, text="Unit Price")
price_label.grid(row=3, column=0, padx=10, pady=10)
price_entry = ctk.CTkEntry(frame, textvariable=price_num, justify="center", font=("Arial", 16), width=100)
price_entry.grid(row=3, column=1, padx=10, pady=10)
price_increase = ctk.CTkButton(frame, text="+", width=40, command=increase_price)
price_increase.grid(row=3, column=2, padx=5, pady=5)
price_decrease = ctk.CTkButton(frame, text="-", width=40, command=decrease_price)
price_decrease.grid(row=3, column=3, padx=5, pady=5)

# Add Item Button
add_item_button = ctk.CTkButton(frame, text="Add Item", command=add_item)
add_item_button.grid(row=4, column=0, columnspan=6, padx=10, pady=10)

# Header for Invoice Table
columns = ('Qty', 'Description', 'Price', 'Total')
header_frame = ctk.CTkFrame(window)
header_frame.pack(pady=10, padx=10, fill="x")
for col in columns:
    header_label = ctk.CTkLabel(header_frame, text=col, width=100, anchor="center")
    header_label.pack(side="left", padx=5)
# Frame for the scrollable table
rows_frame = ctk.CTkFrame(window)
rows_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Adding Canvas to make the table scrollable
canvas = ctk.CTkCanvas(rows_frame, bg="#2B2B2B", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ctk.CTkScrollbar(rows_frame, orientation="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Frame inside the Canvas
scrollable_frame = ctk.CTkFrame(canvas, fg_color="#2B2B2B")

# Add the scrollable frame to the Canvas
scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Configure scrolling
def configure_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scroll)
canvas.configure(yscrollcommand=scrollbar.set)

# Function to add a row to the table
def add_row(data):
    row_frame = ctk.CTkFrame(scrollable_frame)
    row_frame.pack(fill="x", pady=5)
    for item in data:
        cell_label = ctk.CTkLabel(row_frame, text=item, width=100, anchor="center")
        cell_label.pack(side="left", padx=5)

# Function to delete all rows from the table
def delete_all_row():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

def process_entry():
    # Get the input value from the entry field
    value = entry_var.get().strip()

    # Check if the value is empty and replace it with "0" to prevent errors
    if value == "":
        value = "0"  

    try:
        value = float(value)  # Convert the value to a float number
    except ValueError:
        value = 0  # If conversion fails, set the value to zero

    # Use the corrected value
    print("Valid input value:", value)

# Create a button to trigger the process_entry function
submit_button = ctk.CTkButton(window, text="check", command=process_entry)
submit_button.pack(pady=10)

# Generate Invoice Button
save_invoice_button = ctk.CTkButton(frame, text="Generate Invoice",command=generate_invoice)
save_invoice_button.grid(row=6, column=0, pady=5, padx=10)

# New Invoice Button
new_invoice_button = ctk.CTkButton(frame, text="New Invoice", command=new_invoice)
new_invoice_button.grid(row=7, column=0, pady=5, padx=10)

# Run the application
window.mainloop()
