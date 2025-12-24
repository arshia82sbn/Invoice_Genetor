"""
Invoice Form Widget - View Component
Form for customer information and item entry
"""
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from typing import Callable, Optional

from app.utils.config import config
from app.utils.log_manager import get_logger

logger = get_logger()

class InvoiceForm(ctk.CTkFrame):
    """Form widget for invoice data entry"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Variables
        self.qty_var = ctk.IntVar(value=0)
        self.price_var = ctk.DoubleVar(value=0.0)

        # Callbacks (to be set by controller)
        self.on_add_item: Optional[Callable] = None

        self._setup_ui()

    def _setup_ui(self):
        """Setup form UI components"""
        # Customer Information Section
        self._create_customer_section()

        # Separator
        ctk.CTkLabel(self, text="").grid(row=2, column=0, pady=10)

        # Item Entry Section
        self._create_item_section()

        # Tax Section
        self._create_tax_section()

    def _create_customer_section(self):
        """Create customer information inputs"""
        # Section Label
        section_label = ctk.CTkLabel(
            self,
            text="Customer Information",
            font=("Arial", 16, "bold")
        )
        section_label.grid(row=0, column=0, columnspan=6, pady=(10, 20), sticky="w")

        # First Name
        first_name_label = ctk.CTkLabel(self, text="First Name")
        first_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.first_name_entry = ctk.CTkEntry(self, width=200)
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Last Name
        last_name_label = ctk.CTkLabel(self, text="Last Name")
        last_name_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.last_name_entry = ctk.CTkEntry(self, width=200)
        self.last_name_entry.grid(row=1, column=3, padx=10, pady=10)

        # Phone
        phone_label = ctk.CTkLabel(self, text="Phone")
        phone_label.grid(row=1, column=4, padx=10, pady=10, sticky="w")
        self.phone_entry = ctk.CTkEntry(self, width=200)
        self.phone_entry.grid(row=1, column=5, padx=10, pady=10)

        # Bind phone input limit
        self.phone_entry.bind("<KeyRelease>", self._limit_phone_input)

    def _create_item_section(self):
        """Create item entry inputs"""
        # Section Label
        section_label = ctk.CTkLabel(
            self,
            text="Add Items",
            font=("Arial", 16, "bold")
        )
        section_label.grid(row=3, column=0, columnspan=6, pady=(10, 20), sticky="w")

        # Quantity
        qty_label = ctk.CTkLabel(self, text="Quantity")
        qty_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.qty_entry = ctk.CTkEntry(
            self,
            textvariable=self.qty_var,
            justify="center",
            font=("Arial", 16),
            width=100
        )
        self.qty_entry.grid(row=4, column=1, padx=10, pady=10)

        qty_increase_btn = ctk.CTkButton(
            self,
            text="+",
            width=40,
            command=self._increase_qty
        )
        qty_increase_btn.grid(row=4, column=2, padx=5, pady=5)

        qty_decrease_btn = ctk.CTkButton(
            self,
            text="-",
            width=40,
            command=self._decrease_qty
        )
        qty_decrease_btn.grid(row=4, column=3, padx=5, pady=5)

        # Description
        desc_label = ctk.CTkLabel(self, text="Description")
        desc_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.desc_entry = ctk.CTkEntry(self, width=400)
        self.desc_entry.grid(row=5, column=1, columnspan=3, padx=10, pady=10)

        # Unit Price
        price_label = ctk.CTkLabel(self, text="Unit Price ($)")
        price_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        self.price_entry = ctk.CTkEntry(
            self,
            textvariable=self.price_var,
            justify="center",
            font=("Arial", 16),
            width=100
        )
        self.price_entry.grid(row=6, column=1, padx=10, pady=10)

        price_increase_btn = ctk.CTkButton(
            self,
            text="+",
            width=40,
            command=self._increase_price
        )
        price_increase_btn.grid(row=6, column=2, padx=5, pady=5)

        price_decrease_btn = ctk.CTkButton(
            self,
            text="-",
            width=40,
            command=self._decrease_price
        )
        price_decrease_btn.grid(row=6, column=3, padx=5, pady=5)

        # Add Item Button
        add_item_btn = ctk.CTkButton(
            self,
            text="Add Item",
            command=self._handle_add_item,
            font=("Arial", 14, "bold"),
            height=40
        )
        add_item_btn.grid(row=7, column=0, columnspan=6, padx=10, pady=20)

    def _create_tax_section(self):
        """Create tax rate input"""
        tax_label = ctk.CTkLabel(self, text="Sales Tax (%)")
        tax_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        self.tax_entry = ctk.CTkEntry(
            self,
            justify="center",
            font=("Arial", 16),
            width=100,
            placeholder_text=str(config.default_tax_rate)
        )
        self.tax_entry.grid(row=8, column=1, padx=10, pady=10)
        self.tax_entry.insert(0, str(config.default_tax_rate))

    def _limit_phone_input(self, event=None):
        """Limit phone input to 10 digits"""
        value = self.phone_entry.get()
        # Remove non-digit characters
        cleaned = ''.join(filter(str.isdigit, value))

        max_length = config.get('validation.phone_max_length', 10)
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length]

        if cleaned != value:
            self.phone_entry.delete(0, ctk.END)
            self.phone_entry.insert(0, cleaned)

    def _increase_qty(self):
        """Increase quantity by 1"""
        self.qty_var.set(self.qty_var.get() + 1)

    def _decrease_qty(self):
        """Decrease quantity by 1"""
        if self.qty_var.get() > 0:
            self.qty_var.set(self.qty_var.get() - 1)

    def _increase_price(self):
        """Increase price by step amount"""
        price_max = config.get('validation.price_max', 500.0)
        price_step = config.get('validation.price_step', 0.5)

        if self.price_var.get() < price_max:
            self.price_var.set(round(self.price_var.get() + price_step, 2))

    def _decrease_price(self):
        """Decrease price by step amount"""
        price_step = config.get('validation.price_step', 0.5)

        if self.price_var.get() > 0:
            new_price = self.price_var.get() - price_step
            self.price_var.set(round(max(0, new_price), 2))

    def _handle_add_item(self):
        """Handle add item button click"""
        if self.on_add_item:
            self.on_add_item()
        else:
            logger.warning("on_add_item callback not set")

    def get_customer_data(self) -> dict:
        """Get customer information from form"""
        return {
            'first_name': self.first_name_entry.get(),
            'last_name': self.last_name_entry.get(),
            'phone': self.phone_entry.get()
        }

    def get_item_data(self) -> dict:
        """Get item information from form"""
        return {
            'qty': str(self.qty_var.get()),
            'desc': self.desc_entry.get(),
            'price': str(self.price_var.get())
        }

    def get_tax_rate(self) -> str:
        """Get tax rate from form"""
        return self.tax_entry.get()

    def clear_item_fields(self):
        """Clear item entry fields"""
        self.qty_entry.delete(0, ctk.END)
        self.desc_entry.delete(0, ctk.END)
        self.price_entry.delete(0, ctk.END)
        self.qty_var.set(0)
        self.price_var.set(0.0)
        logger.debug("Item fields cleared")

    def clear_all_fields(self):
        """Clear all form fields"""
        self.first_name_entry.delete(0, ctk.END)
        self.last_name_entry.delete(0, ctk.END)
        self.phone_entry.delete(0, ctk.END)
        self.tax_entry.delete(0, ctk.END)
        self.tax_entry.insert(0, str(config.default_tax_rate))
        self.clear_item_fields()
        logger.debug("All form fields cleared")