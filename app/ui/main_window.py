"""
Main Window - View Layer
Assembles all UI components into the main application window
"""
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from app.ui.invoice_form import InvoiceForm
from app.ui.invoice_table import InvoiceTable
from app.utils.config import config
from app.utils.log_manager import get_logger

logger = get_logger()

class MainWindow(ctk.CTk):
    """Main application window"""

    def __init__(self):
        super().__init__()

        # Configure window
        self.title(config.app_title)
        self.geometry(config.window_size)
        self._set_appearance_mode(config.theme)

        # Create UI components
        self._setup_ui()

        logger.info("Main window initialized")

    def _setup_ui(self):
        """Setup main window UI"""
        # Main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Form section (top)
        self.invoice_form = InvoiceForm(main_container)
        self.invoice_form.pack(fill="x", padx=10, pady=10)

        # Separator
        separator = ctk.CTkFrame(main_container, height=2, fg_color="gray")
        separator.pack(fill="x", padx=20, pady=10)

        # Table section (middle)
        table_label = ctk.CTkLabel(
            main_container,
            text="Invoice Items",
            font=("Arial", 16, "bold")
        )
        table_label.pack(pady=(10, 5))

        self.invoice_table = InvoiceTable(main_container, height=250)
        self.invoice_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons section (bottom)
        self._create_buttons(main_container)

        # Summary section
        self._create_summary(main_container)

    def _create_buttons(self, parent):
        """Create action buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(pady=10)

        # Generate Invoice Button
        self.generate_btn = ctk.CTkButton(
            button_frame,
            text="Generate Invoice",
            font=("Arial", 14, "bold"),
            height=40,
            width=200,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.generate_btn.pack(side="left", padx=10)

        # New Invoice Button
        self.new_invoice_btn = ctk.CTkButton(
            button_frame,
            text="New Invoice",
            font=("Arial", 14, "bold"),
            height=40,
            width=200,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.new_invoice_btn.pack(side="left", padx=10)

        # Clear Items Button
        self.clear_items_btn = ctk.CTkButton(
            button_frame,
            text="Clear All Items",
            font=("Arial", 14, "bold"),
            height=40,
            width=200,
            fg_color="red",
            hover_color="darkred"
        )
        self.clear_items_btn.pack(side="left", padx=10)

    def _create_summary(self, parent):
        """Create invoice summary display"""
        summary_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        summary_frame.pack(fill="x", padx=10, pady=10)

        # Subtotal
        self.subtotal_label = ctk.CTkLabel(
            summary_frame,
            text="Subtotal: $0.00",
            font=("Arial", 14)
        )
        self.subtotal_label.pack(side="left", padx=20, pady=10)

        # Tax
        self.tax_label = ctk.CTkLabel(
            summary_frame,
            text="Tax: $0.00",
            font=("Arial", 14)
        )
        self.tax_label.pack(side="left", padx=20, pady=10)

        # Total
        self.total_label = ctk.CTkLabel(
            summary_frame,
            text="Total: $0.00",
            font=("Arial", 18, "bold")
        )
        self.total_label.pack(side="left", padx=20, pady=10)

    def update_summary(self, subtotal: float, tax_amount: float, total: float):
        """Update summary display"""
        self.subtotal_label.configure(text=f"Subtotal: ${subtotal:.2f}")
        self.tax_label.configure(text=f"Tax: ${tax_amount:.2f}")
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def show_success(self, title: str, message: str):
        """Show success message"""
        CTkMessagebox(title=title, message=message, icon="check")

    def show_error(self, title: str, message: str):
        """Show error message"""
        CTkMessagebox(title=title, message=message, icon="cancel")

    def show_info(self, title: str, message: str):
        """Show info message"""
        CTkMessagebox(title=title, message=message, icon="info")

    def confirm_action(self, title: str, message: str) -> bool:
        """Show confirmation dialog"""
        msg = CTkMessagebox(
            title=title,
            message=message,
            icon="question",
            option_1="Cancel",
            option_2="OK"
        )
        return msg.get() == "OK"